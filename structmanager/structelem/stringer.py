"""
Stringer (:mod:`structmanager.structelem.stringer`)
================================================

.. currentmodule:: structmanager.structelem.stringer

"""
import numpy as np

from base import SE1D


class Stringer(SE1D):
    """Stringer

    Each cross-section (profile) dimension is defined according do the PBARL
    entry of Nastran's Quick Reference Guide.

    Attributes
    ----------

    profile (`str`)
        - `Z_t` - Z section defined with one variable:
            - `t` (variable): profile thickness
            - `b` (constant): flange width
            - `h` (constant): height

        - `Z_t_b` - Z section defined with two variables:
            - `t` (variable): profile thickness
            - `b` (variable): flange width
            - `h` (constant): height

        - `Z_t_b_h` - Z section defined with three variables:
            - `t` (variable): profile thickness
            - `b` (variable): flange width
            - `h` (variable): height

        - `Z_tf_tw_b_h` - Z section defined with four variables:
            - `tf` (variable): flange thickness
            - `tw` (variable): web thickness
            - `b` (variable): flange width
            - `h` (variable): height

        - `B_t` - Blade section defined with one variable:
            - `t` (variable): thickness
            - `h` (constant): height
            - `L` (constant): length

        - `B_t_h` - Blade section defined with two variables:
            - `t` (variable): thickness
            - `h` (variable): height
            - `L` (constant): length

        The stringer's attributes will vary from one `profile` to another.

    """
    def __init__(self, name, *eids):
        super(Stringer, self).__init__(name, *eids)
        self.profile = 'B_t'
        # optimization constraints
        self.all_constraints += ['buckling']
        self.constraints['buckling'] = 1

        if self.elements is not None:
            # reading L from FE data
            # - taking the distance between the two farthest nodes
            nodes = []
            for element in self.elements:
                for node in element.nodes:
                    nodes.append(node)
            self.nodes = set(nodes)
            ccoords = np.array([n.xyz for n in self.nodes])
            xs = ccoords[:, 0]
            ys = ccoords[:, 1]
            zs = ccoords[:, 2]
            #TODO use scipy.spatial.distance.pdist instead
            dist = np.subtract.outer(xs, xs)**2
            dist += np.subtract.outer(ys, ys)**2
            dist += np.subtract.outer(zs, zs)**2
            dist **= 0.5
            self.L = dist.max()

