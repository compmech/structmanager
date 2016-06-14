from operator import itemgetter

import numpy as np


class Forces2D(object):
    """Store forces for a 1D structural element

    TODO add explanations about each force vector

    """
    def __init__(self, forces):
        self.forces = forces
        self.mx = forces[0]
        self.my = forces[1]
        self.mxy = forces[2]
        self.bmx = forces[3]
        self.bmy = forces[4]
        self.bmxy = forces[5]
        self.tx = forces[6]
        self.ty = forces[7]


def read_forces_2d(op2, se):
    """Read forces for a 1D structural element

    Parameters
    ----------

    op2 : PyNastran's OP2 results
        OP2 result class from PyNastran.
    se : :class:`.SE` object
        The structural element for which the forces should be read.

    """
    #FIXME try to fix op2.subcases and submit a pull request
    subcases = sorted(op2.subcase_key.keys())
    num_subcases = len(subcases)

    se_forces = None

    # LINEAR ELEMENTS

    # CQUAD4
    forces = op2.cquad4_force
    values = forces.values()
    if len(values) > 0:
        force1 = values[0]
        if se_forces is None:
            num_vectors = force1.data.shape[2]
            se_forces = np.zeros((num_vectors, len(se.eids), num_subcases))

        i_op2 = np.in1d(force1.element, se.eids)
        i_panel = np.in1d(se.eids, force1.element)

        for i, force in enumerate(forces.values()):
            se_forces[:, i_panel, i] = force.data[-1, i_op2, :].swapaxes(-1, -2)

    # CTRIA3
    forces = op2.ctria3_force
    values = forces.values()
    if len(values) > 0:
        force1 = forces.values()[0]

        if se_forces is None:
            num_vectors = force1.data.shape[2]
            se_forces = np.zeros((num_vectors, len(se.eids), num_subcases))

        i_op2 = np.in1d(force1.element, se.eids)
        i_panel = np.in1d(se.eids, force1.element)

        for i, force in enumerate(forces.values()):
            se_forces[:, i_panel, i] = data[-1, i_op2, :].swapaxes(-1, -2)

    return Forces2D(se_forces)


def read_forces_2d_hdf5():
    try:
        import tables
    except ImportError:
        raise ImportError('Python "tables" module required')
    except:
        raise RuntimeError
    r = tables.read_file(op2path)

    test_eids = [1508952, 1508978, 1508979, 1508980, 1508981, 1508982, 1509014,
            1509042, 1509043, 1509044, 1509045, 1509046, 1509088, 1509116,
            1509117, 1509118, 1509119, 1509120, 1509162, 1509179, 1509180,
            1509181, 1509182, 1509183, 1509254, 1509275, 1509276, 1509277,
            1509278, 1509279, 1515843, 1515844, 1515890, 1515891, 1515892]

    getter = itemgetter(test_eids)
    order = ['EID', 'MX', 'MY', 'MXY', 'BMX', 'BMY', 'BMXY', 'TX', 'TY',
            'DOMAIN_ID']

