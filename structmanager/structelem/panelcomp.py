"""
Composite Panel (:mod:`structmanager.structelem.panelcomp`)
========================================================

.. currentmodule:: structmanager.structelem.panelcomp

"""
import numpy as np

from .base import SE2D


class PanelComp(SE2D):
    """Composite Panel

    This class should be used for cylindrical panels (i.e. fuselage panels).
    For plates please refer to :class:`.Plate`.

    For wing panels this class should also be adopted.

    Attributes
    ----------

    """
    def __init__(self, name, eids, model=None):
        super(PanelComp, self).__init__(name, eids, model) #change to super(PanelComp, self)?
        # geometric parameters
        self.r = None
        self.a = None
        self.b = None
        self.t = None
        self.t_lb = None
        self.t_ub = None
        self.p45 = None
        self.p45_lb = 0.1
        self.p45_ub = None
        self.p90 = 0.1
        # material properties
        # all material properties are got from FE model at ses.py

        self.is_isotropic = None #change to orthotropic?
        # optimization constraints
        self.all_constraints = ['vonMises', 'buckling']
        self.constraints = {'vonMises': 1,
                            'buckling': 1}

        # finding corner nodes
        # - assuming that they are those that share only one inner element
        # - radius calculated assuming the panel has a common center
        if self.elements is not None:
            nodes = []
            for element in self.elements:
                for node in element.nodes:
                    nodes.append(node)
            self.nodes = set(nodes)
            ccoords = np.array([n.xyz for n in self.nodes])
            xs = ccoords[:, 0]
            ys = ccoords[:, 1]
            zs = ccoords[:, 2]
            rs = (ys**2 + zs**2)**0.5
            thetas = np.arctan2(zs, ys)
            self.r = rs.mean()
            self.a = xs.max() - xs.min()
            self.b = (thetas.max() - thetas.min())*self.r

            # retrieving plies thicknesses from panel
            self.t0 = self.elements[0].pid.Thickness(0)
            self.t45 = self.elements[0].pid.Thickness(1) + self.elements[0].pid.Thickness(2)
            self.t90 = self.elements[0].pid.Thickness(3)
            self.t = self.t0 + self.t45 + self.t90

            # calculating the thickness ratio
            self.p45 = self.t45/self.t




