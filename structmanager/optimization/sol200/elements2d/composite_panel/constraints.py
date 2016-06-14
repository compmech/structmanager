import structmanager.sol200.output_codes as output_codes_SOL200


def constrain_buckling(panelcomp, eig=1.0):

    OUTC = output_codes_SOL200.OUTC

    eid = panelcomp.get_central_element().eid

    dcid = panelcomp.constraints['buckling']

    # reading membrane force Nxx
    code_Nxx = OUTC['FORCE']['CQUAD4']['Membrane force x']
    dresp_Nxx = DRESP1('PCfNxx', 'FORCE', 'ELEM', region=None,
                       atta=code_Nxx, attb=None, atti=eid)
    panelcomp.add_dresp(dresp_Nxx)

    # reading membrane force Nyy
    code_Nyy = OUTC['FORCE']['CQUAD4']['Membrane force y']
    dresp_Nyy = DRESP1('PCfNyy', 'FORCE', 'ELEM', region=None,
                       atta=code_Nyy, attb=None, atti=eid)
    panelcomp.add_dresp(dresp_Nyy)

    # reading membrane force Nxy
    code_Nxy = OUTC['FORCE']['CQUAD4']['Membrane force xy']
    dresp_Nxy = DRESP1('PCfNxy', 'FORCE', 'ELEM', region=None,
                       atta=code_Nxy, attb=None, atti=eid)
    panelcomp.add_dresp(dresp_Nxy)

    # calculating buckling eigenvalue using an external subroutine
    # all parameters (desvars, dtables, dresp's) that this DRESP3 needs to run are listed below
    # creating DRESP3
    dresp = DRESP3('PCBUCK1', 'PCBUCK', 'BUCK_PC')
    dresp.add_dvar(panelcomp.dvars['PCt'].id)
    #dresp.add_dvar(dvar_t.id)
    dresp.add_dtable(panelcomp.dtables['PCa'][0])
    dresp.add_dtable(panelcomp.dtables['PCb'][0])
    dresp.add_dtable(panelcomp.dtables['PCr'][0])
    dresp.add_dtable(panelcomp.dtables['PCE1'][0])
    dresp.add_dtable(panelcomp.dtables['PCE2'][0])
    dresp.add_dtable(panelcomp.dtables['PCG12'][0])
    dresp.add_dtable(panelcomp.dtables['PCn12'][0])
    dresp.add_dtable(panelcomp.dtables['PCn21'][0])
    dresp.add_dresp1(dresp_Nxx.id)
    dresp.add_dresp1(dresp_Nyy.id)
    dresp.add_dresp1(dresp_Nxy.id)
    panelcomp.add_dresp(dresp)
    # applying constraint of buckling: lower eigenvalue >= 1.0
    panelcomp.add_constraint(dcid, dresp, eig, None)

