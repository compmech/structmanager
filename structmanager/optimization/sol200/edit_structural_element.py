from opt_cards import DCONSTR

def add_dtable(se, key, value):
    """Add a DTABLE entry to the SE and the optmodel

    Parameters
    ----------
    key : str
        The DTABLE unique key. The algorithm automatically attempts to add
        a sufix to prevent repeated keys.
    value : float
        The value corresponding to `key`.

    Returns
    -------
    key : str
        The resulting key.

    """
    optmodel = se.model.optmodel
    origkey = key
    if key in optmodel.dtables.keys():
        if len(key) >= 8:
            raise ValueError('{0} is an already existing DTABLE entry!'.
                             format(key))
        if key in optmodel.dtable_prefixes:
            optmodel.dtable_prefixes[key] += 1
        else:
            optmodel.dtable_prefixes[key] = 0
        sufix = str(optmodel.dtable_prefixes[key])
        key = key + sufix.rjust(8 - len(key), '0')
        if len(key) > 8:
            raise ValueError('Use a smaller key')

    if origkey in se.dtables.keys():
        raise
    se.dtables[origkey] = [key, value]
    optmodel.dtables[key] = float(value)

    return key


def add_dresp(se, dresp):
    """Add a DRESP(123) entry to the SE and the optmodel

    Parameters
    ----------
    dresp : :class:`DRESP1`, :class:`DRESP2` or :class:`DRESP3`
        The response object.

    """
    se.dresps.append(dresp)
    se.model.optmodel.dresps[dresp.id] = dresp
    if isinstance(dresp, DRESP3):
        se.model.optmodel.groups.add(dresp.group)


def add_deqatn(se, deqatn):
    """Add a DEQATN entry to the SE and the optmodel

    Parameters
    ----------
    deqatn : :class:`DEQATN`
        The equation to be added.

    """
    se.deqatns.append(deqatn)
    se.model.optmodel.deqatns[deqatn.id] = deqatn


def add_dvar(se, dvar):
    """Add a DESVAR entry to the SE and the optmodel

    Parameters
    ----------
    dvar : :class:`DESVAR`
        Design variable object.

    """
    if dvar.label in se.dvars.keys():
        raise
    se.dvars[dvar.label] = dvar
    se.model.optmodel.dvars[dvar.id] = dvar


def add_dvprel(se, dvprel):
    """Add a DVPREL(12) entry to the SE and the optmodel

    Parameters
    ----------
    dvprel : :class:`DVPREL1` or :class:`DVPREL2`
        Design property-to-variable object.

    """
    se.dvprels.append(dvprel)
    se.model.optmodel.dvprels[dvprel.id] = dvprel


def add_constraint(se, dcid, dresp, lb, ub):
    """Add a DCONSTR entry to the SE and the optmodel

    Parameters
    ----------
    dcid : int
        Design constraint set id.
    dresp : :class:`DRESP1`, :class:`DRESP2` or :class:`DRESP3`
        The response object.
    lb : float or None
        Lower boundary for the constraint.
    ub : float or None
        Upper boundary for the constraint.

    """
    dconstr = DCONSTR(dcid, dresp.id, lb, ub)
    se.dconstrs.append(dconstr)
    se.model.optmodel.dconstrs[dconstr.id] = dconstr
