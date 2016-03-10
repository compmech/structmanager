subroutine R3SGRT(GRPID, TYPNAM, nresp, grdtyp, ERROR)
    !  ----------------------------------------------------------------------
    ! 
    !      PURPOSE: VERIFY THE EXTERNAL RESPONSE TYPE
    ! 
    !      GRPID   input integer        - Group ID
    !      TYPNAM  input character*8    - Name of external response type
    !      nresp   outpt integer        - number of responses for this dresp3
    !      grdtyp  outpt integer        - integer array of length nresp
    !                                    indicating how gradients are to be
    !                                    computed
    !              = 1 user to supply analytic gradients
    !                  varies during approx. optimization
    !              = 2 user to supply analytic gradients
    !                  invariant during approx. optimization
    !              = 3 finite difference technique to provide gradients
    !                  varies during approx. optimization
    !              = 4 finite difference technique to provide gradients
    !                  invariant during approx. optimization
    ! 
    !      ERROR   input/output integer -error code for the call.
    ! 
    !    Method
    !       Match the user input: typnam with the list of available
    !       external response types. Once a match is found, nresp and grdtyp
    !       are set.  If no match is found, set error code.
    ! 
    !    Called by
    !              R3CGRT
    ! 
    !    NOTE:
    !      The writer of this routine is responsible to specify
    !      NTYPES and R3TYPE.
    !  ----------------------------------------------------------------------
    ! 
    !      VARIABLES PASSED IN/out
    ! 
    integer GRPID, ERROR, nresp
    integer grdtyp(*)
    character*8 TYPNAM
    !
    ! LOCAL VARIABLES
    !
    integer NTYPES, BADTYP
    parameter(NTYPES=4)
    CHARACTER*8 R3TYPE(NTYPES)
    !
    data BADTYP/7554/
    data R3TYPE/'METHOD1'/
 
    ERROR = 0
    do ITYPE = 1, NTYPES
        if (TYPNAM .eq. R3TYPE(ITYPE)) then
            nresp = 1
            grdtyp(1) = 3
            goto 200
        end if
    end do
    ERROR = BADTYP
200 continue
    return
end subroutine r3sgrt
