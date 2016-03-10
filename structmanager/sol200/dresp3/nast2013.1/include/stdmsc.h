/*
** stdmsc.h
**
**  General defines for MSC/NASTRAN & MSC/EMAS.
*/
#ifndef STDMSC_H
#define STDMSC_H

/*
** Get the proper Operating System definitions.
*/
#include "stdsystm.h"

/*
** Note, the internal 64-bit Alpha must be able to
** define _SINGLE via '-DSINGLE'.  To permit this, and
** ensure that we don't get caught on some other system,
** undefine _SINGLE if both _DOUBLE and _SINGLE are defined.
*/
#if defined(_DOUBLE)
# if defined(_SINGLE)
#  undef    _SINGLE
# endif
#endif

/*
** If stdsystm has not defined the required types, provide
** default definitions here.
**
** The macros DEFINED_*_TYPES are not used outside this file.
*/
#if defined DEFINED_INTEGER_TYPES
# undef DEFINED_INTEGER_TYPES
#else
# define A4CHAR            int
# ifndef _NT
#  define BOOLEAN          int
# endif
# define INTEGER           int
# define INTEGER_int
# define LOGICAL           int
# define UINTEGER          unsigned int
# define INTEGER_MAX  INT_MAX
# define UINTEGER_MAX UINT_MAX
#endif

#if defined DEFINED_REAL_TYPES
# undef DEFINED_REAL_TYPES
#else
# define REAL              float
#endif

#if defined DEFINED_PRECISION_TYPES
# undef DEFINED_PRECISION_TYPES
#else
# define MACHINEPRECISION  double
# define MACHINEPRECISION_double
# define DOUBLEPRECISION   double
#endif

#if defined DEFINED_CHARACTER_TYPES
# undef DEFINED_CHARACTER_TYPES
#else
# define CHARACTER         char *
#endif

/* Make sure INTEGER8 and UINTEGER8 are defined in _SINGLE mode */
#if defined _SINGLE
# ifndef   INTEGER8
#  define  INTEGER8    INTEGER
#  define  UINTEGER8   UINTEGER
# endif
#endif

#endif
