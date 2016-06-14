"""
Structural Analysis Model (:mod:`structmanager.structmodel`)
============================================================

.. currentmodule:: structmanager.structmodel

"""
import os
from string import strip

import numpy as np

from structelem import (SE1D, SE2D, Panel, PanelComp, InnerFlange, Web,
        OuterFlange, ShearClipFrame, ShearClipSkin, Stringer)
from sas import FrameAssembly, FrameShearClipAssembly, StiffenedPanelAssembly, StiffenedPanelCutout
from nastranmodel import NastranModel

from outreader import read_forces_1d, read_forces_2d


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
        # structural elements
        self.sefilepath = sefilepath
        self.safilepath = safilepath
        self.panels = {}
        self.panelcomps = {}
        self.innerflanges = {}
        self.webs = {}
        self.outerflanges = {}
        self.shearclipframes = {}
        self.shearclipskins = {}
        self.stringers = {}
		#self.panelcutout = {}
		#self.stringersegment = {}
        self.ses = {'panel': Panel,
					'panelcomp': PanelComp,
                    'innerflange': InnerFlange,
                    'web': Web,
                    'outerflange': OuterFlange,
                    'shearclipframe': ShearClipFrame,
                    'shearclipskin': ShearClipSkin,
                    'stringer': Stringer}
        # structural assemblies
        self.frames = {}
        self.stiffenedpanels = {}
		#self.stiffenedpanelcutout = {}
        self.sas = {'stiffenedpanelassembly': StiffenedPanelAssembly,
                    'frameshearclipassembly': FrameShearClipAssembly,
                    'frameassembly': FrameAssembly,
                    'stiffenedpanelcutout': StiffenedPanelCutout,}
        self.build()


    def read_forces(self):
        if self.nastranmodel.op2 is None:
            print('ERROR - No op2 file loaded')
            return
        op2 = self.nastranmodel.op2
        # reading forces for each SE
        for sename in self.ses.keys():
            sename = sename.lower()
            se_container = getattr(self, sename + 's')
            already_print = False
            for se in se_container.values():
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
        panels = self.panels
        innerflanges = self.innerflanges
        webs = self.webs
        outerflanges = self.outerflanges
        shearclipframes = self.shearclipframes
        shearclipskins = self.shearclipskins
        stringers = self.stringers
        frames = self.frames
        stiffenedpanels = self.stiffenedpanels
		#compositepanels = self.panelcutout
        compositepanels = self.panels
		#compositestringers = self.stringersegment
        compositestringers = self.stringers
		#compositestiffenedpanels = self.stiffenedpanelcutout
        compositestiffenedpanels = self.stiffenedpanels

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

            seClass = self.ses.get(sename)
            if seClass is None:
                continue

            eids = map(int, fields[2:])

            container = getattr(self, sename + 's')
            se = seClass(name, eids, self)
            container[name] = se

        # reading structural assemblies
        if self.safilepath is not None:
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

                saClass = self.sas.get(saname)
                if saClass is None:
                    continue

                if saname == 'frameassembly':
                    n1, n2, n3 = fields[2:]
                    frames[name] = saClass(name, outerflanges[n1], webs[n2],
                            innerflanges[n3])

                if saname == 'frameshearclipassembly':
                    n1, n2, n3, n4, n5 = fields[2:]
                    frames[name] = saClass(name, shearclipskins[n1],
                            shearclipframes[n2], outerflanges[n3], webs[n4],
                            innerflanges[n5])

                if saname == 'stiffenedpanelassembly':
                    n1, n2, n3, n4, n5 = fields[2:]
                    stiffenedpanels[name] = saClass(name, panels[n1], frames[n2],
                            frames[n3], stringers[n4], stringers[n5])
                #TODO
                #if saname == 'stiffenedpanelcuotut':
                #    n1, n2, n3 = fields[2:]
                #    compositestiffenedpanels[name] = saClass(name, panels[n1], stringers[n2], stringers[n3])
