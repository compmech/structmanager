from ..cards_opt import (DRESP1, DCONSTR, DEQATN, DRESP2, DRESP3, DESVAR,
        DVPREL1, DVPREL2)
import ..output_codes as output_codes_SOL200


def constrain_stress(self, Fy, average=False):
    """Add a stress constrain

    Parameters
    ----------
    Fy : float
        The stress threshold to be used in the constraint. The sign of
        `Fy` will determine whether this threshold if for tension or
        compression.
    average : bool, optional
        If False the central element is chosen, otherwise ...
        #TODO not implemented

    """
    self.create_dvars()
    eid = self.get_central_element().eid
    OUTC = output_codes_SOL200.OUTC

    eltype = self.elements[0].type

    if Fy > 0:
        dcid = self.constraints['stress_tension']
        if eltype == 'CBAR':
            atta = OUTC['STRESS']['CBAR']['End A maximum']
        else:
            raise NotImplementedError
        label = 'STRmaxS'
    else:
        dcid = self.constraints['stress_compression']
        if eltype == 'CBAR':
            atta = OUTC['STRESS']['CBAR']['End A minimum']
        else:
            raise NotImplementedError
        label = 'STRminS'

    dresp1 = DRESP1(label, 'STRESS', 'ELEM', None, atta=atta, attb=None,
                    atti=eid)
    self.add_dresp(dresp1)
    if Fy > 0:
        self.add_constraint(dcid, dresp1, None, Fy)
    else:
        self.add_constraint(dcid, dresp1, Fy, None)


def constrain_stress_tension(self, Fty, average=False):
    """Add a tension stress constraint

    Parameters
    ----------
    Fty : float
        The tension stress threshold to be used in the constraint.
    average : bool, optional
        If False the central element is chosen, otherwise ...
        #TODO not implemented
    """
    self.create_dvars()
    self.constrain_stress(Fy=abs(Fty), average=average)


def constrain_stress_compression(self, Fcy, average=False):
    """Add a compressive stress constraint

    Parameters
    ----------
    Fcy : float
        The compression stress threshold to be used in the constraint.
    average : bool, optional
        If False the central element is chosen, otherwise ...
        #TODO not implemented

    """
    self.create_dvars()
    self.constrain_stress(Fy=-abs(Fcy), average=average)
