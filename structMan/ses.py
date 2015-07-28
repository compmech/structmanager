from operator import itemgetter

import numpy as np


class SE(object):
    def __init__(self, name, *eids):
        self.name = name
        self.eids = eids
        self.model = None
        self.forces = None

    def __str__(self):
        return (('%s: ' % self.__class__.__name__)  + self.name +
                ', Elements: ' + ', '.join(map(str, self.eids)))

    def __repr__(self):
        return str(self)


class SE1D(SE):
    def __init__(self, name, *eids):
        super(SE1D, self).__init__(name, *eids)
        # internal forces
        self.bendingMomentA_plane1 = None
        self.bendingMomentA_plane2 = None
        self.bendingMomentB_plane1 = None
        self.bendingMomentB_plane2 = None
        self.shear_plane1 = None
        self.shear_plane2 = None
        self.axial = None
        self.torque = None

    def read_forces(self):
        if self.model.op2 is None:
            print('No op2 file defined for Panel.model')
        # LINEAR ELEMENTS
        # CBAR

        #TODO try to fix op2.subcases and submit a pull request
        subcases = self.model.op2.subcases
        #
        num_subcases = len(subcases)
        forces = self.model.op2.cbar_force
        force1 = forces[subcases[0]]
        num_vectors = 8
        elements = np.sort(force1.axial.keys())

        self.forces = np.zeros((num_vectors, len(self.eids), num_subcases))

        getter = itemgetter(*self.eids)

        for i, subcase in enumerate(subcases):
            data = forces[subcase]
            # Bending End A plane 1 and plane 2
            tmp = getter(data.bendingMomentA)
            print tmp
            self.forces[0, :, i], self.forces[1, :, i] = zip(*tmp)
            # Bending End B plane 1 and plane 2
            tmp = getter(data.bendingMomentB)
            self.forces[2, :, i], self.forces[3, :, i] = zip(*tmp)
            # Shear plane 1 and plane 2
            tmp = getter(data.shear)
            self.forces[4, :, i], self.forces[5, :, i] = zip(*tmp)
            # Axial force
            self.forces[6, :, i] = getter(data.axial)
            # Torque
            self.forces[7, :, i] = getter(data.torque)

        self.bendingMomentA_plane1 = self.forces[0]
        self.bendingMomentA_plane2 = self.forces[1]
        self.bendingMomentB_plane1 = self.forces[2]
        self.bendingMomentB_plane2 = self.forces[3]
        self.shear_plane1 = self.forces[4]
        self.shear_plane2 = self.forces[5]
        self.axial = self.forces[6]
        self.torque = self.forces[7]


class SE2D(SE):
    def __init__(self, name, *eids):
        super(SE2D, self).__init__(name, *eids)
        # internal forces
        self.mx = None
        self.my = None
        self.mxy = None
        self.bmx = None
        self.bmy = None
        self.bmxy = None
        self.tx = None
        self.ty = None

    def read_forces(self):
        if self.model.op2 is None:
            print('No op2 file defined for Panel.model')
        #TODO try to fix op2.subcases and submit a pull request
        subcases = self.model.op2.subcases
        #
        num_subcases = len(subcases)
        forces = self.model.op2.cquad4_force
        force1 = forces[subcases[0]]
        num_vectors = force1.data.shape[2]

        self.forces = np.zeros((num_vectors, len(self.eids), num_subcases))

        # LINEAR ELEMENTS
        # CQUAD4
        i_op2 = np.in1d(force1.element, self.eids)
        i_panel = np.in1d(self.eids, force1.element)

        for i, subcase in enumerate(subcases):
            data = forces[subcase].data
            self.forces[:, i_panel, i] = data[-1, i_op2, :].swapaxes(-1, -2)

        # CTRIA3
        forces = self.model.op2.ctria3_force
        force1 = forces[subcases[0]]
        i_op2 = np.in1d(force1.element, self.eids)
        i_panel = np.in1d(self.eids, force1.element)

        for i, subcase in enumerate(subcases):
            data = forces[subcase].data
            self.forces[:, i_panel, i] = data[-1, i_op2, :].swapaxes(-1, -2)

        self.mx = self.forces[0]
        self.my = self.forces[1]
        self.mxy = self.forces[2]
        self.bmx = self.forces[3]
        self.bmy = self.forces[4]
        self.bmxy = self.forces[5]
        self.tx = self.forces[6]
        self.ty = self.forces[7]


class Panel(SE2D):
    """Panel"""
    idDESVAR = 1000000
    idDVPREL = 1000000
    idDCONSTR = 1000000
    idDRESP = 1000000
    def __init__(self, name, *eids):
        super(Panel, self).__init__(name, *eids)
        self.radius1 = None
        self.radius2 = None
        self.width = None
        self.length = None
        self.thickness = None
        self.xaxis = 'stringer'
        self.model = None
        # parameters related to optimization
        self.dvars = []


class InnerFlange(SE1D):
    idDESVAR = 2100000
    idDVPREL = 2100000
    idDCONSTR = 2100000
    idDRESP = 2100000
    def __init__(self, name, *eids):
        super(InnerFlange, self).__init__(name, *eids)


class Web(SE2D):
    idDESVAR = 2200000
    idDVPREL = 2200000
    idDCONSTR = 2200000
    idDRESP = 2200000
    def __init__(self, name, *eids):
        super(Web, self).__init__(name, *eids)


class OuterFlange(SE1D):
    idDESVAR = 2300000
    idDVPREL = 2300000
    idDCONSTR = 2300000
    idDRESP = 2300000
    def __init__(self, name, *eids):
        super(OuterFlange, self).__init__(name, *eids)


class ShearClipFrame(SE2D):
    """Shear Clip Attachment to Frame"""
    idDESVAR = 2400000
    idDVPREL = 2400000
    idDCONSTR = 2400000
    idDRESP = 2400000
    def __init__(self, name, *eids):
        super(ShearClipFrame, self).__init__(name, *eids)


class ShearClipSkin(SE1D):
    """Shear Clip Attachment to Skin"""
    idDESVAR = 2500000
    idDVPREL = 2500000
    idDCONSTR = 2500000
    idDRESP = 2500000
    def __init__(self, name, *eids):
        super(ShearClipSkin, self).__init__(name, *eids)


class Stringer(SE1D):
    """Stringer"""
    idDESVAR = 3000000
    idDVPREL = 3000000
    idDCONSTR = 3000000
    idDRESP = 3000000
    def __init__(self, name, *eids):
        super(Stringer, self).__init__(name, *eids)

