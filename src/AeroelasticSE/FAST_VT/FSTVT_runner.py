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
#os.environ['OPENMDAO_KEEPDIRS'] = '1'

iec.run()
