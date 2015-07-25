import os
import cPickle as pickle
from pprint import pformat
from collections import Iterable

from output_codes import OUTC, get_output_code
from cards_opt import *
from cards_solver import *


class Genesis(object):
    """GENESIS optimization model

    This class corresponds to an optimization model.

    ==================  ======================================================
    Attribute           Description
    ==================  ======================================================
    ``dvprops``         ``dict`` of :class:`.DVPROP3` objects
    ``deqatns``         ``dict`` of :class:`.DEQATN` objects
    ``dtables``         ``dict`` of :class:`.DTABLE`
    ``dresps``          ``dict`` of :class:`.DRESP1` or :class:`.DRESP23`
                        objects
    ``dcons``           ``dict`` of :class:`.DCONS` objects
    ``dvars``           ``dict`` of :class:`.DVAR` objects
    ``dvar_codes``      ``dict`` classifying the :class:`.DVAR` objects by
                        their unique codes
    ``dlinks``          ``dict`` of :class:`.DLINK` objects
    ``newprops``        ``dict`` with different NASTRAN cards, see
                        :meth:`.reset_newprops`
    ``nodal_displ``     ``dict`` with the nodal displacements constraints as
                        detailed in :meth:`.nodal_displ_from_excel`
    ``loads_list``      ``list`` containing the load cases' ids
    ``spcs_list``       ``list`` containing the single point constraint id
                        for each load case
    ``num_cycles``      ``int`` indicating the number of design cycles
    ``outputdir``       ``str`` path to the output directory
    ``genesisfile``     ``file`` handler to GENESIS's output file
    ``nastranfile``     ``file`` handler to NASTRAN's output file
    ==================  ======================================================

    """
    def __init__(self):
        self.dvprops = {}
        self.reset_newprops()
        self.deqatns = {}
        self.dtables = {}
        self.dresps = {}
        self.dcons = {}
        self.dvars = {}
        self.dvar_codes = {}
        self.dlinks = {}
        #TODO future implementation
        #self.externalDRESP3 = {}
        # Description
        # ``externalDRESP3``  ``dict`` of :class:`.DRESP23` objects, containing
        #                     external design responses to be considered
        self.topocheck = False
        self.nodal_displ = None
        self.loads_list = None
        self.spcs_list = None
        self.num_cycles = None
        self.outputdir = None
        self.genesisfile = None
        self.nastranfile = None
        self.datname = None


    def nodal_displ_from_excel(self, xls_file):
        """Create nodal displacement constraints based on an Excel file.

        This function reads the xls file with nodal displacement constraints
        and returns a dictionary with the format::

            nd = {load_case_id1 : {grid_1 : {output : [minvalue, maxvalue],
                                   grid_2 :  output : [minvalue, maxvalue],
                                   grid_3 :  output : [minvalue, maxvalue]}}
                  load_case_id2 : {grid_1 : {output : [minvalue, maxvalue],
                                   grid_3 :  outout : [minvalue, maxvalue]}}}

        where ``minvalue`` and ``maxvalue`` are the minimum and maximum
        displacement values.

        Parameters
        ----------
        xls_file : str
            The full path to the Excel file.

        Returns
        -------
        output : str
            A string with one of the values:

            - ``'Translation X'``
            - ``'Translation Y'``
            - ``'Translation Z'``
            - ``'Rotation X'``
            - ``'Rotation Y'``
            - ``'Rotation Z'``
            - ``'Translation Total'``
            - ``'Absolute X'``
            - ``'Absolute Y'``
            - ``'Absolute Z'``

        """
        from excel import Excel

        if not xls_file:
            return None

        ex = Excel(xls_file)
        found = False
        for row in range(1, 100):
            for col in range(1, 23):
                refvalue = str(ex.get_cell(1, row, col))
                if refvalue.find('DISPLACEMENT CONSTRAINTS') > -1:
                    found = True
                    break
            if found:
                break
        nd = {}
        irow = row + 2
        #TODO this try/except block is mainly to avoid Excel from being
        #     a defunct
        try:
            for row in range(irow, 65536):
                load_id = ex.get_cell(1, row, col)
                if load_id.__class__.__name__ == 'NoneType':
                    break
                #
                load_id = int(load_id)
                node_id = ex.get_cell(1, row, col + 1)
                node_id = int(node_id)
                output = ex.get_cell(1, row, col + 2)
                output = str(output)
                minvalue = ex.get_cell(1, row, col + 3)
                minvalue = float(minvalue)
                maxvalue = ex.get_cell(1, row, col + 4)
                maxvalue = float(maxvalue)
                if not load_id in nd.keys():
                    nd[load_id] = {}
                if not node_id in nd[load_id].keys():
                    nd[load_id][node_id] = {}
                nd[load_id][node_id][output] = [minvalue, maxvalue]
            ex.close()
            self.nodal_displ = nd

        except:
            ex.close()
            print('nodal_displ_from_excel() failed!')

            return None

        for load_id in nd.keys():
            for node_id in nd[load_id].keys():
                for con_name in nd[load_id][node_id].keys():
                    con_minvalue = nd[load_id][node_id][con_name][0]
                    con_maxvalue = nd[load_id][node_id][con_name][1]

                    for k, v in OUTC['DISP'].iteritems():
                        if v.find(con_name) > -1:
                            code = k
                            break

                    if code == 7:
                        #DRESP1 x
                        labelx = 'x' + str(node_id)
                        dresp1 = DRESP1(labelx, 'DISP', '', '', 1, [node_id])
                        self.dresps[dresp1.id] = dresp1
                        dresp1xid = dresp1.id

                        #DRESP1 y
                        labely = 'y' + str(node_id)
                        dresp1 = DRESP1(labely, 'DISP', '', '', 2, [node_id])
                        self.dresps[dresp1.id] = dresp1
                        dresp1yid = dresp1.id

                        #DRESP1 z
                        labelz = 'z' + str(node_id)
                        dresp1 = DRESP1(labelz, 'DISP', '', '', 3, [node_id])
                        self.dresps[dresp1.id] = dresp1
                        dresp1zid = dresp1.id

                        #DEQATN
                        eq = ('T(%s,%s,%s)=SQRT(%s**2+%s**2+%s**2)' %
                        (labelx, labely, labelz, labelx, labely, labelz))
                        deqatn = DEQATN(eq)
                        self.deqatns[deqatn.id] = deqatn

                        #DRESP23
                        label = 'r' + str(node_id)
                        dresp23 =  DRESP23(label, deqatn.id)
                        dresp23.add_dresp1(dresp1xid)
                        dresp23.add_dresp1(dresp1yid)
                        dresp23.add_dresp1(dresp1zid)
                        self.dresps[dresp23.id] = dresp23

                        #DCONS
                        stress_type = 'positive'
                        lid_lb_ub = [str(load_id), con_minvalue, con_maxvalue]
                        self.dcons[dresp23.id] = DCONS(dresp23.id, lid_lb_ub,
                                                       stress_type)
                    elif (code == 8 or code == 9 or code == 10):
                        #DRESP1
                        label = 'a' + str(node_id)
                        dresp1 = DRESP1(label, 'DISP', '', '', code, [node_id])
                        self.dresps[dresp1.id] = dresp1

                        #DEQATN
                        eq = 'D(%s)=ABS(%s)' % (label, label)
                        deqatn = DEQATN(eq)
                        self.deqatns[deqatn.id] = deqatn

                        #DRESP23
                        label = 'r' + str(node_id)
                        dresp23 = DRESP23(label, deqatn.id)
                        dresp23.add_dresp1(dresp23.id)
                        self.dresps[dresp23.id] = dresp23

                        #DCONS
                        stress_type = 'positive'
                        lid_lb_ub = [str(load_id), con_minvalue, con_maxvalue]
                        self.dcons[dresp23.id] = DCONS(dresp23.id, lid_lb_ub,
                                                       stress_type)
                    else:
                        #DRESP1
                        label = 'r' + str(node_id)
                        dresp1 = DRESP1(label, 'DISP', '', '', code, [node_id])
                        self.dresps[dresp1.id] = dresp1

                        #DCONS
                        stress_type = 'both'
                        lid_lb_ub = [str(load_id), con_minvalue, con_maxvalue]
                        self.dcons[dresp1.id] = DCONS(dresp1.id, lid_lb_ub,
                                                      stress_type)


    def dlinks_from_excel(self, xls_file):
        """Read links between variables from an Excel file.

        The Excel file should have the following format:

        ======= ====== ======= ======= ======= ======= ======= ======= =======
        .       col j  col j+1 col j+2 col j+3 col j+4 col j+5 col j+6 col j+7
        ======= ====== ======= ======= ======= ======= ======= ======= =======
        row i   DLINK
        row i+1
        row i+2 dvar   c0      c       ivar1   c1      ivar2   c2      ...
        row i+3 LP.1.1 0.      1.      LS.1.1  0.4     LS.1.2  0.6     ...
        ======= ====== ======= ======= ======= ======= ======= ======= =======

        where the relative position between the cell with ``DLINK`` and the
        others must be held.

        Parameters
        ----------
        xls_file : str
            The full path of the Excel file.

        """
        from excel import Excel

        ex = Excel(xls_file)
        found = False
        print('Reading Excel File %s...' % xls_file)
        for row in range(1, 101):
            for col in range(1, 256):
                rvalue = ex.get_cell(1, row, col)
                if 'DLINK' == rvalue:
                    found = True
                    break
            if found:
                break
        dlinks = {}
        count = -1
        irow = row + 3
        for row in range(irow, 65536):
            dvar_code = ex.get_cell(1, row, col)
            if dvar_code is None:
                break
            print('    creating DLINK for variable: %s' % dvar_code)
            c0 = ex.get_cell(1, row, col + 1)
            c = ex.get_cell(1, row, col + 2)
            ivar_code_1 = ex.get_cell(1, row, col + 3)
            c_1 = ex.get_cell(1, row, col + 4)
            ivar_code_2 = ex.get_cell(1, row, col + 5)
            c_2 = ex.get_cell(1, row, col + 6)
            ivar_code_3 = ex.get_cell(1, row, col + 7)
            c_3 = ex.get_cell(1, row, col + 8)

            dvar = self.dvar_codes[dvar_code]
            ivar_1 = self.dvar_codes[ivar_code_1]

            try:
                dvi_ci = [ivar_1.id, float(c_1)]
            except:
                dvi_ci = [ivar_1.id, str(c_1)]

            if ivar_code_2.__class__.__name__ <> 'NoneType':
                ivar_2 = self.dvar_codes[ivar_code_2]
                dvi_ci = dvi_ci + [ivar_2.id, float(c_2)]

            if ivar_code_3.__class__.__name__ <> 'NoneType':
                ivar_3 = self.dvar_codes[ivar_code_3]
                dvi_ci = dvi_ci + [ivar_3.id, float(c_3)]

            count += 1
            self.dlinks[count] = DLINK(dvar.id, dvi_ci, c0=c0, cmult=c)

        ex.close()


    def set_output_file(self, path):
        """Define the data related to the output file.

        The output directory is estimated based on ``path``.

        Parameters
        ----------
        path : str
            The full path of the output file.

        """
        self.outputdir = os.path.dirname(path)
        self.datname = path

        tmppath = os.path.join(self.outputdir, 'genesis.temp')
        self.genesisfile = open(tmppath, 'w')

        tmppath = os.path.join(self.outputdir, 'nastran.temp')
        self.nastranfile = open(tmppath, 'w')


    def _read_inputs(self, topocheck=False, topo_max_elem=1,
            manufact_cons_input=[], manufact_cons_coord=0):
        #TODO probably remove this method
        self.topocheck = topocheck
        self.topo_max_elem = topo_max_elem
        self.manufact_cons_input = manufact_cons_input
        self.manufact_cons_coord = manufact_cons_coord


    def add_dvprop(self, *args):
        dvprop = DVPROP3(*args)
        self.dvprops[dvprop.id] = dvprop


    def print_model(self):
        """Print the whole model.

        """
        self._print_dvprops()
        self._print_dvars()
        self._print_dresps()
        self._print_deqatns()
        self._print_dcons()
        self._print_dobj()
        self._print_dlinks()
        self._print_newprops()
        self.merge_temp_files()


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


    def create_dvars(self):
        """Create the design variables.

        The method :meth:`.DVPROP3.create_dvar` of each property contained in
        the dictionary `dvprops` is called.

        """
        self.dvars = {}
        self.dvar_codes = {}

        if len(self.dvprops) == 0:
            raise RuntimeError('No DVPROPs defined!')

        for dvprop in self.dvprops.values():
            dvprop.create_dvars()
            for dvar in dvprop.dvars:
                self.dvars[dvar.id] = dvar
                self.dvar_codes[dvar.code] = dvar


    def constrain_pshell(self, pid, cname, rtype, allow_C, allow_T):
        """Add constraints to the bottom and top faces of a shell property.

        Parameters
        ----------
        pid : int
            Property id.
        cname : str or list
            The name of the constraint, as described in :mod:`.output_codes`,
            without the sufix ``'Bottom'``  or ``'Top'``.
        rtype : str
            The type of response. For shells it is usually ``'STRESS'``.
        allow_C : float
            The allowable for compression.
        allow_T : float
            The allowable for tension.

        """
        if rtype.upper() == 'STRESS':
            label = 'minmaxS'
        ptype = 'PSHELL'
        eltype = 'SOLID'
        region = ''
        lid_lb_ub = []
        lid_lb_ub.append('ALL')
        lid_lb_ub.append(allow_C)
        lid_lb_ub.append(allow_T)

        if not isinstance(cname, Iterable):
            cname = [cname]

        for name in cname:
            name = name.strip()

            # Bottom Face
            namebot = name + ' Bottom'
            atta = get_output_code(rtype, eltype, namebot)
            output_name = OUTC[rtype][eltype][atta]

            stress_type = 'positive'
            if output_name.find('Minor') > -1:
                stress_type = 'negative'
            elif output_name.find('Normal') > -1:
                stress_type = 'both'
            else:
                #TODO perhaps we need a shear allowable
                if output_name.upper().find('SHEAR') > -1:
                    stress_type = 'positive'
                    lid_lb_ub[1] = lid_lb_ub[1] / 2.
                    lid_lb_ub[2] = lid_lb_ub[2] / 2.

            dresp1 = DRESP1(label, rtype, ptype, region, atta, pid)
            dcons = DCONS(dresp1.id, lid_lb_ub, stress_type)
            self.dresps[dresp1.id] = dresp1
            self.dcons[dresp1.id] = dcons

            # Top Face
            nametop = name + ' Top'
            atta = get_output_code(rtype, eltype, nametop)
            output_name = OUTC[rtype][eltype][atta]

            stress_type = 'positive'
            if output_name.find('Minor') > -1:
                stress_type = 'negative'
            elif output_name.find('Normal') > -1:
                stress_type = 'both'
            else:
                #TODO perhaps we need a shear allowable
                if output_name.upper().find('SHEAR') > -1:
                    stress_type = 'positive'
                    lid_lb_ub[1] = lid_lb_ub[1] / 2.
                    lid_lb_ub[2] = lid_lb_ub[2] / 2.

            region = ''
            dresp1 = DRESP1(label, rtype, ptype, region, atta, pid)
            dcons = DCONS(dresp1.id, lid_lb_ub, stress_type)
            self.dresps[dresp1.id] = dresp1
            self.dcons[dresp1.id] = dcons


    def constrain_pbar(self, pid, name, rtype, eltype, allow_C, allow_T):
        """Add constraints to all stress recovery points of a bar property.

        Parameters
        ----------
        pid : int
            Property id.
        name : str or list
            The name of the constraint, as described in :mod:`.output_codes`,
            with only the prefix (``'Shear'``, ``'Normal'``, etc).
        rtype : str
            The type of response. For bar elements it is usually ``'STRESS'``.
        eltype : str
            The section type: ``'RECT'``, ``'CIRCLE'``, etc.
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


        for namei in name:
            if 'Normal X' in namei:
                cons_names = ['Normal X Point 1 at end A',
                              'Normal X Point 2 at end A',
                              'Normal X Point 3 at end A',
                              'Normal X Point 4 at end A',
                              'Normal X Point 9 at end B',
                              'Normal X Point 10 at end B',
                              'Normal X Point 11 at end B',
                              'Normal X Point 12 at end B']
            elif 'Shear' in namei:
                cons_names = ['Shear XZ Point 5 at end A',
                              'Shear XY Point 6 at end A',
                              'Shear XZ Point 7 at end A',
                              'Shear XY Point 8 at end A',
                              'Shear XZ Point 13 at end B',
                              'Shear XY Point 14 at end B',
                              'Shear XZ Point 15 at end B',
                              'Shear XY Point 16 at end B']
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
                else:
                    #TODO perhaps we need a shear allowable
                    if output_name.upper().find('SHEAR') > -1:
                        stress_type = 'positive'
                        lid_lb_ub[1] = lid_lb_ub[1] / 2.
                        lid_lb_ub[2] = lid_lb_ub[2] / 2.

                dresp1 = DRESP1(label, rtype, ptype, region, atta, pid)
                dcons = DCONS(dresp1.id, lid_lb_ub, stress_type)
                self.dresps[dresp1.id] = dresp1
                self.dcons[dresp1.id] = dcons


    def constrain_two_vars(self, var1, var2, maxdiff):
        """Constraint two vars in order to keep a maximum relative difference

        Parameters
        ----------
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
        dresp2 = DRESP23('tmplabel', deqatn.id, region='')
        dresp2.label = 'v1v2{0:d}'.format(dresp2.id)
        dresp2.add_dvar(var1.id)
        dresp2.add_dvar(var2.id)
        dcons = DCONS(dresp2.id, ['ALL', '', maxdiff], 'positive')

        self.deqatns[deqatn.id] = deqatn
        self.dresps[dresp2.id] = dresp2
        self.dcons[dresp2.id] = dcons


    def create_dobj(self):
        """Create the design objective.

        """
        dresp1 =  DRESP1('mass','MASS', '', '', '', '')
        self.dresps[dresp1.id] = dresp1
        self.dobj = DOBJ(dresp1.id)

        #TODO move away from here
        # defining spc[i] = spc[0] if the number of spc is
        # lower than the number of load cases
        for i in range(len(self.loads_list)):
            if (i+1) > len(self.spcs_list):
                self.spcs_list.append(self.spcs_list[0])


    def create_topometric_data(self):
        #TODO method intended to be used with any FE model
        for dvprop in self.dvprops.values():
            dvpropid = dvprop.id
            dsplit = DSPLIT(dvpropid, dvprop.ptype, self.topo_max_elem,
                self.manufact_cons_input, self.manufact_cons_coord)
            dsplit.print_card(self.genesisfile)


    def _print_newprops(self):
        for pcard in self.newprops.values():
            for newprop in pcard.values():
                newprop.print_card(self.genesisfile)


    def _print_dvars(self):
        for dvar in self.dvars.values():
            dvar.print_card(self.genesisfile)


    def _print_dvprops(self):
        for dvprop in self.dvprops.values():
            dvprop.print_card(self.genesisfile)


    def _print_dresps(self):
        for dresp in self.dresps.values():
            dresp.print_card(self.genesisfile)


    def _print_deqatns(self):
        for deqatn in self.deqatns.values():
            deqatn.print_card(self.genesisfile)


    def _print_dcons(self):
        for dcons in self.dcons.values():
            dcons.print_card(self.genesisfile)


    def _print_dobj(self):
        self.dobj.print_card(self.genesisfile)


    def _print_dlinks(self):
        for dlink in self.dlinks.values():
            dlink.print_card(self.genesisfile)


    def simx_create_output_file(self):
        self.simx_export_nastran_file()


    def simx_export_nastran_file(self):
        import simx

        simx.export_current_model(self.nastranfile.name)


    def merge_temp_files(self):
        """Merge the temporary file handlers into the final input file.

        The file handlers contained in the attributes ``genesisfile`` and
        ``nastranfile`` are used to write a unique output file given by the
        attribute ``datname``.

        """
        import files

        files.merge_temp_files(self)


    def pickle_dump(self, path):
        file1 = self.genesisfile
        file2 = self.nastranfile
        # clearing file handlers that cannot be pickled
        self.genesisfile = None
        self.nastranfile = None
        self.mergedfile = None
        pickle.dump(self, open(path, 'w'))
        # recovering file handlers
        self.genesisfile = file1
        self.nastranfile = file2

        return True


    def pickle_load(path):
        self = pickle.load(open(path, 'r'))
        #FIXME see if these file handlers below need to be reloaded
        #create a method to recover them and call this method when
        #necessary
        path = os.path.join(self.outputdir, 'genesis.temp')
        self.genesisfile = open(path, 'w')

        path = os.path.join(self.outputdir, 'nastran.temp')
        self.nastranfile = open(path, 'w')

        return self
