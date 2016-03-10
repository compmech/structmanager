/*
 ****************
 *    ftncalls.h    define macros to facilitate passing character
 *                  strings between Fortran programs and C programs.
 *                  Also, see the description of the _FTN_CALL_TYPE_...
 *                  variables in stdsystm.h and the discussion of
 *                  Fortran-C interlanguage calls in SYSDEV Memo 71-xx.
 ****************
 *
 *    Passing Character Arguments Between C and Fortran
 *
 ****************
 *
 *    NOTE:  In the commentary below, two dots (..) are used as pseudo
 *           comment delimiters instead of slash,asterisk and
 *           asterisk,slash to avoid problems of "nested comments"
 *           in the commentary.
 *
 ****************
 *
 *    For each character string to be passed to a Fortran program,
 *    specify a FTN_CHAR_ARG_DCL_xxx macro in the declaration section
 *    of the code block containing the call.  Because of the way these
 *    macros are implemented for some systems (e.g., UNIX), they must
 *    be the LAST declarations in the code block.  Also, the macros
 *    must apear AFTER the definition of the string being referenced.
 *
 *    Somewhere in open code but before the subroutine call,
 *    place a FTN_CHAR_ARG_DEF or FTN_CHAR_ARG_DEFLEN macro to
 *    fill in the contents of the descriptor declared using the
 *    FTN_CHAR_ARG_DCL_xxx macro.
 *
 *    In the actual call itself, define the calling sequence argument
 *    using a FTN_CHAR_ARG macro with the same arguments used in
 *    the corresponding FTN_CHAR_ARG_DEF macro.
 *
 *             *** IMPORANT NOTE ***
 *    When using the FTN_CHAR_ARG_DCL_.. macros described below,
 *    DO NOT end the macro specifications with a semi-colon.
 *    If these macros generate any statements, they will properly
 *    end these statements with the appropriate terminating
 *    characters.
 *
 *    USAGE:
 *       FTN_CHAR_ARG_DCL_AUTO(descripname,stringname)
 *               to declare a descriptor with "auto" storage class.
 *       FTN_CHAR_ARG_DCL_STATIC(descripname,stringname)
 *               to declare a descriptor with "static" storage class.
 *       FTN_CHAR_ARG_DCL_STD(descripname,stringname)
 *               to declare a descriptor with no special storage class.
 *       FTN_CHAR_ARG_DEF(descripname,stringname)
 *               to fill in a descriptor with the string name and with
 *               the default string length.
 *       FTN_CHAR_ARG_DEFLEN(descripname,stringname,stringlength)
 *               to fill in a descriptor with the string name and with
 *               the actual string length.
 *       FTN_CHAR_ARG(desripname,stringname,stringlength)
 *               to generate the appropriate calling sequence argument
 *               for the specified string.
 *
 *    where
 *
 *       descripname  is the variable name to be used for the string
 *                    descriptor.
 *       stringname   is the variable name of the actual character string.
 *       stringlength is the actual length of character string.
 *
 *    In addition, a CPP variable _FTN_CALL_CHAR_FORMAT will be defined
 *    that can be used to define the appropriate calling sequence
 *    format if the implicit length specification must be used to pass
 *    character string length to the Fortran program instead of
 *    passing an explicit string length variable.  The implicit length
 *    information is REQUIRED if the Fortran routine declares the
 *    character variable as CHARACTER*(*).
 *    This CPP variable will be set to one of the following values:
 *
 *      _FTN_CALL_CHAR_DESCRIP    if string descriptors are used to
 *                                describe Fortran character string
 *                                arguments.
 *                                This is the format, for example, for --
 *                                --  Digital VAX/VMS Fortran
 *                                --  Cray UNICOS Fortran
 *                                --  Watcom F77 for Intel Windows NT
 *      _FTN_CALL_CHAR_ADD_LEN    if string lengths are passed as
 *                                additional calling sequence arguments
 *                                added to the end of the standard
 *                                calling sequence argument list.
 *                                This is the format, for example, for --
 *                                --  Most UNIX systems other than UNICOS
 *                                --  Intel Fortran Reference Compiler
 *                                    for Intel Windows NT
 *                                The type of the string length is defined
 *                                by the FTNIMPLICITLEN typedef.
 *      _FTN_CALL_CHAR_MIXED_LEN  if string lengths are passed as
 *                                additional calling sequence arguments
 *                                immediately following the character
 *                                arguments.
 *                                This is the format, for example, for --
 *                                --  Microsoft PowerStation Fortran
 *                                    for Intel Windows NT
 *                                --  Digital Visual Fortran for Intel
 *                                    Windows NT, assuming that the
 *                                       /iface:mixed_str_len_arg
 *                                    option is used or taken by default.
 *                                The type of the string length is defined
 *                                by the FTNIMPLICITLEN typedef.
 *      _FTN_CALL_CHAR_SHADOW_CLSQ if string lengths (as well as other
 *                                argument lengths) are passed in a
 *                                "shadow" calling sequence arguments
 *                                immediately following the character
 *                                arguments.
 *                                This format is only for use with IBM
 *                                MVS VS/FORTRAN when used with SAS/C.
 *                                This interface is quite complicated when
 *                                Fortran is to be called from C and uses
 *                                the SAS/C "InterLanguage Communication"
 *                                facilities to actually implement the
 *                                calls.  For prototype statements, the
 *                                prototype must NOT describe the arguments
 *                                because of the way the calls are actually
 *                                built.
 *                                The type of the string length is defined
 *                                by the FTNIMPLICITLEN typedef.
 *
 *    The FTNIMPLICITLEN typedef is normally defined to be "int".
 *
 *    Also, if _FTN_CALL_CHAR_FORMAT is set to _FTN_CALL_CHAR_DESCRIP,
 *    the F2CPLEN macro is defined that will extract the string length
 *    information from the descriptor in a way similar to the way the
 *    F2CP macro extracts the actual string pointer from the
 *    descriptor.  Note that this macro is ONLY defined when
 *    _FTN_CALL_CHAR_FORMAT has the value _FTN_CALL_CHAR_DESCRIP.
 *
 *    The recommended way of calling the Fortran routine is to include
 *    an explicit calling sequence argument that has the string length
 *    instead of relying on the implicit length facilities of Fortran.
 *
 *    If the implicit length facilities of Fortran must be used, the
 *    required calling techniques are more complicated than just passing
 *    an explicit calling sequence argument.  The _FTN_CALL_CHAR_FORMAT
 *    variable can be used to construct the proper calling sequence
 *    format as follows:
 *
 *       Assume that Fortran routine XYZ is to be called with
 *       two character arguments, char1 and char2, and three
 *       integer arguments, int1, int2 and int3, and assume that
 *       the Fortran routine starts as follows:
 *
 *           SUBROUTINE XYZ ( CHAR1, INT1, INT2, CHAR2, INT3 )
 *           INTEGER INT1, INT2, INT3
 *           CHARACTER*(*) CHAR1, CHAR2
 *           ...
 *
 *       The C code must include the following segments:
 *
 *           ...
 *           .. Declare FORTRAN routine name and prototype ..
 *           #if defined(_UC_FTN_NAME)
 *           .. Upper case name is correct ..
 *           #elif defined(_LC_FTN_NAME)
 *           #define XYZ    xyz
 *           #elif defined(_TU_FTN_NAME)
 *           #define XYZ    xyz_
 *           #elif defined(_DOS_PRAGMA_FTN_NAME)
 *           #pragma aux XYZ "XYZ";
 *           #endif
 *           #if _FTN_CALL_CHAR_FORMAT == _FTN_CALL_CHAR_DESCRIP
 *           void _FTN_CALL_TYPE_PROTO XYZ ( CHARACTER,
 *                      INTEGER *, INTEGER *,
 *                      CHARACTER, INTEGER * );
 *           #elif _FTN_CALL_CHAR_FORMAT == _FTN_CALL_CHAR_ADD_LEN
 *           void _FTN_CALL_TYPE_PROTO XYZ ( CHARACTER,
 *                      INTEGER *, INTEGER *,
 *                      CHARACTER, INTEGER *,
 *                      FTNIMPLICITLEN, FTNIMPLICITLEN );
 *           #elif _FTN_CALL_CHAR_FORMAT == _FTN_CALL_CHAR_MIXED_LEN
 *           void _FTN_CALL_TYPE_PROTO XYZ ( CHARACTER, FTNIMPLICITLEN,
 *                      INTEGER *, INTEGER *,
 *                      CHARACTER, FTNIMPLICITLEN, INTEGER * );
 *           #elif _FTN_CALL_CHAR_FORMAT == _FTN_CALL_CHAR_SHADOW_CLSQ
 *           void _FTN_CALL_TYPE_PROTO XYZ ( );
 *           #endif
 *
 *           ...
 *           .. Declare FORTRAN CHARACTER string descriptors,
 *           .. where xxx is one of AUTO, STATIC or STD.
 *           ..
 *           char char1[...];
 *           char char2[...];
 *           FTNIMPLICITLEN char1_len, char2_len;
 *           ...
 *           .. Declare the other variables ..
 *           INTEGER int1, int2, int3;
 *           .. Other declarations ..
 *           ...
 *           FTN_CHAR_ARG_DCL_xxx(char1_descrip,char1)
 *           FTN_CHAR_ARG_DCL_xxx(char2_descrip,char2)
 *
 *           ...
 *           .. Initialize FORTRAN CHARACTER string descriptors ..
 *           char1_len = ...
 *           char2_len = ...
 *           FTN_CHAR_ARG_DEFLEN(char1_descrip,char1,char1_len);
 *           FTN_CHAR_ARG_DEFLEN(char2_descrip,char2,char2_len);
 *
 *           ...
 *           .. Call the FORTRAN routine ..
 *           #if ( _FTN_CALL_CHAR_FORMAT == _FTN_CALL_CHAR_DESCRIP ) || \
 *               ( _FTN_CALL_CHAR_FORMAT == _FTN_CALL_CHAR_MIXED_LEN ) || \
 *               ( _FTN_CALL_CHAR_FORMAT == _FTN_CALL_CHAR_SHADOW_CLSQ )
 *           _FTN_CALL_TYPE_CALL XYZ (
 *                 FTN_CHAR_ARG(char1_descrip,char1,char1_len),
 *                 &int1, &int2,
 *                 FTN_CHAR_ARG(char2_descrip,char2,char2_len),
 *                 &int3 );
 *           #elif _FTN_CALL_CHAR_FORMAT == _FTN_CALL_CHAR_ADD_LEN
 *           _FTN_CALL_TYPE_CALL XYZ (
 *                 FTN_CHAR_ARG(char1_descrip,char1,char1_len),
 *                 &int1, &int2,
 *                 FTN_CHAR_ARG(char2_descrip,char2,char2_len),
 *                 &int3,
 *                 char1_len, char2_len );
 *           #endif
 *
 ****************
 *
 *    If C programs are not passed character strings from Fortran
 *    programs, other than declaring the names properly using the
 *    _UC_FTN_NAME, _LC_FTN_NAME, _TU_FTN_NAME and
 *    _DOS_PRAGMA_FTN_NAME CPP variables and including
 *    _FTN_CALL_TYPE_ENTRY in the function declaration, no special
 *     calling sequence modifications are necessary.
 *
 ****************
 *
 *    If C programs are passed character strings from Fortran but
 *    do not require the implicit character length specifications,
 *    the use of the _FTN_CALL_CHAR_FORMAT CPP variable is required
 *    but the code formats are simpler than for those C programs that
 *    require the implicit character length specifications.
 *    routines, suggested coding is as follows (note that although this
 *    suggested coding is similar to that given below for the routines
 *    that require the implicit length, there are significant and
 *    important differences).
 *
 *       Assume that a Fortran routine calls C routine ABC with
 *       two character arguments, char1 and char2, and three
 *       integer arguments, int1, chr1len and chr2len, and assume that
 *       the Fortran routine includes code as follows:
 *
 *           SUBROUTINE XYZ ( ... )
 *           ...
 *           CHARACTER CHAR1*(n1), CHAR2*(n2)
 *           ...
 *           CALL ABC ( INT1, CHAR1, LEN(CHAR1), CHAR2, LEN(CHAR2) )
 *
 *       The C routine must include the following code segments:
 *
 *           #include "ftncalls.h"
 *
 *           .. Declare C routine name as FORTRAN callable ..
 *           #if defined(_UC_FTN_NAME)
 *           .. Upper case name is correct ..
 *           #elif defined(_LC_FTN_NAME)
 *           #define ABC    abc
 *           #elif defined(_TU_FTN_NAME)
 *           #define ABC    abc_
 *           #elif defined(_DOS_PRAGMA_FTN_NAME)
 *           #pragma aux ABC "ABC";
 *           #endif
 *           ...
 *           .. Define the entry code properly ..
 *           #if _FTN_CALL_CHAR_FORMAT != _FTN_CALL_CHAR_MIXED_LEN
 *           void _FTN_CALL_TYPE_ENTRY ABC ( INTEGER *int1,
 *                      CHARACTER char1, INTEGER *char1len,
 *                      CHARACTER char2, INTEGER *char2len )
 *           #else _FTN_CALL_CHAR_FORMAT == _FTN_CALL_CHAR_MIXED_LEN
 *           void _FTN_CALL_TYPE_ENTRY ABC ( INTEGER *int1,
 *                      CHARACTER char1, FTNIMPLICITLEN char1_len, INTEGER *char1len,
 *                      CHARACTER char2, FTNIMPLICITLEN char2_len, INTEGER *char2len )
 *           #endif   .. _FTN_CALL_CHAR_FORMAT ..
 *
 *           ... The variables char1len and char2len have the explicitly
 *           ... specified lengths associated with the char1 and char2
 *           ... parameters.  Note that if the Fortran code includes a
 *           ...  sub-string specification on the character variable
 *           ...  passed to the C program, the Fortran code must be changed
 *           ...  to (or equivalent):
 *           ...   CALL ABC ( INT1, CHAR1(L1:L2), L2-L1+1,
 *           ...  *           CHAR2(L3:L4), L4-L3+1 )
 *           ... The explicit char1len char2len length values, as received
 *           ... by the C program, would still have the proper length values.
 *
 *           Note that, in the
 *                 _FTN_CALL_CHAR_FORMAT == _FTN_CALL_CHAR_MIXED_LEN
 *           code section, the char1_len and char2_len calling sequence
 *           arguments should be ignored in the main code body unless
 *           the code segment that uses them is wrapped in
 *             #if _FTN_CALL_CHAR_FORMAT == _FTN_CALL_CHAR_MIXED_LEN
 *              ... code segment using char1_len and char2_len ...
 *             #endif
 *
 ****************
 *
 *    If C programs must accept implicit character length specifications
 *    from Fortran programs, suggested coding is as follows (note that
 *    although this suggested coding is similar to that given above for
 *    the routines that do not require the implicit length, there are
 *    significant and important differences).
 *
 *       Assume that a Fortran routine calls C routine ABC with
 *       two character arguments, char1 and char2, and three
 *       integer arguments, int1, int2 and int3, and assume that
 *       the Fortran routine includes code as follows:
 *
 *           SUBROUTINE XYZ ( ... )
 *           ...
 *           CHARACTER CHAR1*(n1), CHAR2*(n2)
 *           ...
 *           CALL ABC ( INT1, CHAR1, INT2, CHAR2, INT3 )
 *
 *       The C routine must include the following code segments
 *       (or equivalent):
 *
 *           #include "ftncalls.h"
 *
 *           .. Declare C routine name as FORTRAN callable ..
 *           #if defined(_UC_FTN_NAME)
 *           .. Upper case name is correct ..
 *           #elif defined(_LC_FTN_NAME)
 *           #define ABC    abc
 *           #elif defined(_TU_FTN_NAME)
 *           #define ABC    abc_
 *           #elif defined(_DOS_PRAGMA_FTN_NAME)
 *           #pragma aux ABC "ABC";
 *           #endif
 *           ...
 *           .. Define the entry code properly ..
 *           #if _FTN_CALL_CHAR_FORMAT == _FTN_CALL_CHAR_DESCRIP
 *           void _FTN_CALL_TYPE_ENTRY ABC ( INTEGER *int1,
 *                      CHARACTER char1, INTEGER *int2,
 *                      CHARACTER char2, INTEGER *int3 )
 *           #elif _FTN_CALL_CHAR_FORMAT == _FTN_CALL_CHAR_ADD_LEN
 *           void _FTN_CALL_TYPE_ENTRY ABC ( INTEGER *int1,
 *                      CHARACTER char1, INTEGER *int2,
 *                      CHARACTER char2, INTEGER *int3,
 *                      FTNIMPLICITLEN char1_len, FTNIMPLICITLEN char2_len )
 *           #elif _FTN_CALL_CHAR_FORMAT == _FTN_CALL_CHAR_MIXED_LEN
 *           void _FTN_CALL_TYPE_ENTRY ABC ( INTEGER *int1,
 *                      CHARACTER char1, FTNIMPLICITLEN char1_len, INTEGER *int2,
 *                      CHARACTER char2, FTNIMPLICITLEN char2_len, INTEGER *int3 )
 *           #elif _FTN_CALL_CHAR_FORMAT == _FTN_CALL_CHAR_SHADOW_CLSQ
 *           void _FTN_CALL_TYPE_ENTRY ABC ( INTEGER *int1,
 *                      CHARACTER char1, INTEGER *int2,
 *                      CHARACTER char2, INTEGER *int3,
 *                      INTEGER *p_int1_len, INTEGER *p_char1_len,
 *                      INTEGER *p_int2_len, INTEGER *p_char2_len,
 *                      INTEGER *p_int3_len )
 *           #endif   .. _FTN_CALL_CHAR_FORMAT ..
 *           {  .. Declare the local variables ..
 *           #if _FTN_CALL_CHAR_FORMAT == _FTN_CALL_CHAR_DESCRIP
 *              auto FTNIMPLICITLEN char1_len = F2CPLEN(char1);
 *              auto FTNIMPLICITLEN char2_len = F2CPLEN(char2);
 *           #elif _FTN_CALL_CHAR_FORMAT == _FTN_CALL_CHAR_SHADOW_CLSQ
 *              auto FTNIMPLICITLEN char1_len = (FTNIMPLICITLEN) *p_char1_len;
 *              auto FTNIMPLICITLEN char2_len = (FTNIMPLICITLEN) *p_char2_len;
 *           #endif   .. _FTN_CALL_CHAR_FORMAT ..
 *
 *           ... The variables char1_len and char2_len have the
 *           ... implicit lengths associated with the char1 and char2
 *           ... parameters.  Note that this method works even if the
 *           ... Fortran code includes a sub-string specification on
 *           ... the character variable passed to the C program, i.e.,
 *           ... if the Fortran call was
 *           ...   CALL ABC ( INT1, CHAR1(L1:L2), INT2, CHAR2(L3:L4), INT3 )
 *           ... the implicit length values, as received by the C program,
 *           ... would be (L2-L1+1) for char1_len and (L4-L3+1) for
 *           ... char2_len.
 *
 ****************
 */

#ifndef _FTN_CALL_ARG_H
#define _FTN_CALL_ARG_H

#include "stdmsc.h"

#define _FTN_CHAR_ARG_LEN 512

#ifdef FTN_CHAR_ARG_DCL_AUTO
#undef FTN_CHAR_ARG_DCL_AUTO
#endif
#ifdef FTN_CHAR_ARG_DCL_STATIC
#undef FTN_CHAR_ARG_DCL_STATIC
#endif
#ifdef FTN_CHAR_ARG_DCL_STD
#undef FTN_CHAR_ARG_DCL_STD
#endif
#ifdef FTN_CHAR_ARG_DEF
#undef FTN_CHAR_ARG_DEF
#endif
#ifdef FTN_CHAR_ARG_DEFLEN
#undef FTN_CHAR_ARG_DEFLEN
#endif
#ifdef FTN_CHAR_ARG
#undef FTN_CHAR_ARG
#endif
#ifdef _FTN_CALL_CHAR_FORMAT
#undef _FTN_CALL_CHAR_FORMAT
#endif
#ifdef _FTN_CALL_CHAR_DESCRIP
#undef _FTN_CALL_CHAR_DESCRIP
#endif
#ifdef _FTN_CALL_CHAR_ADD_LEN
#undef _FTN_CALL_CHAR_ADD_LEN
#endif
#ifdef _FTN_CALL_CHAR_MIXED_LEN
#undef _FTN_CALL_CHAR_MIXED_LEN
#endif
#ifdef _FTN_CALL_CHAR_SHADOW_CLSQ
#undef _FTN_CALL_CHAR_SHADOW_CLSQ
#endif
#ifdef FTNIMPLICITLEN_TYPE
#undef FTNIMPLICITLEN_TYPE
#endif

#define _FTN_CALL_CHAR_DESCRIP       1
#define _FTN_CALL_CHAR_ADD_LEN       2
#define _FTN_CALL_CHAR_MIXED_LEN     3
#define _FTN_CALL_CHAR_SHADOW_CLSQ   4

#if (defined(_NT) || defined(_WINDOWS) || defined(_DOS)) && defined(__WATCOMC__)
/* Define the macros for Watcom C for Intel platforms. */
#define _FTN_CALL_CHAR_FORMAT    _FTN_CALL_CHAR_DESCRIP
#define FTN_CHAR_ARG_DCL_AUTO(defname,stringname) \
    auto struct _string_descrip defname;
#define FTN_CHAR_ARG_DCL_STATIC(defname,stringname) \
    static struct _string_descrip defname = \
    { stringname, sizeof(stringname)-1 };
#define FTN_CHAR_ARG_DCL_STD(defname,stringname) \
    struct _string_descrip defname;
#define FTN_CHAR_ARG_DEF(defname,stringname) \
    { defname.string = stringname; \
      defname.string_length = _FTN_CHAR_ARG_LEN; }
#define FTN_CHAR_ARG_DEFLEN(defname,stringname,stringlength) \
    { defname.string = stringname; \
      defname.string_length = stringlength; }
#define FTN_CHAR_ARG(defname,stringname,stringlength) &defname
#define F2CPLEN(fp)  (FTNIMPLICITLEN) fp->string_length
#elif defined(_VMS) || defined(_OPENVMS)
/* Define the macros for Digital VMS and OpenVMS for both VAX and Alpha AXP. */
#include <descrip.h>
#define _FTN_CALL_CHAR_FORMAT    _FTN_CALL_CHAR_DESCRIP
#define FTN_CHAR_ARG_DCL_AUTO(defname,stringname) \
    auto struct dsc$descriptor_s defname;
#define FTN_CHAR_ARG_DCL_STATIC(defname,stringname) \
    static $DESCRIPTOR(defname,stringname);
#define FTN_CHAR_ARG_DCL_STD(defname,stringname) \
    struct dsc$descriptor_s defname;
#define FTN_CHAR_ARG_DEF(defname,stringname) \
    { defname.dsc$w_length = _FTN_CHAR_ARG_LEN; \
      defname.dsc$b_dtype = DSC$K_DTYPE_T; \
      defname.dsc$b_class = DSC$K_CLASS_S; \
      defname.dsc$a_pointer = stringname; }
#define FTN_CHAR_ARG_DEFLEN(defname,stringname,stringlength) \
    { defname.dsc$w_length = stringlength; \
      defname.dsc$b_dtype = DSC$K_DTYPE_T; \
      defname.dsc$b_class = DSC$K_CLASS_S; \
      defname.dsc$a_pointer = stringname; }
#define FTN_CHAR_ARG(defname,stringname,stringlength) &defname
#define F2CPLEN(fp)  (FTNIMPLICITLEN) fp->dsc$w_length
#elif defined(_UNICOS) || defined(_UNICOSC90) || defined(_UNICOSTS)
#include <fortran.h>
#define _FTN_CALL_CHAR_FORMAT    _FTN_CALL_CHAR_DESCRIP
#define FTN_CHAR_ARG_DCL_AUTO(defname,stringname) \
    auto _fcd defname = _cptofcd(stringname,_FTN_CHAR_ARG_LEN);
#define FTN_CHAR_ARG_DCL_STATIC(defname,stringname) \
    static _fcd defname = _cptofcd(stringname,sizeof(stringname)-1);
#define FTN_CHAR_ARG_DCL_STD(defname,stringname) \
    _fcd defname = _cptofcd(stringname,_FTN_CHAR_ARG_LEN);
#define FTN_CHAR_ARG_DEF(defname,stringname)
#define FTN_CHAR_ARG_DEFLEN(defname,stringname,stringlength) \
    defname = _cptofcd(stringname,stringlength)
#define FTN_CHAR_ARG(defname,stringname,stringlength)  defname
#define F2CPLEN(fp)  (FTNIMPLICITLEN)_fcdlen(fp)
#elif (defined(_MSC_VER) && defined(_WIN32)  && defined(_M_IX86) && \
       !defined(__ICL) && !defined(NO_FTN_CVF)) || \
      (defined(_MSC_VER) && defined(_WIN64) && \
       !defined(__ICL) && !defined(__INTEL_COMPILER) \
        && !defined(NO_FTN_CVF)) || \
      ((defined(__ICL) || defined(__INTEL_COMPILER)) && \
       (defined(FTN_MIXEDLEN) || defined(FTN_CVF)) && !defined(NO_FTN_CVF))
  /* Compiling for Intel Windows NT using Microsoft Visual C.
   * Also assume that Digital Visual Fortran for Intel will be used
   * and that calls between C and Fortran will be in Microsoft
   * Powerstation Fortran format, i.e., __stdcall (causes file name
   * mangling, that is, adding @nn to external name where nn is the
   * length of the calling sequence in bytes) and with implicit character
   * length arguments mixed in-line with the rest of the calling
   * sequence arguments.  This also requires that the following
   * compiler options be specified (or taken by default) for Digital
   * Visual Fortran:
   *     /iface:(default,mixed_str_len_arg)
   * This mode is also established when using the Intel Compilers and
   * when -DFTN_MIXEDLEN or -DFTN_CVF is specified.
   */
#define _FTN_CALL_CHAR_FORMAT    _FTN_CALL_CHAR_MIXED_LEN
#define FTN_CHAR_ARG_DCL_AUTO(defname,stringname)
#define FTN_CHAR_ARG_DCL_STATIC(defname,stringname)
#define FTN_CHAR_ARG_DCL_STD(defname,stringname)
#define FTN_CHAR_ARG_DEF(defname,stringname)
#define FTN_CHAR_ARG_DEFLEN(defname,stringname,stringlength)
#define FTN_CHAR_ARG(defname,stringname,stringlength)  \
    stringname, (FTNIMPLICITLEN) stringlength
#elif defined(I370)
  /* Compiling for IBM MVS using SAS/C compiler.
   * For SAS/C, those functions that pass character arguments to
   * Fortran routines (or routines that require a Fortran style
   * calling sequence) must be declared as __FORTRAN so that the
   * Interlanguage Communications processing will build the proper
   * the proper calling sequence format.  This declaration is only
   * required on the prototype statement.  The function declarations
   * for the C functions that accept Fortran calls do not require
   * any specific declarations except for defining the calling
   * sequence so that any implicit CHARACTER argument length values
   * can be obtained.
   */
#define _FTN_CALL_CHAR_FORMAT    _FTN_CALL_CHAR_SHADOW_CLSQ
#define FTNIMPLICITLEN_TYPE
typedef INTEGER FTNIMPLICITLEN;
#define FTN_CHAR_ARG_DCL_AUTO(defname,stringname)
#define FTN_CHAR_ARG_DCL_STATIC(defname,stringname)
#define FTN_CHAR_ARG_DCL_STD(defname,stringname)
#define FTN_CHAR_ARG_DEF(defname,stringname)
#define FTN_CHAR_ARG_DEFLEN(defname,stringname,stringlength)
#define FTN_CHAR_ARG(defname,stringname,stringlength)  \
    _STRING(stringname,stringlength)
#else
/* Define the macros for the (fairly) normal UNIX convention of simply
 * passing a pointer to the character string.
 */
#define _FTN_CALL_CHAR_FORMAT    _FTN_CALL_CHAR_ADD_LEN
# if defined(_UNIX) && \
     ( defined (_HPUX) || defined(_HPUX_11) || defined(_HPUX_IA64) )
# define FTNIMPLICITLEN_TYPE
 typedef long FTNIMPLICITLEN;
# endif
# if (defined(_NT) || defined(_WINDOWS)) && defined(_8664NT)
# define FTNIMPLICITLEN_TYPE
typedef __int64 FTNIMPLICITLEN;
# endif
# if defined(_8664LINUX) && (defined(_ECL) || defined(__INTEL_COMPILER))
# define FTNIMPLICITLEN_TYPE
typedef __int64 FTNIMPLICITLEN;
# endif
#define FTN_CHAR_ARG_DCL_AUTO(defname,stringname)
#define FTN_CHAR_ARG_DCL_STATIC(defname,stringname)
#define FTN_CHAR_ARG_DCL_STD(defname,stringname)
#define FTN_CHAR_ARG_DEF(defname,stringname)
#define FTN_CHAR_ARG_DEFLEN(defname,stringname,stringlength)
#define FTN_CHAR_ARG(defname,stringname,stringlength)  stringname
#endif

#if !defined(FTNIMPLICITLEN_TYPE)
 typedef int FTNIMPLICITLEN;
#else
# undef FTNIMPLICITLEN_TYPE
#endif

#endif   /* _FTN_CALL_ARG_H */
