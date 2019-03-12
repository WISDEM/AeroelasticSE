import os
import numpy as np

from CaseGen_General import CaseGen_General
from CaseGen_IEC import CaseGen_IEC

# def power_curve():

#     fastBatch = runFAST_pywrapper_batch(FAST_ver='OpenFAST')

#     fastBatch.FAST_exe = 'C:/Users/egaertne/WT_Codes/openfast/build/glue-codes/fast/openfast.exe'   # Path to executable
#     fastBatch.FAST_InputFile = '5MW_Land_DLL_WTurb.fst'   # FAST input file (ext=.fst)
#     fastBatch.FAST_directory = 'C:/Users/egaertne/WT_Codes/models/openfast/glue-codes/fast/5MW_Land_DLL_WTurb'   # Path to fst directory files
#     fastBatch.FAST_runDirectory = 'temp/OpenFAST/power_curve'
#     namebase = 'power_curve'

#     ## Generate case list using General Case Generator
#     ## Specify several variables that change independently or collectly

#     # inital conditions
#     U = [3., 4., 5., 6., 7., 8., 9., 10., 11., 12., 13., 14., 15., 16., 17., 18., 19., 20., 21., 22., 23., 24., 25]
#     omega = [6.972, 7.183, 7.506, 7.942, 8.469, 9.156, 10.296, 11.431, 11.89, 12.1, 12.1, 12.1, 12.1, 12.1, 12.1, 12.1, 12.1, 12.1, 12.1, 12.1, 12.1, 12.1, 12.1]
#     pitch = [0., 0., 0., 0., 0., 0., 0., 0., 0., 3.823, 6.602, 8.668, 10.450, 12.055, 13.536, 14.920, 16.226, 17.473, 18.699, 19.941, 21.177, 22.347, 23.469]

    # case_inputs = {}
#     case_inputs[("Fst","TMax")] = {'vals':[120.], 'group':0}
#     case_inputs[("InflowWind","WindType")] = {'vals':[1], 'group':0}
#     case_inputs[("InflowWind","HWindSpeed")] = {'vals':U, 'group':1}
#     case_inputs[("ElastoDyn","RotSpeed")] = {'vals':omega, 'group':1}
#     case_inputs[("ElastoDyn","BlPitch1")] = {'vals':pitch, 'group':1}
#     case_inputs[("ElastoDyn","BlPitch2")] = case_inputs[("ElastoDyn","BlPitch1")]
#     case_inputs[("ElastoDyn","BlPitch3")] = case_inputs[("ElastoDyn","BlPitch1")]
    
#     from CaseGen_General import CaseGen_General
#     case_list, case_name_list = CaseGen_General(case_inputs, dir_matrix=fastBatch.FAST_runDirectory, namebase=namebase)

#     fastBatch.case_list = case_list
#     fastBatch.case_name_list = case_name_list

#     # fastBatch.run_serial()
#     fastBatch.run_multi(4)


def RotorSE_rated(namebase, TMax, U, Omega, Pitch, rho, mu, shearExp):

    # Default Runtime
    T      = 60.
    TStart = 30.
    
    # Overwrite for testing
    if TMax < T:
        T      = TMax
        TStart = 0.

    case_inputs = {}
    case_inputs[("Fst","TMax")]              = {'vals':[T], 'group':0}
    case_inputs[("Fst","TStart")]            = {'vals':[TStart], 'group':0}
    case_inputs[("Fst","OutFileFmt")]        = {'vals':[2], 'group':0}
    
    case_inputs[("InflowWind","WindType")]   = {'vals':[1], 'group':0}
    case_inputs[("InflowWind","HWindSpeed")] = {'vals':[U], 'group':0}
    case_inputs[("InflowWind","PLexp")] = {'vals':[shearExp], 'group':0}

    case_inputs[("ElastoDyn","RotSpeed")]    = {'vals':[Omega], 'group':0}
    case_inputs[("ElastoDyn","BlPitch1")]    = {'vals':[Pitch], 'group':0}
    case_inputs[("ElastoDyn","BlPitch2")]    = {'vals':[Pitch], 'group':0}
    case_inputs[("ElastoDyn","BlPitch3")]    = {'vals':[Pitch], 'group':0}
    case_inputs[("ElastoDyn","YawDOF")]      = {'vals':['False'], 'group':0}
    case_inputs[("ElastoDyn","FlapDOF1")]    = {'vals':['True'], 'group':0}
    case_inputs[("ElastoDyn","FlapDOF2")]    = {'vals':['True'], 'group':0}
    case_inputs[("ElastoDyn","EdgeDOF")]     = {'vals':['True'], 'group':0}
    case_inputs[("ElastoDyn","DrTrDOF")]     = {'vals':['False'], 'group':0}
    case_inputs[("ElastoDyn","GenDOF")]      = {'vals':['True'], 'group':0} 
    case_inputs[("ElastoDyn","TwFADOF1")]    = {'vals':['False'], 'group':0}
    case_inputs[("ElastoDyn","TwFADOF2")]    = {'vals':['False'], 'group':0}
    case_inputs[("ElastoDyn","TwSSDOF1")]    = {'vals':['False'], 'group':0}
    case_inputs[("ElastoDyn","TwSSDOF2")]    = {'vals':['False'], 'group':0}

    case_inputs[("ServoDyn","PCMode")]       = {'vals':[5], 'group':0}
    case_inputs[("ServoDyn","VSContrl")]     = {'vals':[5], 'group':0}

    case_inputs[("AeroDyn15","WakeMod")]     = {'vals':[1], 'group':0}
    case_inputs[("AeroDyn15","AFAeroMod")]   = {'vals':[2], 'group':0}
    case_inputs[("AeroDyn15","TwrPotent")]   = {'vals':[0], 'group':0}
    case_inputs[("AeroDyn15","TwrShadow")]   = {'vals':['False'], 'group':0}
    case_inputs[("AeroDyn15","TwrAero")]     = {'vals':['False'], 'group':0}
    case_inputs[("AeroDyn15","AirDens")]     = {'vals':[rho], 'group':0}
    case_inputs[("AeroDyn15","KinVisc")]     = {'vals':[mu], 'group':0}

    case_inputs[("AeroDyn15","SkewMod")]     = {'vals':[1], 'group':0}
    case_inputs[("AeroDyn15","TipLoss")]     = {'vals':['True'], 'group':0}
    case_inputs[("AeroDyn15","HubLoss")]     = {'vals':['True'], 'group':0}
    case_inputs[("AeroDyn15","TanInd")]      = {'vals':['True'], 'group':0}
    case_inputs[("AeroDyn15","AIDrag")]      = {'vals':['True'], 'group':0}
    case_inputs[("AeroDyn15","TIDrag")]      = {'vals':['True'], 'group':0}
    case_inputs[("AeroDyn15","IndToler")]    = {'vals':[1.e-5], 'group':0}
    case_inputs[("AeroDyn15","MaxIter")]     = {'vals':[5000], 'group':0}
    case_inputs[("AeroDyn15","UseBlCm")]     = {'vals':['True'], 'group':0}
    

    namebase += '_rated'
    case_list, case_name_list = CaseGen_General(case_inputs, namebase=namebase, save_matrix=False)

    channels  = ["TipDxc1", "TipDyc1"]
    channels += ["RootMxc1", "RootMyc1", "RootMzc1", "RootMxc2", "RootMyc2", "RootMzc2", "RootMxc3", "RootMyc3", "RootMzc3"]
    channels += ["RootFxc1", "RootFyc1", "RootFzc1", "RootFxc2", "RootFyc2", "RootFzc2", "RootFxc3", "RootFyc3", "RootFzc3"]
    channels += ["RtAeroCp", "RotTorq", "RotThrust", "RotSpeed"]

    return case_list, case_name_list, channels

def RotorSE_DLC_1_4_Rated(fst_vt, runDir, namebase, TMax, turbine_class, turbulence_class, Vrated, U_init=[], Omega_init=[], pitch_init=[], Turbsim_exe=''):

    # Default Runtime
    T      = 60.
    TStart = 30.
    # TStart = 0.
    
    # Overwrite for testing
    if TMax < T:
        T      = TMax
        TStart = 0.


    iec = CaseGen_IEC()
    iec.init_cond[("ElastoDyn","RotSpeed")] = {'U':  U_init}
    iec.init_cond[("ElastoDyn","RotSpeed")]['val'] = Omega_init
    iec.init_cond[("ElastoDyn","BlPitch1")] = {'U':  U_init}
    iec.init_cond[("ElastoDyn","BlPitch1")]['val'] = pitch_init
    iec.init_cond[("ElastoDyn","BlPitch2")] = iec.init_cond[("ElastoDyn","BlPitch1")]
    iec.init_cond[("ElastoDyn","BlPitch3")] = iec.init_cond[("ElastoDyn","BlPitch1")]
    iec.Turbine_Class = turbine_class
    iec.Turbulence_Class = turbulence_class
    iec.D = fst_vt['ElastoDyn']['TipRad']*2.
    iec.z_hub = fst_vt['InflowWind']['RefHt']

    iec.dlc_inputs = {}
    iec.dlc_inputs['DLC']   = [1.4]
    iec.dlc_inputs['U']     = [[Vrated]]
    iec.dlc_inputs['Seeds'] = [[]]
    iec.dlc_inputs['Yaw']   = [[]]
    iec.transient_dir_change        = '-'  # '+','-','both': sign for transient events in EDC, EWS
    iec.transient_shear_orientation = 'v'  # 'v','h','both': vertical or horizontal shear for EWS

    iec.wind_dir        = runDir
    iec.case_name_base  = namebase + '_gust'
    iec.Turbsim_exe     = ''
    iec.debug_level     = 0
    iec.parallel_windfile_gen = False
    iec.run_dir         = runDir

    case_inputs = {}
    case_inputs[("Fst","TMax")]              = {'vals':[T], 'group':0}
    case_inputs[("Fst","TStart")]            = {'vals':[TStart], 'group':0}
    case_inputs[("Fst","OutFileFmt")]        = {'vals':[2], 'group':0}

    case_inputs[("ElastoDyn","YawDOF")]      = {'vals':['True'], 'group':0}
    case_inputs[("ElastoDyn","FlapDOF1")]    = {'vals':['True'], 'group':0}
    case_inputs[("ElastoDyn","FlapDOF2")]    = {'vals':['True'], 'group':0}
    case_inputs[("ElastoDyn","EdgeDOF")]     = {'vals':['True'], 'group':0}
    case_inputs[("ElastoDyn","DrTrDOF")]     = {'vals':['False'], 'group':0}
    case_inputs[("ElastoDyn","GenDOF")]      = {'vals':['True'], 'group':0} 
    case_inputs[("ElastoDyn","TwFADOF1")]    = {'vals':['False'], 'group':0}
    case_inputs[("ElastoDyn","TwFADOF2")]    = {'vals':['False'], 'group':0}
    case_inputs[("ElastoDyn","TwSSDOF1")]    = {'vals':['False'], 'group':0}
    case_inputs[("ElastoDyn","TwSSDOF2")]    = {'vals':['False'], 'group':0}

    case_inputs[("ServoDyn","PCMode")]       = {'vals':[5], 'group':0}
    case_inputs[("ServoDyn","VSContrl")]     = {'vals':[5], 'group':0}
    case_inputs[("ServoDyn","YCMode")]       = {'vals':[5], 'group':0}

    case_inputs[("AeroDyn15","WakeMod")]     = {'vals':[1], 'group':0}
    case_inputs[("AeroDyn15","AFAeroMod")]   = {'vals':[2], 'group':0}
    case_inputs[("AeroDyn15","TwrPotent")]   = {'vals':[0], 'group':0}
    case_inputs[("AeroDyn15","TwrShadow")]   = {'vals':['False'], 'group':0}
    case_inputs[("AeroDyn15","TwrAero")]     = {'vals':['False'], 'group':0}

    case_inputs[("AeroDyn15","SkewMod")]     = {'vals':[1], 'group':0}
    case_inputs[("AeroDyn15","TipLoss")]     = {'vals':['True'], 'group':0}
    case_inputs[("AeroDyn15","HubLoss")]     = {'vals':['True'], 'group':0}
    case_inputs[("AeroDyn15","TanInd")]      = {'vals':['True'], 'group':0}
    case_inputs[("AeroDyn15","AIDrag")]      = {'vals':['True'], 'group':0}
    case_inputs[("AeroDyn15","TIDrag")]      = {'vals':['True'], 'group':0}
    case_inputs[("AeroDyn15","IndToler")]    = {'vals':[1.e-5], 'group':0}
    case_inputs[("AeroDyn15","MaxIter")]     = {'vals':[5000], 'group':0}
    case_inputs[("AeroDyn15","UseBlCm")]     = {'vals':['True'], 'group':0}
    
    case_list, case_name_list = iec.execute(case_inputs=case_inputs)

    channels  = ["TipDxc1", "TipDyc1", "TipDzc1", "TipDxc2", "TipDyc2", "TipDzc2", "TipDxc3", "TipDyc3", "TipDzc3"]
    channels += ["RootMxc1", "RootMyc1", "RootMzc1", "RootMxc2", "RootMyc2", "RootMzc2", "RootMxc3", "RootMyc3", "RootMzc3"]
    channels += ["RootFxc1", "RootFyc1", "RootFzc1", "RootFxc2", "RootFyc2", "RootFzc2", "RootFxc3", "RootFyc3", "RootFzc3"]
    channels += ["RtAeroCp", "RotTorq", "RotThrust", "RotSpeed", "NacYaw"]

    channels += ["B1N1Fx", "B1N2Fx", "B1N3Fx", "B1N4Fx", "B1N5Fx", "B1N6Fx", "B1N7Fx", "B1N8Fx", "B1N9Fx"]
    channels += ["B1N1Fy", "B1N2Fy", "B1N3Fy", "B1N4Fy", "B1N5Fy", "B1N6Fy", "B1N7Fy", "B1N8Fy", "B1N9Fy"]

    return case_list, case_name_list, channels

def RotorSE_DLC_7_1_Steady(fst_vt, runDir, namebase, TMax, turbine_class, turbulence_class, U, U_init=[], Omega_init=[], pitch_init=[], Turbsim_exe=''):
    # Extreme 1yr return period wind speed with a power fault resulting in the blade not feathering

    # Default Runtime
    T      = 60.
    TStart = 30.
    
    # Overwrite for testing
    if TMax < T:
        T      = TMax
        TStart = 0.

    Pitch = 0.
    Omega = 0.

    case_inputs = {}
    case_inputs[("Fst","TMax")]              = {'vals':[T], 'group':0}
    case_inputs[("Fst","TStart")]            = {'vals':[TStart], 'group':0}
    case_inputs[("Fst","OutFileFmt")]        = {'vals':[2], 'group':0}
    
    case_inputs[("InflowWind","WindType")]   = {'vals':[1], 'group':0}
    case_inputs[("InflowWind","HWindSpeed")] = {'vals':[U], 'group':0}
    case_inputs[("InflowWind","PLexp")] = {'vals':[0.11], 'group':0}

    case_inputs[("ElastoDyn","RotSpeed")]    = {'vals':[Omega], 'group':0}
    case_inputs[("ElastoDyn","BlPitch1")]    = {'vals':[Pitch], 'group':0}
    case_inputs[("ElastoDyn","BlPitch2")]    = {'vals':[Pitch], 'group':0}
    case_inputs[("ElastoDyn","BlPitch3")]    = {'vals':[Pitch], 'group':0}
    case_inputs[("ElastoDyn","YawDOF")]      = {'vals':['True'], 'group':0}
    case_inputs[("ElastoDyn","FlapDOF1")]    = {'vals':['True'], 'group':0}
    case_inputs[("ElastoDyn","FlapDOF2")]    = {'vals':['True'], 'group':0}
    case_inputs[("ElastoDyn","EdgeDOF")]     = {'vals':['True'], 'group':0}
    case_inputs[("ElastoDyn","DrTrDOF")]     = {'vals':['False'], 'group':0}
    case_inputs[("ElastoDyn","GenDOF")]      = {'vals':['False'], 'group':0} 
    case_inputs[("ElastoDyn","TwFADOF1")]    = {'vals':['False'], 'group':0}
    case_inputs[("ElastoDyn","TwFADOF2")]    = {'vals':['False'], 'group':0}
    case_inputs[("ElastoDyn","TwSSDOF1")]    = {'vals':['False'], 'group':0}
    case_inputs[("ElastoDyn","TwSSDOF2")]    = {'vals':['False'], 'group':0}

    case_inputs[("ServoDyn","PCMode")]       = {'vals':[0], 'group':0}
    case_inputs[("ServoDyn","VSContrl")]     = {'vals':[5], 'group':0}
    case_inputs[("ServoDyn","YCMode")]       = {'vals':[5], 'group':0}

    case_inputs[("AeroDyn15","WakeMod")]     = {'vals':[1], 'group':0}
    case_inputs[("AeroDyn15","AFAeroMod")]   = {'vals':[1], 'group':0}
    case_inputs[("AeroDyn15","TwrPotent")]   = {'vals':[0], 'group':0}
    case_inputs[("AeroDyn15","TwrShadow")]   = {'vals':['False'], 'group':0}
    case_inputs[("AeroDyn15","TwrAero")]     = {'vals':['False'], 'group':0}

    case_inputs[("AeroDyn15","SkewMod")]     = {'vals':[1], 'group':0}
    case_inputs[("AeroDyn15","TipLoss")]     = {'vals':['True'], 'group':0}
    case_inputs[("AeroDyn15","HubLoss")]     = {'vals':['True'], 'group':0}
    case_inputs[("AeroDyn15","TanInd")]      = {'vals':['True'], 'group':0}
    case_inputs[("AeroDyn15","AIDrag")]      = {'vals':['True'], 'group':0}
    case_inputs[("AeroDyn15","TIDrag")]      = {'vals':['True'], 'group':0}
    case_inputs[("AeroDyn15","IndToler")]    = {'vals':[1.e-5], 'group':0}
    case_inputs[("AeroDyn15","MaxIter")]     = {'vals':[5000], 'group':0}
    case_inputs[("AeroDyn15","UseBlCm")]     = {'vals':['True'], 'group':0}
    

    namebase += '_idle50yr'
    case_list, case_name_list = CaseGen_General(case_inputs, namebase=namebase, save_matrix=False)

    channels  = ["TipDxc1", "TipDyc1", "TipDzc1", "TipDxc2", "TipDyc2", "TipDzc2", "TipDxc3", "TipDyc3", "TipDzc3"]
    channels += ["RootMxc1", "RootMyc1", "RootMzc1", "RootMxc2", "RootMyc2", "RootMzc2", "RootMxc3", "RootMyc3", "RootMzc3"]
    channels += ["RootFxc1", "RootFyc1", "RootFzc1", "RootFxc2", "RootFyc2", "RootFzc2", "RootFxc3", "RootFyc3", "RootFzc3"]
    channels += ["RtAeroCp", "RotTorq", "RotThrust", "RotSpeed", "NacYaw"]

    channels += ["B1N1Fx", "B1N2Fx", "B1N3Fx", "B1N4Fx", "B1N5Fx", "B1N6Fx", "B1N7Fx", "B1N8Fx", "B1N9Fx"]
    channels += ["B1N1Fy", "B1N2Fy", "B1N3Fy", "B1N4Fy", "B1N5Fy", "B1N6Fy", "B1N7Fy", "B1N8Fy", "B1N9Fy"]

    return case_list, case_name_list, channels


def RotorSE_DLC_1_1_Turb(fst_vt, runDir, namebase, TMax, turbine_class, turbulence_class, U, U_init=[], Omega_init=[], pitch_init=[], Turbsim_exe=''):
    
    # Default Runtime
    T      = 630.
    TStart = 30.
    
    # Overwrite for testing
    if TMax < T:
        T      = TMax
        TStart = 0.


    iec = CaseGen_IEC()
    iec.init_cond[("ElastoDyn","RotSpeed")] = {'U':  U_init}
    iec.init_cond[("ElastoDyn","RotSpeed")]['val'] = Omega_init
    iec.init_cond[("ElastoDyn","BlPitch1")] = {'U':  U_init}
    iec.init_cond[("ElastoDyn","BlPitch1")]['val'] = pitch_init
    iec.init_cond[("ElastoDyn","BlPitch2")] = iec.init_cond[("ElastoDyn","BlPitch1")]
    iec.init_cond[("ElastoDyn","BlPitch3")] = iec.init_cond[("ElastoDyn","BlPitch1")]
    iec.Turbine_Class = turbine_class
    iec.Turbulence_Class = turbulence_class
    iec.D = fst_vt['ElastoDyn']['TipRad']*2.
    iec.z_hub = fst_vt['InflowWind']['RefHt']

    iec.dlc_inputs = {}
    iec.dlc_inputs['DLC']   = [1.1]
    iec.dlc_inputs['U']     = [[U]]
    # iec.dlc_inputs['Seeds'] = [[1]]
    iec.dlc_inputs['Seeds'] = [[310414237, 1764051066, 1935526301, 333954657, -960771537, 714191176]] # nothing special about these seeds, randomly generated
    iec.dlc_inputs['Yaw']   = [[]]
    iec.transient_dir_change        = '-'  # '+','-','both': sign for transient events in EDC, EWS
    iec.transient_shear_orientation = 'v'  # 'v','h','both': vertical or horizontal shear for EWS

    iec.wind_dir        = runDir
    iec.case_name_base  = namebase + '_turb'
    iec.Turbsim_exe     = Turbsim_exe
    iec.debug_level     = 0
    iec.parallel_windfile_gen = False
    iec.run_dir         = runDir

    case_inputs = {}
    case_inputs[("Fst","TMax")]              = {'vals':[T], 'group':0}
    case_inputs[("Fst","TStart")]            = {'vals':[TStart], 'group':0}
    case_inputs[("Fst","OutFileFmt")]        = {'vals':[2], 'group':0}

    case_inputs[("ElastoDyn","YawDOF")]      = {'vals':['True'], 'group':0}
    case_inputs[("ElastoDyn","FlapDOF1")]    = {'vals':['True'], 'group':0}
    case_inputs[("ElastoDyn","FlapDOF2")]    = {'vals':['True'], 'group':0}
    case_inputs[("ElastoDyn","EdgeDOF")]     = {'vals':['True'], 'group':0}
    case_inputs[("ElastoDyn","DrTrDOF")]     = {'vals':['False'], 'group':0}
    case_inputs[("ElastoDyn","GenDOF")]      = {'vals':['True'], 'group':0} 
    case_inputs[("ElastoDyn","TwFADOF1")]    = {'vals':['False'], 'group':0}
    case_inputs[("ElastoDyn","TwFADOF2")]    = {'vals':['False'], 'group':0}
    case_inputs[("ElastoDyn","TwSSDOF1")]    = {'vals':['False'], 'group':0}
    case_inputs[("ElastoDyn","TwSSDOF2")]    = {'vals':['False'], 'group':0}

    case_inputs[("ServoDyn","PCMode")]       = {'vals':[5], 'group':0}
    case_inputs[("ServoDyn","VSContrl")]     = {'vals':[5], 'group':0}
    case_inputs[("ServoDyn","YCMode")]       = {'vals':[5], 'group':0}

    case_inputs[("AeroDyn15","WakeMod")]     = {'vals':[1], 'group':0}
    case_inputs[("AeroDyn15","AFAeroMod")]   = {'vals':[2], 'group':0}
    case_inputs[("AeroDyn15","TwrPotent")]   = {'vals':[0], 'group':0}
    case_inputs[("AeroDyn15","TwrShadow")]   = {'vals':['False'], 'group':0}
    case_inputs[("AeroDyn15","TwrAero")]     = {'vals':['False'], 'group':0}

    case_inputs[("AeroDyn15","SkewMod")]     = {'vals':[1], 'group':0}
    case_inputs[("AeroDyn15","TipLoss")]     = {'vals':['True'], 'group':0}
    case_inputs[("AeroDyn15","HubLoss")]     = {'vals':['True'], 'group':0}
    case_inputs[("AeroDyn15","TanInd")]      = {'vals':['True'], 'group':0}
    case_inputs[("AeroDyn15","AIDrag")]      = {'vals':['True'], 'group':0}
    case_inputs[("AeroDyn15","TIDrag")]      = {'vals':['True'], 'group':0}
    case_inputs[("AeroDyn15","IndToler")]    = {'vals':[1.e-5], 'group':0}
    case_inputs[("AeroDyn15","MaxIter")]     = {'vals':[5000], 'group':0}
    case_inputs[("AeroDyn15","UseBlCm")]     = {'vals':['True'], 'group':0}
    
    case_list, case_name_list = iec.execute(case_inputs=case_inputs)

    channels  = ["TipDxc1", "TipDyc1", "TipDzc1", "TipDxc2", "TipDyc2", "TipDzc2", "TipDxc3", "TipDyc3", "TipDzc3"]
    channels += ["RootMxc1", "RootMyc1", "RootMzc1", "RootMxc2", "RootMyc2", "RootMzc2", "RootMxc3", "RootMyc3", "RootMzc3"]
    channels += ["RootFxc1", "RootFyc1", "RootFzc1", "RootFxc2", "RootFyc2", "RootFzc2", "RootFxc3", "RootFyc3", "RootFzc3"]
    channels += ["RtAeroCp", "RotTorq", "RotThrust", "RotSpeed", "NacYaw"]

    channels += ["B1N1Fx", "B1N2Fx", "B1N3Fx", "B1N4Fx", "B1N5Fx", "B1N6Fx", "B1N7Fx", "B1N8Fx", "B1N9Fx"]
    channels += ["B1N1Fy", "B1N2Fy", "B1N3Fy", "B1N4Fy", "B1N5Fy", "B1N6Fy", "B1N7Fy", "B1N8Fy", "B1N9Fy"]

    return case_list, case_name_list, channels


if __name__ == "__main__":

    # power_curve()

    case_list, case_name_list = RotorSE_rated('test', 60., 11., 12.1, 0.)


