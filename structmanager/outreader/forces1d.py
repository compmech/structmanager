import numpy as np


class Forces1D(object):
    """Store forces for a 1D structural element

    TODO add explanations about each force vector

    """
    def __init__(self, forces):
        self.forces = forces
        self.bending_moment_a1 = forces[0]
        self.bending_moment_a2 = forces[1]
        self.bending_moment_b1 = forces[2]
        self.bending_moment_b2 = forces[3]
        self.shear1 = forces[4]
        self.shear2 = forces[5]
        self.axial = forces[6]
        self.torque = forces[7]


def read_forces_1d(op2, se):
    """Read forces for a 1D structural element

    Parameters
    ----------

    op2 : PyNastran's OP2 results
        OP2 result class from PyNastran.
    se : :class:`.SE` object
        The structural element for which the forces should be read.

    """
    # LINEAR ELEMENTS
    # CBAR
    subcases = op2.subcases
    num_subcases = len(subcases)
    forces = op2.cbar_force
    force1 = forces[subcases[0]]
    num_vectors = force1.data.shape[2]

    forces = np.zeros((num_vectors, len(se.eids), num_subcases))

    i_op2 = np.in1d(force1.element, se.eids)
    i_panel = np.in1d(se.eids, force1.element)

    for i, subcase in enumerate(subcases):
        data = forces[subcase].data
        forces[:, i_panel, i] = data[-1, i_op2, :].swapaxes(-1, -2)

    return Forces1D(forces)
