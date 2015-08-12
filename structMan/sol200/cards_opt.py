"""
Optimization cards (:mod:`structMan.sol200.cards_opt`)
======================================================

.. currentmodule:: structMan.sol200.cards_opt`

Many input cards related to the optimization problem are wrapped in this
module. The input cards more related to the solver are contained in module
:mod:`structMan.sol200.cards_solver`.

.. rubric:: Classes

.. autosummary::

    structMan.sol200.cards_opt.DCONSTR
    structMan.sol200.cards_opt.DEQATN
    structMan.sol200.cards_opt.DESVAR
    structMan.sol200.cards_opt.DLINK
    structMan.sol200.cards_opt.DRESP1
    structMan.sol200.cards_opt.DRESP2
    structMan.sol200.cards_opt.DRESP3
    structMan.sol200.cards_opt.DTABLE
    structMan.sol200.cards_opt.DVPREL1

"""
from sizing_data import SDATA
from utils import format_float as ff


class DVPREL(object):
    uniqueid = 9000000


class DRESP(object):
    uniqueid = 9000000


class DRESP1(DRESP):
    """Design response DRESP1

    Parameters
    ----------
    label : str
        User-defined label.
    rtype : str
        Response type.
    ptype : str
        Element flag ('ELEM') or property entry name ('PBAR', PSHELL' etc).
    region : int or None, optional
        Region identifier for constraint screening.
    atta, attb: int or float or None
        Response attributes.
    atti : int or float or None or list, optional
        Response attributes.

    """
    def __init__(self, label, rtype, ptype, region=None, atta=None, attb=None,
            atti=None):
        if region is None:
            region = ''
        if atta is None:
            atta = ''
        if attb is None:
            attb = ''
        if atti is None:
            atti = ''
        self.id = DRESP.uniqueid
        DRESP.uniqueid += 1
        self.label = label
        self.rtype = rtype
        self.ptype = ptype
        self.region = region
        self.atta = atta
        self.attb = attb
        self.atti = atti

    def print_card(self, file):
        """Print the corresponding input card

        """
        dresp1str = ('%s% 8d% 8s% 8s% 8s% 8s% 8s% 8s' %
                     ('DRESP1'.ljust(8), self.id, self.label, self.rtype,
                      self.ptype, self.region, self.atta, self.attb))
        if isinstance(self.atti, (int, str)):
            dresp1str = dresp1str + str(self.atti).rjust(8)
        elif isinstance(self.atti, list):
            atticount = 8
            for i in range(0, len(self.atti)):
                atticount += 1
                if atticount == 10:
                    file.write(dresp1str + '\n')
                    dresp1str = '+'.ljust(8)
                    atticount = 2
                dresp1str += str(self.atti[i]).rjust(8)
        file.write(dresp1str + '\n')


class PRINTAUX(object):
    """Base class for :class:`DRESP23` and :class:`BASEDV2`

    """
    def __init__(self):
        pass

    def print_aux(self, label, listaux, file):
        auxstr = '+'.ljust(8) + label.ljust(8)
        count = 2
        for aux_id in listaux:
            count += 1
            if count == 10:
                file.write(auxstr + '\n')
                count = 3
                auxstr = '+'.ljust(8)
            auxstr += str(aux_id).rjust(8)
        file.write(auxstr + '\n')


class DRESP23(PRINTAUX):
    """Base class for DVPREL2, DVCREL2, DVMREL2, DRESP2, DRESP3 etc

    """
    def __init__(self):
        super(DRESP23, self).__init__()
        self.dvars = []
        self.dtable = []
        self.dresp1 = []

    def add_dvar(self, dvar_id):
        self.dvars.append(dvar_id)

    def add_dtable(self, cons_label):
        self.dtable.append(cons_label)

    def add_dresp1(self, dresp1_id):
        self.dresp1.append(dresp1_id)


class DRESP2(DRESP23):
    """Design response DRESP2

    Define equation responses that are used in the design, either as an
    objective function or as constraints.

    Parameters
    ----------
    label : str
        User-defined label.
    eqid : int or str
        :class:`.DEQATN` entry identification number, or string informing a
        pre-programmed function.
    region : int or None, optional
        Region used for constraint screening.

    Notes
    -----
    To add variables, table entries or other :class:`.DRESP1` responses use the
    methods: :meth:`.add_dvar`, :meth:`.add_dtable` and :meth:`.add_dresp1`.

    """
    def __init__(self, label, eqid, region=None):
        super(DRESP2, self).__init__()
        if region is None:
            region = ''
        self.id = DRESP.uniqueid
        DRESP.uniqueid += 1
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
        drespstr = ('%s% 8d% 8s% 8s% 8s\n' % ('DRESP2'.ljust(8), self.id,
                    self.label, str(self.eqid), self.region))

        file.write(drespstr)

        if len(self.dvars) > 0:
            self.print_aux('DESVAR', self.dvars, file)
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
        User-defined label.
    group : str
        Group name the external response type belongs to.
    type : str
        External response type.
    region : int, optional
        :class:`.DEQATN` entry identification number.

    Notes
    -----
    To add variables, table entries or other :class:`.DRESP1` responses use the
    methods: :meth:`.add_dvar`, :meth:`.add_dtable` and :meth:`.add_dresp1`.

    """
    def __init__(self, label, group, type, region=''):
        super(DRESP3, self).__init__()
        self.id = DRESP.uniqueid
        DRESP.uniqueid += 1
        self.label = label
        self.group = group
        self.type = type
        self.region = region

    def print_card(self, file):
        """Print the corresponding input card

        Parameters
        ----------
        file : file
            File object with a :meth:`write` method.

        """
        drespstr = ('%s% 8d% 8s% 8s% 8s% 8s\n' % ('DRESP3'.ljust(8), self.id,
                    self.label, self.group, self.type, self.region))
        file.write(drespstr)

        if len(self.dvars) > 0:
            self.print_aux('DESVAR', self.dvars, file)
        if len(self.dtable) > 0:
            self.print_aux('DTABLE', self.dtable, file)
        if len(self.dresp1) > 0:
            self.print_aux('DRESP1', self.dresp1, file)


class DESVAR(object):
    """Design Variable

    Parameters
    ----------
    label : str
        User-supplied name for printing purposes.
    xinit : float
        Initial value.
    xlb : float
        Lower bound.
    xub : float
        Upper bound.
    dvprel1 : :class:`.DVPREL1` or None, optional
        The corresponding design variable-to-property relation.
    code : str or None, optional
        An additional code to identify the design varible.

    """
    uniqueid = 9000000

    def __init__(self, label, xinit, xlb, xub, dvprel1=None, code=None):
        self.id = DESVAR.uniqueid
        DESVAR.uniqueid += 1
        self.defaults()
        self.label = label
        self.xinit = xinit
        self.xlb = xlb
        self.xub = xub
        self.dvprel1 = dvprel1
        self.code = code

    def defaults(self):
        self.delx = ''
        self.ddval = ''

    def print_card(self, file):
        """Print the corresponding input card

        Parameters
        ----------
        file : file
            File object with a :meth:`write` method.

        """
        #file.write('$dvar.id dvar.code %8d %-8s\n' % (self.id, self.code))
        #file.write('$HMNAME DESVAR %8d %-8s\n' % (self.id, self.label))
        file.write('%s% 8d% 8s%s%s%s% 8s% 8s\n' % ('DESVAR'.ljust(8), self.id,
            self.label, ff(self.xinit), ff(self.xlb), ff(self.xub),
            str(self.delx), str(self.ddval)))

    def show_card(self):
        print('%s% 8d% 8s%s%s%s% 8s% 8s\n' % ('DESVAR'.ljust(8),
              self.id, self.label, ff(self.xinit), ff(self.xlb), ff(self.xub),
              str(self.delx), str(self.ddval)))


class BASEDV2(PRINTAUX):
    """Base class for DVPREL2, DVCREL2 and DVMREL2

    """
    def __init__(self):
        super(BASEDV2, self).__init__()
        self.dvars = []
        self.dtable = []

    def add_dvar(self, dvar_id):
        self.dvars.append(dvar_id)

    def add_dtable(self, cons_label):
        self.dtable.append(cons_label)


class DVPREL1(object):
    """Design Variable-to-Property relation

    This is a wrapper for the DVPREL1 card in NASTRAN.

    Parameters
    ----------
    type : str
        Name of a property entry, such as "PBAR", "PBEAM", etc.
    pid : int
        Property entry identification number.
    pname : str
        Parameter name such as "T", "A", "DIM1", or a field position of the
        property entry.
    dvids : list
        Ids of the design variables that will be related to this property
        parameter.
    coefs : list
        Multipliers to each corresponding design variable.
    c0 : float, optional
        Constant term of relation.

    """
    def __init__(self, type, pid, pname, dvids, coefs, c0=0.):
        self.id = DVPREL.uniqueid
        DVPREL.uniqueid += 1
        self.type = type
        self.pid = pid
        self.pname = pname
        self.dvids = dvids
        self.coefs = coefs
        self.c0 = c0

        assert len(dvids) == len(coefs), 'Lengths must be the same'
        assert len(dvids) > 0, 'At least one variable must be related'


    def print_card(self, file):
        """Print the corresponding input card

        Parameters
        ----------
        file : file
            File object with a :meth:`write` method.

        """
        file.write('%s% 8d% 8s% 8d% 8s% 8s% 8s%s\n' %
                   ('DVPREL1'.ljust(8), self.id, self.type, self.pid,
                       self.pname, '', '', ff(self.c0)))

        fieldnum = 0
        dvprel1str = '+'.ljust(8)
        for i in range(len(self.dvids)):
            fieldnum += 2
            if fieldnum == 10:
                file.write(dvprel1str + '\n')
                dvprel1str = '+'.ljust(8)
                fieldnum = 2
            dvprel1str += ('% 8d%s' % (self.dvids[i], ff(self.coefs[i])))
        file.write(dvprel1str + '\n')


class DVPREL2(BASEDV2):
    """Design Variable-to-Property relation

    This is a wrapper for the DVPREL1 card in NASTRAN.

    Parameters
    ----------
    type : str
        Name of a property entry, such as "PBAR", "PBEAM", etc.
    pid : int
        Property entry identification number.
    pname : str
        Parameter name such as "T", "A", "DIM1", or a field position of the
        property entry.
    eqid : int or str
        :class:`.DEQATN` entry identification number, or string informing a
        pre-programmed function.

    """
    def __init__(self, type, pid, pname, eqid):
        super(DVPREL2, self).__init__()
        self.id = DVPREL.uniqueid
        DVPREL.uniqueid += 1
        self.type = type
        self.pid = pid
        self.pname = pname
        self.eqid = eqid

    def print_card(self, file):
        """Print the corresponding input card

        Parameters
        ----------
        file : file
            File object with a :meth:`write` method.

        """
        dvprel2str = ('%s% 8d% 8s% 8d% 8s% 8s% 8s% 8s\n' %
                      ('DVPREL2'.ljust(8), self.id, self.type, self.pid,
                       self.pname, '', '', str(self.eqid)))

        file.write(dvprel2str)

        if len(self.dvars) > 0:
            self.print_aux('DESVAR', self.dvars, file)
        if len(self.dtable) > 0:
            self.print_aux('DTABLE', self.dtable, file)


class DCONSTR(object):
    """Design constraint

    Parameters
    ----------
    dcid : int
        Design constraint set identification number.
    rid : int
        The corresponding design response id.
    lallow : float
        Lower bound on the response quantity.
    uallow : float
        Upper bound on the response quantity.

    """
    uniqueid = 9000000

    def __init__(self, dcid, rid, lallow, uallow):
        self.id = DCONSTR.uniqueid
        DCONSTR.uniqueid += 1
        self.dcid = dcid
        self.rid = rid
        self.lallow = lallow if lallow is not None else ''
        self.uallow = uallow if uallow is not None else ''

    def print_card(self, file):
        """Print the corresponding input card

        Parameters
        ----------
        file : file
            File object with a :meth:`write` method.

        """
        dconstr = ('%s% 8d% 8d% 8s% 8s' % ('DCONSTR'.ljust(8), self.dcid,
            self.rid, str(self.lallow), str(self.uallow)))
        file.write(dconstr + '\n')


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

    Parameters
    ----------
    ddvid : int
        Dependent design variable identification number.
    c0 : float
        Constant term.
    cmult : float
        Constant multiplier.
    idvs : list
        The independent variables.
    cs : list
        The multipliers for each variable.

    Notes
    -----
    Be sure that no dependent variables are being used as independent
    variables.

    By default `c0 = 0` and `cmult = 1`.

    The values of `dvi` and `ci` are inputed as follows::

        indep_dv_c = [dv1, c1, dv2, c2, ...]
        indep_dv_c = [1000000, 1., 1000001, 1., ...]

    """
    uniqueid = 9000000

    def __init__(self, ddvid, idvs, cs, c0=0., cmult=1.):
        self.id = DLINK.uniqueid
        DLINK.uniqueid += 1
        self.ddvid = ddvid
        self.c0 = c0
        self.cmult = cmult
        self.idvs = idvs
        self.cs = cs

        assert len(idvs) == len(cs), 'Lengths must be the same'
        assert len(idvs) > 0, 'At least one independent variable required'

    def print_card(self, file):
        """Print the corresponding input card

        Parameters
        ----------
        file : file
            File object with a :meth:`write` method.

        """
        dlinkstr = ('%s% 8d% 8d%s%s' % ('DLINK'.ljust(8), self.id,
                    self.ddvid, ff(self.c0), ff(self.cmult)))
        dvicicount = 4
        for i in range(len(self.idvs)):
            dvicicount += 2
            if dvicicount == 10:
                file.write(dlinkstr + '\n')
                dlinkstr = '+'.ljust(8)
                dvicicount = 2
            dlinkstr += ('% 8d%s' % (self.idvs[i], ff(self.cs[i])))

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
              56 characters in the first line, and 64 characters for the
              subsequent lines.

    """
    uniqueid = 9000000

    def __init__(self, eq):
        self.id = DEQATN.uniqueid
        DEQATN.uniqueid += 1
        self.eq = '  ' + eq

    def print_card(self, file):
        """Print the corresponding input card

        Parameters
        ----------
        file : file
            File object with a :meth:`write` method.

        """
        eq = self.eq
        deqatn_str = '%s% 8d' % ('DEQATN'.ljust(8), self.id)
        check = eq[:56].find(';')
        if check == -1:
            check = 55
        deqatn_str += eq[:check+1]
        deqatn_str += '\n'
        file.write(deqatn_str)

        eq = eq[check+1:]

        while len(eq) > 0:
            check = eq[:64].find(';')
            if check == -1:
                check = 63
            deqatn_str = '+       ' + eq[:check+1].ljust(64) + '\n'
            file.write(deqatn_str)
            eq = eq[check+1:]


class DTABLE(object):
    """Design Table used to define many constants

    Hints:

    - There can be any number of DTABLE entries in the bulk data.
    - The user must avoid repeated labels for constants
    - The constant label must be <= 8 characters.

    All values for the constants must be of the 'Real' type.  Ex::

        input_dict={'c1':1. , 'c2':2., 'max8char':999.}

    """
    def __init__(self, input_dict={}):
        self.input_dict = input_dict

    def print_card(self, file):
        """Print the corresponding input card

        Parameters
        ----------
        file : file
            File object with a :meth:`write` method.

        """
        if len(self.input_dict) > 0:
            keys = self.input_dict.keys()
            dtable_str = 'DTABLE'.ljust(8)
            count = 0
            for k in sorted(keys):
                v = self.input_dict[k]
                count += 2
                if count == 10:
                    file.write(dtable_str + '\n')
                    dtable_str = '+'.ljust(8)
                    count = 2
                dtable_str += '% 8s%s' % (str(k), ff(v))
            file.write(dtable_str + '\n')


if __name__ == '__main__':
    with open('tmp.bdf', 'w') as f:
        test = DRESP2('test',1,100)
        for i in range(1,16):
            test.add_dvar(i)
            test.add_dresp1(i)
        test.print_card(f)
