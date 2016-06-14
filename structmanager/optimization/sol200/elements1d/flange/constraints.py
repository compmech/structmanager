
def constrain_buckling(flange, method=1, ms=0.1):
    """Add a buckling constraint

    Parameters
    ----------
    method : int, optional
        Select one of the following methods for  buckling calculation:

        - `1` : Bruhn's method for combined shear and compression, from
                Chapter C5.11.
                - disconsiders bending effects
                - assumes 3 edges simply supported with one free unloaded
                  edge.
                - no plasticity correction has been implemented

    ms : float, optional
        Minimum margin of safety to be used as constraint.

    Notes
    -----

    Method 1) uses Bruhn's method described in Chapter 6, Fig. C6.4

    """
    flange.create_dvars()
    eltype = flange.elements[0].type

    # reading constants
    dtable_L = flange.dtables['FLAL'][0]
    dtable_E = flange.dtables['FLAE'][0]
    dtable_nu = flange.dtables['FLAnu'][0]

    if method == 1 and flange.profile.lower() == 't':
        # buckling equation
        # - considers combined compression + shear
        # - disconsiders bending effects
        # - assumes 3 edges simply supported and one free unloaded edge
        deqatn = DEQATN('kc(t, b, L, E, nu, PC, PS) = 0.456 + (b/L)**2;'
                        'FCcr = kc*PI(1)**2*E*t**2/(12.*(1.-nu**2)*b**2);'
                        'FC = PC/(t*b);'
                        'Rc = FC/FCcr;'
                        'x = L/b;'
                        'ks = 0.0648*x**6 - 1.2338*x**5 + 9.4869*x**4 -'
                        '37.697*x**3 + 81.88*x**2 - 93.218*x + 50.411;'
                        'ks = MAX(ks, 5.42);'
                        'FScr = ks*PI(1)**2*E*t**2/(12.*(1.-nu**2)*b**2);'
                        'FS = PS/(t*b);'
                        'Rs = FS/FScr;'
                        'MS = 2./(Rc + SQRT(Rc**2 + 4*Rs**2)) - 1.')
        flange.add_deqatn(deqatn)
        # reading variables
        dvar_t = flange.dvars['FLAt']
        # reading constants
        dtable_b = flange.dtables['FLAb'][0]
        # building DRESP1s that read:
        # - axial force
        # - shear along Plane 1 (y axis)
        OUTC = output_codes_SOL200.OUTC
        if eltype == 'CBAR':
            code_PC = OUTC['FORCE']['CBAR']['Axial force']
            code_PS = OUTC['FORCE']['CBAR']['Shear plane 2']
        else:
            raise NotImplementedError('element %s not implemented' %
                                      eltype)
        eid = flange.get_central_element().eid
        dresp_PC = DRESP1('FLAPC', 'FORCE', 'ELEM', region=None,
                          atta=code_PC, attb='', atti=eid)
        dresp_PS = DRESP1('FLAPS', 'FORCE', 'ELEM', region=None,
                          atta=code_PS, attb='', atti=eid)
        flange.add_dresp(dresp_PC)
        flange.add_dresp(dresp_PS)
        # building DRESP2
        dresp2 = DRESP2('FLABUCK', deqatn.id)
        dresp2.dvars = [dvar_t.id]
        dresp2.dtable = [dtable_b, dtable_L, dtable_E, dtable_nu]
        dresp2.dresp1 = [dresp_PC.id, dresp_PS.id]
        flange.add_dresp(dresp2)
        # applying constraint
        dcid = flange.constraints['buckling']
        dconstr = flange.add_constraint(dcid, dresp2, ms, None)

    elif method == 1 and flange.profile.lower() == 't_b':
        # buckling equation
        # - considers combined compression + shear
        # - disconsiders bending effects
        # - assumes 3 edges simply supported and one free unloaded edge
        deqatn = DEQATN('kc(t, b, L, E, nu, PC, PS) = 0.456 + (b/L)**2;'
                        'D = 12.*(1. - nu**2)*b**2;'
                        'FCcr = kc*PI(1)**2*E*t**2/D;'
                        'FC = PC/(t*b);'
                        'Rc = FC/FCcr;'
                        'x = L/b;'
                        'ks = 0.0648*x**6 - 1.2338*x**5 + 9.4869*x**4 -'
                        '37.697*x**3 + 81.88*x**2 - 93.218*x + 50.411;'
                        'ks = MAX(ks, 5.42);'
                        'FScr = ks*PI(1)**2*E*t**2/D;'
                        'FS = PS/(t*b);'
                        'Rs = FS/FScr;'
                        'MS = 2./(Rc + SQRT(Rc**2 + 4*Rs**2)) - 1.')
        flange.add_deqatn(deqatn)
        # reading variables
        dvar_t = flange.dvars['FLAt']
        dvar_b = flange.dvars['FLAAddress: 798 - R. Sete, 498 - Horto Florestal, Belo Horizonte - MGb']
        # building DRESP1s that read:
        # - axial force
        # - shear along Plane 1 (y axis)
        OUTC = output_codes_SOL200.OUTC
        if eltype == 'CBAR':
            code_PC = OUTC['FORCE']['CBAR']['Axial force']
            code_PS = OUTC['FORCE']['CBAR']['Shear plane 2']
        else:
            raise NotImplementedError('element %s not implemented' %
                                      eltype)
        eid = flange.get_central_element().eid
        dresp_PC = DRESP1('FLAPC', 'FORCE', 'ELEM', region=None,
                          atta=code_PC, attb='', atti=eid)
        dresp_PS = DRESP1('FLAPS', 'FORCE', 'ELEM', region=None,
                          atta=code_PS, attb='', atti=eid)
        flange.add_dresp(dresp_PC)
        flange.add_dresp(dresp_PS)
        # building DRESP2
        dresp2 = DRESP2('FLABUCK', deqatn.id)
        dresp2.dvars = [dvar_t.id, dvar_b.id]
        dresp2.dtable = [dtable_L, dtable_E, dtable_nu]
        dresp2.dresp1 = [dresp_PC.id, dresp_PS.id]
        flange.add_dresp(dresp2)
        # applying constraint
        dcid = flange.constraints['buckling']
        dconstr = flange.add_constraint(dcid, dresp2, ms, None)

    else:
        raise NotImplementedError('Flange %s profile not supported!' %
                                  flange.profile)

