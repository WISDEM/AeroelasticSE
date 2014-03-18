/*  RAINFLOW $ Revision: 1.1 $ */
/*  by Adam Nieslony, 2009     */
/*  The original code has been modified by Gregory Hayman 2012 as follows: */
/*    abs() has been replaced everywhere with fabs()                       */
/*    the function now applies the Goodman correction to the damage cycle  */
/*      load ranges using a user-supplied fixed load mean, or a fixed load */
/*      mean of zero.                                                      */
/*    the user can supply a the value of a partial damage cycle: uc_mult   */

#include <math.h>
#include "mex.h"

/* ++++++++++ BEGIN RF3 [ampl ampl_mean nr_of_cycle] */
/* ++++++++++ Rain flow without time analysis */
void
rf3(mxArray *array_ext, mxArray *hs[], double lfm, double l_ult, double uc_mult) {
    double *pr, *po, a[16384], range, mean, adj_range, lfmargin, adj_zero_mean_range;
    int tot_num, index, j, cNr;
    mxArray *array_out;
    
    lfmargin = l_ult - fabs(lfm);
   // mexPrintf("lfm = %f\n", lfm);
   // mexPrintf("l_ult = %f\n", l_ult);
  //  mexPrintf("uc_mult = %f\n", uc_mult);
    
    tot_num = mxGetM(array_ext) * mxGetN(array_ext);
    pr = (double *)mxGetPr(array_ext);
    
    array_out = mxCreateDoubleMatrix(5, tot_num-1, mxREAL);
    po = (double *)mxGetPr(array_out);
    
    j = -1;
    cNr = 1;
    for (index=0; index<tot_num; index++) {
        a[++j]=*pr++;
        while ( (j >= 2) && (fabs(a[j-1]-a[j-2]) <= fabs(a[j]-a[j-1])) ) {
            range=fabs(a[j-1]-a[j-2]);
            switch(j)
{
                case 0: { break; }
                case 1: { break; }
                case 2: {
                    mean=(a[0]+a[1])/2;
                    adj_range = range * lfmargin / ( l_ult - fabs(mean) );
                    adj_zero_mean_range = range * l_ult / ( l_ult - fabs(mean) );
                    a[0]=a[1];
                    a[1]=a[2];
                    j=1;
                    if (range > 0) {
                        *po++=range;
                        *po++=mean;
                        *po++=adj_range;
                        *po++=uc_mult;
                        *po++=adj_zero_mean_range;
                    }
                    break;
                }
                default: {
                    mean=(a[j-1]+a[j-2])/2;
                    adj_range = range * lfmargin / ( l_ult - fabs(mean) );
                    adj_zero_mean_range = range * l_ult / ( l_ult - fabs(mean) );
                    a[j-2]=a[j];
                    j=j-2;
                    if (range > 0) {
                        *po++=range;
                        *po++=mean;
                        *po++=adj_range;
                        *po++=1.00;
                        *po++=adj_zero_mean_range;
                        cNr++;
                    }
                    break;
                }
            }
        }
    }
    for (index=0; index<j; index++) {
        range=fabs(a[index]-a[index+1]);
        mean=(a[index]+a[index+1])/2;
        adj_range = range * lfmargin / ( l_ult - fabs(mean) );
        adj_zero_mean_range = range * l_ult / ( l_ult - fabs(mean) );
        if (range > 0){
            *po++=range;
            *po++=mean;
            *po++=adj_range;
            *po++=uc_mult;
            *po++=adj_zero_mean_range;
        }
    }
  /* you can free the allocated memeory */
  /* for array_out data                 */
    mxSetN(array_out, tot_num - cNr);
    hs[0]=array_out;
}
/* ++++++++++ END RF3 */




/* mexFunction - main function called from MATLAB. */
void
mexFunction( int nlhs,       mxArray *plhs[],
int nrhs, const mxArray *prhs[] )
{
    mxArray *array_in0;
    mxArray *array_in1;
    double  lmf, l_ult, uc_mult;
    int ind;
    
    if (nrhs < 1) {
        mexErrMsgTxt("RAINFLOW requires at least one input argument.");
    } else if (nlhs > 1) {
        mexErrMsgTxt("RAINFLOW requires only one output argument.");
    }
    
    if (mxIsComplex(prhs[0]) || !mxIsDouble(prhs[0])) {
        mexErrMsgTxt("RAINFLOW requires DOUBLE ARRAY as first input argument.");
    } else { array_in0 = (mxArray *)prhs[0]; }
    
    switch(nrhs) {
        case 1: {
            rf3(array_in0, plhs, 0.0, 99e19, 0.5);
            break;
        }
        case 2: {
            if (mxIsDouble(prhs[1]))
            {
               lmf = *(double *)mxGetPr(prhs[1]);
            }
            else if (mxIsSingle(prhs[1]))
            {
               lmf = (double)*(double *)mxGetPr(prhs[1]);
            }             
            rf3(array_in0, plhs, lmf, 99e99, 0.5);
            break;
            
        }
        case 3: {
            rf3(array_in0, plhs, 0.0, 99e99, 0.5);
            break;
        }
        case 4: {
           if (!mxIsDouble(prhs[1])) {
                mexErrMsgTxt("RAINFLOW requires  second input arg to be DOUBLE.");
            }
           if (!mxIsDouble(prhs[2])) {
                mexErrMsgTxt("RAINFLOW requires  third input arg to be DOUBLE.");
            }
           if (!mxIsDouble(prhs[3])) {
                mexErrMsgTxt("RAINFLOW requires  fourth input arg to be DOUBLE.");
            }
            lmf = *(double *)mxGetPr(prhs[1]);
            l_ult = *(double *)mxGetPr(prhs[2]);
            uc_mult = *(double *)mxGetPr(prhs[3]);
            rf3(array_in0, plhs, lmf, l_ult, uc_mult);
            break;
        }
        default: {
            mexErrMsgTxt("RAINFLOW: To many input arguments.");
            break;
        }
    }
}
