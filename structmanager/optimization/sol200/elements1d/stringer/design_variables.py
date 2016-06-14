from structmanager.sol200 import (DRESP1, DCONSTR, DEQATN, DRESP2, DESVAR,
                              DVPREL1, DVPREL2)


def create_dvars(stringer):
    if stringer.dvars_created:
        return
    stringer.dvars_created = True
    pid = stringer.pid
    ptype = stringer.ptype

    stringer.add_dtable('STRE', stringer.E)
    stringer.add_dtable('STRnu', stringer.nu)

    if stringer.profile.lower() == 'z_t':
        dvar_t = DESVAR('STRZt', stringer.t, stringer.t_lb, stringer.t_ub)
        stringer.add_dvar(dvar_t)
        dtable_b = stringer.add_dtable('STRZb', stringer.b)
        dtable_h = stringer.add_dtable('STRZh', stringer.h)
        if ptype == 'PBAR':
            # calculating A
            deqatn = DEQATN('A(t,b,h) = 2*t*b + t*h')
            stringer.add_deqatn(deqatn)
            dvprel = DVPREL2('PBAR', pid=pid, pname='A', eqid=deqatn.id)
            dvprel.add_dvar(dvar_t.id)
            dvprel.add_dtable(dtable_b)
            dvprel.add_dtable(dtable_h)
            stringer.add_dvprel(dvprel)
            # assuming y-axis towards radial (normal) direction
            # calculating I1 = Izz
            deqatn = DEQATN('I1f(t,b,h) = t*b**3/12.;'
                            'I1w = h*t**3/12.;'
                            'd = t/2. + b/2.;'
                            'Ad2f = t*b*d**2;'
                            'I1 = 2*(I1f + Ad2f) + I1w')
            stringer.add_deqatn(deqatn)
            dvprel = DVPREL2('PBAR', pid=pid, pname='I1', eqid=deqatn.id)
            dvprel.add_dvar(dvar_t.id)
            dvprel.add_dtable(dtable_b)
            dvprel.add_dtable(dtable_h)
            stringer.add_dvprel(dvprel)
            # calculating I2 = Iyy
            deqatn = DEQATN('I2f(t,b,h) = b*t**3/12.;'
                            'I2w = t*h**3/12.;'
                            'd = h/2. - t/2.;'
                            'Ad2f = t*b*d**2;'
                            'I2 = 2*(I2f + Ad2f) + I2w')
            stringer.add_deqatn(deqatn)
            dvprel = DVPREL2('PBAR', pid=pid, pname='I2', eqid=deqatn.id)
            dvprel.add_dvar(dvar_t.id)
            dvprel.add_dtable(dtable_b)
            dvprel.add_dtable(dtable_h)
            stringer.add_dvprel(dvprel)
            # calculating J
            deqatn = DEQATN('I1f(t,b,h) = t*b**3/12.;'
                            'I1w = h*t**3/12.;'
                            'd = t/2. + b/2.;'
                            'Ad2f = t*b*d**2;'
                            'I1 = 2*(I1f + Ad2f) + I1w;'
                            'I2f = b*t**3/12.;'
                            'I2w = t*h**3/12.;'
                            'd = h/2. - t/2.;'
                            'Ad2f = t*b*d**2;'
                            'I2 = 2*(I2f + Ad2f) + I2w;'
                            'J = I1 + I2')
            stringer.add_deqatn(deqatn)
            dvprel = DVPREL2('PBAR', pid=pid, pname='J', eqid=deqatn.id)
            dvprel.add_dvar(dvar_t.id)
            dvprel.add_dtable(dtable_b)
            dvprel.add_dtable(dtable_h)
            stringer.add_dvprel(dvprel)
        else:
            raise NotImplementedError('%s not supported!' % ptype)

    elif stringer.profile.lower() == 'z_t_b':
        dvar_t = DESVAR('STRZt', stringer.t, stringer.t_lb, stringer.t_ub)
        dvar_b = DESVAR('STRZb', stringer.b, stringer.b_lb, stringer.b_ub)
        stringer.add_dvar(dvar_t)
        stringer.add_dvar(dvar_b)
        dtable_h = stringer.add_dtable('STRZh', stringer.h)
        if ptype == 'PBAR':
            # calculating A
            deqatn = DEQATN('A(t,b,h) = 2*t*b + t*h')
            stringer.add_deqatn(deqatn)
            dvprel = DVPREL2('PBAR', pid=pid, pname='A', eqid=deqatn.id)
            dvprel.add_dvar(dvar_t.id)
            dvprel.add_dvar(dvar_b.id)
            dvprel.add_dtable(dtable_h)
            stringer.add_dvprel(dvprel)
            # assuming y-axis towards radial (normal) direction
            # calculating I1 = Izz
            deqatn = DEQATN('I1f(t,b,h) = t*b**3/12.;'
                            'I1w = h*t**3/12.;'
                            'd = t/2. + b/2.;'
                            'Ad2f = t*b*d**2;'
                            'I1 = 2*(I1f + Ad2f) + I1w')
            stringer.add_deqatn(deqatn)
            dvprel = DVPREL2('PBAR', pid=pid, pname='I1', eqid=deqatn.id)
            dvprel.add_dvar(dvar_t.id)
            dvprel.add_dvar(dvar_b.id)
            dvprel.add_dtable(dtable_h)
            stringer.add_dvprel(dvprel)
            # calculating I2 = Iyy
            deqatn = DEQATN('I2f(t,b,h) = b*t**3/12.;'
                            'I2w = t*h**3/12.;'
                            'd = h/2. - t/2.;'
                            'Ad2f = t*b*d**2;'
                            'I2 = 2*(I2f + Ad2f) + I2w')
            stringer.add_deqatn(deqatn)
            dvprel = DVPREL2('PBAR', pid=pid, pname='I2', eqid=deqatn.id)
            dvprel.add_dvar(dvar_t.id)
            dvprel.add_dvar(dvar_b.id)
            dvprel.add_dtable(dtable_h)
            stringer.add_dvprel(dvprel)
            # calculating J
            deqatn = DEQATN('I1f(t,b,h) = t*b**3/12.;'
                            'I1w = h*t**3/12.;'
                            'd = t/2. + b/2.;'
                            'Ad2f = t*b*d**2;'
                            'I1 = 2*(I1f + Ad2f) + I1w;'
                            'I2f = b*t**3/12.;'
                            'I2w = t*h**3/12.;'
                            'd = h/2. - t/2.;'
                            'Ad2f = t*b*d**2;'
                            'I2 = 2*(I2f + Ad2f) + I2w;'
                            'J = I1 + I2')
            stringer.add_deqatn(deqatn)
            dvprel = DVPREL2('PBAR', pid=pid, pname='J', eqid=deqatn.id)
            dvprel.add_dvar(dvar_t.id)
            dvprel.add_dvar(dvar_b.id)
            dvprel.add_dtable(dtable_h)
            stringer.add_dvprel(dvprel)
        else:
            raise NotImplementedError('%s not supported!' % ptype)

    elif stringer.profile.lower() == 'z_t_b_h':
        dvar_t = DESVAR('STRZt', stringer.t, stringer.t_lb, stringer.t_ub)
        dvar_b = DESVAR('STRZb', stringer.b, stringer.b_lb, stringer.b_ub)
        dvar_h = DESVAR('STRZh', stringer.h, stringer.h_lb, stringer.h_ub)
        stringer.add_dvar(dvar_t)
        stringer.add_dvar(dvar_b)
        stringer.add_dvar(dvar_h)
        if ptype == 'PBAR':
            # calculating A
            deqatn = DEQATN('A(t,b,h) = 2*t*b + t*h')
            stringer.add_deqatn(deqatn)
            dvprel = DVPREL2('PBAR', pid=pid, pname='A', eqid=deqatn.id)
            dvprel.add_dvar(dvar_t.id)
            dvprel.add_dvar(dvar_b.id)
            dvprel.add_dvar(dvar_h.id)
            stringer.add_dvprel(dvprel)
            # assuming y-axis towards radial (normal) direction
            # calculating I1 = Izz
            deqatn = DEQATN('I1f(t,b,h) = t*b**3/12.;'
                            'I1w = h*t**3/12.;'
                            'd = t/2. + b/2.;'
                            'Ad2f = t*b*d**2;'
                            'I1 = 2*(I1f + Ad2f) + I1w')
            stringer.add_deqatn(deqatn)
            dvprel = DVPREL2('PBAR', pid=pid, pname='I1', eqid=deqatn.id)
            dvprel.add_dvar(dvar_t.id)
            dvprel.add_dvar(dvar_b.id)
            dvprel.add_dvar(dvar_h.id)
            stringer.add_dvprel(dvprel)
            # calculating I2 = Iyy
            deqatn = DEQATN('I2f(t,b,h) = b*t**3/12.;'
                            'I2w = t*h**3/12.;'
                            'd = h/2. - t/2.;'
                            'Ad2f = t*b*d**2;'
                            'I2 = 2*(I2f + Ad2f) + I2w')
            stringer.add_deqatn(deqatn)
            dvprel = DVPREL2('PBAR', pid=pid, pname='I2', eqid=deqatn.id)
            dvprel.add_dvar(dvar_t.id)
            dvprel.add_dvar(dvar_b.id)
            dvprel.add_dvar(dvar_h.id)
            stringer.add_dvprel(dvprel)
            # calculating J
            deqatn = DEQATN('I1f(t,b,h) = t*b**3/12.;'
                            'I1w = h*t**3/12.;'
                            'd = t/2. + b/2.;'
                            'Ad2f = t*b*d**2;'
                            'I1 = 2*(I1f + Ad2f) + I1w;'
                            'I2f = b*t**3/12.;'
                            'I2w = t*h**3/12.;'
                            'd = h/2. - t/2.;'
                            'Ad2f = t*b*d**2;'
                            'I2 = 2*(I2f + Ad2f) + I2w;'
                            'J = I1 + I2')
            stringer.add_deqatn(deqatn)
            dvprel = DVPREL2('PBAR', pid=pid, pname='J', eqid=deqatn.id)
            dvprel.add_dvar(dvar_t.id)
            dvprel.add_dvar(dvar_b.id)
            dvprel.add_dvar(dvar_h.id)
            stringer.add_dvprel(dvprel)
        else:
            raise NotImplementedError('%s not supported!' % ptype)

    elif stringer.profile.lower() == 'z_tf_tw_b_h':
        dvar_tf = DESVAR('STRZtf', stringer.tf, stringer.tf_lb, stringer.tf_ub)
        dvar_tw = DESVAR('STRZtw', stringer.tw, stringer.tw_lb, stringer.tw_ub)
        dvar_b = DESVAR('STRZb', stringer.b, stringer.b_lb, stringer.b_ub)
        dvar_h = DESVAR('STRZh', stringer.h, stringer.h_lb, stringer.h_ub)
        stringer.add_dvar(dvar_tf)
        stringer.add_dvar(dvar_tw)
        stringer.add_dvar(dvar_b)
        stringer.add_dvar(dvar_h)
        if ptype == 'PBAR':
            # calculating A
            deqatn = DEQATN('A(tf,tw,b,h) = 2*tf*b + tw*h')
            stringer.add_deqatn(deqatn)
            dvprel = DVPREL2('PBAR', pid=pid, pname='A', eqid=deqatn.id)
            dvprel.add_dvar(dvar_tf.id)
            dvprel.add_dvar(dvar_tw.id)
            dvprel.add_dvar(dvar_b.id)
            dvprel.add_dvar(dvar_h.id)
            stringer.add_dvprel(dvprel)
            # assuming y-axis towards radial (normal) direction
            # calculating I1 = Izz
            deqatn = DEQATN('I1f(tf,tw,b,h) = tf*b**3/12.;'
                            'I1w = h*tw**3/12.;'
                            'd = tw/2. + b/2.;'
                            'Ad2f = tf*b*d**2;'
                            'I1 = 2*(I1f + Ad2f) + I1w')
            stringer.add_deqatn(deqatn)
            dvprel = DVPREL2('PBAR', pid=pid, pname='I1', eqid=deqatn.id)
            dvprel.add_dvar(dvar_tf.id)
            dvprel.add_dvar(dvar_tw.id)
            dvprel.add_dvar(dvar_b.id)
            dvprel.add_dvar(dvar_h.id)
            stringer.add_dvprel(dvprel)
            # calculating I2 = Iyy
            deqatn = DEQATN('I2f(tf,tw,b,h) = b*tf**3/12.;'
                            'I2w = tw*h**3/12.;'
                            'd = h/2. - tf/2.;'
                            'Ad2f = tf*b*d**2;'
                            'I2 = 2*(I2f + Ad2f) + I2w')
            stringer.add_deqatn(deqatn)
            dvprel = DVPREL2('PBAR', pid=pid, pname='I2', eqid=deqatn.id)
            dvprel.add_dvar(dvar_tf.id)
            dvprel.add_dvar(dvar_tw.id)
            dvprel.add_dvar(dvar_b.id)
            dvprel.add_dvar(dvar_h.id)
            stringer.add_dvprel(dvprel)
            # calculating J
            deqatn = DEQATN('I1f(tf,tw,b,h) = tf*b**3/12.;'
                            'I1w = h*tw**3/12.;'
                            'd = tw/2. + b/2.;'
                            'Ad2f = tf*b*d**2;'
                            'I1 = 2*(I1f + Ad2f) + I1w;'
                            'I2f = b*tf**3/12.;'
                            'I2w = tw*h**3/12.;'
                            'd = h/2. - tf/2.;'
                            'Ad2f = tf*b*d**2;'
                            'I2 = 2*(I2f + Ad2f) + I2w;'
                            'J = I1 + I2')
            stringer.add_deqatn(deqatn)
            dvprel = DVPREL2('PBAR', pid=pid, pname='J', eqid=deqatn.id)
            dvprel.add_dvar(dvar_tf.id)
            dvprel.add_dvar(dvar_tw.id)
            dvprel.add_dvar(dvar_b.id)
            dvprel.add_dvar(dvar_h.id)
            stringer.add_dvprel(dvprel)
        else:
            raise NotImplementedError('%s not supported!' % ptype)

    elif stringer.profile.lower() == 'b_t':
        dvar_t = DESVAR('STRBt', stringer.t, stringer.t_lb, stringer.t_ub)
        stringer.add_dvar(dvar_t)
        dtable_h = stringer.add_dtable('STRBh', stringer.h)
        stringer.add_dtable('STRBL', stringer.L)
        if ptype == 'PBAR':
            # calculating A
            deqatn = DEQATN('A(t,h) = t*h')
            stringer.add_deqatn(deqatn)
            dvprel = DVPREL2('PBAR', pid=pid, pname='A', eqid=deqatn.id)
            dvprel.add_dvar(dvar_t.id)
            dvprel.add_dtable(dtable_h)
            stringer.add_dvprel(dvprel)
            # assuming y-axis towards radial (normal) direction
            # calculating I1 = Izz
            deqatn = DEQATN('I1(t,h) = t*h**3/12. + t*h*(h/2.)**2')
            stringer.add_deqatn(deqatn)
            dvprel = DVPREL2('PBAR', pid=pid, pname='I1', eqid=deqatn.id)
            dvprel.add_dvar(dvar_t.id)
            dvprel.add_dtable(dtable_h)
            stringer.add_dvprel(dvprel)
            # calculating I2 = Iyy
            deqatn = DEQATN('I2(t,h) = h*t**3/12.')
            stringer.add_deqatn(deqatn)
            dvprel = DVPREL2('PBAR', pid=pid, pname='I2', eqid=deqatn.id)
            dvprel.add_dvar(dvar_t.id)
            dvprel.add_dtable(dtable_h)
            stringer.add_dvprel(dvprel)
            # calculating J
            deqatn = DEQATN('I1(t,h) = t*h**3/12. + t*h*(h/2.)**2;'
                            'I2 = h*t**3/12.;'
                            'J = I1 + I2')
            stringer.add_deqatn(deqatn)
            dvprel = DVPREL2('PBAR', pid=pid, pname='J', eqid=deqatn.id)
            dvprel.add_dvar(dvar_t.id)
            dvprel.add_dtable(dtable_h)
            stringer.add_dvprel(dvprel)
        else:
            raise NotImplementedError('%s not supported!' % ptype)

    elif stringer.profile.lower() == 'b_t_h':
        dvar_t = DESVAR('STRBt', stringer.t, stringer.t_lb, stringer.t_ub)
        dvar_h = DESVAR('STRBh', stringer.h, stringer.h_lb, stringer.h_ub)
        stringer.add_dvar(dvar_t)
        stringer.add_dvar(dvar_h)
        stringer.add_dtable('STRBL', stringer.L)
        if ptype == 'PBAR':
            # calculating A
            deqatn = DEQATN('A(t,h) = t*h')
            stringer.add_deqatn(deqatn)
            dvprel = DVPREL2('PBAR', pid=pid, pname='A', eqid=deqatn.id)
            dvprel.add_dvar(dvar_t.id)
            dvprel.add_dvar(dvar_h.id)
            stringer.add_dvprel(dvprel)
            # assuming y-axis towards radial (normal) direction
            # calculating I1 = Izz
            deqatn = DEQATN('I1(t,h) = t*h**3/12. + t*h*(h/2.)**2')
            stringer.add_deqatn(deqatn)
            dvprel = DVPREL2('PBAR', pid=pid, pname='I1', eqid=deqatn.id)
            dvprel.add_dvar(dvar_t.id)
            dvprel.add_dvar(dvar_h.id)
            stringer.add_dvprel(dvprel)
            # calculating I2 = Iyy
            deqatn = DEQATN('I2(t,h) = h*t**3/12.')
            stringer.add_deqatn(deqatn)
            dvprel = DVPREL2('PBAR', pid=pid, pname='I2', eqid=deqatn.id)
            dvprel.add_dvar(dvar_t.id)
            dvprel.add_dvar(dvar_h.id)
            stringer.add_dvprel(dvprel)
            # calculating J
            deqatn = DEQATN('I1(t,h) = t*h**3/12. + t*h*(h/2.)**2;'
                            'I2 = h*t**3/12.;'
                            'J = I1 + I2')
            stringer.add_deqatn(deqatn)
            dvprel = DVPREL2('PBAR', pid=pid, pname='J', eqid=deqatn.id)
            dvprel.add_dvar(dvar_t.id)
            dvprel.add_dvar(dvar_h.id)
            stringer.add_dvprel(dvprel)
        else:
            raise NotImplementedError('%s not supported!' % ptype)

    else:
        raise NotImplementedError('Stringer %s profile not supported!' %
                                  stringer.profile)

