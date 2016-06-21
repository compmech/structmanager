def plate_buckling(panel, method=1, load_idealization='avg'):
    """Calculate Margin of Safety for Buckling

    Parameters
    ----------
    method : int, optional
        Select one of the following methods for buckling calculation:

        - `1` : Bruhn's method using Equation C9.4:

                - considers compressive (Nxx only) and shear loads
                - no plasticity correction has been implemented

    load_idealization : str, optional
        Load idealization scheme. Tells how the loads should be extracted
        from the finite elements belonging to the panel:

        - `'avg'` : average the load from all elements
        - `'critical'` : takes the minimum Nxx and maximum Nxy in module
        - `'min_MS'` : takes the minimum margin of safety
        - `'avg_MS'` : takes the average margin of safety

    Returns
    -------
    ms : array-like
        The margin of safety. The array shape will depend on the number of
        load cases read from the op2 file.

    """
    try:
        from structmanager.methods.metallic.panel import FScr_skin, FCcr_skin
    except:
        raise ImportError('Analysis methods not implemented')

    if panel.forces is None:
        raise RuntimeError('No output data found for Panel {0}'.format(panel.name))

    if method == 1:
        r = panel.r
        t = panel.t
        a = panel.a
        b = panel.b
        nu = panel.material.nu
        Ec = panel.material.Ec
        FCcr = FCcr_skin(a, b, t, r, Ec, nu)
        FScr = FScr_skin(a, b, t, r, Ec, nu)

        Nxx = panel.forces[0]
        Nxy = panel.forces[2]
        if load_idealization.lower() == 'avg':
            Nxx = Nxx.mean(axis=0)
            Nxy = Nxy.mean(axis=0)
        elif load_idealization.lower() == 'critical':
            Nxx = Nxx[np.argmin(Nxx, axis=0)]
            Nxy = Nxx[np.argmax(np.abs(Nxy), axis=0)]
        FC = Nxx/t
        FS = np.abs(Nxy/t)
        Rc = FC/FCcr
        Rs = FS/FScr

        ms = 2./(Rc + SQRT(Rc**2 + 4*Rs**2)) - 1.

        if load_idealization.lower() == 'min_MS':
            ms = ms.min(axis=0)
        elif load_idealization.lower() == 'avg_MS':
            ms = ms.mean(axis=0)

    else:
        raise ValueError('method = {0} not implemented!'.format(method))

    return ms
