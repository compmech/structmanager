from ..cards_opt import DESVAR, DVPREL1


def create(panel, pid):
    if panel.dvars_created:
        return
    panel.dvars_created = True
    pid = panel.pid
    ptype = panel.ptype

    if ptype == 'PSHELL':
        dvar_t = DESVAR('PANt', panel.t, panel.t_lb, panel.t_ub)
        panel.add_dvar(dvar_t)
        dvprel = DVPREL1('PSHELL', pid=pid, pname='T', dvids=[dvar_t.id],
                         coeffs=[1.])
        panel.add_dvprel(dvprel)
        panel.add_dtable('PANr', panel.r)
        panel.add_dtable('PANa', panel.a)
        panel.add_dtable('PANb', panel.b)
        panel.add_dtable('PANE', panel.E)
        panel.add_dtable('PANnu', panel.nu)
    else:
        raise NotImplementedError('%s not supported!' % ptype)
