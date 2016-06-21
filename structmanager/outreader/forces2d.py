from operator import itemgetter

import numpy as np
from pyNastran.op2.data_in_material_coord import get_eids_from_op2_vector


class Forces2D(object):
    """Store forces for a 1D structural element

    TODO add explanations about each force vector

    """
    def __init__(self, forces):
        self.forces = forces
        self.mx = dict((sub, force[..., 0]) for sub, force in forces.items())
        self.my = dict((sub, force[..., 1]) for sub, force in forces.items())
        self.mxy = dict((sub, force[..., 2]) for sub, force in forces.items())
        self.bmx = dict((sub, force[..., 3]) for sub, force in forces.items())
        self.bmy = dict((sub, force[..., 4]) for sub, force in forces.items())
        self.bmxy = dict((sub, force[..., 5]) for sub, force in forces.items())
        self.tx = dict((sub, force[..., 6]) for sub, force in forces.items())
        self.ty = dict((sub, force[..., 7]) for sub, force in forces.items())


def read_forces_2d(op2, se):
    """Read forces for a 1D structural element

    Parameters
    ----------

    op2 : PyNastran's OP2 results
        OP2 result class from PyNastran.
    se : :class:`.SE` object
        The structural element for which the forces should be read.

    """
    se_forces = {}

    for vecname in ['cquad4_force', 'ctria3_force']:
        vectors = getattr(op2, vecname)
        for subcase, vector in vectors.items():
            eids = get_eids_from_op2_vector(vector)
            check = np.in1d(eids, se.eids)
            se_forces[subcase] = vector.data[:, check]

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

