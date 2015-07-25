class InnerFlange(object):
    def __init__(self, name, *eids):
        self.name = name
        self.eids = eids

    def __str__(self):
        return ('InnerFlange: ' + self.name +
                ', Elements: ' + ', '.join(map(str, self.eids)))

    def __repr__(self):
        return str(self)


class Web(object):
    def __init__(self, name, *eids):
        self.name = name
        self.eids = eids

    def __str__(self):
        return ('Web: ' + self.name +
                ', Elements: ' + ', '.join(map(str, self.eids)))

    def __repr__(self):
        return str(self)


class OuterFlange(object):
    def __init__(self, name, *eids):
        self.name = name
        self.eids = eids

    def __str__(self):
        return ('OuterFlange: ' + self.name +
                ', Elements: ' + ', '.join(map(str, self.eids)))

    def __repr__(self):
        return str(self)


class ShearClipSkin(object):
    """Shear Clip Attachment to Skin"""
    def __init__(self, name, *eids):
        self.name = name
        self.eids = eids

    def __str__(self):
        return ('Shear Clip Attachment to Skin: ' + self.name +
                ', Elements: ' + ', '.join(map(str, self.eids)))

    def __repr__(self):
        return str(self)


class ShearClipFrame(object):
    """Shear Clip Attachment to Frame"""
    def __init__(self, name, *eids):
        self.name = name
        self.eids = eids

    def __str__(self):
        return ('Shear Clip Attachment to Frame: ' + self.name +
                ', Elements: ' + ', '.join(map(str, self.eids)))

    def __repr__(self):
        return str(self)


class Stringer(object):
    """Stringer"""
    def __init__(self, name, *eids):
        self.name = name
        self.eids = eids

    def __str__(self):
        return ('Stringer: ' + self.name +
                ', Elements: ' + ', '.join(map(str, self.eids)))

    def __repr__(self):
        return str(self)


class Panel(object):
    """Panel"""
    def __init__(self, name, *eids):
        self.name = name
        self.eids = eids
        self.radius1 = None
        self.radius2 = None
        self.width = None
        self.length = None
        self.thickness = None
        self.xaxis = 'stringer'
        self.corners = None
        self.model = None
        self.dvars = []

    def __str__(self):
        return ('Panel: ' + self.name +
                ', Elements: ' + ', '.join(map(str, self.eids)))

    def __repr__(self):
        return str(self)

