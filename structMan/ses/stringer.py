"""
Stringer SEs (:mod:`structMan.ses.stringer`)
============================================

.. currentmodule:: structMan.ses.stringer

"""
import numpy as np

from ses import SE1D

from structMan.sol200 import (DRESP1, DCONSTR, DEQATN, DRESP2, DESVAR,
                              DVPREL1, DVPREL2)
import structMan.sol200.output_codes as output_codes_SOL200


class Stringer(SE1D):
    """Stringer

    Each cross-section (profile) dimension is defined according do the PBARL
    entry of Nastran's Quick Reference Guide.

    Attributes
    ----------

    profile (`str`)
        - `Z_t` - Z section defined with one variable:
            - `t` (variable): profile thickness
            - `b` (constant): flange width
            - `h` (constant): height

        - `Z_t_b` - Z section defined with two variables:
            - `t` (variable): profile thickness
            - `b` (variable): flange width
            - `h` (constant): height

        - `Z_t_b_h` - Z section defined with three variables:
            - `t` (variable): profile thickness
            - `b` (variable): flange width
            - `h` (variable): height

        - `Z_tf_tw_b_h` - Z section defined with four variables:
            - `tf` (variable): flange thickness
            - `tw` (variable): web thickness
            - `b` (variable): flange width
            - `h` (variable): height

        - `B_t` - Blade section defined with one variable:
            - `t` (variable): thickness
            - `h` (constant): height
            - `L` (constant): length

        - `B_t_h` - Blade section defined with two variables:
            - `t` (variable): thickness
            - `h` (variable): height
            - `L` (constant): length

        The stringer's attributes will vary from one `profile` to another.

    """
    def __init__(self, name, *eids):
        super(Stringer, self).__init__(name, *eids)
        self.profile = 'B_t'
        # optimization constraints
        self.all_constraints += ['buckling']
        self.constraints['buckling'] = 1

        if self.elements is not None:
            # reading L from FE data
            # - taking the distance between the two farthest nodes
            nodes = []
            for element in self.elements:
                for node in element.nodes:
                    nodes.append(node)
            self.nodes = set(nodes)
            ccoords = np.array([n.xyz for n in self.nodes])
            xs = ccoords[:, 0]
            ys = ccoords[:, 1]
            zs = ccoords[:, 2]
            #TODO use scipy.spatial.distance.pdist instead
            dist = np.subtract.outer(xs, xs)**2
            dist += np.subtract.outer(ys, ys)**2
            dist += np.subtract.outer(zs, zs)**2
            dist **= 0.5
            self.L = dist.max()


    def create_dvars(self):
        if self.dvars_created:
            return
        self.dvars_created = True
        pid = self.pid
        ptype = self.ptype

        self.add_dtable('STRE', self.E)
        self.add_dtable('STRnu', self.nu)

        if self.profile.lower() == 'z_t':
            dvar_t = DESVAR('STRZt', self.t, self.t_lb, self.t_ub)
            self.add_dvar(dvar_t)
            dtable_b = self.add_dtable('STRZb', self.b)
            dtable_h = self.add_dtable('STRZh', self.h)
            if ptype == 'PBAR':
                # calculating A
                deqatn = DEQATN('A(t,b,h) = 2*t*b + t*h')
                self.add_deqatn(deqatn)
                dvprel = DVPREL2('PBAR', pid=pid, pname='A', eqid=deqatn.id)
                dvprel.add_dvar(dvar_t.id)
                dvprel.add_dtable(dtable_b)
                dvprel.add_dtable(dtable_h)
                self.add_dvprel(dvprel)
                # assuming y-axis towards radial (normal) direction
                # calculating I1 = Izz
                deqatn = DEQATN('I1f(t,b,h) = t*b**3/12.;'
                                'I1w = h*t**3/12.;'
                                'd = t/2. + b/2.;'
                                'Ad2f = t*b*d**2;'
                                'I1 = 2*(I1f + Ad2f) + I1w')
                self.add_deqatn(deqatn)
                dvprel = DVPREL2('PBAR', pid=pid, pname='I1', eqid=deqatn.id)
                dvprel.add_dvar(dvar_t.id)
                dvprel.add_dtable(dtable_b)
                dvprel.add_dtable(dtable_h)
                self.add_dvprel(dvprel)
                # calculating I2 = Iyy
                deqatn = DEQATN('I2f(t,b,h) = b*t**3/12.;'
                                'I2w = t*h**3/12.;'
                                'd = h/2. - t/2.;'
                                'Ad2f = t*b*d**2;'
                                'I2 = 2*(I2f + Ad2f) + I2w')
                self.add_deqatn(deqatn)
                dvprel = DVPREL2('PBAR', pid=pid, pname='I2', eqid=deqatn.id)
                dvprel.add_dvar(dvar_t.id)
                dvprel.add_dtable(dtable_b)
                dvprel.add_dtable(dtable_h)
                self.add_dvprel(dvprel)
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
                self.add_deqatn(deqatn)
                dvprel = DVPREL2('PBAR', pid=pid, pname='J', eqid=deqatn.id)
                dvprel.add_dvar(dvar_t.id)
                dvprel.add_dtable(dtable_b)
                dvprel.add_dtable(dtable_h)
                self.add_dvprel(dvprel)
            else:
                raise NotImplementedError('%s not supported!' % ptype)

        elif self.profile.lower() == 'z_t_b':
            dvar_t = DESVAR('STRZt', self.t, self.t_lb, self.t_ub)
            dvar_b = DESVAR('STRZb', self.b, self.b_lb, self.b_ub)
            self.add_dvar(dvar_t)
            self.add_dvar(dvar_b)
            dtable_h = self.add_dtable('STRZh', self.h)
            if ptype == 'PBAR':
                # calculating A
                deqatn = DEQATN('A(t,b,h) = 2*t*b + t*h')
                self.add_deqatn(deqatn)
                dvprel = DVPREL2('PBAR', pid=pid, pname='A', eqid=deqatn.id)
                dvprel.add_dvar(dvar_t.id)
                dvprel.add_dvar(dvar_b.id)
                dvprel.add_dtable(dtable_h)
                self.add_dvprel(dvprel)
                # assuming y-axis towards radial (normal) direction
                # calculating I1 = Izz
                deqatn = DEQATN('I1f(t,b,h) = t*b**3/12.;'
                                'I1w = h*t**3/12.;'
                                'd = t/2. + b/2.;'
                                'Ad2f = t*b*d**2;'
                                'I1 = 2*(I1f + Ad2f) + I1w')
                self.add_deqatn(deqatn)
                dvprel = DVPREL2('PBAR', pid=pid, pname='I1', eqid=deqatn.id)
                dvprel.add_dvar(dvar_t.id)
                dvprel.add_dvar(dvar_b.id)
                dvprel.add_dtable(dtable_h)
                self.add_dvprel(dvprel)
                # calculating I2 = Iyy
                deqatn = DEQATN('I2f(t,b,h) = b*t**3/12.;'
                                'I2w = t*h**3/12.;'
                                'd = h/2. - t/2.;'
                                'Ad2f = t*b*d**2;'
                                'I2 = 2*(I2f + Ad2f) + I2w')
                self.add_deqatn(deqatn)
                dvprel = DVPREL2('PBAR', pid=pid, pname='I2', eqid=deqatn.id)
                dvprel.add_dvar(dvar_t.id)
                dvprel.add_dvar(dvar_b.id)
                dvprel.add_dtable(dtable_h)
                self.add_dvprel(dvprel)
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
                self.add_deqatn(deqatn)
                dvprel = DVPREL2('PBAR', pid=pid, pname='J', eqid=deqatn.id)
                dvprel.add_dvar(dvar_t.id)
                dvprel.add_dvar(dvar_b.id)
                dvprel.add_dtable(dtable_h)
                self.add_dvprel(dvprel)
            else:
                raise NotImplementedError('%s not supported!' % ptype)

        elif self.profile.lower() == 'z_t_b_h':
            dvar_t = DESVAR('STRZt', self.t, self.t_lb, self.t_ub)
            dvar_b = DESVAR('STRZb', self.b, self.b_lb, self.b_ub)
            dvar_h = DESVAR('STRZh', self.h, self.h_lb, self.h_ub)
            self.add_dvar(dvar_t)
            self.add_dvar(dvar_b)
            self.add_dvar(dvar_h)
            if ptype == 'PBAR':
                # calculating A
                deqatn = DEQATN('A(t,b,h) = 2*t*b + t*h')
                self.add_deqatn(deqatn)
                dvprel = DVPREL2('PBAR', pid=pid, pname='A', eqid=deqatn.id)
                dvprel.add_dvar(dvar_t.id)
                dvprel.add_dvar(dvar_b.id)
                dvprel.add_dvar(dvar_h.id)
                self.add_dvprel(dvprel)
                # assuming y-axis towards radial (normal) direction
                # calculating I1 = Izz
                deqatn = DEQATN('I1f(t,b,h) = t*b**3/12.;'
                                'I1w = h*t**3/12.;'
                                'd = t/2. + b/2.;'
                                'Ad2f = t*b*d**2;'
                                'I1 = 2*(I1f + Ad2f) + I1w')
                self.add_deqatn(deqatn)
                dvprel = DVPREL2('PBAR', pid=pid, pname='I1', eqid=deqatn.id)
                dvprel.add_dvar(dvar_t.id)
                dvprel.add_dvar(dvar_b.id)
                dvprel.add_dvar(dvar_h.id)
                self.add_dvprel(dvprel)
                # calculating I2 = Iyy
                deqatn = DEQATN('I2f(t,b,h) = b*t**3/12.;'
                                'I2w = t*h**3/12.;'
                                'd = h/2. - t/2.;'
                                'Ad2f = t*b*d**2;'
                                'I2 = 2*(I2f + Ad2f) + I2w')
                self.add_deqatn(deqatn)
                dvprel = DVPREL2('PBAR', pid=pid, pname='I2', eqid=deqatn.id)
                dvprel.add_dvar(dvar_t.id)
                dvprel.add_dvar(dvar_b.id)
                dvprel.add_dvar(dvar_h.id)
                self.add_dvprel(dvprel)
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
                self.add_deqatn(deqatn)
                dvprel = DVPREL2('PBAR', pid=pid, pname='J', eqid=deqatn.id)
                dvprel.add_dvar(dvar_t.id)
                dvprel.add_dvar(dvar_b.id)
                dvprel.add_dvar(dvar_h.id)
                self.add_dvprel(dvprel)
            else:
                raise NotImplementedError('%s not supported!' % ptype)

        elif self.profile.lower() == 'z_tf_tw_b_h':
            dvar_tf = DESVAR('STRZtf', self.tf, self.tf_lb, self.tf_ub)
            dvar_tw = DESVAR('STRZtw', self.tw, self.tw_lb, self.tw_ub)
            dvar_b = DESVAR('STRZb', self.b, self.b_lb, self.b_ub)
            dvar_h = DESVAR('STRZh', self.h, self.h_lb, self.h_ub)
            self.add_dvar(dvar_tf)
            self.add_dvar(dvar_tw)
            self.add_dvar(dvar_b)
            self.add_dvar(dvar_h)
            if ptype == 'PBAR':
                # calculating A
                deqatn = DEQATN('A(tf,tw,b,h) = 2*tf*b + tw*h')
                self.add_deqatn(deqatn)
                dvprel = DVPREL2('PBAR', pid=pid, pname='A', eqid=deqatn.id)
                dvprel.add_dvar(dvar_tf.id)
                dvprel.add_dvar(dvar_tw.id)
                dvprel.add_dvar(dvar_b.id)
                dvprel.add_dvar(dvar_h.id)
                self.add_dvprel(dvprel)
                # assuming y-axis towards radial (normal) direction
                # calculating I1 = Izz
                deqatn = DEQATN('I1f(tf,tw,b,h) = tf*b**3/12.;'
                                'I1w = h*tw**3/12.;'
                                'd = tw/2. + b/2.;'
                                'Ad2f = tf*b*d**2;'
                                'I1 = 2*(I1f + Ad2f) + I1w')
                self.add_deqatn(deqatn)
                dvprel = DVPREL2('PBAR', pid=pid, pname='I1', eqid=deqatn.id)
                dvprel.add_dvar(dvar_tf.id)
                dvprel.add_dvar(dvar_tw.id)
                dvprel.add_dvar(dvar_b.id)
                dvprel.add_dvar(dvar_h.id)
                self.add_dvprel(dvprel)
                # calculating I2 = Iyy
                deqatn = DEQATN('I2f(tf,tw,b,h) = b*tf**3/12.;'
                                'I2w = tw*h**3/12.;'
                                'd = h/2. - tf/2.;'
                                'Ad2f = tf*b*d**2;'
                                'I2 = 2*(I2f + Ad2f) + I2w')
                self.add_deqatn(deqatn)
                dvprel = DVPREL2('PBAR', pid=pid, pname='I2', eqid=deqatn.id)
                dvprel.add_dvar(dvar_tf.id)
                dvprel.add_dvar(dvar_tw.id)
                dvprel.add_dvar(dvar_b.id)
                dvprel.add_dvar(dvar_h.id)
                self.add_dvprel(dvprel)
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
                self.add_deqatn(deqatn)
                dvprel = DVPREL2('PBAR', pid=pid, pname='J', eqid=deqatn.id)
                dvprel.add_dvar(dvar_tf.id)
                dvprel.add_dvar(dvar_tw.id)
                dvprel.add_dvar(dvar_b.id)
                dvprel.add_dvar(dvar_h.id)
                self.add_dvprel(dvprel)
            else:
                raise NotImplementedError('%s not supported!' % ptype)

        elif self.profile.lower() == 'b_t':
            dvar_t = DESVAR('STRBt', self.t, self.t_lb, self.t_ub)
            self.add_dvar(dvar_t)
            dtable_h = self.add_dtable('STRBh', self.h)
            self.add_dtable('STRBL', self.L)
            if ptype == 'PBAR':
                # calculating A
                deqatn = DEQATN('A(t,h) = t*h')
                self.add_deqatn(deqatn)
                dvprel = DVPREL2('PBAR', pid=pid, pname='A', eqid=deqatn.id)
                dvprel.add_dvar(dvar_t.id)
                dvprel.add_dtable(dtable_h)
                self.add_dvprel(dvprel)
                # assuming y-axis towards radial (normal) direction
                # calculating I1 = Izz
                deqatn = DEQATN('I1(t,h) = t*h**3/12. + t*h*(h/2.)**2')
                self.add_deqatn(deqatn)
                dvprel = DVPREL2('PBAR', pid=pid, pname='I1', eqid=deqatn.id)
                dvprel.add_dvar(dvar_t.id)
                dvprel.add_dtable(dtable_h)
                self.add_dvprel(dvprel)
                # calculating I2 = Iyy
                deqatn = DEQATN('I2(t,h) = h*t**3/12.')
                self.add_deqatn(deqatn)
                dvprel = DVPREL2('PBAR', pid=pid, pname='I2', eqid=deqatn.id)
                dvprel.add_dvar(dvar_t.id)
                dvprel.add_dtable(dtable_h)
                self.add_dvprel(dvprel)
                # calculating J
                deqatn = DEQATN('I1(t,h) = t*h**3/12. + t*h*(h/2.)**2;'
                                'I2 = h*t**3/12.;'
                                'J = I1 + I2')
                self.add_deqatn(deqatn)
                dvprel = DVPREL2('PBAR', pid=pid, pname='J', eqid=deqatn.id)
                dvprel.add_dvar(dvar_t.id)
                dvprel.add_dtable(dtable_h)
                self.add_dvprel(dvprel)
            else:
                raise NotImplementedError('%s not supported!' % ptype)

        elif self.profile.lower() == 'b_t_h':
            dvar_t = DESVAR('STRBt', self.t, self.t_lb, self.t_ub)
            dvar_h = DESVAR('STRBh', self.h, self.h_lb, self.h_ub)
            self.add_dvar(dvar_t)
            self.add_dvar(dvar_h)
            self.add_dtable('STRBL', self.L)
            if ptype == 'PBAR':
                # calculating A
                deqatn = DEQATN('A(t,h) = t*h')
                self.add_deqatn(deqatn)
                dvprel = DVPREL2('PBAR', pid=pid, pname='A', eqid=deqatn.id)
                dvprel.add_dvar(dvar_t.id)
                dvprel.add_dvar(dvar_h.id)
                self.add_dvprel(dvprel)
                # assuming y-axis towards radial (normal) direction
                # calculating I1 = Izz
                deqatn = DEQATN('I1(t,h) = t*h**3/12. + t*h*(h/2.)**2')
                self.add_deqatn(deqatn)
                dvprel = DVPREL2('PBAR', pid=pid, pname='I1', eqid=deqatn.id)
                dvprel.add_dvar(dvar_t.id)
                dvprel.add_dvar(dvar_h.id)
                self.add_dvprel(dvprel)
                # calculating I2 = Iyy
                deqatn = DEQATN('I2(t,h) = h*t**3/12.')
                self.add_deqatn(deqatn)
                dvprel = DVPREL2('PBAR', pid=pid, pname='I2', eqid=deqatn.id)
                dvprel.add_dvar(dvar_t.id)
                dvprel.add_dvar(dvar_h.id)
                self.add_dvprel(dvprel)
                # calculating J
                deqatn = DEQATN('I1(t,h) = t*h**3/12. + t*h*(h/2.)**2;'
                                'I2 = h*t**3/12.;'
                                'J = I1 + I2')
                self.add_deqatn(deqatn)
                dvprel = DVPREL2('PBAR', pid=pid, pname='J', eqid=deqatn.id)
                dvprel.add_dvar(dvar_t.id)
                dvprel.add_dvar(dvar_h.id)
                self.add_dvprel(dvprel)
            else:
                raise NotImplementedError('%s not supported!' % ptype)

        else:
            raise NotImplementedError('Stringer %s profile not supported!' %
                                      self.profile)


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

        Notes
        -----

        Method 1) uses Bruhn's method described in Chapter 6, Fig. C6.4

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

