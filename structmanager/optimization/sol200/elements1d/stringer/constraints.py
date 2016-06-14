import structmanager.sol200.output_codes as output_codes_SOL200

from structmanager.sol200 import (DRESP1, DCONSTR, DEQATN, DRESP2, DESVAR,
                              DVPREL1, DVPREL2)


def constrain_buckling(self, method=1, ms=0.1):
    """Add a buckling constraint

    Parameters
    ----------
    method : int, optional
        Select one of the following methods for buckling calculation:

        For `profile`  in ['Z_t', 'Z_t_b' or 'Z_t_b_h']:

        - `1` : Bruhn's method for Channel- and Z-section stiffeners. From
                Fig. C6.4 for `tw=tf` (thickness web = thickness flange)
                - considers only compressive loads
                - no plasticity correction has been implemented

        For `profile`  in ['B_t', 'B_t_h']:

        - `1` : Bruhn's method for combined shear and compression, from
                Chapter C5.11.
                - disconsiders bending effects
                - assumes 3 edges simply supported with one free unloaded
                  edge.
                - no plasticity correction has been implemented

    ms : float, optional
        Minimum margin of safety to be used as constraint.

    """
    self.create_dvars()
    eltype = self.elements[0].type

    # reading constants
    dtable_E = self.dtables['STRE'][0]
    dtable_nu = self.dtables['STRnu'][0]

    if method == 1 and self.profile.lower() == 'z_t':
        # buckling equation
        deqatn = DEQATN(
            'bf(t, b, h, E, nu, FA) = b-t/2.;'
            'bw = h-t;'
            'x = bf/bw;'
            'Kw = -206.08*x**5 + 588.3*x**4 - 596.43*x**3 '
               '+ 249.62*x**2 -41.924*x + 6.4545;'
            'SIGMAcr = Kw*PI(1)**2*E*t**2/(12.*(1.-nu**2)*bw**2);'
            'MS = SIGMAcr/ABS(MIN(FA, 0.0001))-1.;')
        self.add_deqatn(deqatn)
        # reading variables
        dvar_t = self.dvars['STRZt']
        # reading constants
        dtable_b = self.dtables['STRZb'][0]
        dtable_h = self.dtables['STRZh'][0]
        # building DRESP1 that reads:
        # - axial stress
        OUTC = output_codes_SOL200.OUTC
        if eltype == 'CBAR':
            atta = OUTC['STRESS']['CBAR']['Axial']
        else:
            raise NotImplementedError('element %s not implemented' %
                                      eltype)
        eid = self.get_central_element().eid
        dresp_FA = DRESP1('STRZFA', 'STRESS', 'ELEM', region=None,
                          atta=atta, attb='', atti=eid)
        self.add_dresp(dresp_FA)
        # building DRESP2
        dresp2 = DRESP2('STRBUCK', deqatn.id)
        dresp2.dvars = [dvar_t.id]
        dresp2.dtable = [dtable_b, dtable_h, dtable_E, dtable_nu]
        dresp2.dresp1 = [dresp_FA.id]
        self.add_dresp(dresp2)
        # applying constraint
        dcid = self.constraints['buckling']
        dconstr = self.add_constraint(dcid, dresp2, ms, None)

    elif method == 1 and self.profile.lower() == 'z_t_b':
        # buckling equation
        deqatn = DEQATN(
            'bf(t, b, h, E, nu, FA) = b-t/2.;'
            'bw = h-t;'
            'x = bf/bw;'
            'Kw = -206.08*x**5 + 588.3*x**4 - 596.43*x**3 '
               '+ 249.62*x**2 -41.924*x + 6.4545;'
            'SIGMAcr = Kw*PI(1)**2*E*t**2/(12.*(1.-nu**2)*bw**2);'
            'MS = SIGMAcr/ABS(MIN(FA, 0.0001))-1.;')
        self.add_deqatn(deqatn)
        # reading variables
        dvar_t = self.dvars['STRZt']
        dvar_b = self.dvars['STRZb']
        # reading constants
        dtable_h = self.dtables['STRZh'][0]
        # building DRESP1 that reads:
        # - axial stress
        OUTC = output_codes_SOL200.OUTC
        if eltype == 'CBAR':
            atta = OUTC['STRESS']['CBAR']['Axial']
        else:
            raise NotImplementedError('element %s not implemented' %
                                      eltype)
        eid = self.get_central_element().eid
        dresp_FA = DRESP1('STRZFA', 'STRESS', 'ELEM', region=None,
                          atta=atta, attb='', atti=eid)
        self.add_dresp(dresp_FA)
        # building DRESP2
        dresp2 = DRESP2('STRBUCK', deqatn.id)
        dresp2.dvars = [dvar_t.id, dvar_b.id]
        dresp2.dtable = [dtable_h, dtable_E, dtable_nu]
        dresp2.dresp1 = [dresp_FA.id]
        self.add_dresp(dresp2)
        # applying constraint
        dcid = self.constraints['buckling']
        dconstr = self.add_constraint(dcid, dresp2, ms, None)

    elif method == 1 and self.profile.lower() == 'z_t_b_h':
        # buckling equation
        deqatn = DEQATN(
            'bf(t, b, h, E, nu, FA) = b-t/2.;'
            'bw = h-t;'
            'x = bf/bw;'
            'Kw = -206.08*x**5 + 588.3*x**4 - 596.43*x**3 '
               '+ 249.62*x**2 -41.924*x + 6.4545;'
            'SIGMAcr = Kw*PI(1)**2*E*t**2/(12.*(1.-nu**2)*bw**2);'
            'MS = SIGMAcr/ABS(MIN(FA, 0.0001))-1.;')
        self.add_deqatn(deqatn)
        # reading variables
        dvar_t = self.dvars['STRZt']
        dvar_b = self.dvars['STRZb']
        dvar_h = self.dvars['STRZh']
        # building DRESP1 that reads:
        # - axial stress
        OUTC = output_codes_SOL200.OUTC
        if eltype == 'CBAR':
            atta = OUTC['STRESS']['CBAR']['Axial']
        else:
            raise NotImplementedError('element %s not implemented' %
                                      eltype)
        eid = self.get_central_element().eid
        dresp_FA = DRESP1('STRZFA', 'STRESS', 'ELEM', region=None,
                          atta=atta, attb='', atti=eid)
        self.add_dresp(dresp_FA)
        # building DRESP2
        dresp2 = DRESP2('STRBUCK', deqatn.id)
        dresp2.dvars = [dvar_t.id, dvar_b.id, dvar_h.id]
        dresp2.dtable = [dtable_E, dtable_nu]
        dresp2.dresp1 = [dresp_FA.id]
        self.add_dresp(dresp2)
        # applying constraint
        dcid = self.constraints['buckling']
        dconstr = self.add_constraint(dcid, dresp2, ms, None)

    elif method == 1 and self.profile.lower() == 'b_t':
        # buckling equation
        # - considers combined compression + shear
        # - disconsiders bending effects
        # - assumes 3 edges simply supported and one free unloaded edge
        deqatn = DEQATN('kc(t, h, L, E, nu, PC, PS) = 0.456 + (h/L)**2;'
                        'FCcr = kc*PI(1)**2*E*t**2/(12.*(1.-nu**2)*h**2);'
                        'FC = PC/(t*h);'
                        'Rc = FC/FCcr;'
                        'x = L/h;'
                        'ks = 0.0648*x**6 - 1.2338*x**5 + 9.4869*x**4 -'
                        '37.697*x**3 + 81.88*x**2 - 93.218*x + 50.411;'
                        'ks = MAX(ks, 5.42);'
                        'FScr = ks*PI(1)**2*E*t**2/(12.*(1.-nu**2)*h**2);'
                        'FS = PS/(t*h);'
                        'Rs = FS/FScr;'
                        'MS = 2./(Rc + SQRT(Rc**2 + 4*Rs**2)) - 1.')
        self.add_deqatn(deqatn)
        # reading variables
        dvar_t = self.dvars['STRBt']
        # reading constants
        dtable_h = self.dtables['STRBh'][0]
        dtable_L = self.dtables['STRBL'][0]
        # building DRESP1s that read:
        # - axial force
        # - shear along Plane 1 (y axis)
        OUTC = output_codes_SOL200.OUTC
        if eltype == 'CBAR':
            code_PC = OUTC['FORCE']['CBAR']['Axial force']
            code_PS = OUTC['FORCE']['CBAR']['Shear plane 1']
        else:
            raise NotImplementedError('element %s not implemented' %
                                      eltype)
        eid = self.get_central_element().eid
        dresp_PC = DRESP1('STRPC', 'FORCE', 'ELEM', region=None,
                          atta=code_PC, attb='', atti=eid)
        dresp_PS = DRESP1('STRPS', 'FORCE', 'ELEM', region=None,
                          atta=code_PS, attb='', atti=eid)
        self.add_dresp(dresp_PC)
        self.add_dresp(dresp_PS)
        # building DRESP2
        dresp2 = DRESP2('STRBUCK', deqatn.id)
        dresp2.dvars = [dvar_t.id]
        dresp2.dtable = [dtable_h, dtable_L, dtable_E, dtable_nu]
        dresp2.dresp1 = [dresp_PC.id, dresp_PS.id]
        self.add_dresp(dresp2)
        # applying constraint
        dcid = self.constraints['buckling']
        dconstr = self.add_constraint(dcid, dresp2, ms, None)

    elif method == 1 and self.profile.lower() == 'b_t_h':
        # buckling equation
        # - considers combined compression + shear
        # - disconsiders bending effects
        # - assumes 3 edges simply supported and one free unloaded edge
        deqatn = DEQATN('kc(t, h, L, E, nu, PC, PS) = 0.456 + (h/L)**2;'
                        'FCcr = kc*PI(1)**2*E*t**2/(12.*(1.-nu**2)*h**2);'
                        'FC = PC/(t*h);'
                        'Rc = FC/FCcr;'
                        'x = L/h;'
                        'ks = 0.0648*x**6 - 1.2338*x**5 + 9.4869*x**4 -'
                        '37.697*x**3 + 81.88*x**2 - 93.218*x + 50.411;'
                        'ks = MAX(ks, 5.42);'
                        'FScr = ks*PI(1)**2*E*t**2/(12.*(1.-nu**2)*h**2);'
                        'FS = PS/(t*h);'
                        'Rs = FS/FScr;'
                        'MS = 2./(Rc + SQRT(Rc**2 + 4*Rs**2)) - 1.')
        self.add_deqatn(deqatn)
        # reading variables
        dvar_t = self.dvars['STRBt']
        dvar_h = self.dvars['STRBh']
        # reading constants
        dtable_L = self.dtables['STRBL'][0]
        # building DRESP1s that read:
        # - axial force
        # - shear along Plane 1 (y axis)
        OUTC = output_codes_SOL200.OUTC
        if eltype == 'CBAR':
            code_PC = OUTC['FORCE']['CBAR']['Axial force']
            code_PS = OUTC['FORCE']['CBAR']['Shear plane 1']
        else:
            raise NotImplementedError('element %s not implemented' %
                                      eltype)
        eid = self.get_central_element().eid
        dresp_PC = DRESP1('STRPC', 'FORCE', 'ELEM', region=None,
                          atta=code_PC, attb='', atti=eid)
        dresp_PS = DRESP1('STRPS', 'FORCE', 'ELEM', region=None,
                          atta=code_PS, attb='', atti=eid)
        self.add_dresp(dresp_PC)
        self.add_dresp(dresp_PS)
        # building DRESP2
        dresp2 = DRESP2('STRBUCK', deqatn.id)
        dresp2.dvars = [dvar_t.id, dvar_h.id]
        dresp2.dtable = [dtable_L, dtable_E, dtable_nu]
        dresp2.dresp1 = [dresp_PC.id, dresp_PS.id]
        self.add_dresp(dresp2)
        # applying constraint
        dcid = self.constraints['buckling']
        dconstr = self.add_constraint(dcid, dresp2, ms, None)

    else:
        raise NotImplementedError('Stringer %s profile not supported!' %
                                  self.profile)

