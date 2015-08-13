import numpy as np

from ses import SE1D

from structMan.sol200 import (DRESP1, DCONSTR, DEQATN, DRESP2, DESVAR,
                              DVPREL1, DVPREL2)
import structMan.sol200.output_codes as output_codes_SOL200


class Flange1D(SE1D):
    """Flange1D base class for :class:`InnerFlange` and :class:`OuterFlange`

    """
    def __init__(self, name, eids, model):
        super(Flange1D, self).__init__(name, eids, model)
        #
        self.profile = 't'
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
            #xs = ccoords[:, 0]
            ys = ccoords[:, 1]
            zs = ccoords[:, 2]
            thetas = np.arctan2(zs, ys)
            rs = (ys**2 + zs**2)**0.5
            self.L = (thetas.max() - thetas.min())*rs.mean()

    def create_dvars(self):
        if self.dvars_created:
            return
        self.dvars_created = True
        pid = self.pid
        ptype = self.ptype

        self.add_dtable('FLAL', self.L)
        self.add_dtable('FLAE', self.E)
        self.add_dtable('FLAnu', self.nu)

        if self.profile.lower() == 't':
            dvar_t = DESVAR('FLAt', self.t, self.t_lb, self.t_ub)
            self.add_dvar(dvar_t)
            dtable_b = self.add_dtable('FLAb', self.b)
            if ptype == 'PBAR':
                # calculating A
                deqatn = DEQATN('A(t,b) = t*b')
                self.add_deqatn(deqatn)
                dvprel = DVPREL2('PBAR', pid=pid, pname='A', eqid=deqatn.id)
                dvprel.add_dvar(dvar_t.id)
                dvprel.add_dtable(dtable_b)
                self.add_dvprel(dvprel)
                # assuming y-axis towards radial (normal) direction
                # calculating I1 = Izz
                deqatn = DEQATN('I1(t,b) = b*t**3/12.')
                self.add_deqatn(deqatn)
                dvprel = DVPREL2('PBAR', pid=pid, pname='I1', eqid=deqatn.id)
                dvprel.add_dvar(dvar_t.id)
                dvprel.add_dtable(dtable_b)
                self.add_dvprel(dvprel)
                # calculating I2 = Iyy
                deqatn = DEQATN('I2(t,b) = t*b**3/12. + t*b*(b/2.)**2')
                self.add_deqatn(deqatn)
                dvprel = DVPREL2('PBAR', pid=pid, pname='I2', eqid=deqatn.id)
                dvprel.add_dvar(dvar_t.id)
                dvprel.add_dtable(dtable_b)
                self.add_dvprel(dvprel)
                # calculating J
                deqatn = DEQATN('I1(t,b) = b*t**3/12.;'
                                'I2 = t*b**3/12. + t*b*(b/2.)**2;'
                                'J = I1 + I2')
                self.add_deqatn(deqatn)
                dvprel = DVPREL2('PBAR', pid=pid, pname='J', eqid=deqatn.id)
                dvprel.add_dvar(dvar_t.id)
                dvprel.add_dtable(dtable_b)
                self.add_dvprel(dvprel)
            else:
                raise NotImplementedError('%s not supported!' % ptype)

        elif self.profile.lower() == 't_b':
            dvar_t = DESVAR('FLAt', self.t, self.t_lb, self.t_ub)
            dvar_b = DESVAR('FLAb', self.b, self.b_lb, self.b_ub)
            self.add_dvar(dvar_t)
            self.add_dvar(dvar_b)
            if ptype == 'PBAR':
                # calculating A
                deqatn = DEQATN('A(t,b) = t*b')
                self.add_deqatn(deqatn)
                dvprel = DVPREL2('PBAR', pid=pid, pname='A', eqid=deqatn.id)
                dvprel.add_dvar(dvar_t.id)
                dvprel.add_dvar(dvar_b.id)
                self.add_dvprel(dvprel)
                # assuming y-axis towards radial (normal) direction
                # calculating I1 = Izz
                deqatn = DEQATN('I1(t,b) = b*t**3/12.')
                self.add_deqatn(deqatn)
                dvprel = DVPREL2('PBAR', pid=pid, pname='I1', eqid=deqatn.id)
                dvprel.add_dvar(dvar_t.id)
                dvprel.add_dvar(dvar_b.id)
                self.add_dvprel(dvprel)
                # calculating I2 = Iyy
                deqatn = DEQATN('I2(t,b) = t*b**3/12. + t*b*(b/2.)**2')
                self.add_deqatn(deqatn)
                dvprel = DVPREL2('PBAR', pid=pid, pname='I2', eqid=deqatn.id)
                dvprel.add_dvar(dvar_t.id)
                dvprel.add_dvar(dvar_b.id)
                self.add_dvprel(dvprel)
                # calculating J
                deqatn = DEQATN('I1(t,b) = b*t**3/12.;'
                                'I2 = t*b**3/12. + t*b*(b/2.)**2;'
                                'J = I1 + I2')
                self.add_deqatn(deqatn)
                dvprel = DVPREL2('PBAR', pid=pid, pname='J', eqid=deqatn.id)
                dvprel.add_dvar(dvar_t.id)
                dvprel.add_dvar(dvar_b.id)
                self.add_dvprel(dvprel)
            else:
                raise NotImplementedError('%s not supported!' % ptype)


    def constrain_buckling(self, method=1, ms=0.1):
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
        self.create_dvars()
        eltype = self.elements[0].type

        # reading constants
        dtable_L = self.dtables['FLAL'][0]
        dtable_E = self.dtables['FLAE'][0]
        dtable_nu = self.dtables['FLAnu'][0]

        if method == 1 and self.profile.lower() == 't':
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
            self.add_deqatn(deqatn)
            # reading variables
            dvar_t = self.dvars['FLAt']
            # reading constants
            dtable_b = self.dtables['FLAb'][0]
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
            eid = self.get_central_element().eid
            dresp_PC = DRESP1('FLAPC', 'FORCE', 'ELEM', region=None,
                              atta=code_PC, attb='', atti=eid)
            dresp_PS = DRESP1('FLAPS', 'FORCE', 'ELEM', region=None,
                              atta=code_PS, attb='', atti=eid)
            self.add_dresp(dresp_PC)
            self.add_dresp(dresp_PS)
            # building DRESP2
            dresp2 = DRESP2('FLABUCK', deqatn.id)
            dresp2.dvars = [dvar_t.id]
            dresp2.dtable = [dtable_b, dtable_L, dtable_E, dtable_nu]
            dresp2.dresp1 = [dresp_PC.id, dresp_PS.id]
            self.add_dresp(dresp2)
            # applying constraint
            dcid = self.constraints['buckling']
            dconstr = self.add_constraint(dcid, dresp2, ms, None)

        elif method == 1 and self.profile.lower() == 't_b':
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
            self.add_deqatn(deqatn)
            # reading variables
            dvar_t = self.dvars['FLAt']
            dvar_b = self.dvars['FLAb']
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
            eid = self.get_central_element().eid
            dresp_PC = DRESP1('FLAPC', 'FORCE', 'ELEM', region=None,
                              atta=code_PC, attb='', atti=eid)
            dresp_PS = DRESP1('FLAPS', 'FORCE', 'ELEM', region=None,
                              atta=code_PS, attb='', atti=eid)
            self.add_dresp(dresp_PC)
            self.add_dresp(dresp_PS)
            # building DRESP2
            dresp2 = DRESP2('FLABUCK', deqatn.id)
            dresp2.dvars = [dvar_t.id, dvar_b.id]
            dresp2.dtable = [dtable_L, dtable_E, dtable_nu]
            dresp2.dresp1 = [dresp_PC.id, dresp_PS.id]
            self.add_dresp(dresp2)
            # applying constraint
            dcid = self.constraints['buckling']
            dconstr = self.add_constraint(dcid, dresp2, ms, None)

        else:
            raise NotImplementedError('Flange %s profile not supported!' %
                                      self.profile)


class InnerFlange(Flange1D):
    """Inner Flange

    It is assumed a rectangular section for the inner flange with two
    parameters `t` (thickness) and `b` (width).

    Attributes
    ----------

    profile (`str`)
        - `t` - defined with one variable:
            - `t` (variable): thickness
            - `b` (constant): width

        - `t_b` - defined with two variables:
            - `t` (variable): thickness
            - `b` (variable): width

        The InnerFlange's attributes will vary from one `profile` to another.

    """
    def __init__(self, name, eids, model=None):
        super(InnerFlange, self).__init__(name, eids, model)


class OuterFlange(Flange1D):
    """Outer Flange

    It is assumed a rectangular section for the outer flange with two
    parameters `t` (thickness) and `b` (width).

    Attributes
    ----------

    profile (`str`)
        - `t` - defined with one variable:
            - `t` (variable): thickness
            - `b` (constant): width

        - `t_b` - defined with two variables:
            - `t` (variable): thickness
            - `b` (variable): width

        The OuterFlange's attributes will vary from one `profile` to another.

    """
    def __init__(self, name, eids, model=None):
        super(OuterFlange, self).__init__(name, eids, model)


