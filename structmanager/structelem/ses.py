"""
Base classes for SEs (:mod:`structmanager.structelem.ses`)
===================================================================

.. currentmodule:: structmanager.structelem.ses

"""
from operator import itemgetter

import numpy as np


class MaterialIsotropic(object):
    def __init__(self, E, nu):
        self.E = E
        self.nu = nu

class MaterialOrthotropic(object):
    def __init__(self, E1, E2, nu12, G12, G13, G23):
        self.E1 = E1
        self.E2 = E2
        self.nu12 = nu12
        self.G12 = G12
        self.G13 = G13
        self.G23 = G23


class SE(object):
    """Structural Element Base-Class

    Attributes
    ----------
    name : str
        The name of the structural element.
    eids : list
        A list containing the elements belonging to this structural element.
    model : :class:`.Model`
        The model containing this SE.

    """
    def __init__(self, name, eids, model):
        self.name = name

        # material properties
        self.material = None

        # optimization parameters
        self.dvars_created = False
        self.dresps = []
        self.dvars = {}
        self.dvprels = []
        self.deqatns = []
        self.dtables = {}
        self.dlinks = []
        self.dconstrs = []
        # outputs
        self.forces = None

        # information from FE model
        self.eids = eids
        self.model = model
        self.ptype = None
        self.mtype = None
        self.pid = None

        # retrieving information from FE model
        bdf = None
        if model is not None:
            if model.nastranmodel is not None:
                if model.nastranmodel.bdf is not None:
                    bdf = model.nastranmodel.bdf
        if bdf is not None:
            self.elements = [bdf.elements[eid] for eid in eids]
            refel = self.elements[0]
            self.ptype = refel.pid.type
            self.pid = refel.Pid()
            if self.ptype == 'PSHELL':
                mat = bdf.materials[refel.pid.Mid()]
            if self.ptype == 'PBAR':
                mat = bdf.materials[refel.pid.Mid()]
            if self.ptype == 'PBARL':
                mat = bdf.materials[refel.pid.Mid()]
            if self.ptype == 'PCOMP':
                mat = bdf.materials[refel.pid.Mid(0)]
            self.mtype = mat.type
            if self.mtype == 'MAT1':
                if mat.g is None and mat.nu is None:
                    raise ValueError('Invalid Material')
                if mat.g is None:
                    mat.nu = mat.nu
                    mat.g = mat.e/(2.*(1. + mat.nu))
                if mat.nu is None:
                    mat.g = mat.g
                    mat.nu = mat.e/(2.*mat.g) - 1.
                if None in [mat.e, mat.g, mat.nu]:
                    raise ValueError('Invalid Material')
                self.material = MaterialIsotropic(mat.e, mat.nu)
            elif self.mtype == 'MAT8':
                if mat.e11 is None:
                    raise ValueError('Invalid Material')
                if mat.e22 is None:
                    raise ValueError('Invalid Material')
                if mat.g12 is None:
                    raise ValueError('Invalid Material')
                if mat.nu12 is None:
                    raise ValueError('Invalid Material')
                if None in [mat.e11, mat.e22, mat.g12, mat.nu12]:
                    raise ValueError('Invalid Material')
                self.material = MaterialOrthotropic(mat.e11, mat.e22, mat.nu12,
                        mat.g12, mat.g13, mat.g23)
            else:
                raise NotImplementedError('%s not supported!' % self.mtype)
        else:
            self.elements = None


    def __str__(self):
        return (('%s: ' % self.__class__.__name__)  + self.name +
                ', Elements: ' + ', '.join(map(str, self.eids)))


    def __repr__(self):
        return str(self)


    def get_central_element(self):
        """Return the element closest to the SE center of gravity

        """
        if self.elements is None:
            return
        x = np.array([e.get_node_positions().mean(axis=0) for e in
            self.elements])
        cg = x.mean(axis=0)
        return self.elements[np.argmin(((x-cg)**2).sum(axis=1))]


class SE1D(SE):
    """Base class for all 1D Structural Elements

    """
    def __init__(self, name, eids, model):
        super(SE1D, self).__init__(name, eids, model)


class SE2D(SE):
    """Base class for all 2D Structural Elements

    """
    def __init__(self, name, eids, model):
        super(SE2D, self).__init__(name, eids, model)


class ShearClipFrame(SE2D):
    """Shear Clip Attachment to Frame

    """
    def __init__(self, name, eids, model=None):
        super(ShearClipFrame, self).__init__(name, eids, model)


class ShearClipSkin(SE1D):
    """Shear Clip Attachment to Skin

    """
    def __init__(self, name, eids, model=None):
        super(ShearClipSkin, self).__init__(name, eids, model)

