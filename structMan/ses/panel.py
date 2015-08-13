import numpy as np

from ses import SE2D

from structMan.sol200 import (DRESP1, DCONSTR, DEQATN, DRESP2, DESVAR,
                              DVPREL1, DVPREL2)

import structMan.sol200.output_codes as output_codes_SOL200


class Panel(SE2D):
    """Panel

    Attributes

    """
    def __init__(self, name, eids, model=None):
        super(Panel, self).__init__(name, eids, model)
        # geometric parameters
        self.radius1 = None
        self.radius2 = None
        self.a = None
        self.b = None
        self.t = None
        self.xaxis = 'stringer'
        # material properties
        # ...
        self.is_isotropic = True
        # optimization constraints
        self.all_constraints = ['vonMises']
        self.constraints = {'vonMises': 1}

        # finding corner nodes
        # - assuming that they are those that share only one inner element
        # - radius calculated assuming the panel has a common center
        if self.elements is not None:
            nodes = []
            for element in self.elements:
                for node in element.nodes:
                    nodes.append(node)
            self.nodes = set(nodes)
            ccoords = np.array([n.xyz for n in self.nodes])
            xs = ccoords[:, 0]
            ys = ccoords[:, 1]
            zs = ccoords[:, 2]
            rs = (ys**2 + zs**2)**0.5
            thetas = np.arctan2(zs, ys)
            self.a = xs.max() - xs.min()
            self.b = (thetas.max() - thetas.min())*rs.mean()

            # retrieving panel thickness and material properties
            self.t = self.elements[0].pid.t


    def create_dvars(self):
        if self.dvars_created:
            return
        self.dvars_created = True
        pid = self.pid
        ptype = self.ptype

        if ptype == 'PSHELL':
            self.add_dtable('PANE', self.E)
            self.add_dtable('PANnu', self.nu)
            dvar_t = DESVAR('PANt', self.t, self.t_lb, self.t_ub)
            self.add_dvar(dvar_t)
            dvprel = DVPREL1('PSHELL', pid=pid, pname='T', dvids=[dvar_t.id],
                             coeffs=[1.])
            self.add_dvprel(dvprel)
        else:
            raise NotImplementedError('%s not supported!' % ptype)


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
        self.create_dvars()
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


