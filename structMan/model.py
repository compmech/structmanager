"""
Model (:mod:`structmanager.model`)
==================================

.. currentmodule:: structmanager.model

"""
from collections import defaultdict
from string import strip

import numpy as np
from pyNastran.bdf.bdf import BDF
from pyNastran.op2.op2 import OP2

from sol200 import SOL200, DESVAR, DVPREL1, DRESP1, DCONSTR
from ses import (Panel, InnerFlange, Web, OuterFlange, ShearClipFrame,
                 ShearClipSkin, Stringer)
from sas import FrameAssembly, FrameShearClipAssembly, StiffenedPanelAssembly


def treat_bdf_subcases(bdf):
    bdf.subcases = []
    for line in bdf.case_control_lines:
        line = line.strip()
        if 'SUBCASE' in line.upper():
            if line[0] == '$':
                continue
            bdf.subcases.append(int(line.split()[-1]))



class Model(object):
    """Model"""
    def __init__(self):
        self.bdf = None
        self.bdfpath = None
        self.op2 = None
        self.op2path = None
        # structural elements
        self.sefile = None
        self.panels = {}
        self.innerflanges = {}
        self.webs = {}
        self.outerflanges = {}
        self.shearclipframes = {}
        self.shearclipskins = {}
        self.stringers = {}
        self.ses = {'panel': Panel,
                    'innerflange': InnerFlange,
                    'web': Web,
                    'outerflange': OuterFlange,
                    'shearclipframe': ShearClipFrame,
                    'shearclipskin': ShearClipSkin,
                    'stringer': Stringer}
        # structural assemblies
        self.safile = None
        self.frames = {}
        self.stiffenedpanels = {}
        self.sas = {'stiffenedpanelassembly': StiffenedPanelAssembly,
                    'frameshearclipassembly': FrameShearClipAssembly,
                    'frameassembly': FrameAssembly,
                    }
        # optimization related
        self.optmodel = SOL200()


    def read_op2(self, vectorized=True):
        if self.op2path is None:
            print('Model.op2path must be defined!')
            return
        if self.op2 is not None:
            print('OP2 already loaded!')
            return
        self.op2 = OP2()
        print('Reading op2 file...')
        self.op2.read_op2(self.op2path, vectorized=vectorized)
        print('finished!')
        #TODO try to fix op2.subcases and submit a pull request
        self.op2.subcases = sorted(self.op2.cquad4_force.keys())

        # reading forces for each SE
        for sename in self.ses.keys():
            print('Reading forces for %s...' % sename)
            sename = sename.lower()
            se_container = getattr(self, sename + 's')
            for se in se_container.values():
                se.read_forces()
            print('finished!')

    def build(self):
        panels = self.panels
        innerflanges = self.innerflanges
        webs = self.webs
        outerflanges = self.outerflanges
        shearclipframes = self.shearclipframes
        shearclipskins = self.shearclipskins
        stringers = self.stringers
        frames = self.frames
        stiffenedpanels = self.stiffenedpanels

        # reading bulk data file
        bdf = BDF()
        self.bdf = bdf
        if self.bdfpath is None:
            print('Model.bdfpath must be defined!')
            return
        bdf.read_bdf(self.bdfpath)
        treat_bdf_subcases(bdf)

        # reading structural elements
        if self.sefile is None:
            print('Model.sefile must be defined!')
            return
        with open(self.sefile) as f:
            lines = f.readlines()
        for line in lines:
            line = strip(line)
            fields = line.split(':')
            if not line:
                continue
            if fields[0].startswith('#'):
                continue
            sename, name = fields[0].split()
            sename = sename.lower()

            seClass = self.ses.get(sename)
            if seClass is None:
                continue

            eids = map(int, fields[1].split(','))

            container = getattr(self, sename + 's')
            se = seClass(name, eids, self)
            container[name] = se

        # reading structural assemblies
        if self.safile is None:
            print('Model.safile must be defined!')
            return
        with open(self.safile) as f:
            lines = f.readlines()
        for line in lines:
            line = strip(line)
            fields = line.split(':')
            if not line:
                continue
            if fields[0].startswith('#'):
                continue
            saname, name = fields[0].split()
            saname = saname.lower()

            saClass = self.sas.get(saname)
            if saClass is None:
                continue

            if saname == 'frameassembly':
                n1, n2, n3 = map(strip, fields[1].split(','))
                frames[name] = saClass(name, outerflanges[n1], webs[n2],
                        innerflanges[n3])

            if saname == 'frameshearclipassembly':
                n1, n2, n3, n4, n5 = map(strip, fields[1].split(','))
                frames[name] = saClass(name, shearclipskins[n1],
                        shearclipframes[n2], outerflanges[n3], webs[n4],
                        innerflanges[n5])

            if saname == 'stiffenedpanelassembly':
                n1, n2, n3, n4, n5 = map(strip, fields[1].split(','))
                stiffenedpanels[name] = saClass(name, panels[n1], frames[n2],
                        frames[n3], stringers[n4], stringers[n5])
