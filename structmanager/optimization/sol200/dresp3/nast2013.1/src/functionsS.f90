!
! Diagonal tension functions for curved stiffened panels
! Written by Saullo Castro, April 2015
!
real*4 function cot(x)
    implicit none
    real*4 x
    cot = 1./tan(x)
end function

real*4 function fSScr_skin(a, b, t, r, Ec_skin, nu_skin)
    ! Curved skin shear buckling allowable
    ! as in Fig.C9.4 and C9.5 pgC9.5 of Bruhn 
    ! - written by Tam Ha, Feb. 2001
    ! - translated to fortran by Saullo Castro, April 2015
    implicit none

    real*4 a, b, t, r, Ec_skin, nu_skin, ks, Z, ratio
    real*4 ks_90_1, ks_30_1, ks_20_1, ks_15_1, ks_10_1
    real*4 ks_90_2, ks_30_2, ks_20_2, ks_15_2, ks_10_2
    real*4 ks_20, ks_15
    real*4 pi
    pi = atan(1.)*4

    ! Calculation for Stringer System (a >= b) as given in Fig.C9.4
    if (a >= b) then
        Z = (b**2 / (r * t)) * sqrt(1. - nu_skin**2)
        Z = min(max(Z, 1.), 1000.)
        ratio = a / b
        ratio = min(ratio, 9.)

        ! For (Z >= 1) .and. (Z <= 17.5) and Z > 17.5, resp., and ratio = 9.0
        ks_90_1 = -0.003397 * Z**3 + 0.07234 * Z**2 - 0.2661 * Z + 5.679
        ks_90_2 = 5.546D-13 * Z**5 - 0.000000001397 * Z**4 + 0.000001298 * Z**3 - 0.0005751 * Z**2 + 0.1733 * Z + 5.38
        ! For (Z >= 1) .and. (Z <= 17.5) and Z > 17.5, resp., and ratio = 3.0
        ks_30_1 = -0.0001824 * Z**3 + 0.01138 * Z**2 + 0.02766 * Z + 5.956
        ks_30_2 = 5.357D-13 * Z**5 - 0.000000001358 * Z**4 + 0.000001254 * Z**3 - 0.000549 * Z**2 + 0.2073 * Z + 5.376
        ! For (Z >= 1) .and. (Z <= 17.5) and Z > 17.5, resp., and ratio = 2.0
        ks_20_1 = -0.0004178 * Z**3 + 0.015 * Z**2 + 0.0321 * Z + 6.483
        ks_20_2 = 4.847D-13 * Z**5 - 0.000000001295 * Z**4 + 0.00000126 * Z**3 - 0.0005772 * Z**2 + 0.2327 * Z + 5.622
        ! For (Z >= 1) .and. (Z <= 17.5) and Z > 17.5, resp., and ratio = 1.5
        ks_15_1 = 0.0002211 * Z**3 - 0.0008322 * Z**2 + 0.1641 * Z + 6.905
        ks_15_2 = 4.612D-13 * Z**5 - 0.000000001224 * Z**4 + 0.000001191 * Z**3 - 0.0005578 * Z**2 + 0.244 * Z + 6.573
        ! For (Z >= 1) .and. (Z <= 17.5) and Z > 17.5, resp., and ratio = 1.0
        ks_10_1 = -0.0003836 * Z**3 + 0.01565 * Z**2 + 0.0998 * Z + 9.243
        ks_10_2 = 6.337D-13 * Z**5 - 0.000000001607 * Z**4 + 0.000001504 * Z**3 - 0.0006901 * Z**2 + 0.295 * Z + 9.049
        ! Calculate ks for actual ratio for (Z >= 1) .and. (Z <= 17.5)
        if ((Z >= 1) .and. (Z <= 17.5) .and.      (abs(ratio - 9) < 0.00001)) then
            ks = ks_90_1
        else if ((Z >= 1) .and. (Z <= 17.5) .and. (abs(ratio - 3) < 0.00001)) then
            ks = ks_30_1
        else if ((Z >= 1) .and. (Z <= 17.5) .and. (abs(ratio - 2) < 0.00001)) then
            ks = ks_20_1
        else if ((Z >= 1) .and. (Z <= 17.5) .and. (abs(ratio - 1.5) < 0.00001)) then
            ks = ks_15_1
        else if ((Z >= 1) .and. (Z <= 17.5) .and. (abs(ratio - 1) < 0.00001)) then
            ks = ks_10_1
        ! Calculate ks for actual ratio for z > 17.5
        else if ((Z > 17.5) .and. (abs(ratio - 9) < 0.00001)) then
            ks = ks_90_2                                       
        else if ((Z > 17.5) .and. (abs(ratio - 3) < 0.00001)) then
            ks = ks_30_2                                       
        else if ((Z > 17.5) .and. (abs(ratio - 2) < 0.00001)) then
            ks = ks_20_2                                       
        else if ((Z > 17.5) .and. (abs(ratio - 1.5) < 0.00001)) then
            ks = ks_15_2                                       
        else if ((Z > 17.5) .and. (abs(ratio - 1) < 0.00001)) then
            ks = ks_10_2
        ! Calculate ks for ratio between curves and 1 <= z <= 17.5 and ratio between curves
        else if ((Z >= 1) .and. (Z <= 17.5) .and. (ratio > 3) .and. (ratio < 9)) then
            ks = ((ratio - 3) / 6) * (ks_90_1 - ks_30_1) + ks_30_1
        else if ((Z >= 1) .and. (Z <= 17.5) .and. (ratio > 2) .and. (ratio < 3)) then
            ks = (ratio - 2) * (ks_30_1 - ks_20_1) + ks_20_1
        else if ((Z >= 1) .and. (Z <= 17.5) .and. (ratio > 1.5) .and. (ratio < 2)) then
            ks = ((ratio - 1.5) / 0.5) * (ks_20_1 - ks_15_1) + ks_15_1
        else if ((Z >= 1) .and. (Z <= 17.5) .and. (ratio > 1) .and. (ratio < 1.5)) then
            ks = ((ratio - 1) / 0.5) * (ks_15_1 - ks_10_1) + ks_10_1
        ! Calculate ks for ratio between curves for z > 17.5 and ratio between curves
        else if ((Z > 17.5) .and. (ratio > 3) .and. (ratio < 9)) then
            ks = ((ratio - 3) / 6) * (ks_90_2 - ks_30_2) + ks_30_2
        else if ((Z > 17.5) .and. (ratio > 2) .and. (ratio < 3)) then
            ks = (ratio - 2) * (ks_30_2 - ks_20_2) + ks_20_2
        else if ((Z > 17.5) .and. (ratio > 1.5) .and. (ratio < 2)) then
            ks = ((ratio - 1.5) / 0.5) * (ks_20_2 - ks_15_2) + ks_15_2
        else if ((Z > 17.5) .and. (ratio > 1) .and. (ratio < 1.5)) then
            ks = ((ratio - 1) / 0.5) * (ks_15_2 - ks_10_2) + ks_10_2
        end if
        ! Calculation for Longeron System (a < b) as given in Fig.C9.5
    else
        Z = (a ** 2 / (r * t)) * sqrt(1 - nu_skin**2)
        z = min(max(Z, 1.), 1000.)

        ratio = b / a
        ratio = min(ratio, 9.)

        ! For ratio = 9.0, 2.0, 1.5 and 1.0
        ks_90_1 = 0.0000255 * Z**3 + 0.001861 * Z**2 + 0.2102 * Z + 5.186
        ks_90_2 = 3.547D-13 * Z**5 - 0.0000000009862 * Z**4 + 0.000001014 * Z**3 - 0.0005071 * Z**2 + 0.2612 * Z + 5.373
        ks_20 = -0.00009053 * Z**3 + 0.01012 * Z**2 + 0.1414 * Z + 6.55
        ks_15 = 0.0000003903 * Z**4 - 0.00006475 * Z**3 + 0.002385 * Z**2 + 0.2678 * Z + 6.769
        ks_10_1 = -0.0001419 * Z**3 + 0.007819 * Z**2 + 0.2241 * Z + 8.98
        ks_10_2 = -2.702D-15 * Z**6 + 0.000000000007884 * Z**5 - 0.00000000876 * Z**4 + 0.000004707 * Z**3 - 0.001335 * Z**2 + 0.3406 * Z + 8.786
        ! Calculate ks for actual ratios
        if ((Z >= 1) .and. (Z <= 18.5) .and. (abs(ratio - 9) < 0.00001)) then
            ks = ks_90_1
        else if ((Z > 18.5) .and. (abs(ratio - 9) < 0.00001)) then
            ks = ks_90_2
        else if ((Z >= 1) .and. (Z <= 10) .and. (abs(ratio - 2) < 0.00001)) then
            ks = ks_20
        else if ((Z >= 1) .and. (Z <= 100) .and. (abs(ratio - 1.5) < 0.00001)) then
            ks = ks_15
        else if ((Z >= 1) .and. (Z <= 13) .and. (abs(ratio - 1.5) < 0.00001)) then
            ks = ks_10_1
        else if ((Z > 13) .and. (abs(ratio - 1.5) < 0.00001)) then
            ks = ks_10_2
        ! Calculate ks for ratios between curves
        else if ((Z >= 1) .and. (Z <= 10) .and. (ratio > 2) .and. (ratio < 9)) then
            ks = ((ratio - 2) / 7) * (ks_90_1 - ks_20) + ks_20
        else if ((Z > 10) .and. (Z <= 18.5) .and. (ratio > 2) .and. (ratio < 9)) then
            ks = ks_90_1
        else if ((Z > 18.5) .and. (ratio > 2) .and. (ratio < 9)) then
            ks = ks_90_2
        else if ((Z >= 1) .and. (Z <= 10) .and. (ratio > 1.5) .and. (ratio < 2)) then
            ks = ((ratio - 1.5) / 0.5) * (ks_20 - ks_15) + ks_15
        else if ((Z > 10) .and. (Z <= 100) .and. (ratio > 1.5) .and. (ratio < 2)) then
            ks = ks_15
        else if ((Z > 100) .and. (ratio > 1.5) .and. (ratio < 2)) then
            ks = ks_90_2
        else if ((Z >= 1) .and. (Z <= 13) .and. (ratio > 1) .and. (ratio < 1.5)) then
            ks = ((ratio - 1) / 0.5) * (ks_15 - ks_10_1) + ks_10_1
        else if ((Z > 13) .and. (Z <= 100) .and. (ratio > 1) .and. (ratio < 1.5)) then
            ks = ((ratio - 1) / 0.5) * (ks_15 - ks_10_2) + ks_10_2
        else if ((Z > 100) .and. (ratio > 1) .and. (ratio < 1.5)) then
            ks = ks_10_2
        end if
    end if
    ! Calculate Shear Buckling allowable
    fSScr_skin = ks*pi**2*Ec_skin*(t/min(a, b))**2/(12 * (1 - nu_skin**2))
end

real*4 function fSCcr_skin(a, b, t, r, Ec_skin, nu_skin)
    ! curved skin compressive buckling allowable 
    ! as in Fig.C9.1 pgC9.2 of Bruhn
    ! - written by Tam Ha, Feb. 2001
    ! - translated to Fortran by Saullo Castro, April 2015
    implicit none

    real*4 Z
    real*4 a, b, t, r, Ec_skin, nu_skin, ratio, kc
    real*4 kc_3000_1, kc_2000_1, kc_1000_1, kc_700_1, kc_500_1
    real*4 kc_3000_2, kc_2000_2, kc_1000_2, kc_700_2, kc_500_2
    real*4 pi
    pi = atan(1.)*4

    Z = min(a, b)**2/(r*t)*sqrt(1-nu_skin**2)
    Z = min(max(Z, 1.), 1000.)
    ratio = r/t
    ratio = min(max(ratio, 500.), 3000.)

    ! for all 1.0 (z >= 1) .and. (z <= 98.5)
    kc_3000_1 = -0.0000002362 * Z**4 + 0.00005587 * Z**3 - 0.004728 * Z**2 + 0.3207 * Z + 3.47
    kc_2000_1 = -0.0000002362 * Z**4 + 0.00005587 * Z**3 - 0.004728 * Z**2 + 0.3207 * Z + 3.47
    kc_1000_1 = -0.00000006608 * Z**4 + 0.00002007 * Z**3 - 0.002178 * Z**2 + 0.2784 * Z + 3.582
    kc_700_1 = -0.000002229 * Z**3 + 0.0006811 * Z**2 + 0.2332 * Z + 3.69
    kc_500_1 = -0.00001555 * Z**3 + 0.003041 * Z**2 + 0.2387 * Z + 3.716
    
    ! for all z > 98.5
    kc_3000_2 = 8.554D-18 * Z**5 - 2.243D-13 * Z**4 + 0.000000002213 * Z**3 - 0.0000112 * Z**2 + 0.1181 * Z + 8.509
    kc_2000_2 = -1.954D-17 * Z**5 + 4.081D-13 * Z**4 - 0.000000002466 * Z**3 + 0.000001274 * Z**2 + 0.1343 * Z + 8.225
    kc_1000_2 = 1.922D-13 * Z**4 - 0.000000001811 * Z**3 + 0.000005994 * Z**2 + 0.1791 * Z + 4.09
    kc_700_2 = 0.000000003334 * Z**3 - 0.00001081 * Z**2 + 0.3248 * Z - 0.7549
    kc_500_2 = 0.0000000002045 * Z**3 - 0.000004684 * Z**2 + 0.4219 * Z + 0.3832

    ! Calculate Kc for (z >= 1) .and. (z <= 98.5) and actual ratio
    if ((Z >= 1) .and. (Z <= 98.5) .and. (ratio >= 3000)) then
       kc = kc_3000_1
    else if ((Z >= 1) .and. (Z <= 98.5) .and. (abs(ratio - 2000) < 0.00001)) then
       kc = kc_3000_1
    else if ((Z >= 1) .and. (Z <= 98.5) .and. (abs(ratio - 1000) < 0.00001)) then
       kc = kc_1000_1
    else if ((Z >= 1) .and. (Z <= 98.5) .and. (abs(ratio - 700) < 0.00001)) then
       kc = kc_700_1
    else if ((Z >= 1) .and. (Z <= 98.5) .and. (abs(ratio - 500) < 0.00001)) then
       kc = kc_500_1

    ! Calculate Kc for z > 98.5 and actual ratio
    else if ((Z > 98.5) .and. (abs(ratio - 3000) < 0.00001)) then
       kc = kc_3000_2
    else if ((Z > 98.5) .and. (abs(ratio - 2000) < 0.00001)) then
       kc = kc_2000_2
    else if ((Z > 98.5) .and. (abs(ratio - 1000) < 0.00001)) then
       kc = kc_1000_2
    else if ((Z > 98.5) .and. (abs(ratio - 700) < 0.00001)) then
       kc = kc_700_2
    else if ((Z > 98.5) .and. (abs(ratio - 500) < 0.00001)) then
       kc = kc_500_2

    ! Calculate Kc for 1 <= z <= 98.5 and actual ratio between curves
    else if ((Z >= 1) .and. (Z <= 98.5) .and. (ratio > 2000) .and. (ratio < 3000)) then
       kc = ((ratio - 2000) / 1000.) * (kc_3000_1 - kc_2000_1) + kc_2000_1
    else if ((Z >= 1) .and. (Z <= 98.5) .and. (ratio > 1000) .and. (ratio < 2000)) then
       kc = ((ratio - 1000) / 1000.) * (kc_2000_1 - kc_1000_1) + kc_1000_1
    else if ((Z >= 1) .and. (Z <= 98.5) .and. (ratio > 700) .and. (ratio < 1000)) then
       kc = ((ratio - 700) / 300.) * (kc_1000_1 - kc_700_1) + kc_700_1
    else if ((Z >= 1) .and. (Z <= 98.5) .and. (ratio > 500) .and. (ratio < 700)) then
       kc = ((ratio - 500) / 200.) * (kc_700_1 - kc_500_1) + kc_500_1

    ! Calculate Kc for z > 98.5 and actual ratio between curves
    else if ((Z > 98.5) .and. (ratio > 2000) .and. (ratio < 3000)) then
       kc = ((ratio - 2000) / 1000.) * (kc_3000_2 - kc_2000_2) + kc_2000_2
    else if ((Z > 98.5) .and. (ratio > 1000) .and. (ratio < 2000)) then
       kc = ((ratio - 1000) / 1000.) * (kc_2000_2 - kc_1000_2) + kc_1000_2
    else if ((Z > 98.5) .and. (ratio > 700) .and. (ratio < 1000)) then
       kc = ((ratio - 700) / 300.) * (kc_1000_2 - kc_700_2) + kc_700_2
    else if ((Z > 98.5) .and. (ratio > 500) .and. (ratio < 700)) then
       kc = ((ratio - 500) / 200.) * (kc_700_2 - kc_500_2) + kc_500_2
    end if

    fSCcr_skin = pi**2*kc*Ec_skin/(12*(1 - nu_skin**2))*(t/min(b, a))**2
end function


real*4 function fSratio_str(kk, a, b)
    ! Ratio of max to ave stress for stringers 
    ! as in FigC11.21 pg.C11.27 of Bruhn
    ! - writen by Tam HA March 9th. 2001
    ! - translated to Fortran by Saullo Castro, April 2015
    implicit none

    real*4 kk, a, b, ratio
    real*4 fst_ratio_0, fst_ratio_2, fst_ratio_4, fst_ratio_6, fst_ratio_8

    ratio = b / a
    if (ratio >= 1) then
       ratio = 1
    end if
    !
    if (kk >= 0.8) then
       kk = 0.8
    end if
    !
    ! Calculate Stress ratios for all k values
    fst_ratio_8 = -0.12625 * ratio + 1.155
    fst_ratio_6 = -0.25591 * ratio + 1.3105
    fst_ratio_4 = -0.38369 * ratio + 1.4657
    fst_ratio_2 = -0.51402 * ratio + 1.619
    fst_ratio_0 = -0.64521 * ratio + 1.7798
    !
    ! Calculate Stress ratios for exact k values
    if (abs(kk - 0.8) < 0.00001) then
       fSratio_str = fst_ratio_8
    else if (abs(kk - 0.6) < 0.00001) then
       fSratio_str = fst_ratio_6
    else if (abs(kk - 0.4) < 0.00001) then
       fSratio_str = fst_ratio_4
    else if (abs(kk - 0.2) < 0.00001) then
       fSratio_str = fst_ratio_2
    else if (abs(kk - 0) < 0.00001) then
       fSratio_str = fst_ratio_0
    end if
    !
    ! Calculate Stress ratios for in between k values
    if ((kk > 0.6) .and. (kk < 0.8)) then
       fSratio_str = (kk - 0.6) * (fst_ratio_8 - fst_ratio_6) / 0.2 + fst_ratio_6
    else if ((kk > 0.4) .and. (kk < 0.6)) then
       fSratio_str = (kk - 0.4) * (fst_ratio_6 - fst_ratio_4) / 0.2 + fst_ratio_4
    else if ((kk > 0.2) .and. (kk < 0.4)) then
       fSratio_str = (kk - 0.2) * (fst_ratio_4 - fst_ratio_2) / 0.2 + fst_ratio_2
    else if ((kk > 0) .and. (kk < 0.2)) then
       fSratio_str = (kk - 0) * (fst_ratio_2 - fst_ratio_0) / 0.2 + fst_ratio_0
    end if
end function

real*4 function fSratio_fr(kk, ask, bsk)
    ! Ratio of max to ave stress for stringers 
    ! as in FigC11.21 pg.C11.27 of Bruhn
    ! - writen by Tam HA March 9th. 2001
    ! - translated to Fortran by Saullo Castro, April 2015
    implicit none

    real*4 kk, ask, bsk
    real*4 ratio
    real*4 ffr_ratio_0, ffr_ratio_2, ffr_ratio_4, ffr_ratio_6, ffr_ratio_8

    ratio = ask / bsk

    if (ratio >= 1) then
       ratio = 1
    end if

    if (kk >= 0.8) then
       kk = 0.8
    end if

    ! Calculate Stress ratios for all k values
    ffr_ratio_8 = -0.12625 * ratio + 1.155
    ffr_ratio_6 = -0.25591 * ratio + 1.3105
    ffr_ratio_4 = -0.38369 * ratio + 1.4657
    ffr_ratio_2 = -0.51402 * ratio + 1.619
    ffr_ratio_0 = -0.64521 * ratio + 1.7798

    ! Calculate Stress ratios for exact k values
    if (abs(kk - 0.8) < 0.00001) then
        fSratio_fr = ffr_ratio_8
    else if (abs(kk - 0.6) < 0.00001) then
        fSratio_fr = ffr_ratio_6
    else if (abs(kk - 0.4) < 0.00001) then
        fSratio_fr = ffr_ratio_4
    else if (abs(kk - 0.2) < 0.00001) then
        fSratio_fr = ffr_ratio_2
    else if (abs(kk - 0) < 0.00001) then
        fSratio_fr = ffr_ratio_0
    end if

    ! Calculate Stress ratios for in between k values
    if ((kk > 0.6) .and. (kk < 0.8)) then
        fSratio_fr = (kk - 0.6) * (ffr_ratio_8 - ffr_ratio_6) / 0.2 + ffr_ratio_6
    else if ((kk > 0.4) .and. (kk < 0.6)) then
        fSratio_fr = (kk - 0.4) * (ffr_ratio_6 - ffr_ratio_4) / 0.2 + ffr_ratio_4
    else if ((kk > 0.2) .and. (kk < 0.4)) then
        fSratio_fr = (kk - 0.2) * (ffr_ratio_4 - ffr_ratio_2) / 0.2 + ffr_ratio_2
    else if ((kk > 0) .and. (kk < 0.2)) then
        fSratio_fr = (kk - 0) * (ffr_ratio_2 - ffr_ratio_0) / 0.2 + ffr_ratio_0
    end if
end function

real*4 function SFC_allow_str(kleft, kright, tleft, tright, tweb, fcy, Ec)
    ! Forced Crippling Allowable for Stringers
    ! Bruhn Fig.C11.38
    ! - writen by Tam HA March 9th. 2001
    ! - translated to Fortran by Saullo Castro, July 2015
    implicit none

    real*4 kleft, kright, tleft, tright, tweb, fcy, Ec
    real*4 ratio, n, c

    if ((kleft == 0) .and. (kright .ne. 0)) then
        ratio = (kright ** 0.6666667) * (tweb / tright) ** 0.3333333
        n = 29930 * ratio + 71.12
    else if ((kright == 0) .and. (kleft .ne. 0)) then
        ratio = (kleft ** 0.6666667) * (tweb / tleft) ** 0.3333333
        n = 29930 * ratio + 71.12
    else if ((kleft == 0) .and. (kright == 0)) then
        n = 0
    else
        ratio = ((kleft ** 0.6666667) * (tweb / tleft) ** 0.3333333 + (kright ** 0.6666667) * (tweb / tright) ** 0.3333333) / 2
        n = 29930 * ratio + 71.12
    end if

    ! Calculate Forced Crippling Allowable for Stringer
    c = fcy * 0.01 / (5.88 * (fcy / Ec + 0.002) ** 0.5)
    SFC_allow_str = -n * c / 1000
end function


real*4 function Ffr_allow(kk, tweb, tskin, Rin, fcy, Ec)
    ! Forced Crippling Allowables for Frames
    ! Bruhn Fig.C11.38
    ! - writen by Tam HA, March 9th. 2001
    ! - translated to fortran by Saullo Castro, July 2015
    implicit none

    real*4 kk, tweb, tskin, Rin, fcy, Ec
    real*4 ratio, N_20, N_40, N_60, N_75, N_100, N_125, n, c

    tweb = tweb / 25.4
    tskin = tskin / 25.4
    Rin = Rin / 25.4
    fcy = fcy * 1.45
    Ec = Ec * 1.45
    ratio = (kk ** 0.6666667) * (tweb / tskin) ** 0.3333333
    
    if (ratio >= 1) then
        ratio = 1
    else if (ratio <= 0) then
        ratio = 0
    end if
    
    if (Rin >= 125) then
        Rin = 125
    else if (Rin <= 20) then
        Rin = 20
    end if
    
    ! for Radius = 20, 40, 60, 75, 100 and 125 in, respectively
    N_20 = 19570 * ratio + 66.79
    N_40 = 21440 * ratio + 85.68
    N_60 = 23110 * ratio + 64.83
    N_75 = 24330 * ratio + 53.9
    N_100 = 26090 * ratio + 96.32
    N_125 = 27920 * ratio + 115.3
    
    ! Calculate N for exact Radius
    if (Rin <= 20) then
        n = N_20
    else if (abs(Rin - 40) < 0.00001) then
        n = N_40
    else if (abs(Rin - 60) < 0.00001) then
        n = N_60
    else if (abs(Rin - 75) < 0.00001) then
        n = N_75
    else if (abs(Rin - 100) < 0.00001) then
        n = N_100
    else if (Rin >= 125) then
        n = N_125
    
    ! Calculate N between Radius
    else if ((Rin > 20) .and. (Rin < 40)) then
        n = -(Rin - 40) * (N_20 - N_40) / 20 + N_40
    else if ((Rin > 40) .and. (Rin < 60)) then
        n = -(Rin - 60) * (N_40 - N_60) / 20 + N_60
    else if ((Rin > 60) .and. (Rin < 75)) then
        n = -(Rin - 75) * (N_60 - N_75) / 15 + N_75
    else if ((Rin > 75) .and. (Rin < 100)) then
        n = -(Rin - 100) * (N_75 - N_100) / 25 + N_100
    else if ((Rin > 100) .and. (Rin < 125)) then
        n = -(Rin - 125) * (N_100 - N_125) / 25 + N_125
    end if
    
    c = fcy * 0.01 / (5.88 * (fcy / Ec + 0.002) ** 0.5)
    Ffr_allow = n * c / 1000
    
    Ffr_allow = Ffr_allow / 1.45
end function




real*4 Function fs_allow_Ftu(ask, bsk, tskin, Afr, Astr, kk, alpha, Ftu_fs)
    ! Allowable Stress in Skin (Ftu_fs and fs_allow_Ftu are in psi)
    ! - as given in Bruhn Fig.C11.42, pg. C11.53 and Eq. 103 pg. C11.37
    ! - written by Reinaldo Sawaguchi Kolososki and adapted by Malcom Petras, 2010
    ! - translated to Fortran by Saullo Castro, July 2015
    implicit none

    real*4 ask, bsk, tskin, Afr, Astr, kk, alpha, Ftu_fs
    real*4 fs_allow_Ftu_30, fs_allow_Ftu_40, fs_allow_Ftu_50, fs_allow_Ftu_62, fs_allow_Ftu_70
    real*4 fs_allow_Ftu_80, fs_allow_Ftu_90, fs_allow_Ftu_100, fs_allow_Ftu_110, fs_allow_Ftu_120
    real*4 x1, x2, y1, y2, delta

    Ftu_fs = 0.001 * Ftu_fs ! transforming from psi to ksi

    delta = 0.3 * tanh(Afr / ask / tskin) + 0.1 * tanh(Astr / bsk / tskin)

    if (kk <= 0.4) then
        fs_allow_Ftu_30 = 10 * kk ** 2 - 10.4 * kk + 13.68
        fs_allow_Ftu_40 = 13.571 * kk ** 2 - 12.929 * kk + 17.891
        fs_allow_Ftu_50 = 28.571 * kk ** 2 - 22.629 * kk + 22.931
        fs_allow_Ftu_62 = 27.857 * kk ** 2 - 23.643 * kk + 27.857
        fs_allow_Ftu_70 = 27.857 * kk ** 2 - 25.043 * kk + 31.377
        fs_allow_Ftu_80 = 34.286 * kk ** 2 - 30.114 * kk + 35.826
        fs_allow_Ftu_90 = 34.286 * kk ** 2 - 31.914 * kk + 40.226
        fs_allow_Ftu_100 = 32.857 * kk ** 2 - 33.943 * kk + 44.957
        fs_allow_Ftu_110 = 41.429 * kk ** 2 - 39.571 * kk + 49.249
        fs_allow_Ftu_120 = 47.143 * kk ** 2 - 43.457 * kk + 53.703
    else
        fs_allow_Ftu_30 = 1.1905 * kk ** 2 - 2.881 * kk + 12.014
        fs_allow_Ftu_40 = 1.1905 * kk ** 2 - 3.6666667 * kk + 16.164
        fs_allow_Ftu_50 = 0.5952 * kk ** 2 - 2.9405 * kk + 19.457
        fs_allow_Ftu_62 = 2.9762 * kk ** 2 - 6.7738 * kk + 24.95
        fs_allow_Ftu_70 = 2.9762 * kk ** 2 - 7.2024 * kk + 28.15
        fs_allow_Ftu_80 = 3.4524 * kk ** 2 - 7.9405 * kk + 31.814
        fs_allow_Ftu_90 = 4.4048 * kk ** 2 - 9.2738 * kk + 35.829
        fs_allow_Ftu_100 = 5.2381 * kk ** 2 - 10.762 * kk + 39.986
        fs_allow_Ftu_110 = 3.8095 * kk ** 2 - 9.0476 * kk + 42.957
        fs_allow_Ftu_120 = 3.4524 * kk ** 2 - 8.9405 * kk + 46.686
    end if

    if (Ftu_fs < 30) then
        Ftu_fs = 30
    end if
    if (Ftu_fs > 120) then
        Ftu_fs = 120
    end if

    if ((Ftu_fs >= 30) .and. (Ftu_fs < 40)) then
        x1 = 30
        x2 = 40
        y1 = fs_allow_Ftu_30
        y2 = fs_allow_Ftu_40
    else if ((Ftu_fs >= 40) .and. (Ftu_fs < 50)) then
        x1 = 40
        x2 = 50
        y1 = fs_allow_Ftu_40
        y2 = fs_allow_Ftu_50
    else if ((Ftu_fs >= 50) .and. (Ftu_fs < 62)) then
        x1 = 50
        x2 = 62
        y1 = fs_allow_Ftu_50
        y2 = fs_allow_Ftu_62
    else if ((Ftu_fs >= 62) .and. (Ftu_fs < 70)) then
        x1 = 62
        x2 = 70
        y1 = fs_allow_Ftu_62
        y2 = fs_allow_Ftu_70
    else if ((Ftu_fs >= 70) .and. (Ftu_fs < 80)) then
        x1 = 70
        x2 = 80
        y1 = fs_allow_Ftu_70
        y2 = fs_allow_Ftu_80
    else if ((Ftu_fs >= 80) .and. (Ftu_fs < 90)) then
        x1 = 80
        x2 = 90
        y1 = fs_allow_Ftu_80
        y2 = fs_allow_Ftu_90
    else if ((Ftu_fs >= 90) .and. (Ftu_fs < 100)) then
        x1 = 90
        x2 = 100
        y1 = fs_allow_Ftu_90
        y2 = fs_allow_Ftu_100
    else if ((Ftu_fs >= 100) .and. (Ftu_fs < 110)) then
        x1 = 100
        x2 = 110
        y1 = fs_allow_Ftu_100
        y2 = fs_allow_Ftu_110
    else if ((Ftu_fs >= 110) .and. (Ftu_fs <= 120)) then
        x1 = 110
        x2 = 120
        y1 = fs_allow_Ftu_110
        y2 = fs_allow_Ftu_120
    end if

    fs_allow_Ftu = (x2 - Ftu_fs) / (x2 - x1) * y1 + (Ftu_fs - x1) / (x2 - x1) * y2

    fs_allow_Ftu = fs_allow_Ftu * (0.65 + delta)

    fs_allow_Ftu = fs_allow_Ftu * 1000. ! transforming from ksi to psi

end function
