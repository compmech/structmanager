include '../functionsS.f90'
!
! Diagonal tension criteria for curved stiffened panels
! Written by Saullo Castro, July 2015
!
subroutine R3SVALS(GRPID, TYPNAM, NITEMS, ARGLIS, NSIZE, ARGVAL, &
                   NWRDA8, ARGCHR, forg, nresp, narg, DR3VAL, senval, error)
    ! ----------------------------------------------------------------------
    !
    !     PURPOSE: COMPUTE THE EXTERNAL RESPONSE
    !
    !     GRPID   INPUT INTEGER        - GROUP ID
    !     TYPNAM  INPUT CHARACTER*8    - NAME OF EXTERNAL RESPONSE TYPE
    !     NITEMS  INPUT INTEGER        - DIMENSION OF ARRAY ARGLIS
    !     NSIZE   INPUT INTEGER        - DIMENSION OF ARRAY ARGVAL
    !     NWRDA8  INPUT INTEGER        - DIMENSION OF CHARACTER ARRAY ARGCHR
    !     ARGLIS  INPUT INTEGER        - ARRAY OF NO. OF ITEMS FOR EACH
    !                                     ARGUMENT type
    !     ARGVAL  INPUT DOUBLE         - ARRAY OF ARGUMENT VALUES (except
    !                                            characters)
    !     ARGCHR  INPUT CHARACTER*8    - ARRAY OF CHARACTER VALUES
    !     nresp   input integer        - number of responses
    !     forg    input integer        - type of call
    !                                     = 0 function evaluation
    !                                     = 1 sensitivity evaluation
    !     narg    input integer        - number of arguments needing gradients
    !     DR3VAL  OUTPUT DOUBLE        - VALUE OF THE EXTERNAL RESPONSEs
    !     senval  output double        - matrix of the sensitivity of the IRth
    !                                    response to the IARGth argument
    !     ERROR   INPUT/OUTPUT INTEGER -ERROR CODE FOR THE CALL.
    !                                   0 = PRINT ERROR MESSAGES
    !                                   1 = DO NOT PRINT ERROR MESSAGES.
    !
    !   METHOD
    !       A)SET UP VARIOUS PARAMETERS FROM THE ARGUMENT LIST
    !       B)if forg = 0 EVALUATE THE EXTERNAL RESPONSE BASED ON THE
    !                     GIVEN TYPNAM
    !       C)else if forg = 1 EVALUATE THE sensitivities of the external
    !                          responses to the arguments that can vary for
    !                          the given typnam
    !       D)RETURN BADTYP ERROR IF TYPNAM IS NOT MATCHED HERE.
    !
    !     nsize - the number of arguments or values in a dresp3 entry
    !
    !     nsize=nv+nc+nr+nnc+ndvp1+ndvp2+ndvc1+ndvc2+ndvm1+ndvm2+nrr2
    !        where:
    !        nv     = number of desvars    nc    = number of dtables
    !        nr     = number of dresp1s    nnc   = number of dnode pairs
    !        ndvp1  = number of dvprel1s   ndvp2 = number dvprel2s
    !        ndvc1  = number of dvcrel1s   ndvc2 = number dvcrel2s
    !        ndvm1  = number of dvmrel1s   ndvm2 = number dvmrel2s
    !        nrr2   = number of dresp2s
    !     narg = nsize - nc
    !
    !   CALLED BY
    !       SENDR3SVALD
    ! ----------------------------------------------------------------------
    !
    ! VARIABLES PASSED IN
    !
    implicit none
        
    character*8 TYPNAM, ARGCHR(NWRDA8)
    integer forg, nresp, narg
    integer GRPID, NITEMS, NSIZE, ARGLIS(NITEMS), ERROR, NWRDA8
    real*4 ARGVAL(NSIZE), DR3VAL(*), senval(nresp,*)
    integer BADTYP
    data BADTYP /7554/


    real*4, external :: cot, fSScr_skin, fSCcr_skin

    real*4 Nxx, Nxy, FC, FS, nu, Ec
    real*4 FScr, FCcr
    real*4 A_ratio, B_ratio, Rc, Rs

    real*4 r, t, a, b
    real*4 ms

    real*4 pi
    pi = atan(1.)*4

    ERROR = 0

    if (TYPNAM .eq. 'METHOD1') then
        ! r --> radius
        ! b --> circumferential distance between stringers
        ! a --> distance between frame rings
        
        ! Variables (DESVAR) from panel
        t = ARGVAL(1) ! Thickness of Panel 1

        ! Constants (DTABLE)
        r = ARGVAL(2) ! Curved panel radius
        a = ARGVAL(3) ! Panel length
        b = ARGVAL(4) ! Panel circumferential width

        Ec = ARGVAL(5) ! Compressive Young's module
        nu = ARGVAL(6) ! Poisson's ratio

        ! Mid-surface stress data (DRESP2)
        Nxx = ARGVAL(7) ! Nxx membrane force
        Nxy = ARGVAL(8) ! Nxy membrane force

        FC = Nxx/t ! Nxx membrane force
        FS = Nxy/t ! Nxy membrane force
        
        FC = FC
        FS = ABS(FS)
        
        FCcr = fSCcr_skin(a, b, t, r, Ec, nu)
        FScr = fSScr_skin(a, b, t, r, Ec, nu)

        Rc = FC/FCcr
        Rs = FS/FScr

        ms = 2./(Rc + SQRT(Rc**2 + 4*Rs**2)) - 1.
    end if


    DR3VAL(1) = ms
    
    return
end subroutine R3SVALS
