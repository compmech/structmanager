def format_float(x, size=8, lr='>'):
    """Format a float number

    Parameters
    ----------
    x : float
        The float number.
    size : int, optional
        Desired size of the output string.
    lr : str ('<' or '>')
        Indicates if it should be left or right aligned.

    Returns
    -------
    out : str
        The formatted string.

    """
    y = str(x)
    if '.' in y:
        has_floating_point = True
    else:
        has_floating_point = False
    if lr == '<':
        y = y.ljust(size)[:size]
    elif lr == '>':
        y = y.rjust(size)[:size]
    else:
        raise ValueError("`lr` must be '<' or '>'")
    if not '.' in y and has_floating_point:
        raise ValueError('Float %f does not fit in size = %d' % (x, size))
    return y

