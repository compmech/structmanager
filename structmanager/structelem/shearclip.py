from base import SE1D, SE2D

class ShearClipWeb(SE2D):
    """Shear Clip Web attached to Frame

    """
    def __init__(self, name, eids, model=None):
        super(ShearClipWeb, self).__init__(name, eids, model)


class ShearClipFoot(SE1D):
    """Shear Clip Flange attached to Skin

    """
    def __init__(self, name, eids, model=None):
        super(ShearClipFoot, self).__init__(name, eids, model)

