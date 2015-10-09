"""
Panel SEs (:mod:`structMan.ses.panel`)
======================================

.. currentmodule:: structMan.ses.panel

"""
import numpy as np

from ses import SE2D

from structMan.sol200 import (DRESP1, DCONSTR, DEQATN, DRESP2, DRESP3, DESVAR,
                              DVPREL1, DVPREL2)

import structMan.sol200.output_codes as output_codes_SOL200


class Panel(SE2D):
    """Panel

    This class should be used for cylindrical panels (i.e. fuselage panels).
    For plates please refer to :class:`.Plate`.

    For wing panels this class should also be adopted.

    Attributes
    ----------

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
        self.all_constraints = ['vonMises', 'buckling']
        self.constraints = {'vonMises': 1,
                            'buckling': 1}

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
            self.r = rs.mean()
            self.a = xs.max() - xs.min()
            self.b = (thetas.max() - thetas.min())*self.r

            # retrieving panel thickness and material properties
            self.t = self.elements[0].pid.t


    def create_dvars(self):
        if self.dvars_created:
            return
        self.dvars_created = True
        pid = self.pid
        ptype = self.ptype

        if ptype == 'PSHELL':
            dvar_t = DESVAR('PANt', self.t, self.t_lb, self.t_ub)
            self.add_dvar(dvar_t)
            dvprel = DVPREL1('PSHELL', pid=pid, pname='T', dvids=[dvar_t.id],
                             coeffs=[1.])
            self.add_dvprel(dvprel)
            self.add_dtable('PANr', self.r)
            self.add_dtable('PANa', self.a)
            self.add_dtable('PANb', self.b)
            self.add_dtable('PANE', self.E)
            self.add_dtable('PANnu', self.nu)
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
            If False the center element is chosen, otherwise it will check each
            element individually and compute the average von Mises stress of
            the panel.

        """
        self.create_dvars()
        if not average:
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

        else:
            dcid = self.constraints['vonMises']
            OUTC = output_codes_SOL200.OUTC
            atta = OUTC['STRESS']['CQUAD4']['von Mises or maximum shear at Z1']
            dresp1_bot = []
            dresp1_top = []
            for eid in self.eids:
                dresp1 = DRESP1('PANZ1VM', 'STRESS', 'ELEM', None, atta=atta,
                                attb=None, atti=eid)
                self.add_dresp(dresp1)
                dresp1_bot.append(dresp1)

                atta = OUTC['STRESS']['CQUAD4']['von Mises or maximum shear at Z2']
                dresp1 = DRESP1('PANZ2VM', 'STRESS', 'ELEM', None, atta=atta,
                                attb=None, atti=eid)
                self.add_dresp(dresp1)
                dresp1_top.append(dresp1)

            dresp2_bot = DRESP2('PANZ1VMA', eqid='AVG')
            dresp2_bot.dresp1 = dresp1_bot[:]
            self.add_dresp(dresp2_bot)
            self.add_constraint(dcid, dresp2_bot, None, Fcy)

            dresp2_top = DRESP2('PANZ2VMA', eqid='AVG')
            dresp2_top.dresp1 = dresp1_top[:]
            self.add_dresp(dresp2_top)
            self.add_constraint(dcid, dresp2_top, None, Fcy)


    def constrain_buckling(self, method=1, ms=0.1):
        """Add a buckling constraint

        Parameters
        ----------
        method : int, optional
            Select one of the following methods for buckling calculation:

            - `1` : Bruhn's method using Equation C9.4:
                    - considers compressive and shear loads
                    - no plasticity correction has been implemented

        ms : float, optional
            Minimum margin of safety to be used as constraint.

        """
        OUTC = output_codes_SOL200.OUTC

        eid = self.get_central_element().eid

        # reading membrane force Nxx
        code_Nxx = OUTC['FORCE']['CQUAD4']['Membrane force x']
        dresp_Nxx = DRESP1('PANfNxx', 'FORCE', 'ELEM', region=None,
                           atta=code_Nxx, attb=None, atti=eid)
        self.add_dresp(dresp_Nxx)
        # reading membrane force Nxy
        code_Nxy = OUTC['FORCE']['CQUAD4']['Membrane force xy']
        dresp_Nxy = DRESP1('PANfNxy', 'FORCE', 'ELEM', region=None,
                           atta=code_Nxy, attb=None, atti=eid)
        self.add_dresp(dresp_Nxy)
        # calculating the margin of safety using an external subroutine
        dresp = DRESP3('PANBUCK1', 'PANBUCK', 'METHOD1')
        dresp.add_dvar(self.dvars['PANt'].id)
        dresp.add_dtable(self.dtables['PANr'][0])
        dresp.add_dtable(self.dtables['PANa'][0])
        dresp.add_dtable(self.dtables['PANb'][0])
        dresp.add_dtable(self.dtables['PANE'][0])
        dresp.add_dtable(self.dtables['PANnu'][0])
        dresp.add_dresp2(dresp_Nxx.id)
        dresp.add_dresp2(dresp_Nxy.id)
        self.add_dresp(dresp)


