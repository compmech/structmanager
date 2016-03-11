! BUCKLING_CPANEL_BARDELL subroutine
!
! Buckling of cylindrical panels.
!
! The required inputs that should be given are described below.
! All inputs will be entered by a DRESP3 NASTRAN Structure.
! 
! Run control
! -----------
! NUM : integer
!   Number of returned eigenvalues
!
! M : integer
!   Number of terms along x
!
! N : integer
!   Number of terms along x
!
! Geometry
! --------
! a : float
!   The panel length (dimension along x)
! b : float
!   The panel circumferential width (dimension along y)
! r : float
!   The panel radius. (Set a high value to simulate a plate)
! t : float, optional (used with ISOTROPIC flag)
!   Panel thickness
!
! Isotropic Material Properties
! -----------------------------
! ISOTROPIC : flag
!   If present in the input, matrix ABD will be calculated based on
!   E, nu and t.
! E : float
!   Elastic modulus
! nu : float
!   Poisson's ratio
!
! Orthotropic Material Properties
! -------------------------------
! ISOTROPIC : FALSE
!   Matrix ABD will be calculated based on E1, E2, G12, nu12, nu21 and t.
! E1 : float
!   Elastic modulus at longitudinal direction
! E2 : float
!   Elastic modulus at transversal direction
! G12 : float
!   Shear modulus between longitudinal and transversal directions
! nu12 : float
!   Poisson's ratio between longitudinal and transversal directions
! nu21 : float
!   Poisson's ratio between transversal nad longitudinal directions
! t : float
!   Laminate thickness
!
! Applied Loads
! -------------
! Nxx : float
!   Nxx longitudinal membrane stress
! Nyy : float
!   Nyy transversal membrane stress
! Nxy : float
!   Nxy shear membrane stress
!
! Laminate Constitutive Variables (matrix ABD)
! -------------------------------------------
! ONLY used if ISOTROPIC = FALSE
!
! A11 : float
!   Membrane stiffness along x
! A12 : float
!   Membrane stiffness
! A16 : float
!   Shear-extension coupling
! A22 : float
!   Membrane stiffness along y
! A26 : float
!   Shear-extension coupling
! A66 : float
!   Membrane Shear stiffness
! ----------------------------------------------------------------------------------
! IN THIS CASE, CONSIDERED LAMINATE IS SMEAR NASTRAN TYPE => ALL Bij TERMS ARE NULL.
! ----------------------------------------------------------------------------------
! B11 : float
!   Bending-extension coupling
! B12 : float
!   Bending-extension coupling
! B16 : float
!   Bending-extension coupling
! B22 : float
!   Bending-extension coupling
! B26 : float
!   Bending-extension coupling
! B66 : float
!   Bending-extension coupling
! -----------------------------------------------------------------------------------------------------
! IN THIS CASE, CONSIDERED LAMINATE IS SMEAR NASTRAN TYPE => ALL D12-21, D16-61, D26-62 TERMS ARE NULL.
! -----------------------------------------------------------------------------------------------------
! D11 : float
!   Bending stiffness
! D12 : float
!   Bending stiffness
! D16 : float
!   Bending-twist stiffness
! D22 : float
!   Bending stiffness
! D26 : float
!   Bending-twist stiffness
! D66 : float
!   Twist (torsion) stiffness
!
! Boundary conditions - Always Simply Supported - All these terms below remain as is in this code.
! ------------------------------------------------------------------------------------------------
! u1tx : float
!   If 1. the edge at x=0 can translate along u   
!   If 0. the edge at x=0 cannot translate along u   
! u1rx : float
!   If 1. the end at x=0 can rotate
!   If 0. the end at x=0 cannot translate along u   
! u2tx : float
!   If 1. the edge at x=a can translate along u   
!   If 0. the edge at x=a cannot translate along u   
! u2rx : float
!   If 1. the end at x=a can rotate
!   If 0. the end at x=a cannot translate along u   
! u1ty : float
!   If 1. the edge at y=0 can translate along u   
!   If 0. the edge at y=0 cannot translate along u   
! u1ry : float
!   If 1. the end at y=0 can rotate
!   If 0. the end at y=0 cannot translate along u   
! u2ty : float
!   If 1. the edge at y=b can translate along u   
!   If 0. the edge at y=b cannot translate along u   
! u2ry : float
!   If 1. the end at y=b can rotate
!   If 0. the end at y=b cannot translate along u   
! v1tx : float
!   If 1. the edge at x=0 can translate along v   
!   If 0. the edge at x=0 cannot translate along v   
! v1rx : float
!   If 1. the end at x=0 can rotate
!   If 0. the end at x=0 cannot translate along v   
! v2tx : float
!   If 1. the edge at x=a can translate along v   
!   If 0. the edge at x=a cannot translate along v   
! v2rx : float
!   If 1. the end at x=a can rotate
!   If 0. the end at x=a cannot translate along v   
! v1ty : float
!   If 1. the edge at y=0 can translate along v   
!   If 0. the edge at y=0 cannot translate along v   
! v1ry : float
!   If 1. the end at y=0 can rotate
!   If 0. the end at y=0 cannot translate along v   
! v2ty : float
!   If 1. the edge at y=b can translate along v   
!   If 0. the edge at y=b cannot translate along v   
! v2ry : float
!   If 1. the end at y=b can rotate
!   If 0. the end at y=b cannot translate along v   
! w1tx : float
!   If 1. the edge at x=0 can translate along w   
!   If 0. the edge at x=0 cannot translate along w   
! w1rx : float
!   If 1. the end at x=0 can rotate
!   If 0. the end at x=0 cannot translate along w   
! w2tx : float
!   If 1. the edge at x=a can translate along w   
!   If 0. the edge at x=a cannot translate along w   
! w2rx : float
!   If 1. the end at x=a can rotate
!   If 0. the end at x=a cannot translate along w   
! w1ty : float
!   If 1. the edge at y=0 can translate along w   
!   If 0. the edge at y=0 cannot translate along w   
! w1ry : float
!   If 1. the end at y=0 can rotate
!   If 0. the end at y=0 cannot translate along w   
! w2ty : float
!   If 1. the edge at y=b can translate along w   
!   If 0. the edge at y=b cannot translate along w   
! w2ry : float
!   If 1. the end at y=b can rotate
!   If 0. the end at y=b cannot translate along w   

! Written by Saullo Castro, November 2015
! Modified by Guilherme Abreu, February 2016

SUBROUTINE R3SVALD(GRPID, TYPNAM, NITEMS, ARGLIS, NSIZE, ARGVAL, &
                   NWRDA8, ARGCHR, forg, nresp, narg, DR3VAL, senval, ERROR)
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
    !     nresp   input INTEGER        - number of responses
    !     forg    input INTEGER        - type of call
    !                                     = 0 function evaluation
    !                                     = 1 sensitivity evaluation
    !     narg    input INTEGER        - number of arguments needing gradients
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
    USE CPANELBARDELL, ONLY: CALC_K0, CALC_KG0
    IMPLICIT NONE
    
    CHARACTER*8, INTENT(IN) :: TYPNAM, ARGCHR(NWRDA8)
    INTEGER, INTENT(IN) :: forg, nresp, narg
    INTEGER, INTENT(IN) :: GRPID, NITEMS, NSIZE, ARGLIS(NITEMS), NWRDA8
    REAL*8, INTENT(IN) :: ARGVAL(NSIZE)
    INTEGER, INTENT(INOUT) :: ERROR
    REAL*8, INTENT(OUT) :: DR3VAL(*), senval(nresp, narg)
    INTEGER BADTYP
    DATA BADTYP /7554/

    ! Bardell's inputs
    REAL*8 A11, A12, A16, A22, A26, A66
    REAL*8 B11, B12, B16, B22, B26, B66
    REAL*8 D11, D12, D16, D22, D26, D66
    REAL*8 u1tx, u1rx, u2tx, u2rx, u1ty, u1ry, u2ty, u2ry
    REAL*8 v1tx, v1rx, v2tx, v2rx, v1ty, v1ry, v2ty, v2ry
    REAL*8 w1tx, w1rx, w2tx, w2rx, w1ty, w1ry, w2ty, w2ry
    REAL*8 a, b, r, Nxx, Nyy, Nxy
    REAL*8 E1, E2, G12, nu12, nu21, t

    ! MKL inputs
    CHARACTER*1 BALANC, JOBVL, JOBVR, SENSE
    INTEGER NT, nulls, NUM, M, N
    REAL*8, ALLOCATABLE :: K0(:, :), KG0(:, :), K02(:, :), KG02(:, :)
    INTEGER LDA, LDB, LDZ
    
    ! workspace
    INTEGER i, j, id, jd
    INTEGER LWORK
    INTEGER, ALLOCATABLE :: IWORK(:)
    REAL*8, ALLOCATABLE :: WORK(:)
    REAL*8 E11, nu, NULLTOL
    CHARACTER (LEN=5) :: ISOTROPIC
    INTEGER, ALLOCATABLE :: TMP(:)

    LOGICAL debug, exist

    ! MKL outputs
    INTEGER Mout, INFO
    INTEGER, ALLOCATABLE :: IFAIL(:)
    REAL*8, ALLOCATABLE :: EIGVALS(:), EIGVECS(:, :)

    ERROR = 0

    debug = .false.
    IF (debug) THEN
        inquire(file='pcbuck.log', exist=exist)

        IF (exist) THEN
            OPEN(unit=10, file='pcbuck.log', status='old', position='append', action='write')
        ELSE
            OPEN(unit=10, file='pcbuck.log', status='new', action='write')
        END IF
    END IF

    ISOTROPIC = "FALSE"
    
    IF (TYPNAM .eq. 'BUCK_PC') THEN
        IF (debug) THEN
            WRITE(10, *) '! DOUBLE PRECISION ROUTINE'
            WRITE(10, *) ''
            WRITE(10, *) 'GRPID', GRPID
            WRITE(10, *) 'NITEMS', NITEMS
            WRITE(10, *) 'NSIZE', NSIZE
            WRITE(10, *) 'ARGLIS', ARGLIS
            WRITE(10, *) 'NWRDA8', NWRDA8
            WRITE(10, *) 'ERROR', ERROR
            WRITE(10, *) 'nresp', nresp
            WRITE(10, *) 'ARGVAL(1)', ARGVAL(1)
            WRITE(10, *) 'ARGVAL(2)', ARGVAL(2)
        END IF

        BALANC = 'N'
        JOBVL = 'N'
        JOBVR = 'N'
        SENSE = 'N'    

        NUM = 10
        M = 15
        N = 15

        ! Tolerance to consider a zero in K0 and KG0
        NULLTOL = 1.e-15 

        ! Default boundary conditions (simply supported)
        u1tx = 0.
        u1rx = 1.
        u2tx = 0.
        u2rx = 1.
        u1ty = 0.
        u1ry = 1.
        u2ty = 0.
        u2ry = 1.
        v1tx = 0.
        v1rx = 1.
        v2tx = 0.
        v2rx = 1.
        v1ty = 0.
        v1ry = 1.
        v2ty = 0.
        v2ry = 1.
        w1tx = 0.
        w1rx = 1.
        w2tx = 0.
        w2rx = 1.
        w1ty = 0.
        w1ry = 1.
        w2ty = 0.
        w2ry = 1.

        t = ARGVAL(1)     ! Getting t from DRESP3
        a = ARGVAL(2)     ! Getting a from DRESP3
        b = ARGVAL(3)     ! Getting b from DRESP3
        r = ARGVAL(4)     ! Getting r from DRESP3
        E1 = ARGVAL(5)    ! Getting E1 from DRESP3
        E2 = ARGVAL(6)    ! Getting E2 from DRESP3
        G12 = ARGVAL(7)   ! Getting G12 from DRESP3
        nu12 = ARGVAL(8)  ! Getting nu12 from DRESP3
        nu21 = ARGVAL(9)  ! Getting nu21 from DRESP3
        Nxx = ARGVAL(10)  ! Getting Nxx from DRESP3
        Nyy = ARGVAL(11)  ! Getting Nyy from DRESP3
        Nxy = ARGVAL(12)  ! Getting Nxy from DRESP3

        IF (debug) THEN
            WRITE(10, *) '! Input'
            WRITE(10, *) '! DRESP3 arguments'
            WRITE(10, *) 't', ARGVAL(1)
            WRITE(10, *) 'a', ARGVAL(2)
            WRITE(10, *) 'b', ARGVAL(3)
            WRITE(10, *) 'r', ARGVAL(4)
            WRITE(10, *) 'E1', ARGVAL(5)
            WRITE(10, *) 'E2', ARGVAL(6)
            WRITE(10, *) 'G12', ARGVAL(7)
            WRITE(10, *) 'nu12', ARGVAL(8)
            WRITE(10, *) 'nu21', ARGVAL(9)
            WRITE(10, *) 'Nxx', ARGVAL(10)
            WRITE(10, *) 'Nyy', ARGVAL(11)
            WRITE(10, *) 'Nxy', ARGVAL(12)
        END IF
        
        NT = 3*M*N

        ! Calculating ABD
        IF (ISOTROPIC == "TRUE") THEN
            G12 = E11/(2*(1 + nu))

            A11 = E11*t/(1 - nu**2)
            A12 = nu*E11*t/(1 - nu**2)
            A16 = 0
            A22 = E11*t/(1 - nu**2)
            A26 = 0
            A66 = G12*t

            B11 = 0
            B12 = 0
            B16 = 0
            B22 = 0
            B26 = 0
            B66 = 0

            D11 = E11*t**3/(12*(1 - nu**2))
            D12 = nu*E11*t**3/(12*(1 - nu**2))
            D16 = 0
            D22 = E11*t**3/(12*(1 - nu**2))
            D26 = 0
            D66 = G12*t**3/12
        END IF
        
        !nu21 = nu12*(E2/E1)
        
        ! ABD Matrix to Orthotropic Material
        A11 = t*(E1/(1.-nu12*nu21))
        A12 = t*(nu12*E2/(1.-nu12*nu21))
        A16 = 0
        A22 = t*(E2/(1.-nu12*nu21))
        A26 = 0
        A66 = t*G12
        
        B11 = 0
        B12 = 0
        B16 = 0
        B22 = 0
        B26 = 0
        B66 = 0
        
        D11 = ((t**3.)/12.)*(E1/(1.-nu12*nu21))
        D12 = ((t**3.)/12.)*(nu12*E2/(1.-nu12*nu21))
        D16 = 0
        D22 = ((t**3.)/12.)*(E2/(1.-nu12*nu21))
        D26 = 0
        D66 = ((t**3.)/12.)*G12
        
        ! allocating arrays
        ALLOCATE(K0(NT, NT))
        ALLOCATE(KG0(NT, NT))

        IF (debug) THEN
            WRITE(10, *) '! Intermediate'
            WRITE(10, *) 'D11', D11
            WRITE(10, *) 'D12', D12
            WRITE(10, *) 'D22', D22
            WRITE(10, *) 'D66', D66
        END IF
        
        ! constitutive stiffness matrix
        CALL CALC_K0(M, N, K0, a, b, r, &
                     A11, A12, A16, A22, A26, A66, &
                     B11, B12, B16, B22, B26, B66, &
                     D11, D12, D16, D22, D26, D66, &
                     u1tx, u1rx, u2tx, u2rx, u1ty, u1ry, u2ty, u2ry, &
                     v1tx, v1rx, v2tx, v2rx, v1ty, v1ry, v2ty, v2ry, &
                     w1tx, w1rx, w2tx, w2rx, w1ty, w1ry, w2ty, w2ry)

        ! geometric stiffness matrix
        CALL CALC_KG0(M, N, KG0, a, b, Nxx, Nyy, Nxy, &
                      w1tx, w1rx, w2tx, w2rx, w1ty, w1ry, w2ty, w2ry)

        ! removing null rows and columns
        ALLOCATE(TMP(NT)) 
        TMP = 0
        WHERE (ABS(SUM(K0, DIM=1)) <= NULLTOL) TMP = 1
        nulls = SUM(TMP)
    
        ALLOCATE(K02(NT-nulls, NT-nulls))
        ALLOCATE(KG02(NT-nulls, NT-nulls))
        
        jd = 0
        DO j=1, NT
            IF (TMP(j) == 1) THEN
                jd = jd+1
                CYCLE
            END IF
            id = 0
            DO i=1, NT
                IF (TMP(i) == 1) THEN
                    id = id+1
                    CYCLE
                END IF
                K02(i-id, j-jd) = K0(i, j)
                KG02(i-id, j-jd) = KG0(i, j)
            END DO
        END DO
        DEALLOCATE(TMP)
    
        ! allocating arrays
        ALLOCATE(IWORK((NT-nulls)*25))
    
        ! allocating output arrays
        ALLOCATE(EIGVALS(NT-nulls))
        ALLOCATE(EIGVECS(NT-nulls, NT-nulls))
        ALLOCATE(IFAIL(NT-nulls))
    
        LDA = NT-nulls
        LDB = NT-nulls
        LDZ = NT-nulls
        
        EIGVALS = EIGVALS*0
        
        ! Workspace query
        LWORK = -1
        ALLOCATE(WORK(10))    
        IF (debug) THEN
            WRITE(10, *) '! flag 1'
        END IF
        CALL DSYGVX(1, "N", "I", "U", (NT-nulls), KG02, LDB, K02, LDA, &
                    -1.D10, 0, 1, NUM, 0., Mout, EIGVALS, EIGVECS, LDZ, &
                    WORK, LWORK, IWORK, IFAIL, INFO)
        LWORK = WORK(1)
        DEALLOCATE(WORK)
        IF (debug) THEN
            WRITE(10, *) '! flag 2'
        END IF
        ! Eigensolver query
        ALLOCATE(WORK(LWORK))
        CALL DSYGVX(1, "N", "I", "U", (NT-nulls), KG02, LDB, K02, LDA, &
                    -1.D10, 0, 1, NUM, 0., Mout, EIGVALS, EIGVECS, LDZ, &
                    WORK, LWORK, IWORK, IFAIL, INFO)
        DEALLOCATE(WORK)
    
        WHERE(EIGVALS /= 0) EIGVALS = -1/EIGVALS
        
        IF (ABS(EIGVALS(1)) < 1.e-6) THEN
            EIGVALS(1) = 666
        END IF
        
        ! Storing eigenvalues
        DR3VAL(1) = EIGVALS(1)

        DEALLOCATE(K0)
        DEALLOCATE(KG0)
        DEALLOCATE(K02)
        DEALLOCATE(KG02)
        DEALLOCATE(IWORK)
        DEALLOCATE(IFAIL)
        DEALLOCATE(EIGVALS)
        DEALLOCATE(EIGVECS)
    
    ELSE
        ERROR = BADTYP
    END IF

    IF (debug) THEN
        WRITE(10, *) '! Result'
        WRITE(10, *) 'EIGVALS(1)', EIGVALS(1)
    END IF
    IF (debug) THEN
        CLOSE(10)
    END IF
    
END SUBROUTINE
    
