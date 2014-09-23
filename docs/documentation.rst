.. module:: aeroelasticse

.. _aeroelasticse:

Documentation
-------------
The important modules in the AeroelasticSE suite of codes include:


Run FAST
========

.. automodule:: AeroelasticSE.runFAST
  :members:
  :special-members:

Run TurbSim
===========

.. automodule:: AeroelasticSE.runTurbSim
   :members:
   :special-members:

FAST openMDAO Components
========================

.. automodule:: AeroelasticSE.FAST_component
   :members:
   :special-members:

Fused FAST
==========

.. automodule:: AeroelasticSE.FusedFAST
   :members:
   :special-members:

FAST VariableTree Runner
========================

.. automodule:: AeroelasticSE.FSTTemplate_runner
   :members:
   :special-members:


Run IEC
=======

This code can run and process a whole study of many run cases, including in parallel on a 
compute cluster.

First prepare a file of cases, e.g. ``some_cases.txt`` and a file of control input, e.g.  ``runbatch-control``.
Examples of these::

    (openmdao-0.9.5)stc-24038s:AeroelasticSE pgraf$ more some_cases.txt
    AnalTime Vhub Hs Tp WaveDir Prob
    3.00e+00 1.00e+01 1.59e+00 1.14e+01 -1.01e+00  1.70e-02
    3.00e+00 1.02e+01 9.49e-01 8.37e+00 -9.48e-01  4.88e-03
    3.00e+00 9.95e+00 1.81e+00 1.14e+01 -4.38e-01  1.78e-02
    3.00e+00 8.87e+00 1.49e+00 1.37e+01 2.29e-03  7.63e-03
    3.00e+00 9.05e+00 1.25e+00 1.09e+01 -1.71e+00  5.62e-03
    # in reality this file might have thousands of cases...

    (openmdao-0.9.5)stc-24038s:AeroelasticSE pgraf$ more runbatch-control.txt
    # key = value file of locations of various files to read and
    # to write
    # and for output keys.
    # and misc. control functionality    
    main_output_file = "runbatch.out"
    output_keys =  RootMxc1  RootMyc1
    output_operations = rf np.std max
    ts_exe = "/Users/pgraf/opt/windcode-7.31.13/TurbSim/build/TurbSim_glin64"
    ts_dir = "/Users/pgraf/work/wese/fatigue12-13/from_gordie/SparFAST3.orig/TurbSim"
    ts_file = "TurbSim.inp"
    fst_exe = "/Users/pgraf/opt/windcode-7.31.13/build/FAST_glin64"
    fst_dir = "/Users/pgraf/work/wese/fatigue12-13/from_gordie/SparFAST3.almostorig"
    fst_file = "NRELOffshrBsline5MW_Floating_OC3Hywind.fst"
    run_dir = "all_runs"


Run::

    python iecApp.py -i some_cases.txt -f runbatch-control.txt

Hopefully you will see FAST running many times, resulting in stdout like::

    RUNS ARE DONE:
    collecting output from copied-back files (not from case recorder), see runbatch.out
    processing case <fusedwind.runSuite.runCase.GenericRunCase object at 0x103e1af50>
    collecting from  /Users/pgraf/work/wese/AeroelasticSE-1_3_14/src/AeroelasticSE/all_runs/raw_casesAna.3.0Wav.-1.0Hs.1.6Vhu.10.0Tp.11.4Pro.0.0
    collecting from  /Users/pgraf/work/wese/AeroelasticSE-1_3_14/src/AeroelasticSE/all_runs/raw_casesAna.3.0Wav.-0.9Hs.0.9Vhu.10.2Tp.8.4Pro.0.0
    collecting from  /Users/pgraf/work/wese/AeroelasticSE-1_3_14/src/AeroelasticSE/all_runs/raw_casesAna.3.0Wav.-0.4Hs.1.8Vhu.10.0Tp.11.4Pro.0.0
    collecting from  /Users/pgraf/work/wese/AeroelasticSE-1_3_14/src/AeroelasticSE/all_runs/raw_casesAna.3.0Wav.0.0Hs.1.5Vhu.8.9Tp.13.7Pro.0.0
    collecting from  /Users/pgraf/work/wese/AeroelasticSE-1_3_14/src/AeroelasticSE/all_runs/raw_casesAna.3.0Wav.-1.7Hs.1.3Vhu.9.1Tp.10.9Pro.0.0

and a file ``runbatch.out`` with the output in the form of a space separated text file table.

.. automodule:: AeroelasticSE.iecApp
   :members:
   :special-members:



