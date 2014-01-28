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

iec.runner.wrapper.FSTexe = 'C:/Models/FAST/FAST.exe'

#OC3 Example
ad_file    = 'NRELOffshrBsline5MW_AeroDyn.ipt'
ad_file_type = 1
blade_file = 'NRELOffshrBsline5MW_Blade.dat'
tower_file = 'NRELOffshrBsline5MW_Tower_Monopile_RF.dat'
platform_file = 'NRELOffshrBsline5MW_Platform_Monopile_RF.dat'
fst_file = 'NRELOffshrBsline5MW_Monopile_RF.fst'
fst_file_type = 1
FAST_DIR = os.path.dirname(os.path.realpath(__file__))
iec.runner.reader.template_path= os.path.join(FAST_DIR,"OC3_Files")
ad_fname = os.path.join(iec.runner.reader.template_path, ad_file)
bl_fname = os.path.join(iec.runner.reader.template_path, blade_file)
tw_fname = os.path.join(iec.runner.reader.template_path, tower_file)
pl_fname = os.path.join(iec.runner.reader.template_path, platform_file)
fs_fname = os.path.join(iec.runner.reader.template_path, fst_file)

iec.runner.reader.ad_file = ad_fname
iec.runner.reader.ad_file_type = ad_file_type
iec.runner.reader.blade_file = bl_fname
iec.runner.reader.tower_file = tw_fname
iec.runner.reader.platform_file = pl_fname
iec.runner.reader.fst_file = fs_fname
iec.runner.reader.fst_file_type = fst_file_type

iec.runner.writer.template_path = os.path.join(FAST_DIR,"tmp")      
fst_file = iec.runner.writer.fst_file
    
iec.runner.wrapper.FSTInputFile = os.path.join(iec.runner.reader.template_path, fst_file)

iec.sequential = True

iec.run()
