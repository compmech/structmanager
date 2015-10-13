"""
Web SE (:mod:`structMan.ses.web`)
============================================

.. currentmodule:: structMan.ses.web

"""
import numpy as np

from ses import SE2D


class Web(SE2D):
    """Web structural element
    """
    def __init__(self, name, eids, model=None):
        super(Web, self).__init__(name, eids, model)
        self.a = None
        self.b = None
        self.t = None
        self.t_lb = None
        self.t_ub = None
        self.all_constraints = ['vonMises', 'buckling']
        self.constraints = {'vonMises': 1,
                            'buckling': 1}

    def create_dvars(self):
        if self.dvars_created:
            return
        self.dvars_created = True
        pid = self.pid
        ptype = self.ptype

        if ptype == 'PSHELL':
            dvar_t = DESVAR('WEBt', self.t, self.t_lb, self.t_ub)
            self.add_dvar(dvar_t)
            dvprel = DVPREL1('PSHELL', pid=pid, pname='T', dvids=[dvar_t.id],
                             coeffs=[1.])
            self.add_dvprel(dvprel)
            self.add_dtable('WEBa', self.a)
            self.add_dtable('WEBb', self.b)
            self.add_dtable('WEBE', self.E)
            self.add_dtable('WEBnu', self.nu)
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
            dresp1 = DRESP1('WEBZ1VM', 'STRESS', 'ELEM', None, atta=atta,
                            attb=None, atti=eid)
            self.add_dresp(dresp1)
            self.add_constraint(dcid, dresp1, None, Fcy)

            atta = OUTC['STRESS']['CQUAD4']['von Mises or maximum shear at Z2']
            dresp1 = DRESP1('WEBZ2VM', 'STRESS', 'ELEM', None, atta=atta,
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
                dresp1 = DRESP1('WEBZ1VM', 'STRESS', 'ELEM', None, atta=atta,
                                attb=None, atti=eid)
                self.add_dresp(dresp1)
                dresp1_bot.append(dresp1)

                atta = OUTC['STRESS']['CQUAD4']['von Mises or maximum shear at Z2']
                dresp1 = DRESP1('WEBZ2VM', 'STRESS', 'ELEM', None, atta=atta,
                                attb=None, atti=eid)
                self.add_dresp(dresp1)
                dresp1_top.append(dresp1)

            dresp2_bot = DRESP2('WEBZ1VMA', eqid='AVG')
            dresp2_bot.dresp1 = dresp1_bot[:]
            self.add_dresp(dresp2_bot)
            self.add_constraint(dcid, dresp2_bot, None, Fcy)

            dresp2_top = DRESP2('WEBZ2VMA', eqid='AVG')
            dresp2_top.dresp1 = dresp1_top[:]
            self.add_dresp(dresp2_top)
            self.add_constraint(dcid, dresp2_top, None, Fcy)


    def constrain_buckling(self, simply_supported=True, method=1, ms=0.1):
        """Add a buckling constraint

        Parameters
        ----------
        method : int, optional
            Select one of the following methods for buckling calculation:

            - `1` : Bruhn's method using Fig. C5.2

                - considers only compressive loads
                - no plasticity correction has been implemented

            - `2` : Bruhn's method using Figs. C5.2 and C5.11 with the
              interaction equation Eq. C5.11.

                - considers compressive and shear loads
                - no plasticity correction has been implemented

            - `3` : Bruhn's method using Figs. C5.2 and C5.15 with the
              interaction equation Eq. C5.8.

                - considers compressive and transverse bending loads
                - no plasticity correction has been implemented

            - `4` : Bruhn's method using Figs. C5.2, C5.11 and C5.15 with the
              interaction curves of Fig. C5.18.

                - considers compressive, shear and transverse bending loads
                - no plasticity correction has been implemented



        ms : float, optional
            Minimum margin of safety to be used as constraint.

        """
        if method not in [1, 2]:
            raise NotImplementedError('Only methods 1 and 2 are implemented!')

        OUTC = output_codes_SOL200.OUTC

        # kc: taking most critical kc from Bruhn's Fig. C5.2
        # ks: taking most critical kc from Bruhn's Fig. C5.11
        if simply_supported:
            kc = 4.
            ks = 5.6
        else:
            kc = 7.4
            ks = 9.3

        if method == 1:
            eid = self.get_central_element().eid
            # calculating the critical buckling stresses
            # using Bruhn's Eq. C5.12 in Page C5.8 for the margin of safety
            # (MS) calculation
            deqatn = DEQATN('D(t,b,E,nu,Nxx) = 12.*(1.-nu**2)*b**2;' +
                            ('FCcr = %0.3f*PI(1)**2*E*t**2/D;' % kc) +
                            'Nxx = MIN(MAX, 0.00000001);' +
                            'MS = FCcr*t/Nxx - 1.'
                           )
            self.add_deqatn(deqatn)
            # reading variables
            dvar_t = self.dvars['WEBt']
            # reading constants
            dtable_b = self.dtables['WEBb'][0]
            dtable_E = self.dtables['WEBE'][0]
            dtable_nu = self.dtables['WEBnu'][0]
            # reading membrane force Nxx
            code_Nxx = OUTC['FORCE']['CQUAD4']['Membrane force x']
            dresp_Nxx = DRESP1('WEBfNxx', 'FORCE', 'ELEM', region=None,
                               atta=code_Nxx, attb=None, atti=eid)
            self.add_dresp(dresp_Nxx)
            # creating DRESP2
            dresp2 = DRESP2('WEBBUCK', deqatn.id)
            dresp2.dvars = [dvar_t.id]
            dresp2.dtable = [dtable_b, dtable_E, dtable_nu]
            dresp2.dresp1 = [dresp_Nxx.id]
            self.add_dresp(dresp2)

            # applying constraint
            dcid = self.constraints['buckling']
            dconstr = self.add_constraint(dcid, dresp2, ms, None)

        elif method == 2:
            eid = self.get_central_element().eid

            # calculating the critical buckling stresses
            # using Bruhn's Eq. C5.12 in Page C5.8 for the margin of safety
            # (MS) calculation
            deqatn = DEQATN('D(t,b,E,nu,Nxx,Nxy) = 12.*(1.-nu**2)*b**2;' +
                            ('FCcr = %0.3f*PI(1)**2*E*t**2/D;' % kc) +
                            ('FScr = %0.3f*PI(1)**2*E*t**2/D;' % ks) +
                            'RC = Nxx/(FCcr*t);' +
                            'RS = Nxy/(FScr*t);' +
                            'MS = 2./(RC + SQRT(RC**2 + 4.*RS**2)) - 1.'
                           )
            self.add_deqatn(deqatn)
            # reading variables
            dvar_t = self.dvars['WEBt']
            # reading constants
            dtable_b = self.dtables['WEBb'][0]
            dtable_E = self.dtables['WEBE'][0]
            dtable_nu = self.dtables['WEBnu'][0]
            # reading membrane force Nxx
            code_Nxx = OUTC['FORCE']['CQUAD4']['Membrane force x']
            dresp_Nxx = DRESP1('WEBfNxx', 'FORCE', 'ELEM', region=None,
                               atta=code_Nxx, attb=None, atti=eid)
            self.add_dresp(dresp_Nxx)
            # reading membrane force Nxy
            code Nxy = OUTC['FORCE']['CQUAD4']['Membrane force xy']
            dresp_Nxy = DRESP1('WEBfNxy', 'FORCE', 'ELEM', region=None,
                               atta=code_Nxy, attb=None, atti=eid)
            self.add_dresp(dresp_Nxy)
            # creating DRESP2
            dresp2 = DRESP2('WEBBUCK', deqatn.id)
            dresp2.dvars = [dvar_t.id]
            dresp2.dtable = [dtable_b, dtable_E, dtable_nu]
            dresp2.dresp1 = [dresp_Nxx.id, dresp_Nxy.id]
            self.add_dresp(dresp2)

            # applying constraint
            dcid = self.constraints['buckling']
            dconstr = self.add_constraint(dcid, dresp2, ms, None)





