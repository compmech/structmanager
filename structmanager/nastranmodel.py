import os

from pyNastran.bdf.bdf import BDF
from pyNastran.op2.op2 import OP2
from pyNastran.op2.data_in_material_coord import data_in_material_coord


class NastranModel(object):
    def __init__(self, bdfpath):
        self.bdf = None
        self.bdfpath = bdfpath
        self.op2 = None
        self.subcases = None
        self.subcases_op2 = None

    def read_bulkdata(self):
        # reading bulk data file
        if self.bdfpath is None:
            print('ERROR - Model.bdfpath must be defined!')
            return
        bdf = BDF()
        self.bdf = bdf

        bdf.read_bdf(self.bdfpath)
        self._treat_bdf_subcases()

    def read_op2(self, op2path):
        if not os.path.isfile(op2path):
            print('ERROR - op2 "{0}" does not exist!'.format(op2path))
            return
        op2 = OP2()
        print('Reading op2 file...')
        op2.read_op2(op2path)
        self.op2 = data_in_material_coord(self.bdf, op2, in_place=True)
        print('finished!')


    def _treat_bdf_subcases(self):
        self.subcases = []
        for line in self.bdf.case_control_lines:
            line = line.strip()
            if 'SUBCASE' in line.upper():
                if line[0] == '$':
                    continue
                self.subcases.append(int(line.split()[-1]))



