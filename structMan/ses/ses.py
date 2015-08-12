from operator import itemgetter

import numpy as np

from structMan.sol200 import (DRESP1, DCONSTR, DEQATN, DRESP2, DESVAR,
                              DVPREL1, DVPREL2)
import structMan.sol200.output_codes as output_codes_SOL200


class SE(object):
    """Structural Element

    Attributes
    ----------
    name : str
        Name.
    eids : list
        A list containing the elements belonging to this structural element.
    all_constraints : list
        A list of strings with all implemented constriants. For each
        constraint 'c' there must be a method `self.constrain_c` that will
        properly handle the creation of each optimization card.
    constraints : dict
        Only the constraints that should be considered. The dictionary should
        have the format::

            constraints{'vonMises': 1, 'buckling': 3}

        where `1` and `3` indicate the design constraint set ids for which
        each respective constraint should be applied.

    """
    def __init__(self, name, *eids):
        self.name = name
        self.eids = eids
        self.model = None
        self.elements = None
        # optimization parameters
        self.dresps = []
        self.dvars = {}
        self.dvprels = []
        self.deqatns = []
        self.dtables = {}
        self.dlinks = []
        self.dconstrs = []
        self.all_constraints = []
        self.constraints = {}
        # outputs
        self.forces = None

    def __str__(self):
        return (('%s: ' % self.__class__.__name__)  + self.name +
                ', Elements: ' + ', '.join(map(str, self.eids)))

    def __repr__(self):
        return str(self)


    def add_dtable(self, key, value):
        """Add a DTABLE entry to the SE and the optmodel

        Parameters
        ----------
        key : str
            The DTABLE unique key. The algorithm automatically attempts to add
            a sufix to prevent repeated keys.
        value : float
            The value corresponding to `key`.

        Returns
        -------
        key : str
            The resulting key.

        """
        optmodel = self.model.optmodel
        origkey = key
        if key in optmodel.dtables.keys():
            if len(key) >= 8:
                raise ValueError('{0} is an already existing DTABLE entry!'.
                                 format(key))
            if key in optmodel.dtable_prefixes:
                optmodel.dtable_prefixes[key] += 1
            else:
                optmodel.dtable_prefixes[key] = 0
            sufix = str(optmodel.dtable_prefixes[key])
            key = key + sufix.rjust(8 - len(key), '0')
            if len(key) > 8:
                raise ValueError('Use a smaller key')

        if origkey in self.dtables.keys():
            raise
        self.dtables[origkey] = [key, value]
        optmodel.dtables[key] = float(value)

        return key


    def add_dresp(self, dresp):
        """Add a DRESP(123) entry to the SE and the optmodel

        Parameters
        ----------
        dresp : :class:`DRESP1`, :class:`DRESP2` or :class:`DRESP3`
            The response object.

        """
        self.dresps.append(dresp)
        self.model.optmodel.dresps[dresp.id] = dresp


    def add_deqatn(self, deqatn):
        """Add a DEQATN entry to the SE and the optmodel

        Parameters
        ----------
        deqatn : :class:`DEQATN`
            The equation to be added.

        """
        self.deqatns.append(deqatn)
        self.model.optmodel.deqatns[deqatn.id] = deqatn


    def add_dvar(self, dvar):
        """Add a DESVAR entry to the SE and the optmodel

        Parameters
        ----------
        dvar : :class:`DESVAR`
            Design variable object.

        """
        if dvar.label in self.dvars.keys():
            raise
        self.dvars[dvar.label] = dvar
        self.model.optmodel.dvars[dvar.id] = dvar


    def add_dvprel(self, dvprel):
        """Add a DVPREL(12) entry to the SE and the optmodel

        Parameters
        ----------
        dvprel : :class:`DVPREL1` or :class:`DVPREL2`
            Design property-to-variable object.

        """
        self.dvprels.append(dvprel)
        self.model.optmodel.dvprels[dvprel.id] = dvprel


    def add_constraint(self, dcid, dresp, lb, ub):
        """Add a DCONSTR entry to the SE and the optmodel

        Parameters
        ----------
        dcid : int
            Design constraint set id.
        dresp : :class:`DRESP1`, :class:`DRESP2` or :class:`DRESP3`
            The response object.
        lb : float or None
            Lower boundary for the constraint.
        ub : float or None
            Upper boundary for the constraint.

        """
        dconstr = DCONSTR(dcid, dresp.id, lb, ub)
        self.dconstrs.append(dconstr)
        self.model.optmodel.dconstrs[dconstr.id] = dconstr


    def get_central_element(self):
        """Return the element closest to the SE center of gravity

        """
        if self.elements is None:
            return
        x = np.array([e.get_node_positions().mean(axis=0) for e in
            self.elements])
        cg = x.mean(axis=0)
        return self.elements[np.argmin(((x-cg)**2).sum(axis=1))]


class SE1D(SE):
    def __init__(self, name, *eids):
        super(SE1D, self).__init__(name, *eids)
        # internal forces
        self.bending_moment_a1 = None
        self.bending_moment_a2 = None
        self.bending_moment_b1 = None
        self.bending_moment_b2 = None
        self.shear1 = None
        self.shear2 = None
        self.axial = None
        self.torque = None

    def read_forces(self):
        if self.model.op2 is None:
            print('No op2 file defined for SE.model')
        # LINEAR ELEMENTS
        # CBAR
        #TODO try to fix op2.subcases and submit a pull request
        subcases = self.model.op2.subcases
        num_subcases = len(subcases)
        forces = self.model.op2.cbar_force
        force1 = forces[subcases[0]]
        if not self.model.op2.is_vectorized:
            num_vectors = 8

            self.forces = np.zeros((num_vectors, len(self.eids), num_subcases))

            getter = itemgetter(*self.eids)

            for i, subcase in enumerate(subcases):
                data = forces[subcase]
                # Bending End A plane 1 and plane 2
                tmp = getter(data.bendingMomentA)
                self.forces[0, :, i], self.forces[1, :, i] = zip(*tmp)
                # Bending End B plane 1 and plane 2
                tmp = getter(data.bendingMomentB)
                self.forces[2, :, i], self.forces[3, :, i] = zip(*tmp)
                # Shear plane 1 and plane 2
                tmp = getter(data.shear)
                self.forces[4, :, i], self.forces[5, :, i] = zip(*tmp)
                # Axial force
                self.forces[6, :, i] = getter(data.axial)
                # Torque
                self.forces[7, :, i] = getter(data.torque)

        elif self.model.op2.is_vectorized:
            num_vectors = force1.data.shape[2]

            self.forces = np.zeros((num_vectors, len(self.eids), num_subcases))

            i_op2 = np.in1d(force1.element, self.eids)
            i_panel = np.in1d(self.eids, force1.element)

            for i, subcase in enumerate(subcases):
                data = forces[subcase].data
                self.forces[:, i_panel, i] = data[-1, i_op2, :].swapaxes(-1, -2)

        self.bending_moment_a1 = self.forces[0]
        self.bending_moment_a2 = self.forces[1]
        self.bending_moment_b1 = self.forces[2]
        self.bending_moment_b2 = self.forces[3]
        self.shear1 = self.forces[4]
        self.shear2 = self.forces[5]
        self.axial = self.forces[6]
        self.torque = self.forces[7]


class SE2D(SE):
    def __init__(self, name, *eids):
        super(SE2D, self).__init__(name, *eids)
        # internal forces
        self.mx = None
        self.my = None
        self.mxy = None
        self.bmx = None
        self.bmy = None
        self.bmxy = None
        self.tx = None
        self.ty = None

    def read_forces(self):
        if self.model.op2 is None:
            print('No op2 file defined for SE.model')
            return
        #TODO try to fix op2.subcases and submit a pull request
        subcases = self.model.op2.subcases
        num_subcases = len(subcases)
        # LINEAR ELEMENTS
        if not self.model.op2.is_vectorized:
            num_vectors = 8
            self.forces = np.zeros((num_vectors, len(self.eids), num_subcases))

            for forces in [self.model.op2.cquad4_force,
                           self.model.op2.ctria3_force]:
                if len(forces.keys()) == 0:
                    continue
                element = np.sort(forces[subcases[0]].mx.keys())
                i_panel = np.in1d(self.eids, element)

                tmp = np.array(self.eids)[i_panel]
                if len(tmp) == 0:
                    continue
                getter = itemgetter(*tmp)

                for i, subcase in enumerate(subcases):
                    data = forces[subcase]
                    # mx
                    self.forces[0, i_panel, i] = getter(data.mx)
                    # my
                    self.forces[1, i_panel, i] = getter(data.my)
                    # mxy
                    self.forces[2, i_panel, i] = getter(data.mxy)
                    # bmx
                    self.forces[3, i_panel, i] = getter(data.bmx)
                    # bmy
                    self.forces[4, i_panel, i] = getter(data.bmy)
                    # bmxy
                    self.forces[5, i_panel, i] = getter(data.bmxy)
                    # tx
                    self.forces[6, i_panel, i] = getter(data.tx)
                    # ty
                    self.forces[7, i_panel, i] = getter(data.ty)

        elif self.model.op2.is_vectorized:
            forces = self.model.op2.cquad4_force
            force1 = forces[subcases[0]]
            num_vectors = force1.data.shape[2]

            self.forces = np.zeros((num_vectors, len(self.eids), num_subcases))

            # CQUAD4
            i_op2 = np.in1d(force1.element, self.eids)
            i_panel = np.in1d(self.eids, force1.element)

            for i, subcase in enumerate(subcases):
                data = forces[subcase].data
                self.forces[:, i_panel, i] = data[-1, i_op2, :].swapaxes(-1, -2)

            # CTRIA3
            forces = self.model.op2.ctria3_force
            force1 = forces[subcases[0]]
            i_op2 = np.in1d(force1.element, self.eids)
            i_panel = np.in1d(self.eids, force1.element)

            for i, subcase in enumerate(subcases):
                data = forces[subcase].data
                self.forces[:, i_panel, i] = data[-1, i_op2, :].swapaxes(-1, -2)

        self.mx = self.forces[0]
        self.my = self.forces[1]
        self.mxy = self.forces[2]
        self.bmx = self.forces[3]
        self.bmy = self.forces[4]
        self.bmxy = self.forces[5]
        self.tx = self.forces[6]
        self.ty = self.forces[7]


class Panel(SE2D):
    """Panel

    Attributes

    """
    def __init__(self, name, *eids):
        super(Panel, self).__init__(name, *eids)
        # geometric parameters
        self.radius1 = None
        self.radius2 = None
        self.width = None
        self.length = None
        self.thickness = None
        self.xaxis = 'stringer'
        # material properties
        self.is_isotropic = True
        self.Ec = None
        self.nu = None
        # optimization constraints
        self.all_constraints = ['vonMises']
        self.constraints = {'vonMises': 1}


    def constrain_vonMises(self, Fcy, average=False):
        """Add a von Mises stress constraint

        Parameters
        ----------
        Fcy : float
            The stress threshold that will be compared to the von Mises stress
            for this constraint.
        average : bool, optional
            If False the center element is chosen, otherwise ...
            #TODO not implemented

        """
        eid = self.get_central_element().eid

        dcid = self.constraints['vonMises']
        OUTC = output_codes_SOL200.OUTC

        atta = OUTC['STRESS']['CQUAD4']['von Mises or maximum shear at Z1']
        dresp1 = DRESP1('PANZ1VM', 'STRESS', 'ELEM', None, atta=atta,
                        attb=None, atti=eid)
        self.add_dresp(dresp1)
        self.add_constraint(dcid, dresp1, None, Fcy)

        atta = OUTC['STRESS']['CQUAD4']['von Mises or maximum shear at Z2']
        dresp1 = DRESP1('PANZ2VM', 'STRESS', 'ELEM', None, atta=atta,
                        attb=None, atti=eid)
        self.add_dresp(dresp1)
        self.add_constraint(dcid, dresp1, None, Fcy)


class InnerFlange(SE1D):
    def __init__(self, name, *eids):
        super(InnerFlange, self).__init__(name, *eids)


        #TODO will be useful
        if False:
            if self.is_PBAR:
                pid = 1
                # calculating A
                deqatn = DEQATN('A(t,b) = t*b')
                self.add_deqatn(deqatn)
                dvprel = DVPREL2('PBAR', pid=pid, pname='A', eqid=deqatn.id)
                dvprel.add_dvar(dvar_t.id)
                dvprel.add_dvar(dvar_b.id)
                self.add_dvprel(dvprel)
                # assuming y-axis towards radial (normal) direction
                # calculating I1
                deqatn = DEQATN('I1(t,b)=t*b**3/12.')
                self.add_deqatn(deqatn)
                dvprel = DVPREL2('PBAR', pid=pid, pname='I1', eqid=deqatn.id)
                dvprel.add_dvar(dvar_t.id)
                dvprel.add_dvar(dvar_b.id)
                self.add_dvprel(dvprel)
                # calculating I2
                deqatn = DEQATN('I1(t,b)=t*b**3/12.')
                self.add_deqatn(deqatn)
                dvprel = DVPREL2('PBAR', pid=pid, pname='I1', eqid=deqatn.id)
                dvprel.add_dvar(dvar_t.id)
                dvprel.add_dvar(dvar_b.id)
                self.add_dvprel(dvprel)
                # calculating I12
                # calculating J
                dvprel = DVPREL2('PBAR', pid=pid, pname='I1', eqid=deqatn.id)


class Web(SE2D):
    def __init__(self, name, *eids):
        super(Web, self).__init__(name, *eids)


class OuterFlange(SE1D):
    def __init__(self, name, *eids):
        super(OuterFlange, self).__init__(name, *eids)


class ShearClipFrame(SE2D):
    """Shear Clip Attachment to Frame

    """
    def __init__(self, name, *eids):
        super(ShearClipFrame, self).__init__(name, *eids)


class ShearClipSkin(SE1D):
    """Shear Clip Attachment to Skin

    """
    def __init__(self, name, *eids):
        super(ShearClipSkin, self).__init__(name, *eids)

