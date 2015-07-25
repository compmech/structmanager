"""
Optimization cards (:mod:`feopt.genesis.cards_opt`)
=============================================

.. currentmodule:: feopt.genesis.cards_opt`

Many input cards related to the optimization problem are wrapped in this
module. The input cards more related to the solver are contained in module
:mod:`feopt.genesis.cards_solver`.

.. rubric:: Classes

.. autosummary::

    feopt.genesis.cards_opt.DCONS
    feopt.genesis.cards_opt.DEQATN
    feopt.genesis.cards_opt.DLINK
    feopt.genesis.cards_opt.DOBJ
    feopt.genesis.cards_opt.DRESP1
    feopt.genesis.cards_opt.DRESP2
    feopt.genesis.cards_opt.DRESP3
    feopt.genesis.cards_opt.DSPLIT
    feopt.genesis.cards_opt.DTABLE
    feopt.genesis.cards_opt.DVAR
    feopt.genesis.cards_opt.DVPROP3

"""
from pprint import pformat
from collections import Iterable

from sizing_data import SDATA


class DSPLIT(object):
    """Defines a region for topometry optimization.

    Parameters
    ----------
    label : str
        User defined name for output purposes.
    ptype : str
        Designable region type ('PROD', 'PBAR', 'PSHELL' etc).
    pid : int
        Property identification number.
    cvalue : int
        Desired maximum number of elements per group.
    cid : int
        Coordinate system identification number.
    manufact_cons_input : list
        A list of strings defining the type1, type2 and type3 of fabrication
        constraints.


    """
    uniqueid = 8000000

    def __init__(self, label, ptype, pid, cvalue, cid, manufact_cons_input):
        self.id = DSPLIT.uniqueid
        DSPLIT.uniqueid += 1
        self.label = label
        self.ptype = ptype
        self.pid = pid
        self.cvalue = cvalue
        self.cid = cid
        self.manufact_cons_input = manufact_cons_input
        self.defaults()

    def defaults(self):
        self.n = ''
        self.symtol = 0.001
        self.symmet = 2
        self.angtype = 'ANGSYM'
        self.type1 = ''
        self.type2 = ''
        self.type3 = ''
        self.coarse = 'COARSE'
        self.ctype = 'MAXELEM'
        if self.manufact_cons_input[0] is not 'None':
            self.type1 = self.manufact_cons[self.manufact_cons_input[0]]
        if self.manufact_cons_input[1] is not 'None':
            self.type2 = self.manufact_cons[self.manufact_cons_input[1]]
        if self.manufact_cons_input[2] is not 'None':
            self.type3 = self.manufact_cons[self.manufact_cons_input[2]]

    def manufact_cons(self):
        """Create manufacture constraints following GENESIS Design Reference

        """
        manufact_cons={}
        manufact_cons['Mirror symmetry with respect to the XY plane']='MXY'
        manufact_cons['Mirror symmetry with respect to the YZ plane']='MYZ'
        manufact_cons['Mirror symmetry with respect to the ZX plane']='MZX'
        manufact_cons['Cyclic symmetry about the X axis']='CX'
        manufact_cons['Cyclic symmetry about the Y axis']='CY'
        manufact_cons['Cyclic symmetry about the Z axis']='CZ'
        manufact_cons['Extrusion along the X axis']='EX'
        manufact_cons['Extrusion along the Y axis']='EY'
        manufact_cons['Extrusion along the Z axis']='EZ'
        self.manufact_cons = manufact_cons

    def print_card(self, file):
        """Print the corresponding input card

        Parameters
        ----------
        file : file
            File object with a :meth:`write` method.

        """
        dconsstr = ('%s,%d,%s,%s,%d' % ('DSPLIT', self.id, self.label,
                    self.ptype, self.pid))
        file.write(dconsstr + '\n')
        if self.cvalue > 1:
            file.write('+,COARSE,%s,%d\n' % (self.ctype, self.cvalue))
        if (self.type1 <> '' or self.type2 <> '' or self.type3 <> ''):
            file.write('+,SYM,%d,%s,%s,%s,%s,%f,%d,%s\n' %
                       (self.cid, self.type1, self.type2, self.type3,
                        self.n, self.symtol, self.symmet, self.angtype))


class DRESP1(object):
    """Design response DRESP1

    Parameters
    ----------
    label : str
        User defined label.
    rtype : str
        Response type ('DISP', 'STRESS', 'FREQ' etc).
    ptype : str
        If ``ptype='ELEM'`` the ATTi are element IDs, if ``ptype='PSHELL'`` etc
        the ATTi are property IDs (see design manual for more info).
    region : int
        Region identifier for constraint screening.
    atta : int
        Displacement component number, item number or eigenvector component.
    atti : list
        Grid, spoint, field point, property, element or material ids.


    """
    uniqueid = 8000000

    def __init__(self, label, rtype, ptype, region, atta, atti):
        self.id = DRESP1.uniqueid
        DRESP1.uniqueid += 1
        self.label = label
        self.rtype = rtype
        self.ptype = ptype
        self.region = region
        self.atta = atta
        self.atti = atti

    def print_card(self, file):
        """Print the corresponding input card

        """
        dresp1str = ('%s,%d,%s,%s,%s,%s,%s' %
                     ('DRESP1', self.id, self.label, self.rtype,
                      self.ptype, self.region, self.atta))
        if isinstance(self.atti, int):
            dresp1str = dresp1str + (',' + str(self.atti))
        elif isinstance(self.atti, list):
            atticount = 7
            for i in range(len(self.atti)):
                atticount += 1
                if atticount == 11:
                    file.write(dresp1str + '\n')
                    dresp1str = '+'
                    atticount = 2
                dresp1str +=  ',' + str(self.atti[i])
        file.write(dresp1str + '\n')


class DRESP23(object):
    def __init__(self):
        self.dvars = []
        self.dtable = []
        self.dresp1 = []

    def add_dvar(self, dvar_id):
        self.dvars.append(dvar_id)

    def add_dtable(self, cons_label):
        self.dtable.append(cons_label)

    def add_dresp1(self, dresp1_id):
        self.dresp1.append(dresp1_id)

    def print_aux (self, label, listaux, file):
        auxstr = '+,' + label
        count = 2
        for aux_id in listaux:
            count += 1
            if count == 11:
                file.write(auxstr + '\n')
                count = 3
                auxstr = '+,' + ' '*len(label)
            auxstr += ',' + str(aux_id)
        file.write(auxstr + '\n')


class DRESP2(DRESP23):
    """Design response DRESP2

    Define equation responses that are used in the design, either as an
    objective function or as constraints.

    Parameters
    ----------
    label : str
        User defined label.
    eqid : int
        :class:`.DEQATN` entry identification number.
    region : int or None, optional
        Region used for constraint screening.

    Notes
    -----
    To add variables, table entries or other :class:`.DRESP1` responses use the
    methods: :meth:`.add_dvar`, :meth:`.add_dtable` and :meth:`.add_dresp1`.

    """
    uniqueid = 8000000

    def __init__(self, label, eqid, region=None):
        if region is None:
            region = ''
        super(DRESP2, self).__init__()
        self.id = DRESP2.uniqueid
        DRESP2.uniqueid += 1
        self.label = label
        self.eqid = eqid
        self.region = region

    def print_card(self, file):
        """Print the corresponding input card

        Parameters
        ----------
        file : file
            File object with a :meth:`write` method.

        """
        drespstr = ('DRESP2,%d,%s,%d,%s\n' %
                     (self.id, self.label, self.eqid, self.region))

        file.write(drespstr)

        if len(self.dvars) > 0:
            self.print_aux('DVAR'  , self.dvars , file)

        if len(self.dtable) > 0:
            self.print_aux('DTABLE', self.dtable, file)

        if len(self.dresp1) > 0:
            self.print_aux('DRESP1', self.dresp1, file)


class DRESP3(DRESP23):
    """Design response DRESP3

    Define use-subroutine or built-in responses that can be used in the design
    either as constraint or as an objective.

    Parameters
    ----------
    label : str
        User defined label.
    libid : int
        Library identification number or a built-in function name (see design
        manual).
    region : int or None, optional
        Region used for constraint screening.

    Notes
    -----
    To add variables, table entries or other :class:`.DRESP1` responses use the
    methods: :meth:`.add_dvar`, :meth:`.add_dtable` and :meth:`.add_dresp1`.

    """
    uniqueid = 8000000

    def __init__(self, label, libid, region=None):
        if region is None:
            region = ''
        super(DRESP3, self).__init__()
        self.id = DRESP3.uniqueid
        DRESP3.uniqueid += 1
        self.label = label
        self.libid = libid
        self.region = region

    def print_card(self, file):
        """Print the corresponding input card

        Parameters
        ----------
        file : file
            File object with a :meth:`write` method.

        """
        drespstr = ('DRESP3,%d,%s,%s,%s\n' %
                     (self.id, self.label, str(self.libid), self.region))

        file.write(drespstr)

        if len(self.dvars) > 0:
            self.print_aux('DVAR'  , self.dvars , file)

        if len(self.dtable) > 0:
            self.print_aux('DTABLE', self.dtable, file)

        if len(self.dresp1) > 0:
            self.print_aux('DRESP1', self.dresp1, file)


class DVAR(object):
    """Design Variable

    """
    uniqueid = 8000000

    def __init__(self, label, init, lb, ub, dvsid, dvprop, code=None):
        self.id = DVAR.uniqueid
        DVAR.uniqueid += 1
        self.defaults()
        self.label = label
        self.init = init
        self.lb = lb
        self.ub = ub
        self.dvsid = dvsid
        self.dvprop = dvprop
        self.code = code

    def defaults(self):
        self.delx = ''
        self.dxmin = ''

    def print_card(self, file):
        """Print the corresponding input card

        Parameters
        ----------
        file : file
            File object with a :meth:`write` method.

        """
        if self.init == self.lb == self.ub:
            pass
        else:
            file.write('$dvar.id dvar.code %8d %-8s \n' % (self.id, self.code))
            file.write('$HMNAME DVAR %8d %-8s \n' % (self.id, self.label))
            file.write('%-s,%d,%s,%f,%f,%f,%s,%s \n' %
                      ('DVAR', self.id, self.label, self.init, self.lb,
                        self.ub, str(self.delx), str(self.dxmin)))
            if self.dvsid <> 'blank':
                file.write('+,' + str(self.dvsid) + '\n')

    def show_card(self):
        print('%-s,%d,%s,%f,%f,%f,%s,%s \n' %
                   ('DVAR', self.id, self.label, self.init, self.lb,
                    self.ub, str(self.delx), str(self.dxmin)))
        if self.dvsid <> 'blank':
            print('+,' + str(self.dvsid) + '\n')


class DVPROP3(object):
    """Design Property DVPROP3

    This is a wrapper for the DVPROP3 card in Genesis.

    Parameters
    ----------
    sizing_data : TODO
        The sizing data for this entry.
    id :

    """
    uniqueid = 8000000

    def __init__(self, sizing_data, pid, ptype, eltype, dvar_labels=None,
                 dvar_codes=None):
        self.id = DVPROP3.uniqueid
        DVPROP3.uniqueid += 1
        self.sizing_data = sizing_data
        self.pid = pid
        self.ptype = ptype
        self.eltype = eltype
        self.dvars = []
        self.dvars_by_code = {}
        self.defaults()

        # The label is used to organize the variables for each component
        if dvar_labels is not None:
            if isinstance(dvar_labels, str):
                self.dvar_labels = [dvar_labels for _ in self.sizing_data]
            elif isinstance(dvar_labels, Iterable):
                if len(dvar_labels) != len(sizing_data):
                    raise ValueError('Required one label for each variable!')
                self.dvar_labels = dvar_labels
            else:
                raise ValueError('"dvar_labels" must be str or an iterable')

        # The code must be unique for each variable
        if dvar_codes is not None:
            if not isinstance(dvar_codes, Iterable):
                raise ValueError('"dvar_codes" must be an Iterable')
            if len(set(dvar_codes)) != len(sizing_data):
                raise ValueError('Required one code for each variable!')
        self.dvar_codes = dvar_codes


    def defaults(self):
        self.ishear = 1
        self.pmin = 1.0e-10
        self.delp = 0.5
        self.dpmin = 0.1


    def create_dvars(self):
        """Create the design variables for the current DVPROP3

        """
        desvars = [i[0] for i in SDATA[self.ptype][self.eltype]]
        #print("create_dvars:")
        #print("    " + pformat(desvars))
        #print("    len(desvars): %s" % len(desvars))
        #print("    self.ptype, self.eltype: %s %s" % (self.ptype, self.eltype))

        for i in range(len(desvars)):
            desvar = desvars[i]
            if self.dvar_labels is None:
                dvar_label = desvar + str(self.id)
            else:
                dvar_label = self.dvar_labels[i]

            dvar_code = None
            if self.dvar_codes is not None:
                dvar_code = self.dvar_codes[i]

            init = self.sizing_data[i][0]
            lb = self.sizing_data[i][1]
            ub = self.sizing_data[i][2]

            if init > ub:
                init = ub
            elif init < lb:
                init = lb

            dvsid = 'blank'
            dvar = DVAR(dvar_label, init, lb, ub, dvsid, self, dvar_code)
            self.dvars.append(dvar)

            if dvar_code is not None:
                self.dvars_by_code[dvar_code] = dvar


    def print_card(self, file):
        """Print the corresponding input card

        Parameters
        ----------
        file : file
            File object with a :meth:`write` method.

        """
        #finding all variables related to this dvprop3 entry
        csd = []
        for dvar in self.dvars:
            if (dvar.init == dvar.lb == dvar.ub):
                csd.append(str(dvar.init))
            else:
                csd.append(str(dvar.id))

        file.write('%s,%d,%d,%s,%d,%f,%f,%f\n' %
                  ('DVPROP3', self.id, self.pid, self.eltype,
                   self.ishear, self.pmin, self.delp, self.dpmin))

        cdsstr = ('%s,%s' % ('+', csd[0]))
        cdsstrcount = 1

        for i in range(len(csd)-1):
            cdsstrcount += 1
            if cdsstrcount > 9:
                cdsstrcount = 1
                file.write(cdsstr + '\n')
                cdsstr = ('%s,%s' % ('+', csd[i+1]))
            else:
                cdsstr = cdsstr + (',%s' % (csd[i+1]))
        file.write(cdsstr + '\n')


class DOBJ(object):
    """Design objective

    """
    def __init__(self, drespid):
        self.rid = drespid
        self.defaults()

    def defaults(self):
        self.label = 'min_MASS'
        self.lid = ''
        self.minmax = 'MIN'

    def print_card(self, file):
        """Print the corresponding input card

        Parameters
        ----------
        file : file
            File object with a :meth:`write` method.

        """
        dobjstr = ('%s,%d,%s,%s,%s' % ('DOBJ', self.rid, self.label,
                   str(self.lid), self.minmax))
        file.write(dobjstr + '\n')


class DCONS(object):
    """Design constraint

    Attributes
    ----------
    drespid : int
        The corresponding design response id.
    lid_lb_ub : list
        A list in the format ``[str, float, float]`` where the fields are
        the load id or 'ALL', the negative allowable and the positive
        allowable.
    stress_type : str
        If the corresponding response is 'negative', 'positive' or 'both'. It
        helps defining the constraints.

    """
    def __init__(self, drespid, lid_lb_ub, stress_type):
        self.rid = drespid
        self.lid_lb_ub = lid_lb_ub
        self.stress_type = stress_type

    def print_card(self, file):
        """Print the corresponding input card

        Parameters
        ----------
        file : file
            File object with a :meth:`write` method.

        """
        dconsstr = ('%s,%d' % ('DCONS', self.rid))
        lidcount = 0
        for i in range(0, len(self.lid_lb_ub), 3):
            lidcount += 1
            if lidcount == 3:
                file.write(dconsstr + '\n')
                dconsstr = ('%s,' % ('+'))
                lidcount = 1
            lb = ''
            ub = ''
            if self.stress_type == 'negative':
                lb = str(float(self.lid_lb_ub[i+1]))
            if self.stress_type == 'positive':
                ub = str(float(self.lid_lb_ub[i+2]))
            if self.stress_type == 'both':
                lb = str(float(self.lid_lb_ub[i+1]))
                ub = str(float(self.lid_lb_ub[i+2]))
            dconsstr = dconsstr + (',%s,%s,%s' %
                                   (str(self.lid_lb_ub[i]), lb, ub))
        file.write(dconsstr + '\n')


class DLINK(object):
    r"""Link between design variables

    DLINK creates links among variables using the form:

    .. math::
        dvar_{dependent} = c_0 + c_{mult} \times (c_1 \times {dvar}_1
                                                + c_2 \times {dvar}_2)

    where:

    - `dvar_{dependent}` is the dependent variable
    - `{dvar}_i` the `i^{th}` design variable
    - `c_0` is a constant
    - `c_{mult}` is a common multiplier
    - `c_i` is an individual multiplier for `{dvar}_i`

    Be sure that no dependent variables are being used as independent
    variables.

    By default ``c0 = 0`` and ``cmult = 1``.

    The values of ``dvi`` and ``ci`` are inputed as follows::

        indep_dv_c = [dv1, c1, dv2, c2, ...]
        indep_dv_c = [1000000, 1., 1000001, 1., ...]

    """
    def __init__(self, dep_var, dvi_ci, c0 = 0., cmult = 1.):
        self.dvid = dep_var
        self.c0 = c0
        self.cmult = cmult
        self.dvi_ci = dvi_ci

    def print_card(self, file):
        """Print the corresponding input card

        Parameters
        ----------
        file : file
            File object with a :meth:`write` method.

        """
        ##if dvars[self.dvid].init == dvars[self.dvid].lb == dvars[self.dvid].ub:
        ##    dlinkstr = ('%s,%f,%f,%f' % ('DLINK', dvars[self.dvid].init, self.c0, self.cmult))
        ##else:
        ##    dlinkstr = ('%s,%d,%f,%f' % ('DLINK', self.dvid, self.c0, self.cmult))
        dlinkstr = ('%s,%d,%f,%f' % ('DLINK', self.dvid, self.c0, self.cmult))
        dvicicount=-3
        for i in range(0, len(self.dvi_ci), 2):
            dvicicount += 1
            if dvicicount == 1 or dvicicount == 5:
                file.write(dlinkstr + '\n')
                dlinkstr = ('%s' % ('+'))
                if dvicicount == 5:
                    dvicicount = 1
            try:
                dlinkstr += (',%d,%f' % (self.dvi_ci[i], self.dvi_ci[i+1]))
            except:
                dlinkstr += (',%d,%s' % (self.dvi_ci[i], self.dvi_ci[i+1]))

        file.write(dlinkstr + '\n')


class DEQATN(object):
    """Equation to calculate customized responses

    Parameters
    ----------
    eq : str
        A string containing the equation. For example, the following equation:

        .. math::
            T(x_1, x_2, x_3) = \sqrt{x_1^2 + x_2^2 + x_3^2}

        can be written as::

            eq = 'T(x1,x2,x3)=SQRT(x1**2+x2**2+x3**2)'

    Notes
    -----
    .. note:: The :meth:`.DEQATN.print_card` method will split the
              equation, when necessary, in order to keep the limit length up to
              62 characters in the first line, and 70 characters for the
              subsequent lines.

    """
    uniqueid = 8000000

    def __init__(self, eq):
        self.id = DEQATN.uniqueid
        DEQATN.uniqueid += 1
        self.eq = str(eq)

    def print_card(self, file):
        """Print the corresponding input card

        Parameters
        ----------
        file : file
            File object with a :meth:`write` method.

        """
        eq = self.eq
        deqatn_str = '{0:8s}{1:8d}'.format('DEQATN', self.id)
        deqatn_str += eq[:62]
        deqatn_str += '\n'
        file.write(deqatn_str)

        eq = eq[62:]

        while len(eq) > 0:
            deqatn_str = '+       ' + eq[:70] + '\n'
            file.write(deqatn_str)
            eq = eq[70:]


class DTABLE(object):
    """Design Table used to define many constants

    Hints:

    - There can be any number of DTABLE entries in the bulk data.
    - The user must avoid repeated labels for constants
    - The constant label must be <= 8 characters.

    All values for the constants must be of the 'Real' type.  Ex::

        input_dict={'c1':1. , 'c2':2., 'max8char':999.}

    """
    uniqueid = 8000000

    def __init__(self, input_dict={}):
        self.id = DTABLE.uniqueid
        DTABLE.uniqueid += 1
        self.input_dict = input_dict

    def print_card(self, file):
        """Print the corresponding input card

        Parameters
        ----------
        file : file
            File object with a :meth:`write` method.

        """
        if len(self.input_dict) > 0:
            keys = sorted(self.input_dict.keys())
            dtable_str = 'DTABLE'
            count = 0
            for k in keys:
                v = self.input_dict[k]
                count += 2
                if count == 10:
                    file.write(dtable_str + '\n')
                    dtable_str = '+'
                    count = 0
                dtable_str += ',%s,%s' % (str(k), str(v))
            file.write(dtable_str + '\n')


if __name__ == '__main__':
    with open('tmp.bdf', 'w') as f:
        test = DEQATN('a+a+b+ca+a+b+ca+a+b+ca+a+b+ca+a+b+ca+a+b+c++++++a+a+b+c+a+d+d+d+f+dsf+sd+f+sdf+sd+f+sdf+sd+f+sdf+sd+fsd')
        test.print_card(f)
