"""
Nastran's Output codes (:mod:`atd.sol200.output_codes`)
=======================================================

.. currentmodule:: atd.sol200.output_codes

"""
OUTC = {}
# STRESS output codes
# ===================
stress = OUTC['STRESS'] = {}

# element CBAR (34)
cbar = stress['CBAR'] = stress[34] = {}
cbar['End A-Point C'] = 2
cbar['End A-Point D'] = 3
cbar['End A-Point E'] = 4
cbar['End A-Point F'] = 5
cbar['Axial'] = 6
cbar['End A maximum'] = 7
cbar['End A minimum'] = 8
cbar['Safety margin in tension'] = 9
cbar['End B-Point C'] = 10
cbar['End B-Point D'] = 11
cbar['End B-Point E'] = 12
cbar['End B-Point F'] = 13
cbar['End B maximum'] = 14
cbar['End B minimum'] = 15
cbar['Safety margin in compression'] = 16

# element CBEAM (2)
cbeam = stress['CBEAM'] = stress[2] = {}
cbeam['End A-External grid point ID'] = 2
cbeam['End A-Station distance/length'] = 3
cbeam['End A-Long. Stress at Point C'] = 4
cbeam['End A-Long. Stress at Point D'] = 5
cbeam['End A-Long. Stress at Point E'] = 6
cbeam['End A-Long. Stress at Point F'] = 7
cbeam['End A-Maximum stress'] = 8
cbeam['End A-Minimum stress'] = 9
cbeam['End A-Safety margin in tension'] = 10
cbeam['End A-Safety margin in compression'] = 11
cbeam['End B-External grid point ID'] = 12
cbeam['End B-Station distance/length'] = 13
cbeam['End B-Long. Stress at Point C'] = 14
cbeam['End B-Long. Stress at Point D'] = 15
cbeam['End B-Long. Stress at Point E'] = 16
cbeam['End B-Long. Stress at Point F'] = 17
cbeam['End B-Maximum stress'] = 18
cbeam['End B-Minimum stress'] = 19
cbeam['End B-Safety margin in tension'] = 20
cbeam['End B-Safety margin in compression'] = 21

# element CBEAM (94)
cbeamNL = stress['CBEAM_NL'] = stress[94] = {}
cbeamNL['End A-External grid point ID'] = 2

cbeamNL['End A-C (Character)'] = 3
cbeamNL['End A-Long. Stress at point C'] = 4
cbeamNL['End A-Equivalent stress at point C'] = 5
cbeamNL['End A-Total strain at point C'] = 6
cbeamNL['End A-Effective plastic strain at point C'] = 7
cbeamNL['End A-Effective creep strain at point C'] = 8

cbeamNL['End A-D (Character)'] = 9
cbeamNL['End A-Long. Stress at point D'] = 10
cbeamNL['End A-Equivalent stress at point D'] = 11
cbeamNL['End A-Total strain at point D'] = 12
cbeamNL['End A-Effective plastic strain at point D'] = 13
cbeamNL['End A-Effective creep strain at point D'] = 14

cbeamNL['End A-E (Character)'] = 15
cbeamNL['End A-Long. Stress at point E'] = 16
cbeamNL['End A-Equivalent stress at point E'] = 17
cbeamNL['End A-Total strain at point E'] = 18
cbeamNL['End A-Effective plastic strain at point E'] = 19
cbeamNL['End A-Effective creep strain at point E'] = 20

cbeamNL['End A-F (Character)'] = 21
cbeamNL['End A-Long. Stress at point F'] = 22
cbeamNL['End A-Equivalent stress at point F'] = 23
cbeamNL['End A-Total strain at point F'] = 24
cbeamNL['End A-Effective plastic strain at point F'] = 25
cbeamNL['End A-Effective creep strain at point F'] = 26

cbeamNL['End B-C (Character)'] = 27
cbeamNL['End B-Long. Stress at point C'] = 28
cbeamNL['End B-Equivalent stress at point C'] = 29
cbeamNL['End B-Total strain at point C'] = 30
cbeamNL['End B-Effective plastic strain at point C'] = 31
cbeamNL['End B-Effective creep strain at point C'] = 32

cbeamNL['End B-D (Character)'] = 33
cbeamNL['End B-Long. Stress at point D'] = 34
cbeamNL['End B-Equivalent stress at point D'] = 35
cbeamNL['End B-Total strain at point D'] = 36
cbeamNL['End B-Effective plastic strain at point D'] = 37
cbeamNL['End B-Effective creep strain at point D'] = 38

cbeamNL['End B-E (Character)'] = 39
cbeamNL['End B-Long. Stress at point E'] = 40
cbeamNL['End B-Equivalent stress at point E'] = 41
cbeamNL['End B-Total strain at point E'] = 42
cbeamNL['End B-Effective plastic strain at point E'] = 43
cbeamNL['End B-Effective creep strain at point E'] = 44

cbeamNL['End B-F (Character)'] = 45
cbeamNL['End B-Long. Stress at point F'] = 46
cbeamNL['End B-Equivalent stress at point F'] = 47
cbeamNL['End B-Total strain at point F'] = 48
cbeamNL['End B-Effective plastic strain at point F'] = 49
cbeamNL['End B-Effective creep strain at point F'] = 50

# element CQUAD4 (33)
cquad4 = stress['CQUAD4'] = stress[33] = {}
cquad4['z1=Fiber distance 1'] = 2
cquad4['Normal x at Z1'] = 3
cquad4['Normal y at Z1'] = 4
cquad4['Shear xy at Z1'] = 5
cquad4['Shear angle at Z1'] = 6
cquad4['Major principal at Z1'] = 7
cquad4['Minor principal at Z1'] = 8
cquad4['von Mises or maximum shear at Z1'] = 9

cquad4['z2=Fiber distance 2'] = 10
cquad4['Normal x at Z2'] = 11
cquad4['Normal y at Z2'] = 12
cquad4['Shear xy at Z2'] = 13
cquad4['Shear angle at Z2'] = 14
cquad4['Major principal at Z2'] = 15
cquad4['Minor principal at Z2'] = 16
cquad4['von Mises or maximum shear at Z2'] = 17

# element CQUAD4_NL (90)k
cquad4NL = stress['CQUAD4_NL'] = stress[90] = {}
cquad4NL['Z1=Fiber distance 1 (plane stress only)'] = 2
cquad4NL['Stress-X (at Z1, if plane stress)'] = 3
cquad4NL['Stress-Y (at Z1, if plane stress)'] = 4
cquad4NL['Stress-Z (plane strain only)'] = 5
cquad4NL['Stress-XY (at Z1, if plane stress)'] = 6
cquad4NL['Equivalent stress (at Z1, if plane stress)'] = 7
cquad4NL['Plastic strain (at Z1, if plane stress)'] = 8
cquad4NL['Creep strain (at Z1, if plane stress)'] = 9
cquad4NL['Strain-X (at Z1, if plane stress)'] = 10
cquad4NL['Strain-Y (at Z1, if plane stress)'] = 11
cquad4NL['Strain-Z (plane strain only)'] = 12
cquad4NL['Strain-XY (at Z1, if plane stress)'] = 13

cquad4NL['Z2=Fiber distance 1 (plane stress only)'] = 14
cquad4NL['Stress-X (at Z2, if plane stress)'] = 15
cquad4NL['Stress-Y (at Z2, if plane stress)'] = 16
cquad4NL['Stress-Z (plane strain only)'] = 17
cquad4NL['Stress-XY (at Z2, if plane stress)'] = 18
cquad4NL['Equivalent stress (at Z2, if plane stress)'] = 19
cquad4NL['Plastic strain (at Z2, if plane stress)'] = 20
cquad4NL['Creep strain (at Z2, if plane stress)'] = 21
cquad4NL['Strain-X (at Z2, if plane stress)'] = 22
cquad4NL['Strain-Y (at Z2, if plane stress)'] = 23
cquad4NL['Strain-Z (plane strain only)'] = 24
cquad4NL['Strain-XY (at Z2, if plane stress)'] = 25

# element CTRIA3 (74)
stress['CTRIA3'] = stress[74] = stress[33]

# element CTRIA3_NL (88)
stress['CTRIA3_NL'] = stress[88] = stress[90]


# FORCE output codes
# ==================
force = OUTC['FORCE'] = {}

# element CBAR (34)
cbar = force['CBAR'] = force[34] = {}
cbar['Bending End A plane 1'] = 2
cbar['Bending End A plane 2'] = 3
cbar['Bending End B plane 1'] = 4
cbar['Bending End B plane 2'] = 5
cbar['Shear plane 1'] = 6
cbar['Shear plane 2'] = 7
cbar['Axial force'] = 8
cbar['Torque'] = 9

# element CBEAM (2)
cbeam = force['CBEAM'] = force[2] = {}
cbeam['End A-External grid point ID'] = 2
cbeam['End A-Station distance/length'] = 3
cbeam['End A-Bending moment plane 1'] = 4
cbeam['End A-Bending moment plane 2'] = 5
cbeam['End A-Web shear plane 1'] = 6
cbeam['End A-Web shear plane 2'] = 7
cbeam['End A-Axial force'] = 8
cbeam['End A-Total torque'] = 9
cbeam['End A-Warping torque'] = 10

cbeam['End B-External grid point ID'] = 11
cbeam['End B-Station distance/length'] = 12
cbeam['End B-Bending moment plane 1'] = 13
cbeam['End B-Bending moment plane 2'] = 14
cbeam['End B-Web shear plane 1'] = 15
cbeam['End B-Web shear plane 2'] = 16
cbeam['End B-Axial force'] = 17
cbeam['End B-Total torque'] = 18
cbeam['End B-Warping torque'] = 19

# element CBUSH (102)
cbush = force['CBUSH'] = force[102] = {}
cbush['Force-x'] = 2
cbush['Force-y'] = 3
cbush['Force-z'] = 4
cbush['Moment-x'] = 5
cbush['Moment-y'] = 6
cbush['Moment-z'] = 7

# element CELAS1 (11)
celas1 = force['CELAS1'] = force[11] = {}
celas1['Force 1'] = 2
celas1['Force 2'] = 3

# element CELAS2 (12)
force['CELAS2'] = force[12] = force[11]

# element CELAS3 (13)
force['CELAS3'] = force[13] = force[11]

# element CELAS4 (14)
force['CELAS4'] = force[14] = force[11]

# element CQUAD4 (33)
cquad4 = force['CQUAD4'] = force[33] = {}
cquad4['Membrane force x'] = 2
cquad4['Membrane force y'] = 3
cquad4['Membrane force xy'] = 4
cquad4['Bending moment x'] = 5
cquad4['Bending moment y'] = 6
cquad4['Bending moment xy'] = 7
cquad4['Shear x'] = 8
cquad4['Shear y'] = 9

# element CQUAD4_comp (95)
cquad4COMP = force['CQUAD4_comp'] = force[95] = {}
cquad4COMP['Theory or blank 1'] = 2
cquad4COMP['Theory or blank 2'] = 3
cquad4COMP['Lamina number'] = 4
cquad4COMP['FP (failure index) / SP (strength ratio) for direct stresses'] = 5
cquad4COMP['Failure mode for Maximum strain theory'] = 6
cquad4COMP['FB (failure index) / ' +
           'SP (strength ratio) or ' +
           '-1 for interlaminar shear-stress'] = 7
cquad4COMP['MAX of FP, FB or -1 or MIN of SP, SB or -1'] = 8
cquad4COMP['Failure flag'] = 9

# element CTRIA3 (74)
force['CTRIA3'] = force[74] = force[33]

# element CTRIA3_comp (97)
force['CTRIA3_comp'] = force[97] = force[95]

def get_output_code(rtype, eltype, name):
    el = OUTC[rtype][eltype]
    comps = name.split()
    for k in el.keys():
        check = 0
        for comp in comps:
            if comp in k:
                check += 1
        if check == len(comps):
            return el[k]
    print comps
    raise ValueError('Matching output code not found')


