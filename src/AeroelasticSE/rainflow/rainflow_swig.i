
%module rainflow_swig

%{
    #define SWIG_FILE_WITH_INIT
    #include "rainflow_swig.h"
%}

%include "numpy.i"

%init %{
    import_array();
%}

%apply (double* INPLACE_ARRAY1, int DIM1) {(double* output, int noutput),(double* peaks, int npeaks)}
%include "rainflow_swig.h"


