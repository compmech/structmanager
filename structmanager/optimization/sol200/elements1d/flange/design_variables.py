from structmanager.sol200 import (DRESP1, DCONSTR, DEQATN, DRESP2, DESVAR,
                              DVPREL1, DVPREL2)

import structmanager.sol200.output_codes as output_codes_SOL200


def create_dvars(flange):
    if flange.dvars_created:
        return
    flange.dvars_created = True
    pid = flange.pid
    ptype = flange.ptype

    flange.add_dtable('FLAL', flange.L)
    flange.add_dtable('FLAE', flange.material.E)
    flange.add_dtable('FLAnu', flange.material.nu)

    if flange.profile.lower() == 't':
        dvar_t = DESVAR('FLAt', flange.t, flange.t_lb, flange.t_ub)
        flange.add_dvar(dvar_t)
        dtable_b = flange.add_dtable('FLAb', flange.b)
        if ptype == 'PBAR':
            # calculating A
            deqatn = DEQATN('A(t,b) = t*b')
            flange.add_deqatn(deqatn)
            dvprel = DVPREL2('PBAR', pid=pid, pname='A', eqid=deqatn.id)
            dvprel.add_dvar(dvar_t.id)
            dvprel.add_dtable(dtable_b)
            flange.add_dvprel(dvprel)
            # assuming y-axis towards radial (normal) direction
            # calculating I1 = Izz
            deqatn = DEQATN('I1(t,b) = b*t**3/12.')
            flange.add_deqatn(deqatn)
            dvprel = DVPREL2('PBAR', pid=pid, pname='I1', eqid=deqatn.id)
            dvprel.add_dvar(dvar_t.id)
            dvprel.add_dtable(dtable_b)
            flange.add_dvprel(dvprel)
            # calculating I2 = Iyy
            deqatn = DEQATN('I2(t,b) = t*b**3/12. + t*b*(b/2.)**2')
            flange.add_deqatn(deqatn)
            dvprel = DVPREL2('PBAR', pid=pid, pname='I2', eqid=deqatn.id)
            dvprel.add_dvar(dvar_t.id)
            dvprel.add_dtable(dtable_b)
            flange.add_dvprel(dvprel)
            # calculating J
            deqatn = DEQATN('I1(t,b) = b*t**3/12.;'
                            'I2 = t*b**3/12. + t*b*(b/2.)**2;'
                            'J = I1 + I2')
            flange.add_deqatn(deqatn)
            dvprel = DVPREL2('PBAR', pid=pid, pname='J', eqid=deqatn.id)
            dvprel.add_dvar(dvar_t.id)
            dvprel.add_dtable(dtable_b)
            flange.add_dvprel(dvprel)
        else:
            raise NotImplementedError('%s not supported!' % ptype)

    elif flange.profile.lower() == 't_b':
        dvar_t = DESVAR('FLAt', flange.t, flange.t_lb, flange.t_ub)
        dvar_b = DESVAR('FLAb', flange.b, flange.b_lb, flange.b_ub)
        flange.add_dvar(dvar_t)
        flange.add_dvar(dvar_b)
        if ptype == 'PBAR':
            # calculating A
            deqatn = DEQATN('A(t,b) = t*b')
            flange.add_deqatn(deqatn)
            dvprel = DVPREL2('PBAR', pid=pid, pname='A', eqid=deqatn.id)
            dvprel.add_dvar(dvar_t.id)
            dvprel.add_dvar(dvar_b.id)
            flange.add_dvprel(dvprel)
            # assuming y-axis towards radial (normal) direction
            # calculating I1 = Izz
            deqatn = DEQATN('I1(t,b) = b*t**3/12.')
            flange.add_deqatn(deqatn)
            dvprel = DVPREL2('PBAR', pid=pid, pname='I1', eqid=deqatn.id)
            dvprel.add_dvar(dvar_t.id)
            dvprel.add_dvar(dvar_b.id)
            flange.add_dvprel(dvprel)
            # calculating I2 = Iyy
            deqatn = DEQATN('I2(t,b) = t*b**3/12. + t*b*(b/2.)**2')
            flange.add_deqatn(deqatn)
            dvprel = DVPREL2('PBAR', pid=pid, pname='I2', eqid=deqatn.id)
            dvprel.add_dvar(dvar_t.id)
            dvprel.add_dvar(dvar_b.id)
            flange.add_dvprel(dvprel)
            # calculating J
            deqatn = DEQATN('I1(t,b) = b*t**3/12.;'
                            'I2 = t*b**3/12. + t*b*(b/2.)**2;'
                            'J = I1 + I2')
            flange.add_deqatn(deqatn)
            dvprel = DVPREL2('PBAR', pid=pid, pname='J', eqid=deqatn.id)
            dvprel.add_dvar(dvar_t.id)
            dvprel.add_dvar(dvar_b.id)
            flange.add_dvprel(dvprel)
        else:
            raise NotImplementedError('%s not supported!' % ptype)

