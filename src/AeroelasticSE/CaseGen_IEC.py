import numpy as np
import os, sys, copy

from CaseGen_General import CaseGen_General, save_case_matric
from pyIECWind import pyIECWind_extreme, pyIECWind_turb

class CaseGen_IEC():

    def __init__(self):
        pass

    def execute(self):

        case_list_all = {}
        dlc_all = []

        for i, dlc in enumerate(self.dlc_inputs['DLC']):
            case_inputs = {}

            # DLC specific variable changes
            if dlc == 1.1 or dlc == 1.2:
                IEC_WindType = 'NTM'
                alpha = 0.2
                iecwind = pyIECWind_turb()
                TMax = 630.

            elif dlc == 1.3:
                IEC_WindType = 'ETM'
                alpha = 0.11
                iecwind = pyIECWind_turb()
                TMax = 630.

            elif dlc == 1.4:
                IEC_WindType = 'ECD'
                alpha = 0.2
                iecwind = pyIECWind_extreme()
                TMax = 90.

            elif dlc == 1.5:
                IEC_WindType = 'EWS'
                alpha = 0.2
                iecwind = pyIECWind_extreme()
                TMax = 90.

            # Windfile generation setup
            iecwind.Turbine_Class = self.Turbine_Class
            iecwind.Turbulence_Class = self.Turbulence_Class
            iecwind.IEC_WindType = IEC_WindType
            iecwind.dir_change = self.transient_dir_change
            iecwind.shear_orient = self.transient_shear_orientation
            iecwind.z_hub = self.z_hub
            iecwind.D = self.D
            iecwind.PLExp = alpha

            iecwind.outdir = self.wind_dir
            iecwind.case_name = self.case_name_base
            iecwind.Turbsim_exe = self.Turbsim_exe
            iecwind.debug_level = self.debug_level

            ## Windfile generation execution
            def gen_windfile(iecwind, IEC_WindType, U, U_out, WindFile_out, WindFile_type_out):

                wind_file, wind_file_type = iecwind.execute(IEC_WindType, U)
                if type(wind_file) is str:
                    U_out.append(U)
                    WindFile_out.append(wind_file)
                    WindFile_type_out.append(wind_file_type)
                elif type(wind_file) is list:
                    U_out.extend([U]*len(wind_file))
                    WindFile_out.extend(wind_file)
                    WindFile_type_out.extend(wind_file_type)
                return U_out, WindFile_out, WindFile_type_out

            U_out = []
            WindFile_out = []
            WindFile_type_out = []
            for i_U, U in enumerate(iec.dlc_inputs['U'][i]):
                if iec.dlc_inputs['Seeds'][i]:
                    for i_seed, seed in enumerate(iec.dlc_inputs['Seeds'][i]):
                        iecwind.seed = seed
                        iecwind.case_name = self.case_name_base + '_U%2.1f'%U + '_Seed%2.1f'%seed
                        U_out, WindFile_out, WindFile_type_out = gen_windfile(iecwind, IEC_WindType, U, U_out, WindFile_out, WindFile_type_out)
                else:
                    U_out, WindFile_out, WindFile_type_out = gen_windfile(iecwind, IEC_WindType, U, U_out, WindFile_out, WindFile_type_out)

            # Set FAST variables from DLC setup
            case_inputs[("Fst","TMax")] = {'vals':[TMax], 'group':0}
            case_inputs[("InflowWind","WindType")] = {'vals':WindFile_type_out, 'group':1}
            case_inputs[("InflowWind","Filename")] = {'vals':WindFile_out, 'group':1}

            # Set FAST variables from inital conditions
            if self.init_cond:
                for var in self.init_cond.keys():
                    inital_cond_i = [np.interp(U, self.init_cond[var]['U'], self.init_cond[var]['val']) for U in U_out]
                    case_inputs[var] = {'vals':inital_cond_i, 'group':1}
            
            # Append current DLC to full list of cases
            case_list, case_name = CaseGen_General(case_inputs, self.run_dir, self.case_name_base)
            case_list_all = self.join_case_dicts(case_list_all, case_list)
            dlc_all.extend([dlc]*len(case_list))

        # Save case matrix file
        self.save_joined_case_matrix(case_list_all, dlc_all)


    def join_case_dicts(self, caselist, caselist_add):
        if caselist:
            keys1 = caselist[0].keys()
            keys2 = caselist_add[0].keys()
            n1 = len(caselist)
            n2 = len(caselist_add)

            common = list(set(keys1) & set(keys2))
            missing1 = list(set(keys1).difference(keys2))
            missing2 = list(set(keys2).difference(keys1))

            # caselist_out = copy.copy(case_list)
            for i in range(n1):
                for var in missing2:
                    caselist[i][var] = np.nan
            for i in range(n2):
                for var in missing1:
                    caselist_add[i][var] = np.nan

            return caselist + caselist_add
        else:
            return caselist_add

    def save_joined_case_matrix(self, caselist, dlc_list):

        change_vars = sorted(caselist[0].keys())

        matrix_out = []
        for case in caselist:
            row_out = [None]*len(change_vars)
            for i, var in enumerate(change_vars):
                row_out[i] = str(case[var])
            matrix_out.append(row_out)
        matrix_out = np.asarray(matrix_out)

        change_vars = [('IEC', 'DLC')] + change_vars
        matrix_out = np.hstack((np.asarray([[i] for i in dlc_list]), matrix_out))

        save_case_matric(matrix_out, change_vars, self.run_dir)



if __name__=="__main__":
    
    iec = CaseGen_IEC()

    # Turbine Data
    iec.init_cond = {} # can leave as {} if data not available
    iec.init_cond[("ElastoDyn","RotSpeed")] = {'U':[3., 4., 5., 6., 7., 8., 9., 10., 11., 12., 13., 14., 15., 16., 17., 18., 19., 20., 21., 22., 23., 24., 25], 'val':[6.972, 7.183, 7.506, 7.942, 8.469, 9.156, 10.296, 11.431, 11.89, 12.1, 12.1, 12.1, 12.1, 12.1, 12.1, 12.1, 12.1, 12.1, 12.1, 12.1, 12.1, 12.1, 12.1]}
    iec.init_cond[("ElastoDyn","BlPitch1")] = {'U':[3., 4., 5., 6., 7., 8., 9., 10., 11., 12., 13., 14., 15., 16., 17., 18., 19., 20., 21., 22., 23., 24., 25], 'val':[0., 0., 0., 0., 0., 0., 0., 0., 0., 3.823, 6.602, 8.668, 10.450, 12.055, 13.536, 14.920, 16.226, 17.473, 18.699, 19.941, 21.177, 22.347, 23.469]}
    iec.init_cond[("ElastoDyn","BlPitch2")] = iec.init_cond[("ElastoDyn","BlPitch1")]
    iec.init_cond[("ElastoDyn","BlPitch3")] = iec.init_cond[("ElastoDyn","BlPitch1")]

    iec.Turbine_Class = 'I' # I, II, III, IV
    iec.Turbulence_Class = 'A'
    iec.D = 126.
    iec.z_hub = 90.

    # DLC inputs
    iec.dlc_inputs = {}
    iec.dlc_inputs['DLC']   = [1.1, 1.2]
    iec.dlc_inputs['U']     = [[8, 9, 10], [8, 9, 10]]
    iec.dlc_inputs['Seeds'] = [[5, 6, 7], [5, 6, 7]]
    iec.dlc_inputs['Yaw']   = [[], []]

    iec.transient_dir_change        = 'both'  # '+','-','both': sign for transient events in EDC, EWS
    iec.transient_shear_orientation = 'both'  # 'v','h','both': vertical or horizontal shear for EWS

    # Naming, file management, etc
    iec.wind_dir = 'temp/wind'
    iec.case_name_base = 'testing'
    iec.Turbsim_exe = 'C:/Users/egaertne/WT_Codes/Turbsim_v2.00.07/bin/TurbSim_x64.exe'
    iec.debug_level = 1
    iec.run_dir = 'temp'

    # Run
    iec.execute()

    
