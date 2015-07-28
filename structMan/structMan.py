from collections import defaultdict
from string import strip

import numpy as np
from pyNastran.bdf.bdf import BDF
from pyNastran.op2.op2 import OP2

from sol200 import SOL200, DESVAR, DVPREL1, DRESP1, DCONSTR
from ses import (Panel, InnerFlange, Web, OuterFlange, ShearClipFrame,
                 ShearClipSkin, Stringer)
from sas import FrameAssembly, FrameAssemblyShearClip, StiffenedPanelAssembly


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
                    'frameassemblyshearclip': FrameAssemblyShearClip,
                    'frameassembly': FrameAssembly,
                    }

    def read_op2(self):
        if self.op2path is None:
            print('Model.op2path must be defined!')
            return
        if self.op2 is not None:
            print('OP2 already loaded!')
            return
        self.op2 = OP2()
        self.op2.read_op2(self.op2path, vectorized=True)
        #TODO try to fix op2.subcases and submit a pull request
        self.op2.subcases = sorted(self.op2.cquad4_force.keys())

        # reading forces for each SE
        for sename in self.ses.keys():
            sename = sename.lower()
            se_container = getattr(self, sename + 's')

            for se in se_container.values():
                se.read_forces()

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
            se = seClass(name, *eids)
            se.model = self
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

            if saname == 'frameassemblyshearclip':
                n1, n2, n3, n4, n5 = map(strip, fields[1].split(','))
                frames[name] = saClass(name, shearclipskins[n1],
                        shearclipframes[n2], outerflanges[n3], webs[n4],
                        innerflanges[n5])

            if saname == 'stiffenedpanelassembly':
                n1, n2, n3, n4, n5 = map(strip, fields[1].split(','))
                stiffenedpanels[name] = saClass(name, panels[n1], frames[n2],
                        frames[n3], stringers[n4], stringers[n5])

        bdf = BDF()
        self.bdf = bdf
        if self.bdfpath is None:
            print('Model.bdfpath must be defined!')
            return
        bdf.read_bdf(self.bdfpath)

        # Finding nodal connectivity
        #TODO why pyNastran does not do this already?
        if False:
            print 1
            nodes = defaultdict(set)
            for element in bdf.elements.values():
                if element.nodes is not None:
                    for node in element.nodes:
                        nodes[node.nid].add(element)
            for node in bdf.nodes.values():
                node.elements = nodes[node.nid]
            print 2

        #
        opt = self.optmodel = SOL200()

        print('Building panels')
        for p in panels.values():
            p.elements = [bdf.elements[eid] for eid in p.eids]
            setelements = set(p.elements)

            # finding corner nodes
            # assuming that they are those that share only one inner element
            nodes = []
            for element in p.elements:
                for node in element.nodes:
                    nodes.append(node)
            p.nodes = set(nodes)
            ccoords = np.array([n.xyz for n in p.nodes])
            xs = ccoords[:, 0]
            ys = ccoords[:, 1]
            zs = ccoords[:, 2]
            rs = (ys**2 + zs**2)**0.5
            thetas = np.arctan2(zs, ys)
            p.length = xs.max() - xs.min()
            p.width = (thetas.max() - thetas.min())*rs.mean()

            # retrieving panel thickness and material properties
            p.pid = p.elements[0].Pid()
            p.thickness = np.array([elem.pid.t for elem in p.elements]).mean()
            p.E = np.array([elem.mid().e for elem in p.elements]).mean()
            p.G = np.array([elem.mid().g for elem in p.elements]).mean()
            p.nu = np.array([elem.mid().nu for elem in p.elements]).mean()


            vonMises = False
            if vonMises:
                #FIXME remove repeated
                # Von Mises Constraints
                dvar = DESVAR('panelT', 1., 0.7, 5.)
                dvprel1 = DVPREL1('PSHELL', p.pid, 'T', [dvar.id], [1.])
                opt.dvars[dvar.id] = dvar
                opt.dvprel1s[dvprel1.id] = dvprel1
                opt.constrain_pshell(1, p.pid, 'CQUAD4', 'STRESS',
                    ['von Mises Z1', 'von Mises Z2'], -30., 40.)

        opt.set_output_file('optcard.bdf')
        opt.print_model()


