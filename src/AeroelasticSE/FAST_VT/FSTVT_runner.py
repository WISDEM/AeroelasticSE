""" This module implements FAST wrapper in terms of fusedwind's VariableTree based representation of a wind turbine.
The variable tree is a generic (wind-code agnostic) and hierarchical structural representation
of a modern wind turbine. 
This module is a very simple tutorial example of reading in a FAST file into a set of variable trees, manipulating environmental conditions and updating the variable trees, then writing a new set of FAST files and running FAST for multiple environmental cases.
"""

import os

from openmdao.lib.casehandlers.api import ListCaseRecorder
# from fusedwind.lib.caseiter import FUSEDCaseIterator
from fusedwind.runSuite.runCase import IECRunCaseBaseVT
from fusedwind.runSuite.runBatch import FUSEDIECCaseIterator
from FSTVT_runIEC import FUSEDFSTCaseRunner


iec = FUSEDIECCaseIterator()

for w in [10, 12]:
    c = IECRunCaseBaseVT()
    c.environment.vhub = w
    c.environment.ti = 10.
    c.simulation.time_stop = 30.
    c.simulation.time_step = 0.02
    c.case_name = 'wsp%2.1f_TI%2.1f' % (w, 10) 
    iec.cases.append(c)
iec.setup_cases()
iec.replace('runner', FUSEDFSTCaseRunner())

iec.sequential = True

print [c.name for c in iec.driver.workflow]
print [c.name for c in iec.runner.driver.workflow]

iec.run()