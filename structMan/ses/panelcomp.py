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


class PanelComp(SE2D):
    """Composite Panel

    This class should be used for cylindrical panels (i.e. fuselage panels).
    For plates please refer to :class:`.Plate`.

    For wing panels this class should also be adopted.

    Attributes
    ----------

    """
    def __init__(self, name, eids, model=None):
        super(Panel, self).__init__(name, eids, model)
        # geometric parameters
        self.r = None
        self.a = None
        self.b = None
        self.t = None
        self.t_lb = None
        self.t_ub = None
        self.aml = None
        self.aml_lb = None
        self.aml_ub = None
        self.aml90 = 0.1
        # material properties
        # ...
        self.is_isotropic = None
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

        if ptype == 'PCOMP':
            dvar_t = DESVAR('PCt', self.t, self.t_lb, self.t_ub)
            self.add_dvar(dvar_t)
            dvar_aml = DESVAR('PCaml', self.aml, self.aml_lb, self.aml_ub)
            self.add_dvar(dvar_aml)

            deqatn0 = DEQATN('T0(t,aml,aml90) = (1.-aml90-aml)*t')
            dvprel2 = DVPREL2('PCOMP', pid=pid, pname='T1', deqatn0.id)
            dvprel2.dvars = [dvar_t.id, dvar_aml.id]
            dvprel2.dtable = [self.aml90]
            self.add_dvprel(dvprel2)

            #TODO
            deqatn45 = DEQATN('T45(t,aml) = aml*t')

            #TODO
            deqatn90 = DEQATN('T90(t,aml90) = aml90*t')

            self.add_dtable('AML90', self.aml90)
            #TODO
            self.add_dtable('PCa', self.a)
            self.add_dtable('PCb', self.b)
            self.add_dtable('PCE1', self.E1)
            self.add_dtable('PCE2', self.E2)
            self.add_dtable('PCnu', self.nu)
        else:
            raise NotImplementedError('%s not supported!' % ptype)


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
        dresp_Nxx = DRESP1('PCfNxx', 'FORCE', 'ELEM', region=None,
                           atta=code_Nxx, attb=None, atti=eid)
        self.add_dresp(dresp_Nxx)

        # reading membrane force Nyy
        code_Nyy = OUTC['FORCE']['CQUAD4']['Membrane force xy']
        dresp_Nyy = DRESP1('PCfNyy', 'FORCE', 'ELEM', region=None,
                           atta=code_Nyy, attb=None, atti=eid)
        self.add_dresp(dresp_Nyy)

        # reading membrane force Nxy
        code_Nxy = OUTC['FORCE']['CQUAD4']['Membrane force xy']
        dresp_Nxy = DRESP1('PCfNxy', 'FORCE', 'ELEM', region=None,
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


