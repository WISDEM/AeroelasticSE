""" This module implements FAST wrapper in terms of fusedwind's VariableTree based representation of a wind turbine.
The variable tree is a generic (wind-code agnostic) and hierarchical structural representation
of a modern wind turbine. 
This module is a very simple tutorial example of reading in a FAST file into a set of variable trees, manipulating environmental conditions and updating the variable trees, then writing a new set of FAST files and running FAST for multiple environmental cases.
"""
# 1 ---------

import os

from openmdao.lib.casehandlers.api import ListCaseRecorder
# from fusedwind.lib.caseiter import FUSEDCaseIterator
from fusedwind.runSuite.runCase import IECRunCaseBaseVT
from fusedwind.runSuite.runBatch import FUSEDIECCaseIterator, PGrafSubComponent
from FSTVT_runIEC import FUSEDFSTCaseRunner

def get_options():
    from optparse import OptionParser
    parser = OptionParser()    
    parser.add_option("-f", "--files", dest="file_locs",  type="string", default="runbatch-control.txt",
                                    help="main input file describing locations of template files, and output fields/files to write")
    (options, args) = parser.parse_args()
    return options, args


iec = FUSEDIECCaseIterator()


# 1 ---------
# 2 ---------

options, args = get_options()

for w in [10, 12]:
    c = IECRunCaseBaseVT()
    c.environment.vhub = w
    c.environment.ti = 10.
   # c.simulation.time_stop = 30.
   # c.simulation.time_step = 0.02
    c.case_name = 'wsp%2.1f_TI%2.1f' % (w, 10) 
    iec.cases.append(c)
#iec.replace('runner', FUSEDFSTCaseRunner(options.file_locs))
iec.replace('runner', FUSEDFSTCaseRunner()) #kld hard-coding
#iec.replace('runner', PGrafSubComponent())

iec.setup_cases()

iec.sequential = True

print [c.name for c in iec.driver.workflow]
print [c.name for c in iec.runner.driver.workflow]

# 2 ---------
# 3 ---------

#iec.runner.run()
iec.run()

# 3 ---------
