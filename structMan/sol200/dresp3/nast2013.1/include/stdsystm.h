/*
** stdsystm.h
**
** Operating system defines for MSC/NASTRAN & MSC/EMAS.
**
** Author Change Log:
**  7/ 8/04 jas  Add support for _stdcall when using Intel compilers
**  7/ 7/04 jjg  Add support for _SINGLE mode for Itanium Linux
**  5/13/04 jas  Add support for _SINGLE mode for Itanium Windows
**  8/11/03 jas  Add support for 64-bit HPUX (using __LP64__) and
**               update 64-bit IRIX to include INTEGER8 definitions
**  2/25/03 dpl  Add support for 64-bit Solaris (using __sparcv9)
**  2/25/02 jas  Correct A4 memory leak on UNICOS
** 11/01/01 jas  Add support for Intel compilers on 32-bit Linux
**  9/17/01 jas  Add support for lower-case FORTRAN names w/o underscore
**  9/12/01 jas  Add support for 64-bit IBM AIX system
**  4/16/01 jas  Add support for HPUX on 64-bit Intel Architecture
** 12/01/99 jas  Add support for Windows on 64-bit Intel Architecture
**  3/24/99 jas  Add support for 64-bit Solaris system.
**  3/23/99 jas  Add support for 32-bit NEC SuperUX
** 10/16/98 jas  Add ASCII_CHARSET, EBCDIC_CHARSET, ... definitions,
**               add LINUX support
**  9/16/98 jas  Add _FTN_CALL_TYPE_... definitions.
**  2/25/98 dnl  Add INTEGER_MAX support.
** 12/01/97 dnl  Make _IRIX32/_UNICOSJ90 changes
** 10/22/97 jas  Add support for Hitachi OSF
**  4/18/96 jas  Add additional defines for Intel and Visual C for NT.
** 11/08/95 dnl  Add all MSCFPP defines.
**  8/ 8/95 jas  Fix support for PC (Watcom compilers) to properly
**               handle CHARACTER data types.
** 11/29/94 jas  Add additional support for NEC SX by allowing
**               platform specific INTEGER, etc. specifications
**               in conjunction with stdmsc.h and stdaries.h.
** 11/15/94 jas  Add support for PC (Watcom compilers) and NEC SX.
** 05/11/94 jas  Add back include of float.h if not sgi.
** 05/09/94 jas  Created to support both stdaries.h and stdmsc.h
*/
#ifndef STDSYSTEM_H
#define STDSYSTEM_H

/*
** Clear all the defines that only this file should make.
*/
#ifdef _TU_FTN_NAME
# undef _TU_FTN_NAME
#endif

#ifdef _UC_FTN_NAME
# undef _UC_FTN_NAME
#endif

#ifdef _ALIGN_DATA
# undef _ALIGN_DATA
#endif

#ifdef _DOS_PRAGMA_FTN_NAME
# undef _DOS_PRAGMA_FTN_NAME
#endif

#ifdef ALIGN_DOUBLE_BNDRY
# undef ALIGN_DOUBLE_BNDRY
#endif

/* Do not undefine _DOUBLE for NEC SuperUX
** The 32-bit NEC system needs this.
*/
#if defined(_DOUBLE) && !defined(SX)
# undef _DOUBLE
#endif

/*
** Do not undefine _SINGLE for Alpha, Solaris or Itanium (IA64).
** The 64-bit (_SINGLE) ALPHA, Solaris and Itanium Windows systems need this.
**
*/
#if defined(__alpha) && !defined(vms) && !defined(_M_ALPHA)
/* Have possible 64-bit ALPHA system. */
#elif defined(__sun) && defined(__SVR4)     /* for _SOLARIS     modei8 all platforms */
/* Have possible 64-bit Solaris system. */
#elif (defined(__ICC) || defined(__INTEL_COMPILER)) && \
    !defined(__i386) && defined(__linux) && !defined(__ia64)
/* Have possible 64-bit x8664 ILP64/I8 system. */
#elif (defined(__ECC) || defined(__INTEL_COMPILER)) \
     && defined(__linux) && defined(__ia64)
/* Have possible 64-bit Itanium ILP64/I8 system. */
#elif defined(_AIX) && (defined(__64BIT__) || defined(_AIX64))
/* Have possible 64-bit AIX ILP64/I8 system. */
#elif defined(_WIN64)
/* The above allows WINdows to be 64 bits. */
#elif (defined(__INTEL_COMPILER) || defined(__ECL)) && defined(_WIN64)
/* Have possible 64-bit Itanium system or 8664 (EM64T/AMD64) system. */
#elif defined(_IRIX64)
/* Have possible IRIX64 ILP64/I8 system. */
#elif defined(__hpux) && !defined(__ia64)
/* Have possible HP-UX PA-RISC ILP64/I8 systems. */
#elif defined(__hpux) && defined(__ia64)
/* Have possible HP-UX Itanium ILP64/I8 systems. */
#else
#if defined( _SINGLE )
# undef _SINGLE
#endif
#endif

#if defined( _IEEEFP )
# undef _IEEEFP
#endif

#if defined( _CRAYFP )
# undef _CRAYFP
#endif

#if defined( _VAXFP )
# undef _VAXFP
#endif

#if defined( _LITTLE )
# undef _LITTLE
#endif

#if defined( _BIG )
# undef _BIG
#endif

#if defined( _VECTOR )
# undef _VECTOR
#endif

#if defined DEFINED_INTEGER_TYPES
# undef DEFINED_INTEGER_TYPES
#endif

#if defined DEFINED_CHARACTER_TYPES
# undef DEFINED_CHARACTER_TYPES
#endif

#if defined DEFINED_REAL_TYPES
# undef DEFINED_REAL_TYPES
#endif

#if defined DEFINED_PRECISION_TYPES
# undef DEFINED_PRECISION_TYPES
#endif

/* The _FTN_CALL_TYPE_...
 * variables are used to set the proper C prototype and
 * entry (function declaration) types for the various
 * platforms to handle Fortran->C and C->Fortran calls
 * properly.  For most platforms, these macros are NULL.
 * The variables and their use are:
 *     _FTN_CALL_TYPE_PROTO   is used to specify the proper call
 *                            declaration for use with prototype
 *                            statements defining the Fortran routines
 *                            routines to be called.
 *     _FTN_CALL_TYPE_ENTRY   is used to specify the proper call
 *                            declaration for use with the function
 *                            header for Fortran-callable C routines.
 *     _FTN_CALL_TYPE_CALL    is used to specify the proper call
 *                            declaration for use with the actual calls
 *                            to Fortran routines (or to Fortran-callable
 *                            C routines).
 */
#if defined _FTN_CALL_TYPE_PROTO
# undef _FTN_CALL_TYPE_PROTO
#endif
#if defined _FTN_CALL_TYPE_ENTRY
# undef _FTN_CALL_TYPE_ENTRY
#endif
#if defined _FTN_CALL_TYPE_CALL
# undef _FTN_CALL_TYPE_CALL
#endif

/*  Only one of ASCII_CHARSET, EBCDIC_CHARSET and UNICODE_CHARSET
 *  can be defined.
 */
#ifdef ASCII_CHARSET
#undef ASCII_CHARSET
#endif
#ifdef EBCDIC_CHARSET
#undef EBCDIC_CHARSET
#endif
#ifdef UNICODE_CHARSET
#undef UNICODE_CHARSET
#endif

/*
** Define various and sundry OS related items.
*/
#if defined(_UNICOS)
/* Set the necessary defines for Cray UNICOS systems. */
# define _UC_FTN_NAME
# include <fortran.h>
# if !defined(_UNIX)
#  define _UNIX
# endif
# define _SINGLE
# define _BIG
# define _VECTOR
# if defined(_CRAYIEEE)
#   define _UNICOSTS
#   define _IEEEFP
#   ifdef _UNICOSJ90
#    undef _UNICOSJ90
#   endif
#   ifdef _UNICOSC90
#    undef _UNICOSC90
#   endif
# else
#   ifdef _UNICOSTS
#    undef _UNICOSTS
#   endif
#   define _CRAYFP
# endif

# define DEFINED_CHARACTER_TYPES
# define CHARACTER            _fcd
# define F2CP( fp ) _fcdtocp( fp )
# define CP2F( cp, len ) _cptofcd( cp, len )
# define DEFINED_PRECISION_TYPES
# define MACHINEPRECISION     float
# define MACHINEPRECISION_float
# define DOUBLEPRECISION      long double
/*
** This _should_ be done, but connect(2) breaks in <sys/socket.h>
** #ifndef _ANSI_PROTO
** #define _ANSI_PROTO
** #endif
*/
#endif   /* UNICOS */

#if defined(_UNICOSX1)
/* Set the necessary defines for Cray UNICOS/MP X1 systems. */
#  if defined(_UC_FTN_NAME)
#   undef _UC_FTN_NAME
#  endif
#  if defined(_LC_FTN_NAME)
#   undef _LC_FTN_NAME
#  endif    /* defined(_LC_FTN_NAME) */
#  if ! defined(_TU_FTN_NAME)
#   define _TU_FTN_NAME
#  endif    /* ! defined(_TU_FTN_NAME) */
#  ifndef _FCD_DEFINED
#   define _FCD_DEFINED
#   define _fcd               char *
#  endif /* _FCD_DEFINED */

#  include <fortran.h>
#  if !defined(_UNIX)
#   define _UNIX
#  endif
#  define _DOUBLE
#  define _IEEEFP
#  define _BIG
#  define _VECTOR
#  define DEFINED_PRECISION_TYPES
#  define MACHINEPRECISION    double
#  define MACHINEPRECISION_double
#  define DOUBLEPRECISION     double
#  define DEFINED_INTEGER_TYPES
#  define A4CHAR;             int
#  define BOOLEAN             int
#  define LOGICAL             int
#  define UINTEGER            unsigned int
#  define INTEGER             int
#  define INTEGER_int
#  define INTEGER_MAX  LONG_MAX
#  define UINTEGER_MAX ULONG_MAX
/*  For 64bit memory offsets ... */
#  define INTEGER8            long
#  define UINTEGER8           unsigned long
#  if defined(_PTR64)
#   undef _PTR64
#  endif
#  define _PTR64 1
#  define F2CP( fp ) fp
#  define CP2F( cp, len ) cp
/*
** This _should_ be done, but connect(2) breaks in <sys/socket.h>
** #ifndef _ANSI_PROTO
** #define _ANSI_PROTO
** #endif
*/
#endif   /* UNICOSX1 */

#if defined( vms )
/* Set the necessary defines for Digital VMS systems. */

# define _UC_FTN_NAME
# define DEFINED_CHARACTER_TYPES
# include <descrip.h>
# define F2CP( fp ) fp->dsc$a_pointer
  typedef struct dsc$descriptor_s *CHARACTER;
# if !defined(SCOPE_CP2F)
#  define SCOPE_CP2F extern
# endif
  SCOPE_CP2F CHARACTER cp2f( char *cp, int len );
# define CP2F( cp, len ) cp2f( cp, len )
   /* Add these lines to increase performance if
    * platform can byte-address Hollerith arrays
    * Note that this is only valid in _DOUBLE mode.
    */
# define A42CP( len, a4p ) ( (char *)a4p )
# define A4CP_FREE( ptr )
# define CP2A4( len, cp ) ( (A4CHAR *)cp )

# define unlink(file) remove(file)

# if !defined(_VMS)
#  define _VMS
# endif
# if defined( VAX )
#  if !defined(_VAXVMS)
#   define _VAXVMS
#  endif
#  define _VAXFP
# else
#  if !defined(_OPENVMS)
#   define _OPENVMS
#  endif    /* !defined(_OPENVMS) */
#  define _IEEEFP
# endif    /*  defined(VAX) */
# define _DOUBLE
# define _LITTLE
#endif    /*  defined(vms) */

#if defined(I370) || defined(__I370__)
/* Set the necessary defines for IBM MVS systems. */
# pragma options copts (trigraphs)

/* For SAS/C, those functions that pass character arguments to
 * Fortran routines (or routines that require a Fortran style
 * calling sequence) must be declared as __fortran so that the
 * Interlanguage Communications processing will build the proper
 * the proper calling sequence format.  This declaration is only
 * required on the prototype statement.  The function declarations
 * for the C functions that accept Fortran calls do not require
 * any specific declarations.
 */
#include <ilc.h>

# define _FTN_CALL_TYPE_PROTO  __fortran

# define _UC_FTN_NAME
   /* Add these lines to increase performance if
    * platform can byte-address Hollerith arrays
    * Note that this is only valid in _DOUBLE mode.
    */
# define A42CP( len, a4p ) ( (char *)a4p )
# define A4CP_FREE( ptr )
# define CP2A4( len, cp ) ( (A4CHAR *)cp )

# ifndef  I370
#  define I370 1
# endif
# if !defined(_MVSESA)
#  define _MVSESA
# endif
# if !defined(_MVS)
#  define _MVS
# endif
# define _DOUBLE
# define _IBMFP
# define _BIG
# define _VECTOR
# define EBCDIC_CHARSET
#endif   /* I370 */

#if defined(__alpha) && !defined(vms) && !defined(_M_ALPHA)
/* Set the necessary defines for Digital Alpha OSF systems
 * and Compaq/Digital Linux systems.
 */
# define _TU_FTN_NAME
# ifndef _ALPHAOSF
#  define _ALPHAOSF
# endif
# if !defined(_UNIX)
#  define _UNIX
# endif
# define _IEEEFP
# define _LITTLE
# if !defined(_SINGLE)
#  define _DOUBLE
   /* Add these lines to increase performance if
    * platform can byte-address Hollerith arrays
    * Note that this is only valid in _DOUBLE mode.
    */
#  define A42CP( len, a4p ) ( (char *)a4p )
#  define A4CP_FREE( ptr )
#  define CP2A4( len, cp ) ( (A4CHAR *)cp )
#  ifndef  _PTR64
#   define _PTR64
#  endif
#  define  INTEGER8           long
#  define UINTEGER8           unsigned long
# else
  /* Add defines for 64-bit Digital Alpha UNIX */
#  define DEFINED_INTEGER_TYPES
#  define A4CHAR              long
#  define BOOLEAN             long
#  define INTEGER             long
#  define INTEGER_long
#  define LOGICAL             long
#  define UINTEGER            unsigned long
#  define INTEGER_MAX  LONG_MAX
#  define UINTEGER_MAX ULONG_MAX
#  define DEFINED_REAL_TYPES
#  define REAL                double
#  define DEFINED_PRECISION_TYPES
#  define MACHINEPRECISION    double
#  define MACHINEPRECISION_double
#  define DOUBLEPRECISION     double
# endif
#endif   /* _alpha, !_vms */

#if defined(sun) && !defined(__SVR4)
/* Set the necessary defines for Sun SUNOS. */
# define _TU_FTN_NAME
   /* Add these lines to increase performance if
    * platform can byte-address Hollerith arrays
    * Note that this is only valid in _DOUBLE mode.
    */
# define A42CP( len, a4p ) ( (char *)a4p )
# define A4CP_FREE( ptr )
# define CP2A4( len, cp ) ( (A4CHAR *)cp )
# ifndef _SUNOS
#  define _SUNOS
# endif
# if !defined(_UNIX)
#  define _UNIX
# endif
# define _DOUBLE
# define _IEEEFP
# define _BIG
#endif   /* SUN */

#if defined(__sun) && defined(__SVR4)
/* Set the necessary defines for Sun Solaris. */
# define _TU_FTN_NAME
# ifndef _SOLARIS
#  define _SOLARIS
# endif
# if !defined(_UNIX)
#  define _UNIX
# endif
# define _IEEEFP
# if !defined(_SINGLE)
#  define _DOUBLE
   /* Add these lines to increase performance if
    * platform can byte-address Hollerith arrays
    * Note that this is only valid in _DOUBLE mode.
    */
#  define A42CP( len, a4p ) ( (char *)a4p )
#  define A4CP_FREE( ptr )
#  define CP2A4( len, cp ) ( (A4CHAR *)cp )
# else
  /* Add defines for 64-bit Solaris */
#  define DEFINED_INTEGER_TYPES
#  define A4CHAR              long
#  define BOOLEAN             long
#  define INTEGER             long
#  define INTEGER_long
#  define LOGICAL             long
#  define UINTEGER            unsigned long
#  define INTEGER_MAX  LONG_MAX
#  define UINTEGER_MAX ULONG_MAX
#  define DEFINED_REAL_TYPES
#  define REAL                double
#  define DEFINED_PRECISION_TYPES
#  define MACHINEPRECISION    double
#  define MACHINEPRECISION_double
#  define DOUBLEPRECISION     double
# endif  /* _SINGLE */
   /*
    * set defines for Solaris_x86 AMD64 and SPARC-64bit systems
    * Note: main difference from Solaris/SPARC-64bit is that the
    *       x86 machines are _LITTLE endian.
    */
# if  defined(__sparcv9) || (defined(__amd64) && defined(__SunOS))
   /* For 64bit memory offsets */
#  ifndef _LP64
#   define _LP64
#  endif
#  define  INTEGER8         long
#  define UINTEGER8         unsigned long
#  define _PTR64   1
#  if defined(__amd64)
#   define _LITTLE
#   ifndef _SOLARIS8664
#     define _SOLARIS8664
#   endif
#  else
#   define _BIG
#   ifndef _SOLARIS64
#     define _SOLARIS64
#   endif
#  endif/* __sparcv9  vs __amd64 */
# else
#  define _BIG
# endif   /* __sparcv9  or  (__amd64 && __SunOS)*/
#endif   /* _sun, __SVR4 */


#if defined(__hpux)
/* Set the necessary defines for Hewlett-Packard HPUX. */
/*
** +ppu   is required on cc for MSC.Nastran,
**        is not used for MSC.Patran.
** This means that the proper naming convention
** must be selected here.  If -D_NOFTNTU is specified,
** then use _LC_FTN_NAME.  Otherwise, by default,
** use _TU_FTN_NAME.
*/
# ifdef _NOFTNTU
#  define _LC_FTN_NAME
# else
#  define _TU_FTN_NAME
# endif
/* Enable HPUX source extensions */
# if !defined( _HPUX_SOURCE )
#  define _HPUX_SOURCE
# endif
/* Enable 64-bit file operations if the compiler supports them */
# if defined(__STDC_EXT__) || !defined(__STDC__) || defined(__LP64__)
#  ifndef _LARGEFILE64_SOURCE
#   define _LARGEFILE64_SOURCE
#  endif
# endif
/* Enable 64-bit pointers if __LP64__ mode is enabled */
# if defined(__LP64__)
#  define _PTR64
#  define  INTEGER8         long
#  define UINTEGER8         unsigned long
# endif
# define _ALIGN_DATA
# if !defined(_UNIX)
#  define _UNIX
# endif
# define _IEEEFP
# define _BIG
# if (0)
  /* Convex support is disabled */
# if ( defined(__HP_CXD_SPP) || defined(__convex__) ) && !defined(_HPUX)
#  ifndef _SPPUX
#    define _SPPUX
#  endif
   /* Add these lines to increase performance if
    * platform can byte-address Hollerith arrays
    * Note that this is only valid in _DOUBLE mode.
    */
# define A42CP( len, a4p ) ( (char *)a4p )
# define A4CP_FREE( ptr )
# define CP2A4( len, cp ) ( (A4CHAR *)cp )
# else
#  ifndef _HPUX
#   define _HPUX
#  endif
#  ifdef _SPPUX
#   undef _SPPUX
#  endif
# endif  /* __HP_CXD_SPP, __convex__, ! _HPUX */
# else
#  ifndef _HPUX
#   define _HPUX
#  endif
#  ifdef _SPPUX
#   undef _SPPUX
#  endif
# endif  /* (0) to disable Convex support */
# if defined(__ia64) && defined(_LP64) /* new defines for IA64 HPUX ... */
#  ifndef  _HPUX_IA64
#   define _HPUX_IA64
#  endif
#  include <stdlib.h>
#  include <string.h>
#  include <math.h>
#  if !defined(__LP64__)
#   define  INTEGER8         long
#   define UINTEGER8         unsigned long
#   define _PTR64   1
#  endif
# endif                                /* new defines for IA64 HPUX ... */
# if !defined(_SINGLE) /* _DOUBLE */
#  define _DOUBLE
   /* Add these lines to increase performance if
    * platform can byte-address Hollerith arrays
    * Note that this is only valid in _DOUBLE mode.
    */
#  define A42CP( len, a4p ) ( (char *)a4p )
#  define A4CP_FREE( ptr )
#  define CP2A4( len, cp ) ( (A4CHAR *)cp )
# else /* _SINGLE: Add defines for ILP64 */
#  define DEFINED_INTEGER_TYPES
#  define A4CHAR              long
#  define BOOLEAN             long
#  define INTEGER             long
#  define INTEGER_long
#  define LOGICAL             long
#  define UINTEGER            unsigned long
#  define INTEGER_MAX  LONG_MAX
#  define UINTEGER_MAX ULONG_MAX
#  define DEFINED_REAL_TYPES
#  define REAL                double
#  define DEFINED_PRECISION_TYPES
#  define MACHINEPRECISION    double
#  define MACHINEPRECISION_double
#  define DOUBLEPRECISION     double
# endif /* _SINGLE */

#endif   /* _hpux */

#if defined(sgi)
/* Set the necessary defines for Silicon-Graphics IRIX. */
# define _TU_FTN_NAME
# define _ALIGN_DATA
# include <sgidefs.h>
# ifndef _IRIX
#  define _IRIX
# endif
# if _MIPS_ISA == _MIPS_ISA_MIPS1 || _MIPS_ISA == _MIPS_ISA_MIPS2 || \
     _MIPS_ISA == _MIPS_ISA_MIPS3
#  ifndef _IRIX32
#   define _IRIX32
#  endif
#  if _MIPS_ISA != _MIPS_ISA_MIPS1
#   ifndef  _LONGLONG
#    define _LONGLONG 1
#   endif
#  endif
# else
#  ifndef _IRIX64
#   define _IRIX64
#  endif
# endif
# if !defined(_UNIX)
#  define _UNIX
# endif
# define _IEEEFP
# define _BIG
# if !defined(_SINGLE)
#  define _DOUBLE
#  ifndef  _PTR64
#   define _PTR64
#  endif
#  define  INTEGER8         long
#  define UINTEGER8         unsigned long
   /* Add these lines to increase performance if
    * platform can byte-address Hollerith arrays
    * Note that this is only valid in _DOUBLE mode.
    */
#  define A42CP( len, a4p ) ( (char *)a4p )
#  define A4CP_FREE( ptr )
#  define CP2A4( len, cp ) ( (A4CHAR *)cp )
# else
  /* Add defines for 64-bit SGI IRIX64 UNIX (ILP64/I8) */
#  define DEFINED_INTEGER_TYPES
#  define A4CHAR              long
#  define BOOLEAN             long
#  define INTEGER             long
#  define INTEGER_long
#  define LOGICAL             long
#  define UINTEGER            unsigned long
#  define INTEGER_MAX  LONG_MAX
#  define UINTEGER_MAX ULONG_MAX
#  define DEFINED_REAL_TYPES
#  define REAL                double
#  define DEFINED_PRECISION_TYPES
#  define MACHINEPRECISION    double
#  define MACHINEPRECISION_double
#  define DOUBLEPRECISION     double
# endif
#endif   /* sgi */

#include <float.h>

#if defined(_AIX)
/* Set the necessary defines for IBM AIX. */
/*
** -qextname is required on xlcc for MSC.Nastran,
**           is not used for MSC.Patran.
** This means that the proper naming convention
** must be selected here.  If -D_NOFTNTU is specified,
** then use _LC_FTN_NAME.  Otherwise, by default,
** use _TU_FTN_NAME.
*/
# ifdef _NOFTNTU
#  define _LC_FTN_NAME
# else
#  define _TU_FTN_NAME
# endif
# if !defined(_SINGLE)
#  define _DOUBLE
   /* Add these lines to increase performance if
    * platform can byte-address Hollerith arrays
    * Note that this is only valid in _DOUBLE mode.
    */
#  define A42CP( len, a4p ) ( (char *)a4p )
#  define A4CP_FREE( ptr )
#  define CP2A4( len, cp ) ( (A4CHAR *)cp )
# else
   /* Add defines for 64-bit AIX (ILP64/I8) */
#  define DEFINED_INTEGER_TYPES
#  define A4CHAR              long
#  define BOOLEAN             long
#  define INTEGER             long
#  define INTEGER_long
#  define LOGICAL             long
#  define UINTEGER            unsigned long
#  define INTEGER_MAX  LONG_MAX
#  define UINTEGER_MAX ULONG_MAX
#  define DEFINED_REAL_TYPES
#  define REAL                double
#  define DEFINED_PRECISION_TYPES
#  define MACHINEPRECISION    double
#  define MACHINEPRECISION_double
#  define DOUBLEPRECISION     double
# endif
# if !defined(_UNIX)
#  define _UNIX
# endif
# define _IEEEFP
# define _BIG
# if defined(__64BIT__) || defined(_AIX64)
   /* Add defines for 64-bit AIX */
#  ifndef  _PTR64
#   define _PTR64
#  endif
#  ifndef  _AIX64
#   define _AIX64
#  endif
#  define  INTEGER8         long
#  define UINTEGER8         unsigned long
# endif  /* __64BIT__ */
#endif   /* _AIX */

#if defined(__convex__) && !defined(__hpux) && !defined(__HP_CXD_SPP)
/* Set the necessary defines for HP/CONVEX C Series */
# define _TU_FTN_NAME
# ifndef _CONVEXOS
#  define _CONVEXOS
# endif
   /* Add these lines to increase performance if
    * platform can byte-address Hollerith arrays
    * Note that this is only valid in _DOUBLE mode.
    */
# define A42CP( len, a4p ) ( (char *)a4p )
# define A4CP_FREE( ptr )
# define CP2A4( len, cp ) ( (A4CHAR *)cp )
# if !defined(_UNIX)
#  define _UNIX
# endif
# define _DOUBLE
# define _IEEEFP
# define _BIG
# define _VECTOR
#endif   /* __convex__, ! __hpux, ! __HP_CXD_SPP */

#ifdef __DOS__
/* Set the necessary defines for Intel DOS/Windows */
# ifdef __WATCOMC__
  /* WATCOM C/C++ Compiler for DOS/WINDOWS */
#  define _DOS_PRAGMA_FTN_NAME
#  define ALIGN_DOUBLE_BNDRY    8   /* align double on 8-byte boundary */
#  define DEFINED_CHARACTER_TYPES
   typedef struct _string_descrip {
       char *string;
       int string_length;
     } *CHARACTER;
#  define F2CP( fp ) (*fp).string
#  ifdef  __WINDOWS_386__
    /* Windows mode */
#   ifndef _WINDOWS
#    define _WINDOWS
#   endif
#   ifdef  _DOS
#    undef  _DOS
#   endif
#   define DEFINED_INTEGER_TYPES
#   define A4CHAR             long
/* #  define BOOLEAN             long  */ /** defined in windows.h **/
#   define INTEGER            long
#   define INTEGER_long
#   define LOGICAL            long
#   define UINTEGER           unsigned long
#   define INTEGER_MAX  LONG_MAX
#   define UINTEGER_MAX ULONG_MAX
#  else
   /* DOS mode */
#   ifndef _DOS
#    define _DOS
#   endif
#   ifdef  _WINDOWS
#    undef  _WINDOWS
#   endif
#  endif
# endif   /* __WATCOMC__ */
# define _DOUBLE
# define _IEEEFP
# define _LITTLE
#endif   /* __DOS__ */

#ifdef __WINDOWS__
/* Set the necessary defines for Intel Windows */
# ifdef __WATCOMC__
   /* WATCOM C/C++ Compiler for WINDOWS */
#  define _DOS_PRAGMA_FTN_NAME
#  define ALIGN_DOUBLE_BNDRY    8   /* align double on 8-byte boundary */
#  define DEFINED_CHARACTER_TYPES
   typedef struct _string_descrip {
       char *string;
       int string_length;
     } *CHARACTER;
#  define F2CP( fp ) (*fp).string
   /* Windows mode */
#  ifndef _WINDOWS
#   define _WINDOWS
#  endif
#  ifdef  _DOS
#   undef  _DOS
#  endif
#  ifdef  _NT
#   undef  _NT
#  endif
# endif   /* __WATCOMC__ */
# define _DOUBLE
# define _IEEEFP
# define _LITTLE
# define DEFINED_INTEGER_TYPES
# define A4CHAR               long
/* #  define BOOLEAN             long  */ /** defined in windows.h **/
# define INTEGER              long
# define INTEGER_long
# define LOGICAL              long
# define UINTEGER             unsigned long
# define INTEGER_MAX  LONG_MAX
# define UINTEGER_MAX ULONG_MAX
#endif   /* __WINDOWS__  */

#ifdef __NT__
/* Set the necessary defines for Microsoft NT on Intel */
# ifdef __WATCOMC__
   /* WATCOM C/C++ Compiler for WINDOWS NT.
    * There are no special Fortran calling conventions needed.
    */
#  define _DOS_PRAGMA_FTN_NAME
#  define ALIGN_DOUBLE_BNDRY    8   /* align double on 8-byte boundary */
#  define DEFINED_CHARACTER_TYPES
   typedef struct _string_descrip {
       char *string;
       int string_length;
     } *CHARACTER;
#  define F2CP( fp ) (*fp).string
# endif   /* __WATCOMC__ */
# ifndef _I386NT
#  define _I386NT
# endif
# ifndef _NT
#  define _NT
# endif
# ifdef  _DOS
#  undef  _DOS
# endif
# ifdef  _WINDOWS
#  undef  _WINDOWS
# endif
# define _DOUBLE
# define _IEEEFP
# define _LITTLE
# define DEFINED_INTEGER_TYPES
# define A4CHAR               int
/* #  define BOOLEAN             int   */ /** defined in windows.h **/
# define INTEGER              int
/* # define INTEGER_long */
# define INTEGER_int
# define LOGICAL              int
# define UINTEGER             unsigned int
# define INTEGER_MAX  LONG_MAX
# define UINTEGER_MAX ULONG_MAX
#endif   /* Windows/NT using Watcom */

#if defined(__ICL) && defined(_WIN32) && \
    !defined(__ECL) && !defined(_WIN64)
  /* Compiling for Intel Windows NT using Intel Referemce Compiler.
   * There are no special Fortran calling conventions needed.
   */
# define _UC_FTN_NAME
# ifndef _I386NT
#  define _I386NT
# endif
# ifndef _NT
#  define _NT
# endif
# ifdef  _DOS
#  undef  _DOS
# endif
# ifdef  _WINDOWS
#  undef  _WINDOWS
# endif
# define _DOUBLE
# define _IEEEFP
# define _LITTLE
# define DEFINED_INTEGER_TYPES
# define A4CHAR               int
/* #  define BOOLEAN             int   */ /** defined in windows.h **/
# define INTEGER              int
/* # define INTEGER_long */
# define INTEGER_int
# define LOGICAL              int
# define UINTEGER             unsigned int
# define INTEGER_MAX  LONG_MAX
# define UINTEGER_MAX ULONG_MAX
# if defined(FTN_STDCALL) || defined(FTN_CVF)
#  define _FTN_CALL_TYPE_PROTO  __stdcall
#  define _FTN_CALL_TYPE_ENTRY  __stdcall
# endif
#endif   /* __ICL, _WIN32, Windows NT using Intel Reference Compiler */

#if (defined(__ECL) || defined(__INTEL_COMPILER)) && defined(_WIN64) && \
    (defined(_M_IA64) || defined(_M_AMD64))
  /* Compiling for Intel Windows NT-64 using Intel Referemce Compiler.
   * There are no special Fortran calling conventions needed.
   * This can either be for Itanium or for EM64T/AMD64,
   * depending on _M_IA64 or _M_AMD64.
   */
# define _UC_FTN_NAME
# ifdef  _IA64NT
#  undef _IA64NT
# endif
# ifdef _8664NT
#  undef _8664NT
# endif
# if defined(_M_IA64)
#  define _IA64NT
# elif defined(_M_AMD64)
#  define _8664NT
# endif
# ifndef _NT
#  define _NT
# endif
# ifdef  _DOS
#  undef  _DOS
# endif
# ifdef  _WINDOWS
#  undef  _WINDOWS
# endif
# define _IEEEFP
# define _LITTLE
# if !defined(_SINGLE)
#  define _DOUBLE
#  define DEFINED_INTEGER_TYPES
#  define A4CHAR              long
/* #  define BOOLEAN             long  */ /** defined in windows.h **/
#  define INTEGER             int
#  define INTEGER_int
#  define LOGICAL             int
#  define UINTEGER            unsigned int
#  ifndef  _PTR64
#   define _PTR64
#  endif
#  define INTEGER_MAX  LONG_MAX
#  define UINTEGER_MAX ULONG_MAX
   /* Add these lines to increase performance if
    * platform can byte-address Hollerith arrays
    * Note that this is only valid in _DOUBLE mode.
    */
#  define A42CP( len, a4p ) ( (char *)a4p )
#  define A4CP_FREE( ptr )
#  define CP2A4( len, cp ) ( (A4CHAR *)cp )
# else
  /* Add defines for 64-bit INTEGER Intel Itanium/EM64T Windows */
#  define DEFINED_INTEGER_TYPES
#  define A4CHAR              __int64
/* #  define BOOLEAN             __int64  */ /** defined in windows.h **/
#  define INTEGER             __int64
#  define INTEGER___int64
#  define LOGICAL             __int64
#  define UINTEGER            unsigned __int64
#  define INTEGER_MAX  _I64_MAX
#  define UINTEGER_MAX _UI64_MAX
#  define DEFINED_REAL_TYPES
#  define REAL                double
#  define DEFINED_PRECISION_TYPES
#  define MACHINEPRECISION    double
#  define MACHINEPRECISION_double
#  define DOUBLEPRECISION     double
# endif  /* ! _SINGLE */
# define  INTEGER8         __int64
# define UINTEGER8         unsigned __int64
#endif   /* __ECL, __INTEL_COMPILER, _WIN64, Windows NT-64 (_NT) using Intel Reference Compiler */

#if defined _MSC_VER && defined _WIN32  && defined _M_IX86 && \
    !defined __ICL && !defined __ECL && !defined __INTEL_COMPILER
  /* Compiling for Intel Windows NT using Microsoft Visual C.
   * Also, unless -DNO_FTN_CVF is defined, assume that Digital
   * Visual Fortran (or equivalent compilers) for Intel will be used
   * and that calls between C and Fortran will be in Microsoft
   * Powerstation Fortran format, i.e., __stdcall (causes file name
   * mangling, that is, adding @nn to external name where nn is the
   * length of the calling sequence in bytes) and with implicit character
   * length arguments mixed in-line with the rest of the calling
   * sequence arguments.  This also requires that the following
   * compiler options be specified (or taken by default) for Digital
   * Visual Fortran:
   *     /iface:(default,mixed_str_len_arg)
   */
# if !defined(NO_FTN_CVF)
#  define _FTN_CALL_TYPE_PROTO  __stdcall
#  define _FTN_CALL_TYPE_ENTRY  __stdcall
# endif
# define _UC_FTN_NAME
# ifndef _I386NT
#  define _I386NT
# endif
# ifndef _NT
#  define _NT
# endif
# ifdef  _DOS
#  undef  _DOS
# endif
# ifdef  _WINDOWS
#  undef  _WINDOWS
# endif
# define _DOUBLE
# define _IEEEFP
# define _LITTLE
# define DEFINED_INTEGER_TYPES
# define A4CHAR              int
/* #  define BOOLEAN             int   */ /** defined in windows.h **/
# define INTEGER             int
/* # define INTEGER_long */
# define INTEGER_int
# define LOGICAL             int
# define UINTEGER            unsigned int
# define DEFINED_PRECISION_TYPES
# define MACHINEPRECISION    double
# define MACHINEPRECISION_double
# define DOUBLEPRECISION     double
# define INTEGER_MAX  LONG_MAX
# define UINTEGER_MAX ULONG_MAX
# define  INTEGER8         __int64
# define UINTEGER8         unsigned __int64
   /* Add these lines to increase performance if
    * platform can byte-address Hollerith arrays
    * Note that this is only valid in _DOUBLE mode.
    */
#  define A42CP( len, a4p ) ( (char *)a4p )
#  define A4CP_FREE( ptr )
#  define CP2A4( len, cp ) ( (A4CHAR *)cp )
#endif   /* _MSC_VER, _WIN32, Microsoft Visual C, Digital Visual Fortran */

#if defined(_MSC_VER) && defined(_WIN64)  && \
    (defined(_M_IA64) || defined(_M_AMD64)) && \
    !defined(__ICL) && !defined(__ECL) && !defined(__INTEL_COMPILER)
  /* Compiling for Intel Windows NT-64 using Microsoft Visual C.
   * Assume that no special Fortran calling conventions are needed.
   * Currently, the only Windows NT IA64 Fortran compiler is the
   * Intel Reference Compiler and it does not have any special requirements.
   */
# define _UC_FTN_NAME
# ifdef  _IA64NT
#  undef _IA64NT
# endif
# ifdef _8664NT
#  undef _8664NT
# endif
# if defined(_M_IA64)
#  define _IA64NT
# elif defined(_M_AMD64)
#  define _8664NT
# endif
# ifndef _NT
#  define _NT
# endif
# ifdef  _DOS
#  undef  _DOS
# endif
# ifdef  _WINDOWS
#  undef  _WINDOWS
# endif
# define _IEEEFP
# define _LITTLE
# if !defined(_SINGLE)
#  define _DOUBLE
#  define DEFINED_INTEGER_TYPES
#  define A4CHAR              int
/* #  define BOOLEAN             int   */ /** defined in windows.h **/
#  define INTEGER             int
#  define INTEGER_int
#  define LOGICAL             int
#  define UINTEGER            unsigned int
   /* Add these lines to increase performance if
    * platform can byte-address Hollerith arrays
    * Note that this is only valid in _DOUBLE mode.
    */
#  define A42CP( len, a4p ) ( (char *)a4p )
#  define A4CP_FREE( ptr )
#  define CP2A4( len, cp ) ( (A4CHAR *)cp )
#  define INTEGER_MAX  LONG_MAX
#  define UINTEGER_MAX ULONG_MAX
# else
  /* Add defines for 64-bit INTEGER Intel Itanium/EM64T Windows */
#  define DEFINED_INTEGER_TYPES
#  define A4CHAR              __int64
/* #  define BOOLEAN             __int64  */ /** defined in windows.h **/
#  define INTEGER             __int64
#  define INTEGER___int64
#  define LOGICAL             __int64
#  define UINTEGER            unsigned __int64
#  define INTEGER_MAX    LONG_MAX
#  define UINTEGER_MAX   ULONG_MAX
#  define DEFINED_REAL_TYPES
#  define REAL                double
#  define DEFINED_PRECISION_TYPES
#  define MACHINEPRECISION    double
#  define MACHINEPRECISION_double
#  define DOUBLEPRECISION     double
#  ifdef _DOUBLE
#   undef _DOUBLE
#  endif
# endif  /* ! _SINGLE */
#  ifndef  _PTR64
#   define _PTR64
#  endif
#  define  INTEGER8         __int64
#  define UINTEGER8         unsigned __int64
#endif   /* _MSC_VER, _WIN64, Microsoft Visual C-64 bit for _NT */

#if defined(__alpha) && !defined(vms) && defined(_M_ALPHA)
  /* Compiling for Digital Alpha Windows NT using Microsoft Visual C.
   * Also assume that Digital DEC Fortran for Alpha will be used
   * and that calls between C and Fortran will be in standard f77
   * format, i.e., with implicit character length arguments added after
   * the normal calling sequence arguments.
   * There are no special Fortran calling conventions needed.
   */
# define _TU_FTN_NAME
# ifndef _ALPHANT
#  define _ALPHANT
# endif
# ifndef _NT
#  define _NT
# endif
# ifdef  _DOS
#  undef  _DOS
# endif
# ifdef  _WINDOWS
#  undef  _WINDOWS
# endif
#  define _DOUBLE
#  define _IEEEFP
#  define _LITTLE
#  define DEFINED_INTEGER_TYPES
#  define A4CHAR              long
/* #  define BOOLEAN             long  */ /** defined in windows.h **/
#  define INTEGER             long
#  define INTEGER_long
#  define LOGICAL             long
#  define UINTEGER            unsigned long
#  define INTEGER_MAX  LONG_MAX
#  define UINTEGER_MAX ULONG_MAX
#endif   /* __alpha, !vms, _M_ALPHA (Alpha _NT) */

#if defined(SX)
/*  Define the necessary things for NEC SX systems.
 *  If _DOUBLE has been pre-defined, the system will be a
 *  "short word" (32-bit INTEGER) system.  Otherwise, it
 *  will be a "long word" (64-bit INTEGER) system.
 */
# if !defined(_SUPERUX)
#  define _SUPERUX
# endif

# define _TU_FTN_NAME

# if defined(_SINGLE)
# define DEFINED_PRECISION_TYPES
# define MACHINEPRECISION     double
# define MACHINEPRECISION_double
# define DOUBLEPRECISION      long double
# define DEFINED_INTEGER_TYPES
# define A4CHAR               long
# define BOOLEAN              long
# define INTEGER              long
# define INTEGER_long
# define LOGICAL              long
# define UINTEGER             unsigned long
# define INTEGER_MAX  LONG_MAX
# define UINTEGER_MAX ULONG_MAX
#else
# ifndef _DOUBLE
# define _DOUBLE
# endif
#endif   /* _SINGLE */

# if !defined(_UNIX)
#  define _UNIX
# endif
# define _IEEEFP
# define _BIG
# define _VECTOR
/*
   For 64bit memory offsets...
*/
#  define  INTEGER8         long
#  define UINTEGER8         unsigned long
#  define _PTR64   1
#endif  /* NEC SX */

#if defined(__uxppx__) || defined(__uxpv__)
/* Defines for Fujitsu UXP/PV */
# define _TU_FTN_NAME
   /* Add these lines to increase performance if
    * platform can byte-address Hollerith arrays
    * Note that this is only valid in _DOUBLE mode.
    */
# define A42CP( len, a4p ) ( (char *)a4p )
# define A4CP_FREE( ptr )
# define CP2A4( len, cp ) ( (A4CHAR *)cp )
# ifndef _UXPV
#  define _UXPV
# endif
# if !defined(_UNIX)
#  define _UNIX
# endif
# define _DOUBLE
# define _BIG
# define _IEEEFP
# define _VECTOR
#endif  /* __uxppx */

#if defined(hitm) && defined(unix) && defined(OSF)
/* Define the symbols needed for Hitachi OSF systems. */
# define _UC_FTN_NAME
# ifndef _HIOSF
#  define _HIOSF
# endif
# if !defined(_UNIX)
#  define _UNIX
# endif
# define _DOUBLE
# define _IBMFP
# define _BIG
#endif   /* hitm, unix, OSF */

#if defined(__GNUC__) && !defined(__alpha) && !defined(__INTEL_COMPILER)
/*
 * Starting with V2006, each Intel/Linux system will have its
 * own section based on hardware architecture and not use these
 * GNU definitions.
*/
/*
 * __GNUC__ will be used for LINUX/Intel systems only.
 */
# define _TU_FTN_NAME
# if !defined(_LINUX)
#  define _LINUX
# endif
# if !defined(_UNIX)
#  define _UNIX
# endif
# define _DOUBLE
# define _IEEEFP
# define _LITTLE
# if defined(__LP64__)
  /* Using Gnu C for 64-bit LINUX */
#  if !defined(_8664LINUX)
#  if !defined(_IA64LINUX)
#   define _IA64LINUX
#  endif
#  endif
#  if !defined(_PTR64)
#   define _PTR64
#  endif
#  define  INTEGER8         long
#  define UINTEGER8         unsigned long
# else
  /* Using Gnu C for 32-bit LINUX */
#  if !defined(_IA32LINUX)
#   define _IA32LINUX
#  endif
#  define DEFINED_INTEGER_TYPES
#  define A4CHAR              long
#  define BOOLEAN             long
#  define INTEGER             long
#  define INTEGER_long
#  define LOGICAL             long
#  define UINTEGER            unsigned long
#   define INTEGER_MAX  LONG_MAX
#   define UINTEGER_MAX ULONG_MAX
# endif  /* __LP64__ */
#endif   /* __GNUC__ */

#if (defined(__ICC) || defined(__INTEL_COMPILER)) && \
    defined(__i386) && defined(__linux)
/*
 * i386 (x86) linux systems.
 */
# define _TU_FTN_NAME
# if !defined(_LINUX)
#  define _LINUX
# endif
# if !defined(_IA32LINUX)
#  define _IA32LINUX
# endif
# if !defined(_UNIX)
#  define _UNIX
# endif
# define _IEEEFP
# define _LITTLE
# define _DOUBLE
# define DEFINED_INTEGER_TYPES
#  define A4CHAR              int
#  define BOOLEAN             int
#  define INTEGER             int
#  define INTEGER_int
#  define LOGICAL             int
#  define UINTEGER            unsigned int
#  define INTEGER_MAX  LONG_MAX
#  define UINTEGER_MAX ULONG_MAX
# define  INTEGER8         __int64
# define UINTEGER8         unsigned __int64
#endif   /* __ICC, __i386, __linux */

#if (defined(__ICC) || defined(__INTEL_COMPILER)) && \
    !defined(__i386) && defined(__linux) && !defined(__ia64)
/*
 * x8664 (Intel em64t and AMD/Opteron) linux systems.
 */
# define _TU_FTN_NAME
# if !defined(_LINUX)
#  define _LINUX
# endif
# if !defined(_8664LINUX)
#  define _8664LINUX
# endif
# if !defined(_UNIX)
#  define _UNIX
# endif
# define _IEEEFP
# define _LITTLE
# if !defined(_PTR64)
#  define _PTR64
# endif
# define  INTEGER8         __int64
# define UINTEGER8         unsigned __int64
# if defined(_SINGLE)
#  define DEFINED_INTEGER_TYPES
#  define A4CHAR              __int64
#  define BOOLEAN             __int64
#  define INTEGER             __int64
#  define INTEGER___int64
#  define LOGICAL             __int64
#  define UINTEGER            unsigned __int64
#  define _I64_MAX    0x7fffffffffffffff
#  define _UI64_MAX   0xffffffffffffffff
#  define INTEGER_MAX  _I64_MAX
#  define UINTEGER_MAX _UI64_MAX
#  define DEFINED_REAL_TYPES
#  define REAL                double
#  define DEFINED_PRECISION_TYPES
#  define MACHINEPRECISION    double
#  define MACHINEPRECISION_double
#  define DOUBLEPRECISION     double
#  ifdef _DOUBLE
#   undef _DOUBLE
#  endif
/* #  define INTEGER           long */
# else
#  ifndef  _DOUBLE
#   define  _DOUBLE
#  endif
   /* Add these lines to increase performance if
    * platform can byte-address Hollerith arrays
    * Note that this is only valid in _DOUBLE mode.
    */
# define A42CP( len, a4p ) ( (char *)a4p )
# define A4CP_FREE( ptr )
# define CP2A4( len, cp ) ( (A4CHAR *)cp )
# endif /* _SINGLE */
#endif   /* __ICC, NOT __i386, __linux (for x86-64) */

#if (defined(__ECC) || defined(__INTEL_COMPILER)) \
     && defined(__linux) && defined(__ia64)
/*
 * IA64 (Itanium) linux systems
 */
# define _TU_FTN_NAME
# if !defined(_LINUX)
#  define _LINUX
# endif
# if !defined(_IA64LINUX)
#  define _IA64LINUX
# endif
# if !defined(_UNIX)
#  define _UNIX
# endif
# define _IEEEFP
# define _LITTLE
# if !defined(_PTR64)
#  define _PTR64
# endif
# define INTEGER8          __int64
# define UINTEGER8         unsigned __int64
# if defined(_SINGLE)
#  define DEFINED_INTEGER_TYPES
#  define A4CHAR              __int64
#  define BOOLEAN             __int64
#  define INTEGER             __int64
#  define INTEGER___int64
#  define LOGICAL             __int64
#  define UINTEGER            unsigned __int64
#  define _I64_MAX    0x7fffffffffffffff
#  define _UI64_MAX   0xffffffffffffffff
#  define INTEGER_MAX  _I64_MAX
#  define UINTEGER_MAX _UI64_MAX
#  define DEFINED_REAL_TYPES
#  define REAL                double
#  define DEFINED_PRECISION_TYPES
#  define MACHINEPRECISION    double
#  define MACHINEPRECISION_double
#  define DOUBLEPRECISION     double
#  ifdef _DOUBLE
#   undef _DOUBLE
#  endif
# else
#  ifndef  _DOUBLE
#   define  _DOUBLE
#  endif
   /* Add these lines to increase performance if
    * platform can byte-address Hollerith arrays
    * Note that this is only valid in _DOUBLE mode.
    */
# define A42CP( len, a4p ) ( (char *)a4p )
# define A4CP_FREE( ptr )
# define CP2A4( len, cp ) ( (A4CHAR *)cp )
# endif   /* SINGLE */
#endif   /* __ECC, __linux */

#ifndef F2CP
# define F2CP( fp ) ( fp )
# define CP2F( cp, len ) ( cp )
#endif

/* If the Hollerith macros have not been defined yet,
 * i.e., if the platform does not have byte-addressability
 * to Hollerith arrays or if the platform is a _SINGLE
 * platform, define the Hollerith macros so that the
 * appropriate utility functions are invoked.
 */
#ifndef A42CP
# define A42CP(len,a4p) cvta4str(len,a4p)
# define A4CP_FREE(ptr) cvta4free((void *)ptr);
# define CP2A4(len,cp)  cvtstra4(len,cp)
#endif

/*
 * Some defined constants...
 */

#ifndef TRUE
# define TRUE 1
# define FALSE 0
#endif

#ifndef NULL
# define NULL 0
#endif

/*
 * Define the "complement" character.  Because the tilde does not
 * always get translated properly when going from/to ASCII to/from
 * EBCDIC, the EBCDIC format uses a trigraph instead.
 */
#ifdef I370
# define COMPLEMENT ??-
#else
# define COMPLEMENT ~
#endif

/* Set the defaults for FORTRAN naming conventions and
 * double alignment if not set above.  The defaults are --
 *    FORTRAN names are upper case.
 *    No special alignment needed for doubles.
 */
#ifndef _TU_FTN_NAME
# ifndef _UC_FTN_NAME
#  ifndef _LC_FTN_NAME
#   ifndef _DOS_PRAGMA_FTN_NAME
#    define _UC_FTN_NAME
#   endif
#  endif
# endif
#endif
#ifndef ALIGN_DOUBLE_BNDRY
# define ALIGN_DOUBLE_BNDRY    0
#endif

/* Set the defaults for Fortran->C and C->Fortran type
 * declarations.  The default is NULL for all of them.
 */
#ifndef  _FTN_CALL_TYPE_PROTO
# define _FTN_CALL_TYPE_PROTO
#endif
#ifndef  _FTN_CALL_TYPE_ENTRY
# define _FTN_CALL_TYPE_ENTRY
#endif
#ifndef  _FTN_CALL_TYPE_CALL
# define _FTN_CALL_TYPE_CALL
#endif

/* Set the default character set to ASCII if it has not
 * already been set.
 */
#if !defined(EBCDIC_CHARSET) && !defined(UNICODE_CHARSET)
# if !defined(ASCII_CHARSET)
#  define ASCII_CHARSET
# endif
#endif

#endif     /* STDSYSTEM_H  */
