"""
Panel SEs (:mod:`structmanager.ses.panel`)
==========================================

.. currentmodule:: structmanager.ses.panel

"""
import numpy as np

from ses import SE2D




class Panel(SE2D):
    """Panel

    This class should be used for cylindrical panels (i.e. fuselage panels).
    For plates please refer to :class:`.Plate`.

    For wing panels this class should also be adopted.

    Attributes
    ----------

    """
    def __init__(self, name, eids, model=None):
        super(Panel, self).__init__(name, eids, model)
        # geometric parameters
        self.r = None
        self.a = None
        self.b = None
        self.t = None
        self.t_lb = None
        self.t_ub = None
        # material properties
        # ...
        self.is_isotropic = True


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

            # retrieving panel thickness and material properties
            self.t = self.elements[0].pid.t
