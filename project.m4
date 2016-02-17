# Macro definitions:

AC_DEFUN([AC_PROG_PYTHON3],[
if test -z "${PYTHON}"; then
   AC_CHECK_PROGS(PYTHON,[python3],no)
else
   AC_CHECK_PROGS(PYTHON,[$PYTHON, python3],no)
fi
if test $PYTHON = "no" ;
then
   AC_MSG_ERROR([Unable to find Python3]);
fi
AC_SUBST(PYTHON)
])

# Call the macros:

AC_PROG_PYTHON3

