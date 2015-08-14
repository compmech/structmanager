"""
SOL200 optimization model (:mod:`structMan.sol200.sol200`)
==========================================================

.. currentmodule:: structMan.sol200.sol200

"""
import os
import cPickle as pickle
from collections import Iterable

from output_codes import OUTC, get_output_code
from cards_opt import *
from cards_solver import *


def section(text, file):
    file.write('$ %s\n' % ('_'*72))
    file.write('$ %s\n' % (' '*72))
    file.write('$ %s\n' % text)
    file.write('$\n')


class SOL200(object):
    """SOL200 optimization model

    This class corresponds to an optimization model.

    ==================  ======================================================
    Attribute           Description
    ==================  ======================================================
    `dobj`              :class:`.DESOBJ` object
    `dvprels`           `dict` of :class:`.DVPREL1` and :class:`.DVPREL2`
                        objects
    `deqatns`           `dict` of :class:`.DEQATN` objects
    `dtable`            :class:`.DTABLE` that will be created based on the
                        `dtables` dictionary
    `dtables`           `dict` that will be used to build a unique DTABLE
    `dtable_prefixes`   `dict` carries IDs to prevent repeated DTABLE
                        constants.
    `dresps`            `dict` of :class:`.DRESP1`, :class:`.DRESP2` or
                        :class:`.DRESP3` objects
    `dconstrs`          `dict` of :class:`.DCONSTR` objects
    `dvars`             `dict` of :class:`.DVAR` objects
    `dvar_codes`        `dict` classifying the :class:`.DVAR` objects by
                          their unique codes
    `dlinks`            `dict` of :class:`.DLINK` objects
    `newprops`          `dict` with different NASTRAN cards, see
                        :meth:`.reset_newprops`
    `nodal_displ`       `dict` with the nodal displacements constraints as
                        detailed in :meth:`.nodal_displ_from_excel`
    `loads_list`        `list` containing the load cases' ids
    `num_cycles`        `int` indicating the number of design cycles
    `outputdir`         `str` path to the output directory
    `sol200filepath`    `str` path to SOL200's output file
    `sol200file`        `file` handler to SOL200's output file
    ==================  ======================================================

    """
    def __init__(self):
        self.dobj = None
        self.dvprels = {}
        self.reset_newprops()
        self.deqatns = {}
        self.dtable = None
        self.dtables = {}
        self.dtable_prefixes = {}
        self.dresps = {}
        self.dconstrs = {}
        self.dcids = set()
        self.dvars = {}
        self.dvar_codes = {}
        self.dlinks = {}
        #TODO future implementation
        #self.externalDRESP3 = {}
        # Description
        # `externalDRESP3`  `dict` of :class:`.DRESP3` objects, containing
        #                     external design responses to be considered
        self.topocheck = False
        self.nodal_displ = None
        self.loads_list = None
        self.num_cycles = None
        self.outputdir = None
        self.sol200filepath = None
        self.sol200file = None


    def set_output_file(self, path):
        """Define the data related to the output file.

        The output directory is estimated based on `path`.

        Parameters
        ----------
        path : str
            The full path of the output file.

        """
        self.outputdir = os.path.dirname(path)
        self.sol200filepath = path


    def _read_inputs(self, topocheck=False, topo_max_elem=1,
            manufact_cons_input=[], manufact_cons_coord=0):
        #TODO probably remove this method
        self.topocheck = topocheck
        self.topo_max_elem = topo_max_elem
        self.manufact_cons_input = manufact_cons_input
        self.manufact_cons_coord = manufact_cons_coord


    def print_model(self):
        """Print the whole model.

        """
        self.sol200file = open(self.sol200filepath, 'wb')

        if len(self.dtables) > 0:
            section('DESIGN CONSTRAINTS', self.sol200file)
            self.dtable = DTABLE(self.dtables)
            self.dtable.print_card(self.sol200file)
        self._print_dvars()
        self._print_dlinks()
        self._print_dvprels()
        self._print_dresps()
        self._print_deqatns()
        self._print_dcons()
        self._print_dobj()
        self._print_newprops()

        self.sol200file.close()


    def reset_newprops(self):
        """Reset the dictionary `newprops`.

        This dictionary contains NASTRAN property cards that should be created
        along with the optimization model.

        The supported cards are those corresponding to the classes defined in
        :mod:`.cards_solver`.

        """
        self.newprops = {}
        self.newprops['PSHELL'] = {}
        self.newprops['PBAR'] = {}
        self.newprops['PBARL'] = {}
        self.newprops['PBEAM'] = {}
        self.newprops['PBEAML'] = {}
        self.newprops['PCOMP'] = {}


    def constrain_pshell(self, dcid, pid, eltype, rtype, names, lallow=None,
            uallow=None):
        """Add constraints to the bottom and top faces of a shell property.

        Parameters
        ----------
        dcid : int
            Design constraint set identification number.
        pid : int
            Property id.
        eltype : str
            Element type ('CQUAD4', 'CTRIA3', etc).
        rtype : str
            The type of response. For shells it is usually `'STRESS'`.
        names : str or list of strings
            The name of the constraint, as in the quick reference guide,
            reproduced in module :mod:`.atd.sol200.output_codes`.
        lallow : float or None, optional
            Lower bound on the response quantity.
        uallow : float or None, optional
            Upper bound on the response quantity.

        """
        ptype = 'PSHELL'
        region = ''
        if lallow is None:
            lallow = ''
        if uallow is None:
            uallow = ''

        if not isinstance(names, (list, tuple)):
            names = [names]

        self.dcids.add(dcid)
        for name in names:
            atta = get_output_code(rtype, eltype, name)
            dresp1 = DRESP1(name[:8], rtype, ptype, region, atta, pid)
            dconstr = DCONSTR(dcid, dresp1.id, lallow, uallow)
            self.dresps[dresp1.id] = dresp1
            self.dconstrs[dconstr.id] = dconstr


    def constrain_pbar(self, dcid, pid, name, rtype, eltype, allow_C, allow_T):
        """Add constraints to all stress recovery points of a bar property.

        Parameters
        ----------
        dcid : int
            Design constraint set identification number.
        pid : int
            Property id.
        name : str or list
            The name of the constraint.
        rtype : str
            The type of response. For bar elements it is usually `'STRESS'`.
        eltype : str
            The section type: `'RECT'`, `'CIRCLE'`, etc.
        allow_C : float
            The allowable for compression.
        allow_T : float
            The allowable for tension.

        """
        if not isinstance(name, Iterable):
            name = [name]
        if rtype.upper() == 'STRESS':
            label = 'minmaxS'
        region = ''
        lid_lb_ub = []
        lid_lb_ub.append('ALL')
        lid_lb_ub.append(allow_C)
        lid_lb_ub.append(allow_T)

        self.dcids.add(dcid)

        for namei in name:
            if 'Axial' in namei:
                cons_names = ['End A-Point C',
                              'End A-Point D',
                              'End A-Point E',
                              'End A-Point F',
                              'End B-Point C',
                              'End B-Point D',
                              'End B-Point E',
                              'End B-Point F']
            ptype = 'PBARL'
            for i in range(len(cons_names)):
                name = cons_names[i]
                atta = get_output_code(rtype, eltype, name)
                output_name = OUTC[rtype][eltype][atta]

                stress_type = 'positive'
                if output_name.find('Minor') > -1:
                    stress_type = 'negative'
                elif output_name.find('Normal') > -1:
                    stress_type = 'both'

                dresp1 = DRESP1(label, rtype, ptype, region, atta, pid)
                dconstr = DCONSTR(dcid, dresp1.id, lid_lb_ub, stress_type)
                self.dresps[dresp1.id] = dresp1
                self.dconstrs[dconstr.id] = dconstr


    def constrain_two_vars(self, dcid, var1, var2, maxdiff):
        """Constrain two vars in order to keep a maximum relative difference

        Parameters
        ----------
        dcid : int
            Design constraint set identification number.
        var1, var2 : int or str
            The variables id (int) or code (str).
        maxdiff : float
            The maximum relative difference that 'var1' and 'var2' must
            respect.

        """
        if isinstance(var1, int):
            var1 = self.dvars.get(var1)
        elif isinstance(var1, str):
            var1 = self.dvar_codes.get(var1)
        else:
            raise ValueError("Invalid data type for 'var1'")

        if isinstance(var2, int):
            var2 = self.dvars.get(var2)
        elif isinstance(var2, str):
            var2 = self.dvar_codes.get(var2)
        else:
            raise ValueError("Invalid data type for 'var2'")

        if var1 is None:
            raise ValueError("'var1' not found!")
        if var2 is None:
            raise ValueError("'var2' not found!")

        deqatn = DEQATN('T(v1,v2)=ABS(v2-v1)/ABS(v1)')
        dresp2 = DRESP2('tmplabel', deqatn.id, region='')
        dresp2.label = 'v1v2{0:d}'.format(dresp2.id)
        dresp2.add_dvar(var1.id)
        dresp2.add_dvar(var2.id)
        self.dcids.add(dcid)
        dconstr = DCONSTR(dcid, dresp2.id, ['ALL', '', maxdiff], 'positive')

        self.deqatns[deqatn.id] = deqatn
        self.dresps[dresp2.id] = dresp2
        self.dconstrs[dconstr.id] = dconstr


    def create_dobj(self):
        """Create the design objective.

        """
        dresp1 =  DRESP1('mass','MASS', '', '', '', '')
        self.dresps[dresp1.id] = dresp1

        #TODO move to the case control section
        if False:
            self.dobj = DOBJ(dresp1.id)

            #TODO move away from here
            # defining spc[i] = spc[0] if the number of spc is
            # lower than the number of load cases
            for i in range(len(self.loads_list)):
                if (i+1) > len(self.spcs_list):
                    self.spcs_list.append(self.spcs_list[0])


    def _print_newprops(self):
        for pcard in self.newprops.values():
            for newprop in pcard.values():
                newprop.print_card(self.sol200file)


    def _print_dvars(self):
        if len(self.dvars) > 0:
            section('DESIGN VARIABLES', self.sol200file)
        for dvar in self.dvars.values():
            dvar.print_card(self.sol200file)


    def _print_dvprels(self):
        if len(self.dvprels) > 0:
            section('DESIGN VARIABLE-TO-PROPERTY RELATIONS', self.sol200file)
        for dvprel in self.dvprels.values():
            dvprel.print_card(self.sol200file)


    def _print_dresps(self):
        if len(self.dresps) > 0:
            section('DESIGN RESPONSES', self.sol200file)
        for dresp in self.dresps.values():
            dresp.print_card(self.sol200file)


    def _print_deqatns(self):
        if len(self.deqatns) > 0:
            section('DESIGN EQUATIONS', self.sol200file)
        for deqatn in self.deqatns.values():
            deqatn.print_card(self.sol200file)


    def _print_dcons(self):
        if len(self.dconstrs) > 0:
            section('DESIGN CONSTRAINTS', self.sol200file)
        for dconstr in self.dconstrs.values():
            dconstr.print_card(self.sol200file)


    def _print_dobj(self):
        if self.dobj is not None:
            section('DESIGN OBJECTIVE', self.sol200file)
            self.dobj.print_card(self.sol200file)


    def _print_dlinks(self):
        if len(self.dlinks) > 0:
            section('DESIGN LINKS', self.sol200file)
        for dlink in self.dlinks.values():
            dlink.print_card(self.sol200file)


    def pickle_dump(self, path):
        file1 = self.sol200file
        # clearing file handlers that cannot be pickled
        self.sol200file = None
        self.mergedfile = None
        pickle.dump(self, open(path, 'w'))
        # recovering file handlers
        self.sol200file = file1

        return True


    def pickle_load(path):
        self = pickle.load(open(path, 'r'))
        #FIXME see if these file handlers below need to be reloaded
        #create a method to recover them and call this method when
        #necessary
        path = os.path.join(self.outputdir, 'sol200.temp')
        self.sol200file = open(path, 'w')

        return self
