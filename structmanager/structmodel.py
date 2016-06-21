"""
Structural Analysis Model (:mod:`structmanager.structmodel`)
============================================================

.. currentmodule:: structmanager.structmodel

"""
import os
from collections import defaultdict
from string import strip

import numpy as np

from structelem.base import SE1D, SE2D
from structelem import se_classes
from sas import sa_classes
from nastranmodel import NastranModel

from outreader import read_forces_1d, read_forces_2d


class dictX(dict):
    def __getattr__(self, attr):
        return self[attr]
    def __setattr__(self, attr, value):
        self[attr] = value


class StructModel(object):
    """Structural Analysis Model Base Class

    Attributes
    ----------

    ses : dict
        All types of supported structural element classes are grouped in this
        dictionary.

    """
    def __init__(self, sefilepath, safilepath=None, bdfpath=None):
        # link to Nastran model
        self.bdfpath = bdfpath
        self.nastranmodel = None
        # structural elements and assemblies
        self.sefilepath = sefilepath
        self.safilepath = safilepath
        self.se_classes = dictX((c.__name__.lower(), c) for c in se_classes)
        self.sa_classes = dictX((c.__name__.lower(), c) for c in sa_classes)
        self.ses = dictX((c.__name__.lower(), dictX()) for c in se_classes)
        self.sas = dictX((c.__name__.lower(), dictX()) for c in sa_classes)
        self.build()


    def read_forces(self):
        if self.nastranmodel.op2 is None:
            print('ERROR - No op2 file loaded')
            return
        op2 = self.nastranmodel.op2
        # reading forces for each SE
        for sename, d in self.ses.items():
            already_print = False
            for se in d.values():
                if not already_print:
                    print('Reading forces for %s...' % sename)
                if isinstance(se, SE1D):
                    se.forces = read_forces_1d(op2, se)
                elif isinstance(se, SE2D):
                    se.forces = read_forces_2d(op2, se)
                if not already_print:
                    print('finished!')
                    already_print = True


    def build(self):
        if self.bdfpath is not None:
            if os.path.isfile(str(self.bdfpath)):
                self.nastranmodel = NastranModel(self.bdfpath)
                self.nastranmodel.read_bulkdata()
            else:
                print('WARNING - Nastran model "{0}" not found!'.
                        format(self.bdfpath))

        # reading structural elements
        if self.sefilepath is None:
            print('sefilepath must be defined!')
            return
        with open(self.sefilepath) as f:
            lines = f.readlines()
        for line in lines:
            line = strip(line)
            if not line:
                continue
            if line.startswith('#'):
                continue
            fields = map(strip, line.split(';'))
            sename, name = fields[:2]
            sename = sename.lower()

            seClass = self.se_classes.get(sename)
            if seClass is None:
                print('ERROR - Ivalid Structural Element: {0}'.format(sename))
                continue

            eids = map(int, fields[2:])
            self.ses[sename][name] = seClass(name, eids, model=self)

        # reading structural assemblies
        if self.safilepath is None:
            return
        with open(self.safilepath) as f:
            lines = f.readlines()
        for line in lines:
            line = strip(line)
            if not line:
                continue
            if line.startswith('#'):
                continue
            fields = line.split(';')
            saname, name = map(strip, fields[:2])
            saname = saname.lower()

            saClass = self.sa_classes.get(saname)
            if saClass is None:
                print('ERROR - Ivalid Structural Assembly: {0}'.format(saname))
                continue

            senames = fields[2:]
            args = [self.ses.get(sename) for sename in senames]
            self.sas[saname][name] = saClass(name, args)
