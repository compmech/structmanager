"""
Composite Panel SEs (:mod:`structmanager.ses.panelcomp`)
========================================================

.. currentmodule:: structmanager.ses.panelcomp

"""
import numpy as np

from ses import SE2D

from structmanager.sol200 import (DRESP1, DCONSTR, DEQATN, DRESP2, DRESP3,
        DESVAR, DTABLE, DVPREL1, DVPREL2)

import structmanager.sol200.output_codes as output_codes_SOL200


class PanelComp(SE2D):
    """Composite Panel

    This class should be used for cylindrical panels (i.e. fuselage panels).
    For plates please refer to :class:`.Plate`.

    For wing panels this class should also be adopted.

    Attributes
    ----------

    """
    def __init__(self, name, eids, model=None):
        super(PanelComp, self).__init__(name, eids, model) #change to super(PanelComp, self)?
        # geometric parameters
        self.r = None
        self.a = None
        self.b = None
        self.t = None
        self.t_lb = None
        self.t_ub = None
        self.p45 = None
        self.p45_lb = 0.1
        self.p45_ub = None
        self.p90 = 0.1
        # material properties
        # all material properties are got from FE model at ses.py

        self.is_isotropic = None #change to orthotropic?
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

            # retrieving plies thicknesses from panel
            self.t0 = self.elements[0].pid.Thickness(0)
            self.t45 = self.elements[0].pid.Thickness(1) + self.elements[0].pid.Thickness(2)
            self.t90 = self.elements[0].pid.Thickness(3)
            self.t = self.t0 + self.t45 + self.t90

            # calculating the thickness ratio
            self.p45 = self.t45/self.t


    def create_dvars(self):
        if self.dvars_created:
            return
        self.dvars_created = True
        pid = self.pid
        ptype = self.ptype

        if ptype == 'PCOMP':
            dvar_t = DESVAR('PCt', self.t, self.t_lb, self.t_ub)
            self.add_dvar(dvar_t)
            dvar_p45 = DESVAR('PCp45', self.p45, self.p45_lb, self.p45_ub)
            self.add_dvar(dvar_p45)
            self.add_dtable('P90', self.p90)
            #DONE
            self.add_dtable('PCa', self.a)
            self.add_dtable('PCb', self.b)
            self.add_dtable('PCr', self.r)
            self.add_dtable('PCE1', self.E1)
            self.add_dtable('PCE2', self.E2)
            self.add_dtable('PCG12', self.G12)
            self.add_dtable('PCn12', self.nu12)
            self.add_dtable('PCn21', self.nu21)

            deqatn0 = DEQATN('T0(t,p45,p90) = (1.-p45-p90)*t')
            self.add_deqatn(deqatn0)
            dvprel2 = DVPREL2('PCOMP', pid, 'T1', deqatn0.id)
            dvprel2.add_dvar(dvar_t.id)
            dvprel2.add_dvar(dvar_p45.id)
            dvprel2.add_dtable(self.dtables['P90'][0])
            self.add_dvprel(dvprel2)

            #DONE
            deqatn45 = DEQATN('T45(t,p45) = (p45/2.)*t')
            self.add_deqatn(deqatn45)
            dvprel2 = DVPREL2('PCOMP', pid, 'T2', deqatn45.id)
            #dvprel2.dvars = [dvar_t.id, dvar_p45.id]
            dvprel2.add_dvar(dvar_t.id)
            dvprel2.add_dvar(dvar_p45.id)
            self.add_dvprel(dvprel2)

            #DONE
            dvprel2 = DVPREL2('PCOMP', pid, 'T3', deqatn45.id)
            #dvprel2.dvars = [dvar_t.id, dvar_p45.id]
            dvprel2.add_dvar(dvar_t.id)
            dvprel2.add_dvar(dvar_p45.id)
            self.add_dvprel(dvprel2)

            #DONE
            deqatn90 = DEQATN('T90(t,p90) = p90*t')
            self.add_deqatn(deqatn90)
            dvprel2 = DVPREL2('PCOMP', pid, 'T4', deqatn90.id)
            #dvprel2.dvars = [dvar_t.id]
            dvprel2.add_dvar(dvar_t.id)
            dvprel2.add_dtable(self.dtables['P90'][0])
            self.add_dvprel(dvprel2)

        else:
            raise NotImplementedError('%s not supported!' % ptype)

    def constrain_buckling(self, eig=1.0):

        OUTC = output_codes_SOL200.OUTC

        eid = self.get_central_element().eid

        dcid = self.constraints['buckling']

        # reading membrane force Nxx
        code_Nxx = OUTC['FORCE']['CQUAD4']['Membrane force x']
        dresp_Nxx = DRESP1('PCfNxx', 'FORCE', 'ELEM', region=None,
                           atta=code_Nxx, attb=None, atti=eid)
        self.add_dresp(dresp_Nxx)

        # reading membrane force Nyy
        code_Nyy = OUTC['FORCE']['CQUAD4']['Membrane force y']
        dresp_Nyy = DRESP1('PCfNyy', 'FORCE', 'ELEM', region=None,
                           atta=code_Nyy, attb=None, atti=eid)
        self.add_dresp(dresp_Nyy)

        # reading membrane force Nxy
        code_Nxy = OUTC['FORCE']['CQUAD4']['Membrane force xy']
        dresp_Nxy = DRESP1('PCfNxy', 'FORCE', 'ELEM', region=None,
                           atta=code_Nxy, attb=None, atti=eid)
        self.add_dresp(dresp_Nxy)

        # calculating buckling eigenvalue using an external subroutine
        # all parameters (desvars, dtables, dresp's) that this DRESP3 needs to run are listed below
        # creating DRESP3
        dresp = DRESP3('PCBUCK1', 'PCBUCK', 'BUCK_PC')
        dresp.add_dvar(self.dvars['PCt'].id)
        #dresp.add_dvar(dvar_t.id)
        dresp.add_dtable(self.dtables['PCa'][0])
        dresp.add_dtable(self.dtables['PCb'][0])
        dresp.add_dtable(self.dtables['PCr'][0])
        dresp.add_dtable(self.dtables['PCE1'][0])
        dresp.add_dtable(self.dtables['PCE2'][0])
        dresp.add_dtable(self.dtables['PCG12'][0])
        dresp.add_dtable(self.dtables['PCn12'][0])
        dresp.add_dtable(self.dtables['PCn21'][0])
        dresp.add_dresp1(dresp_Nxx.id)
        dresp.add_dresp1(dresp_Nyy.id)
        dresp.add_dresp1(dresp_Nxy.id)
        self.add_dresp(dresp)
        # applying constraint of buckling: lower eigenvalue >= 1.0
        self.add_constraint(dcid, dresp, eig, None)

