.. _tutorial-label:

.. currentmodule:: rotorse.rotoraero

Tutorial
========

The following examples are called as test cases in the modules  (:mod:`AeroelasticSE.runFAST`),   (:mod:`AeroelasticSE.runTurbSim`),  (:mod:`AeroelasticSE.FusedFAST`),  (:mod:`AeroelasticSE.iecApp`),

running FAST one time
---------------------

.. literalinclude:: ../src/AeroelasticSE/runFAST.py
    :start-after: def example
    :end-before: def turbsim_example

This will print something like:

>>> max power
>>> 11840.0

Run::

  python runFAST.py --help

to see options for this example.


running TurbSim one time
------------------------

.. literalinclude:: ../src/AeroelasticSE/runTurbSim.py
    :start-after: if __name__==


running FusedFAST
-----------------

.. literalinclude:: ../src/AeroelasticSE/FusedFAST.py
    :start-after: def openFAST_test


running FAST_component
----------------------

.. literalinclude:: ../src/AeroelasticSE/FAST_component.py
    :start-after: def FAST_component_test
    :end-before: end FAST_component_test


running FAST_iter_component
---------------------------

.. literalinclude:: ../src/AeroelasticSE/FAST_component.py
    :start-after: def FAST_iter_component_test
    :end-before: end FAST_iter_component_test



