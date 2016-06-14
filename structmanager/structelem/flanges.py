"""
Ring frame flanges (:mod:`structmanager.ses.flanges`)
=====================================================

.. currentmodule:: structmanager.ses.flanges

"""
import numpy as np

from ses import SE1D


class Flange1D(SE1D):
    """Flange1D base class for :class:`.InnerFlange` and :class:`.OuterFlange`

    .. autoattribute:: Flange1D.profile

    """
    ##L (`float`) - flange length
    def __init__(self, name, eids, model):
        super(Flange1D, self).__init__(name, eids, model)

        self.profile = 't'

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
            #xs = ccoords[:, 0]
            ys = ccoords[:, 1]
            zs = ccoords[:, 2]
            thetas = np.arctan2(zs, ys)
            rs = (ys**2 + zs**2)**0.5
            self.L = (thetas.max() - thetas.min())*rs.mean()


class InnerFlange(Flange1D):
    """Inner Flange

    It is assumed a rectangular section for the inner flange with two
    parameters `t` (thickness) and `b` (width).

    Attributes
    ----------

    profile (`str`)
        - `t` - defined with one variable:
            - `t` (variable): thickness
            - `b` (constant): width

        - `t_b` - defined with two variables:
            - `t` (variable): thickness
            - `b` (variable): width

        The InnerFlange's attributes will vary from one `profile` to another.

    """
    def __init__(self, name, eids, model=None):
        super(InnerFlange, self).__init__(name, eids, model)


class OuterFlange(Flange1D):
    """Outer Flange

    It is assumed a rectangular section for the outer flange with two
    parameters `t` (thickness) and `b` (width).

    Attributes
    ----------

    profile (`str`)
        - `t` - defined with one variable:
            - `t` (variable): thickness
            - `b` (constant): width

        - `t_b` - defined with two variables:
            - `t` (variable): thickness
            - `b` (variable): width

        The OuterFlange's attributes will vary from one `profile` to another.

    """
    def __init__(self, name, eids, model=None):
        super(OuterFlange, self).__init__(name, eids, model)


