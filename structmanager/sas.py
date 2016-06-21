"""
Structural Assemblies - SAs (:mod:`structmanager.sas`)
======================================================

.. currentmodule:: structmanager.sas

"""
class FrameAssembly(object):
    """Frame Assembly"""
    def __init__(self, name, args):
        args = outerflange, web, innerflange
        self.name = name
        self.outerflange = outerflange
        self.web = web
        self.innerflange = innerflange

    def __str__(self):
        return ('FrameAssembly: ' + self.name +
                '\n-' + str(self.outerflange) +
                '\n-' + str(self.web) +
                '\n-' + str(self.innerflange)
                )

    def __repr__(self):
        return str(self)


class FrameShearClipAssembly(object):
    """Frame Assembly with Shear Clip"""
    def __init__(self, name, args):
        shearclipskin, shearclipframe, outerflange, web, innerflange = args
        self.name = name
        self.shearclipskin = shearclipskin
        self.shearclipframe = shearclipframe
        self.outerflange = outerflange
        self.web = web
        self.innerflange = innerflange

    def __str__(self):
        return ('FrameShearClipAssembly: ' + self.name +
                '\n-' + str(self.shearclipskin) +
                '\n-' + str(self.shearclipframe) +
                '\n-' + str(self.outerflange) +
                '\n-' + str(self.web) +
                '\n-' + str(self.innerflange)
                )

    def __repr__(self):
        return str(self)


class StiffenedPanelAssembly(object):
    """Stiffened Panel Assembly"""
    def __init__(self, name, args):
        panel, fr1, fr2, str1, str2 = args
        self.name = name
        self.panel = panel
        self.fr1 = fr1
        self.fr2 = fr2
        self.str1 = str1
        self.str2 = str2

    def __str__(self):
        return ('Stiffened Panel Assembly: ' + self.name +
                '\n-' + str(self.panel) +
                '\n-' + str(self.fr1) +
                '\n-' + str(self.fr2) +
                '\n-' + str(self.str1) +
                '\n-' + str(self.str2))

    def __repr__(self):
        return str(self)

class StiffenedPanelCutout(object):
    """Stiffened Panel Cutout"""
    def __init__(self, name, args):
        panelcutout, str1, str2 = args
        self.name = name
        self.panelcutout = panelcutout
        self.str1 = str1
        self.str2 = str2

    def __str__(self):
        return ('Stiffened Panel Cutout: ' + self.name +
                '\n-' + str(self.panelcutout) +
                '\n-' + str(self.str1) +
                '\n-' + str(self.str2))

    def __repr__(self):
        return str(self)

sa_classes = [
        FrameAssembly,
        FrameShearClipAssembly,
        StiffenedPanelAssembly,
        StiffenedPanelCutout,
        ]

