from ..cards_opt import (DRESP1, DCONSTR, DEQATN, DRESP2, DRESP3, DESVAR,
        DVPREL1, DVPREL2)
import ..output_codes as output_codes_SOL200


def constrain_vonMises(panel, Fcy, average=False, dcid=1):
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
    panel.create_dvars()
    if not average:
        eid = panel.get_central_element().eid

        dcid = dcid
        OUTC = output_codes_SOL200.OUTC

        atta = OUTC['STRESS']['CQUAD4']['von Mises or maximum shear at Z1']
        dresp1 = DRESP1('PANZ1VM', 'STRESS', 'ELEM', None, atta=atta,
                        attb=None, atti=eid)
        panel.add_dresp(dresp1)
        panel.add_constraint(dcid, dresp1, None, Fcy)

        atta = OUTC['STRESS']['CQUAD4']['von Mises or maximum shear at Z2']
        dresp1 = DRESP1('PANZ2VM', 'STRESS', 'ELEM', None, atta=atta,
                        attb=None, atti=eid)
        panel.add_dresp(dresp1)
        panel.add_constraint(dcid, dresp1, None, Fcy)

    else:
        dcid = dcid
        OUTC = output_codes_SOL200.OUTC
        atta = OUTC['STRESS']['CQUAD4']['von Mises or maximum shear at Z1']
        dresp1_bot = []
        dresp1_top = []
        for eid in panel.eids:
            dresp1 = DRESP1('PANZ1VM', 'STRESS', 'ELEM', None, atta=atta,
                            attb=None, atti=eid)
            panel.add_dresp(dresp1)
            dresp1_bot.append(dresp1)

            atta = OUTC['STRESS']['CQUAD4']['von Mises or maximum shear at Z2']
            dresp1 = DRESP1('PANZ2VM', 'STRESS', 'ELEM', None, atta=atta,
                            attb=None, atti=eid)
            panel.add_dresp(dresp1)
            dresp1_top.append(dresp1)

        dresp2_bot = DRESP2('PANZ1VMA', eqid='AVG')
        dresp2_bot.dresp1 = dresp1_bot[:]
        panel.add_dresp(dresp2_bot)
        panel.add_constraint(dcid, dresp2_bot, None, Fcy)

        dresp2_top = DRESP2('PANZ2VMA', eqid='AVG')
        dresp2_top.dresp1 = dresp1_top[:]
        panel.add_dresp(dresp2_top)
        panel.add_constraint(dcid, dresp2_top, None, Fcy)


def constrain_buckling(panel, method=1, ms=0.1):
    """Add a buckling constraint

    Parameters
    ----------
    method : int, optional
        Select one of the following methods for buckling calculation:

        - `1` : Bruhn's method using Equation C9.4:

                - considers compressive (Nxx only) and shear loads
                - no plasticity correction has been implemented

    ms : float, optional
        Minimum margin of safety to be used as constraint.

    """
    OUTC = output_codes_SOL200.OUTC

    eid = panel.get_central_element().eid

    # reading membrane force Nxx
    code_Nxx = OUTC['FORCE']['CQUAD4']['Membrane force x']
    dresp_Nxx = DRESP1('PANfNxx', 'FORCE', 'ELEM', region=None,
                       atta=code_Nxx, attb=None, atti=eid)
    panel.add_dresp(dresp_Nxx)
    # reading membrane force Nxy
    code_Nxy = OUTC['FORCE']['CQUAD4']['Membrane force xy']
    dresp_Nxy = DRESP1('PANfNxy', 'FORCE', 'ELEM', region=None,
                       atta=code_Nxy, attb=None, atti=eid)
    panel.add_dresp(dresp_Nxy)
    # calculating the margin of safety using an external subroutine
    dresp = DRESP3('PANBUCK1', 'PANBUCK', 'METHOD1')
    dresp.add_dvar(panel.dvars['PANt'].id)
    dresp.add_dtable(panel.dtables['PANr'][0])
    dresp.add_dtable(panel.dtables['PANa'][0])
    dresp.add_dtable(panel.dtables['PANb'][0])
    dresp.add_dtable(panel.dtables['PANE'][0])
    dresp.add_dtable(panel.dtables['PANnu'][0])
    dresp.add_dresp1(dresp_Nxx.id)
    dresp.add_dresp1(dresp_Nxy.id)
    panel.add_dresp(dresp)
