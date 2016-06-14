from structmanager.sol200 import (DRESP1, DCONSTR, DEQATN, DRESP2, DRESP3,
        DESVAR, DTABLE, DVPREL1, DVPREL2)


def create_dvars(panelcomp):
    if panelcomp.dvars_created:
        return
    panelcomp.dvars_created = True
    pid = panelcomp.pid
    ptype = panelcomp.ptype

    if ptype == 'PCOMP':
        dvar_t = DESVAR('PCt', panelcomp.t, panelcomp.t_lb, panelcomp.t_ub)
        panelcomp.add_dvar(dvar_t)
        dvar_p45 = DESVAR('PCp45', panelcomp.p45, panelcomp.p45_lb, panelcomp.p45_ub)
        panelcomp.add_dvar(dvar_p45)
        panelcomp.add_dtable('P90', panelcomp.p90)
        #DONE
        panelcomp.add_dtable('PCa', panelcomp.a)
        panelcomp.add_dtable('PCb', panelcomp.b)
        panelcomp.add_dtable('PCr', panelcomp.r)
        panelcomp.add_dtable('PCE1', panelcomp.E1)
        panelcomp.add_dtable('PCE2', panelcomp.E2)
        panelcomp.add_dtable('PCG12', panelcomp.G12)
        panelcomp.add_dtable('PCn12', panelcomp.nu12)
        panelcomp.add_dtable('PCn21', panelcomp.nu21)

        deqatn0 = DEQATN('T0(t,p45,p90) = (1.-p45-p90)*t')
        panelcomp.add_deqatn(deqatn0)
        dvprel2 = DVPREL2('PCOMP', pid, 'T1', deqatn0.id)
        dvprel2.add_dvar(dvar_t.id)
        dvprel2.add_dvar(dvar_p45.id)
        dvprel2.add_dtable(panelcomp.dtables['P90'][0])
        panelcomp.add_dvprel(dvprel2)

        #DONE
        deqatn45 = DEQATN('T45(t,p45) = (p45/2.)*t')
        panelcomp.add_deqatn(deqatn45)
        dvprel2 = DVPREL2('PCOMP', pid, 'T2', deqatn45.id)
        #dvprel2.dvars = [dvar_t.id, dvar_p45.id]
        dvprel2.add_dvar(dvar_t.id)
        dvprel2.add_dvar(dvar_p45.id)
        panelcomp.add_dvprel(dvprel2)

        #DONE
        dvprel2 = DVPREL2('PCOMP', pid, 'T3', deqatn45.id)
        #dvprel2.dvars = [dvar_t.id, dvar_p45.id]
        dvprel2.add_dvar(dvar_t.id)
        dvprel2.add_dvar(dvar_p45.id)
        panelcomp.add_dvprel(dvprel2)

        #DONE
        deqatn90 = DEQATN('T90(t,p90) = p90*t')
        panelcomp.add_deqatn(deqatn90)
        dvprel2 = DVPREL2('PCOMP', pid, 'T4', deqatn90.id)
        #dvprel2.dvars = [dvar_t.id]
        dvprel2.add_dvar(dvar_t.id)
        dvprel2.add_dtable(panelcomp.dtables['P90'][0])
        panelcomp.add_dvprel(dvprel2)

    else:
        raise NotImplementedError('%s not supported!' % ptype)

