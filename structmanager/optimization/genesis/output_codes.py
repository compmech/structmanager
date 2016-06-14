"""
Output codes (:mod:`feopt.genesis.output_codes`)
================================================

.. currentmodule:: feopt.genesis.output_codes

Maps the output codes used in GENESIS in a ``dict`` named ``OUTC``, accessed
throught::

    from output_codes import OUTC

"""
OUTC={} # OUTC ==> output_code
OUTC['DISP'] = {}
OUTC['DISP'][1]  = 'Translation X'
OUTC['DISP'][2]  = 'Translation Y'
OUTC['DISP'][3]  = 'Translation Z'
OUTC['DISP'][4]  = 'Rotation X'
OUTC['DISP'][5]  = 'Rotation Y'
OUTC['DISP'][6]  = 'Rotation Z'
OUTC['DISP'][7]  = 'Translation Total'
OUTC['DISP'][8]  = 'Absolute X'
OUTC['DISP'][9]  = 'Absolute Y'
OUTC['DISP'][10] = 'Absolute Z'
for key in OUTC['DISP'].keys():
    OUTC['DISP'][OUTC['DISP'][key]] = key
OUTC['STRESS'] = {}
OUTC['STRESS']['SOLID'] = {}
OUTC['STRESS']['SOLID'][1] = 'Max shear Bottom'
OUTC['STRESS']['SOLID'][2] = 'von Mises Bottom'
OUTC['STRESS']['SOLID'][3] = 'Major Principal Bottom'
OUTC['STRESS']['SOLID'][4] = 'Minor Principal Bottom'
OUTC['STRESS']['SOLID'][5] = 'Normal X Bottom'
OUTC['STRESS']['SOLID'][6] = 'Normal Y Bottom'
OUTC['STRESS']['SOLID'][7] = 'Shear XY Bottom'
OUTC['STRESS']['SOLID'][8] = 'Max shear Top'
OUTC['STRESS']['SOLID'][9] = 'von Mises Top'
OUTC['STRESS']['SOLID'][10] = 'Major Principal Top'
OUTC['STRESS']['SOLID'][11] = 'Minor Principal Top'
OUTC['STRESS']['SOLID'][12] = 'Normal X Top'
OUTC['STRESS']['SOLID'][13] = 'Normal Y Top'
OUTC['STRESS']['SOLID'][14] = 'Shear XY Top'
for key in OUTC['STRESS']['SOLID'].keys():
    value = OUTC['STRESS']['SOLID'][key]
    OUTC['STRESS']['SOLID'][value] = key
OUTC['STRESS']['SQUARE'] = {}
OUTC['STRESS']['SQUARE'][1]  = 'Normal X Point 1 at end A'
OUTC['STRESS']['SQUARE'][2]  = 'Normal X Point 2 at end A'
OUTC['STRESS']['SQUARE'][3]  = 'Normal X Point 3 at end A'
OUTC['STRESS']['SQUARE'][4]  = 'Normal X Point 4 at end A'
OUTC['STRESS']['SQUARE'][5]  = 'Shear XZ Point 5 at end A'
OUTC['STRESS']['SQUARE'][6]  = 'Shear XY Point 6 at end A'
OUTC['STRESS']['SQUARE'][7]  = 'Shear XZ Point 7 at end A'
OUTC['STRESS']['SQUARE'][8]  = 'Shear XY Point 8 at end A'
OUTC['STRESS']['SQUARE'][9]  = 'Normal X Point 9 at end B'
OUTC['STRESS']['SQUARE'][10] = 'Normal X Point 10 at end B'
OUTC['STRESS']['SQUARE'][11] = 'Normal X Point 11 at end B'
OUTC['STRESS']['SQUARE'][12] = 'Normal X Point 12 at end B'
OUTC['STRESS']['SQUARE'][13] = 'Shear XZ Point 13 at end B'
OUTC['STRESS']['SQUARE'][14] = 'Shear XY Point 14 at end B'
OUTC['STRESS']['SQUARE'][15] = 'Shear XZ Point 15 at end B'
OUTC['STRESS']['SQUARE'][16] = 'Shear XY Point 16 at end B'
for key in OUTC['STRESS']['SQUARE'].keys():
    value = OUTC['STRESS']['SQUARE'][key]
    OUTC['STRESS']['SQUARE'][value] = key
OUTC['STRESS']['RECT'] = OUTC['STRESS']['SQUARE']
#        OUTC['FORCE'] = {}
#        OUTC['FORCE']['BAR'] = {}
#        OUTC['FORCE']['BAR'][1] = 'Axial force at end A'
#        OUTC['FORCE']['BAR'][2] = 'Shear in plane 1 at end A'
#        OUTC['FORCE']['BAR'][3] = 'Shear in plane 2 at end A'
#        OUTC['FORCE']['BAR'][4] = 'Torque at end A'
#        OUTC['FORCE']['BAR'][5] = 'Moment in plane 2 at end A'
#        OUTC['FORCE']['BAR'][6] = 'Moment in plane 1 at end A'
#        OUTC['FORCE']['BAR'][7] = 'Axial force at end B'
#        OUTC['FORCE']['BAR'][8] = 'Shear in plane 1 at end B'
#        OUTC['FORCE']['BAR'][9] = 'Shear in plane 2 at end B'
#        OUTC['FORCE']['BAR'][10] = 'Torque at end B'
#        OUTC['FORCE']['BAR'][11] = 'Moment in plane 2 at end B'
#        OUTC['FORCE']['BAR'][12] = 'Moment in plane 1 at end B'

def get_output_code(rtype, eltype, outstr):
    """Translate an output string into a code

    Parameters
    ----------
    rtype : str
        Response type.
    eltype : str
        Element type.
    outstr : str
        String corresponding to the desired output. Examples::

            'Normal X Point 4 at end A'
            'Moment in plane 1 at end B'

    Returns
    -------
    code : int
        The output code.

    """
    if type(outstr) is str:
        return OUTC[rtype][eltype][outstr]
    else:
        return outstr
