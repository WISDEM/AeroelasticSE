""" This module implements FAST wrapper in terms of fusedwind's VariableTree based representation of a wind turbine.
The variable tree is a generic (wind-code agnostic) and hierarchical structural representation
of a modern wind turbine. 
This module is a very simple tutorial example of reading in a FAST file into a set of variable trees, manipulating environmental conditions and updating the variable trees, then writing a new set of FAST files and running FAST for multiple environmental cases.
"""

import os
import numpy as np
from openmdao.lib.casehandlers.api import ListCaseRecorder
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
options, args = get_options()

#------------------ Initialize DLC ------------------#
# Must be specified for each DLC
c = IECRunCaseBaseVT()
c.init_conditions.DLC = 1.4


#---------- User inputs---------#
c.basic_turbine.hub_height = 80
c.init_conditions.RefHt = 180
IECstandard = '"3"'


V_range = np.arange(4, 25, 2)														# Wind speed range
Hs_range = [0.672, 0.745, 0.899,1.116,1.358,1.655,1.92,2.289,2.761,3.266, 4.177]	# Wave height range
Tp_range = [7.495,7.147,6.436,5.94,5.711,5.749,5.828,6.091,6.486,6.869,7.729]		# Wave period range

if c.init_conditions.DLC == 6.1 or c.init_conditions.DLC == c.init_conditions.DLC == 6.2 or c.init_conditions.DLC == 6.3 or c.init_conditions.DLC == 7.1:
    c.environment.shear_exp = .11
else:
    c.environment.shear_exp = .14

if c.init_conditions.DLC == 1.1 or c.init_conditions.DLC == 1.2 or c.init_conditions.DLC == 1.6 or c.init_conditions.DLC == 2.1 or c.init_conditions.DLC == 6.4:
    IEC_WindType = 'NTM'
elif c.init_conditions.DLC == 1.3:
    IEC_WindType = 'ETM'
elif c.init_conditions.DLC == 1.4: 
    IEC_WindType = 'ECD'
elif c.init_condiitions.DLC == 1.5:
    IEC_WindType = 'EWS'
elif c.init_conditions.DLC == 2.3:
    IEC_WindType = 'EOG'
elif c.init_conditions.DLC == 6.1 or c.init_conditions.DLC == 6.2:
    IEC_WindType = '1EWM50'
elif c.init_conditions.DLC == 6.3 or c.init_conditions.DLC == 7.1:
    IEC_WindType = '1EWM1'

# Initial Conditions
WSPtfmPitch = [0,4,12,15,22]														# Wind speeds used for ptfm pitch interp
PtfmPitch = [0,.5, 6, 4, 2.8]														# Pitch points used for ptfm pitch interp
WSPtfmSurge =[0, 4, 12.1, 14,22]													# Wind speeds used for ptfm surge interp
PtfmSurge = [0,1.6, 12.3, 9.3, 5.9]													# Surge points used for pftm surge interp
WSPitch =[0,12,14,22]																# Wind speeds used for blade pitch interp
Pitch =[0,0,6.2,18.9]																# Pitch points used for blade pitch interp
WSRpm =[0,4,9,12]																	# Wind speeds used for rotor speed interp
Rpm =[0,7,14.2,16]																	# Rotor speeds used for rotor speed interp

numgrid_z = 37 																		# TurbSim horizontal grid
numgrid_y = 39 																		# TurbSim vertical grid
grid_height = 200																	# Grid height [m]
grid_width = 190																	# Grid width [m]

if c.init_conditions.DLC == 1.1 or c.init_conditions.DLC == 1.2 or c.init_conditions.DLC == 2.1 or c.init_conditions.DLC == 6.4:
    c.simulation.time_stop = 630
elif c.init_conditions.DLC == 1.4 or c.init_conditions.DLC == 1.5 or c.init_conditions.DLC == 2.3:
    c.simulation.time_stop = 90
elif c.init_conditions.DLC == 1.6 or c.init_conditions.DLC == 6.1 or c.init_conditions.DLC == 6.2 or c.init_conditions.DLC == 6.3 or c.init_conditions.DLC == 7.1:
    c.simulation.time_stop = 3630

if c.init_conditions.DLC == 2.1:
    seeds = np.arrange(1,13, 1)
else:
    seeds = np.arange(1,7,1)

numcases = len(V_range +1)*len(seeds)
# ---------------------------#

# Loop over wind speeds, wave heights, wave periods and seeds to make each of the ad, ptm, and fst files
num = 0

for i in range(0, len(seeds-2)):
	for j in range(0,len(V_range)):

		# initialize_IECRunCaseBaseVT()
		c.environment.vhub = V_range[j]
		c.environment.Hs = Hs_range[j]
		c.environment.Tp = Tp_range[j]
		num = num + 1
		waveseed1 = 123456789 + num
		waveseed2 = 1011121320 + num
		c.case_name = 'DLC_%2.1f_V%2.1f_Hs%2.1f_Tp%2.1f_S%2.1f' % (c.init_conditions.DLC, c.environment.vhub, c.environment.Hs, c.environment.Tp, num)
		
		#------------------ Aerodyn Inputs ------------------#
		c.aero_inputs.WindFile = 'turbsim.hh' #this will need to change for each case
		c.aero_inputs.NumFoil = 5
		print(c.aero_inputs.NumFoil)

		#------------------ FAST Inputs ------------------#
		c.fst_inputs.VSContrl = 2
		c.fst_inputs.TStart = 30
		c.fst_inputs.PtfmModel = 3
		c.fst_inputs.PtfmFile = 'NRELOffshrBsline5MW_Platform_Monopile_RF.dat'
		c.fst_inputs.TwrFile = 'NRELOffshrBsline5MW_Tower_Monopile_RF'
		c.fst_inputs.ADFile = 'NRELOffshrBsline5MW_AeroDyn.ipt'
		c.fst_inputs.BldFile1 = 'NRELOffshrBsline5MW_Blade.dat'
		c.fst_inputs.BldFile2 = 'NRELOffshrBsline5MW_Blade.dat'
		c.fst_inputs.BldFile3 = 'NRELOffshrBsline5MW_Blade.dat'

		if c.init_conditions.DLC == 1.1 or c.init_conditions.DLC == 1.2 or c.init_conditions.DLC == 2.1 or c.init_conditions.DLC == 6.4:
		    c.fst_inputs.TMax = 500
		elif c.init_conditions.DLC == 1.4 or c.init_conditions.DLC == 1.5 or c.init_conditions.DLC == 2.3:
		    c.fst_inputs.TMax = 90
		elif c.init_conditions.DLC == 1.6 or c.init_conditions.DLC == 6.1 or c.init_conditions.DLC == 6.2 or c.init_conditions.DLC == 6.3 or c.init_conditions.DLC == 7.1:
		    c.fst_inputs.TMax = 3630

		if c.init_conditions.DLC == 6.1 or c.init_conditions.DLC == 6.2 or c.init_conditions.DLC == 6.4 or c.init_conditions.DLC == 7.1:
		    c.fst_inputs.TimGenOn = 9999.9
		else:
		    c.fst_inputs.TimGenOn = 0

		if c.init_conditions.DLC == 2.1:
		    c.fst_inputs.TPitManS1 = 60
		elif c.init_conditions.DLC == 2.3:
		    c.fst_inputs.TPitManS1 = [60.2, 68.6, 62.3]
		elif c.init_conditions.DLC == 6.1 or c.init_conditions.DLC == 6.2 or c.init_conditions.DLC == 6.3 or c.init_conditions.DLC == 6.4 or c.init_conditions.DLC == 7.1:
		    c.fst_inputs.TPitManS1 = 0
		else:
		    c.fst_inputs.TPitManS1 = 9999.9

		if c.init_conditions.DLC == 2.1:
		    c.fst_inputs.TPitManS2 = 60.2
		elif c.init_conditions.DLC == 2.3:
		    c.fst_inputs.TPitManS2 = [60.2, 68.6, 62.3]
		elif c.init_conditions.DLC == 6.1 or 6.2 or 6.3 or 6.4 or 7.1:
		    c.fst_inputs.TPitManS2 = 0
		else:
		    c.fst_inputs.TPitManS2 = 60.2

		if c.init_conditions.DLC == 2.1:
		    c.fst_inputs.TPitManS3 = 60.2
		elif c.init_conditions.DLC == 2.3:
		    c.fst_inputs.TPitManS3 = [60.2, 68.6, 62.3]
		elif c.init_conditions.DLC == 6.1 or 6.2 or 6.3 or 6.4 or 7.1:
		    c.fst_inputs.TPitManS3 = 0
		else:
		    c.fst_inputs.TPitManS3 = 60.2

		if c.init_conditions.DLC == 2.1:
		    c.fst_inputs.TPitManE1 = [60, 60.775, 61.2, 61.6, 61.96, 62.36]
		elif c.init_conditions.DLC == 2.3:
		    c.fst_inputs.TPitManE1 = [71.324, 79.725, 71.06]
		elif c.init_conditions.DLC == 6.1 or c.init_conditions.DLC == 6.2 or c.init_conditions.DLC == 6.3 or c.init_conditions.DLC == 6.4 or c.init_conditions.DLC == 7.1:
		    c.fst_inputs.TPitManE1 = 0
		else:
		    c.fst_inputs.TPitManE1 = 9999.9

		if c.init_conditions.DLC == 2.1:
		    c.fst_inputs.TPitManE2 = [71.325, 70.55, 70.15, 69.75, 69.36, 68.96]
		elif c.init_conditions.DLC == 2.3:
		    c.fst_inputs.TPitManE2 = [71.324, 79.725, 71.06]
		elif c.init_conditions.DLC == 6.1 or c.init_conditions.DLC == 6.2 or c.init_conditions.DLC == 6.3 or c.init_conditions.DLC == 6.4 or c.init_conditions.DLC == 7.1:
		    c.fst_inputs.TPitManE2 = 0
		else:
		    c.fst_inputs.TPitManE2 = 9999.9

		if c.init_conditions.DLC == 2.1:
		    c.fst_inputs.TPitManE3 = [71.325, 70.55, 70.15, 69.75, 69.36, 68.96]
		elif c.init_conditions.DLC == 2.3:
		    c.fst_inputs.TPitManE3 = [71.324, 79.725, 71.06]
		elif c.init_conditions.DLC == 6.1 or 6.2 or 6.3 or 6.4 or 7.1:
		    c.fst_inputs.TPitManE3 = 0
		else:
		    c.fst_inputs.TPitManE3 = 9999.9

		if c.init_conditions.DLC == 2.3 or c.init_conditions.DLC == 6.1 or c.init_conditions.DLC == 6.2 or c.init_conditions.DLC == 6.3 or c.init_conditions.DLC == 6.4:
		    c.fst_inputs.BlPitchF1 = 89
		else:
		    c.fst_inputs.BlPitchF1 = 0


		if c.init_conditions.DLC == 2.1 or c.init_conditions.DLC == 2.3 or c.init_conditions.DLC == 6.1 or c.init_conditions.DLC == 6.2 or c.init_conditions.DLC == 6.3 or c.init_conditions.DLC == 6.4 or c.init_conditions.DLC == 7.1:
		    c.fst_inputs.BlPitchF2 = 89
		else:
		    c.fst_inputs.BlPitchF2 = 0

		if c.init_conditions.DLC == 2.1 or c.init_conditions.DLC == 2.3 or c.init_conditions.DLC == 6.1 or c.init_conditions.DLC == 6.2 or c.init_conditions.DLC == 6.3 or c.init_conditions.DLC == 6.4 or c.init_conditions.DLC == 7.1:
		    c.fst_inputs.BlPitchF3 = 89
		else:
		    c.fst_inputs.BlPitchF3 = 0

		if c.init_conditions.DLC == 2.1 or c.init_conditions.DLC == 2.3 or c.init_conditions.DLC == 6.1 or c.init_conditions.DLC == 6.2 or c.init_conditions.DLC == 6.3 or c.init_conditions.DLC == 6.4 or c.init_conditions.DLC == 7.1:
		    c.fst_inputs.PCMode = 0
		else:
		    c.fst_inputs.PCMode = 1

		c.fst_inputs.BlPitch1 = np.interp(V_range[j], WSPitch, Pitch)
		c.fst_inputs.BlPitch2 = np.interp(V_range[j], WSPitch, Pitch)
		c.fst_inputs.BlPitch3 = np.interp(V_range[j], WSPitch, Pitch)
		c.fst_inputs.RotSpeed = np.interp(V_range[j], WSRpm, Rpm)

		#------------------ Platform Inputs ------------------#
		c.ptfm_inputs.WaveHs = c.environment.Hs
		c.ptfm_inputs.WaveTp = c.environment.Tp
		c.ptfm_inputs.WaveSeed1 = waveseed1
		c.ptfm_inputs.WaveSeed2 = waveseed2
		c.ptfm_inputs.PtfmSway = 0
		c.ptfm_inputs.PtfmHeave = 0
		c.ptfm_inputs.PtfmRoll = 0
		c.ptfm_inputs.PtfmYaw = 0
		c.ptfm_inputs.WAMITFile = 'model'
		c.ptfm_inputs.WaveTMax = 3630
		c.ptfm_inputs.WaveSeed1 = 123456
		c.ptfm_inputs.WaveSeed2 = 123457
		c.ptfm_inputs.WaveMod = 2
		c.ptfm_inputs.WaveDT = 0.25
		c.ptfm_inputs.CurrSSV0 = 0
		c.ptfm_inputs.CurrSSDir = 0
		c.ptfm_inputs.CurrNSRef = 20
		c.ptfm_inputs.CurrNSV0 = 0

		if c.init_conditions.DLC == 6.1 or c.init_conditions.DLC == 6.2 or c.init_conditions.DLC == 6.3 or c.init_conditions.DLC == 7.1:
			wd = [330,0,30]
			for k in range(0, len(wd)):
				c.environment.WaveDir = wd(k)
		else:   
			c.environment.WaveDir = 0

		if c.init_conditions.DLC == 6.1 or c.init_conditions.DLC == 6.2 or c.init_conditions.DLC == 6.3 or c.init_conditions.DLC == 6.4 or c.init_conditions.DLC == 7.1:
		    c.ptfm_inputs.PtfmSurge = 0
		    c.ptfm_inputs.PtfmPitch = 0
		else:
		    c.ptfm_inputs.PtfmSurge = np.interp(V_range[j], WSPtfmSurge, PtfmSurge)
		    c.ptfm_inputs.PtfmPitch = np.interp(V_range[j], WSPtfmPitch, PtfmPitch)
		
		if c.init_conditions.DLC == 6.1 or c.init_conditions.DLC == 6.3 or c.init_conditions.DLC == 7.1:
			ny = [-8,0,8]
			for k in range(0,len(ny)):
		    		c.fst_inputs.YawNeut = ny(k)
		elif c.init_conditions.DLC == 6.2:
			ny = [20, 40, 60, 80, 100, 120, 140, 160, 180, -160, -140, -120, -100, -80, -60, -40, -20, 0]
			for k in range(0,len(ny)):
		    		c.fst_inputs.YawNeut = ny(k)
		else:
		    c.fst_inputs.YawNeut = 0

		print("RUNNING DLC " + str(c.init_conditions.DLC))

		print "appending c"
		iec.cases.append(c)

iec.replace('runner', FUSEDFSTCaseRunner(options.file_locs))
iec.setup_cases()
iec.sequential = True

print [c.name for c in iec.driver.workflow]
print [c.name for c in iec.runner.driver.workflow]
iec.run()
