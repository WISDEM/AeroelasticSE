import os,re
import sys
from openmdao.api import Component
from FST_vartrees_params3 import FstModel

def fix_path(name):
    """ split a path, then reconstruct it using os.path.join """
    name = re.split("\\\|/", name)
    new = name[0]
    for i in range(1,len(name)):
        new = os.path.join(new, name[i])
    return new

class Fst8InputBase(object):

    model_name = 'FAST Model'

class Fst8InputReader(Component):

    def __init__(self):
        super(Fst8InputReader, self).__init__()
        #self.fst_infile = ''   #Master FAST file
        #self.fst_directory = ''   #Directory of master FAST file set
        #self.ad_file_type = 0   #Enum(0, (0,1), desc='Aerodyn file type, 0=old Aerodyn, 1 = new Aerdyn')
        
        # This currently doesn't mean anything for FAST8
        # self.fst_file_type = 0   #Enum(0, (0,1), desc='Fst file type, 0=old FAST, 1 = new FAST')    

        FstModel(self, 'fst_vt')
    
    def solve_nonlinear(self, params, unknowns, resids):
    	  
        fst_file = os.path.join(params['fst_vt:fst_directory'], params['fst_vt:FSTInputFile'])
        f = open(fst_file)

        # Header of .fst file
        f.readline()
        params['fst_vt:description'] = f.readline().rstrip()

        # Simulation Control (fst_sim_ctrl)
        f.readline()
        boolflag = f.readline().split()[0]
        if boolflag == 'False':
            params['fst_vt:fst_sim_ctrl:Echo'] = False
        else:
            params['fst_vt:fst_sim_ctrl:Echo'] = True
        params['fst_vt:fst_sim_ctrl:AbortLevel'] = f.readline().split()[0][1:-1]
        params['fst_vt:fst_sim_ctrl:TMax'] = float(f.readline().split()[0])
        params['fst_vt:fst_sim_ctrl:DT']  = float(f.readline().split()[0])
        params['fst_vt:fst_sim_ctrl:InterpOrder']  = int(f.readline().split()[0])
        params['fst_vt:fst_sim_ctrl:NumCrctn']  = int(f.readline().split()[0])
        params['fst_vt:fst_sim_ctrl:DT_UJac']  = float(f.readline().split()[0])
        params['fst_vt:fst_sim_ctrl:UJacSclFact']  = float(f.readline().split()[0])

        # Feature Switches and Flags (ftr_swtchs_flgs)
        f.readline()
        params['fst_vt:ftr_swtchs_flgs:CompElast'] = int(f.readline().split()[0])
        params['fst_vt:ftr_swtchs_flgs:CompInflow'] = int(f.readline().split()[0])
        params['fst_vt:ftr_swtchs_flgs:CompAero'] = int(f.readline().split()[0])
        params['fst_vt:ftr_swtchs_flgs:CompServo'] = int(f.readline().split()[0])
        params['fst_vt:ftr_swtchs_flgs:CompHydro'] = int(f.readline().split()[0])
        params['fst_vt:ftr_swtchs_flgs:CompSub'] = int(f.readline().split()[0])
        params['fst_vt:ftr_swtchs_flgs:CompMooring'] = int(f.readline().split()[0])
        params['fst_vt:ftr_swtchs_flgs:CompIce'] = int(f.readline().split()[0])

        # Input Files (input_files)
        f.readline()
        params['fst_vt:input_files:EDFile'] = f.readline().split()[0][1:-1]
        params['fst_vt:input_files:BDBldFile1'] = f.readline().split()[0][1:-1]
        params['fst_vt:input_files:BDBldFile2'] = f.readline().split()[0][1:-1]
        params['fst_vt:input_files:BDBldFile3'] = f.readline().split()[0][1:-1]
        params['fst_vt:input_files:InflowFile'] = f.readline().split()[0][1:-1]
        params['fst_vt:input_files:AeroFile'] = f.readline().split()[0][1:-1]
        params['fst_vt:input_files:ServoFile'] = f.readline().split()[0][1:-1]
        params['fst_vt:input_files:HydroFile'] = f.readline().split()[0][1:-1]
        params['fst_vt:input_files:SubFile'] = f.readline().split()[0][1:-1]
        params['fst_vt:input_files:MooringFile'] = f.readline().split()[0][1:-1]
        params['fst_vt:input_files:IceFile'] = f.readline().split()[0][1:-1]

        # FAST Output Parameters (fst_output_params)
        f.readline()
        boolflag = f.readline().split()[0]
        if boolflag == 'False':
            params['fst_vt:fst_out_params:SumPrint'] = False
        else:
            params['fst_vt:fst_out_params:SumPrint'] = True
        params['fst_vt:fst_out_params:SttsTime'] = float(f.readline().split()[0])
        params['fst_vt:fst_out_params:ChkptTime'] = float(f.readline().split()[0])
        params['fst_vt:fst_out_params:DT_Out'] = float(f.readline().split()[0])
        params['fst_vt:fst_out_params:TStart'] = float(f.readline().split()[0])
        params['fst_vt:fst_out_params:OutFileFmt'] = int(f.readline().split()[0])
        boolflag = f.readline().split()[0]
        if boolflag == 'False':
            params['fst_vt:fst_out_params:TabDelim'] = False
        else:
            params['fst_vt:fst_out_params:TabDelim'] = True
        params['fst_vt:fst_out_params:OutFmt'] = f.readline().split()[0][1:-1]

        # Linearization
        f.readline()
        params['fst_vt:linearization:Linearize'] = f.readline().split()[0]
        params['fst_vt:linearization:NLinTimes'] = f.readline().split()[0]
        params['fst_vt:linearization:LinTimes'] = re.findall(r'[^,\s]+', f.readline())[0:2]
        params['fst_vt:linearization:LinInputs'] = f.readline().split()[0]
        params['fst_vt:linearization:LinOutputs'] = f.readline().split()[0]
        params['fst_vt:linearization:LinOutJac'] = f.readline().split()[0]
        params['fst_vt:linearization:LinOutMod'] = f.readline().split()[0]

        # Visualization ()
        f.readline()
        params['fst_vt:visualization:WrVTK'] = int(f.readline().split()[0])
        params['fst_vt:visualization:VTK_type'] = int(f.readline().split()[0])
        boolflag = f.readline().split()[0]
        if boolflag == 'False':
            params['fst_vt:visualization:VTK_fields'] = False
        else:
            params['fst_vt:visualization:VTK_fields'] = True
        params['fst_vt:visualization:VTK_fps'] = float(f.readline().split()[0])

        params = self.ElastoDynReader(params)
        params = self.BladeStrucReader(params)
        params = self.TowerReader(params)
        params = self.InflowWindReader(params)
        # Wnd wind file if necessary
        if params['fst_vt:inflow_wind:WindType'] == 1:
            #simple wind, no file necessary
            pass
        elif params['fst_vt:inflow_wind:WindType'] == 2:
            exten = params['fst_vt:uniform_wind_params:Filename'].split('.')[1]
            if exten == "wnd":
                self.WndWindReader(params['fst_vt:uniform_wind_params:Filename'])
            else:
                sys.exit("Wind reader for file extension {} not yet implemented".format(exten))
        elif params['fst_vt:inflow_wind:WindType'] == 3:
            exten = params['fst_vt:turbsim_wind_params:Filename'].split('.')[1]
            if exten == "wnd":
                self.WndWindReader(params['fst_vt:turbsim_wind_params:Filename'])
            else:
                sys.exit("Wind reader for file extension {} not yet implemented".format(exten))
        elif params['fst_vt:inflow_wind:WindType'] == 4:
            print "Assuming binary bladed-style FilenameRoot is of type .wnd"
            self.WndWindReader("{0}.wnd".format(params['fst_vt:bladed_wind_params:FilenameRoot']))
        else:
            sys.exit("Reader functionality for wind type {} not yet implemented".format(params['fst_vt:inflow_wind:WindType']))
        params = self.AeroDynReader(params)
        params = self.ServoDynReader(params)

    def ElastoDynReader(self, params):

        ed_file = os.path.join(params['fst_vt:fst_directory'], params['fst_vt:input_files:EDFile'])
        f = open(ed_file)

        f.readline()
        f.readline()

        # Simulation Control (ed_sim_ctrl)
        f.readline()
        boolflag = f.readline().split()[0]
        if boolflag == 'False':
            params['fst_vt:ed_sim_ctrl:Echo'] = False
        else:
            params['fst_vt:ed_sim_ctrl:Echo'] = True
        params['fst_vt:ed_sim_ctrl:Method']  = int(f.readline().split()[0])
        params['fst_vt:ed_sim_ctrl:DT'] = float(f.readline().split()[0])

        # Environmental Condition (envir_cond)
        f.readline()
        params['fst_vt:envir_cond:Gravity'] = float(f.readline().split()[0])

        # Degrees of Freedom (dof)
        f.readline()
        boolflag = f.readline().split()[0]
        if boolflag == 'False':
            params['fst_vt:dof:FlapDOF1'] = False
        else:
            params['fst_vt:dof:FlapDOF1'] = True
        boolflag = f.readline().split()[0]
        if boolflag == 'False':
            params['fst_vt:dof:FlapDOF2'] = False
        else:
            params['fst_vt:dof:FlapDOF2'] = True
        boolflag = f.readline().split()[0]
        if boolflag == 'False':
            params['fst_vt:dof:EdgeDOF'] = False
        else:
            params['fst_vt:dof:EdgeDOF'] = True
        boolflag = f.readline().split()[0]
        if boolflag == 'False':
            params['fst_vt:dof:TeetDOF'] = False
        else:
            params['fst_vt:dof:TeetDOF'] = True
        boolflag = f.readline().split()[0]
        if boolflag == 'False':
            params['fst_vt:dof:DrTrDOF'] = False
        else:
            params['fst_vt:dof:DrTrDOF'] = True
        boolflag = f.readline().split()[0]
        if boolflag == 'False':
            params['fst_vt:dof:GenDOF'] = False
        else:
            params['fst_vt:dof:GenDOF'] = True
        boolflag = f.readline().split()[0]
        if boolflag == 'False':
            params['fst_vt:dof:YawDOF'] = False
        else:
            params['fst_vt:dof:YawDOF'] = True
        boolflag = f.readline().split()[0]
        if boolflag == 'False':
            params['fst_vt:dof:TwFADOF1'] = False
        else:
            params['fst_vt:dof:TwFADOF1'] = True
        boolflag = f.readline().split()[0]
        if boolflag == 'False':
            params['fst_vt:dof:TwFADOF2'] = False
        else:
            params['fst_vt:dof:TwFADOF2'] = True
        boolflag = f.readline().split()[0]
        if boolflag == 'False':
            params['fst_vt:dof:TwSSDOF1'] = False
        else:
            params['fst_vt:dof:TwSSDOF1'] = True
        boolflag = f.readline().split()[0]
        if boolflag == 'False':
            params['fst_vt:dof:TwSSDOF2'] = False
        else:
            params['fst_vt:dof:TwSSDOF2'] = True
        boolflag = f.readline().split()[0]
        if boolflag == 'False':
            params['fst_vt:dof:PtfmSgDOF'] = False
        else:
            params['fst_vt:dof:PtfmSgDOF'] = True
        boolflag = f.readline().split()[0]
        if boolflag == 'False':
            params['fst_vt:dof:PtfmSwDOF'] = False
        else:
            params['fst_vt:dof:PtfmSwDOF'] = True
        boolflag = f.readline().split()[0]
        if boolflag == 'False':
            params['fst_vt:dof:PtfmHvDOF'] = False
        else:
            params['fst_vt:dof:PtfmHvDOF'] = True
        boolflag = f.readline().split()[0]
        if boolflag == 'False':
            params['fst_vt:dof:PtfmRDOF'] = False
        else:
            params['fst_vt:dof:PtfmRDOF'] = True
        boolflag = f.readline().split()[0]
        if boolflag == 'False':
            params['fst_vt:dof:PtfmPDOF'] = False
        else:
            params['fst_vt:dof:PtfmPDOF'] = True
        boolflag = f.readline().split()[0]
        if boolflag == 'False':
            params['fst_vt:dof:PtfmYDOF'] = False
        else:
            params['fst_vt:dof:PtfmYDOF'] = True

        # Initial Conditions (init_conds)
        f.readline()
        params['fst_vt:init_conds:OoPDefl']    = float(f.readline().split()[0])
        params['fst_vt:init_conds:IPDefl']     = float(f.readline().split()[0])
        params['fst_vt:init_conds:BlPitch1']   = float(f.readline().split()[0])
        params['fst_vt:init_conds:BlPitch2']   = float(f.readline().split()[0])
        params['fst_vt:init_conds:BlPitch3']   = float(f.readline().split()[0])
        params['fst_vt:init_conds:TeetDefl']   = float(f.readline().split()[0])
        params['fst_vt:init_conds:Azimuth']    = float(f.readline().split()[0])
        params['fst_vt:init_conds:RotSpeed']   = float(f.readline().split()[0])
        params['fst_vt:init_conds:NacYaw']     = float(f.readline().split()[0])
        params['fst_vt:init_conds:TTDspFA']    = float(f.readline().split()[0])
        params['fst_vt:init_conds:TTDspSS']    = float(f.readline().split()[0])
        params['fst_vt:init_conds:PtfmSurge']  = float(f.readline().split()[0])
        params['fst_vt:init_conds:PtfmSway']   = float(f.readline().split()[0])
        params['fst_vt:init_conds:PtfmHeave']  = float(f.readline().split()[0])
        params['fst_vt:init_conds:PtfmRoll']   = float(f.readline().split()[0])
        params['fst_vt:init_conds:PtfmPitch']  = float(f.readline().split()[0])
        params['fst_vt:init_conds:PtfmYaw']    = float(f.readline().split()[0])


        # Turbine Configuration (turb_config)
        f.readline()
        params['fst_vt:turb_config:NumBl']      = int(f.readline().split()[0])
        params['fst_vt:turb_config:TipRad']     = float(f.readline().split()[0])
        params['fst_vt:turb_config:HubRad']     = float(f.readline().split()[0])
        params['fst_vt:turb_config:PreCone1']   = float(f.readline().split()[0])
        params['fst_vt:turb_config:PreCone2']   = float(f.readline().split()[0])
        params['fst_vt:turb_config:PreCone3']   = float(f.readline().split()[0])
        params['fst_vt:turb_config:HubCM']      = float(f.readline().split()[0])
        params['fst_vt:turb_config:UndSling']   = float(f.readline().split()[0])
        params['fst_vt:turb_config:Delta3']     = float(f.readline().split()[0])
        params['fst_vt:turb_config:AzimB1Up']   = float(f.readline().split()[0])
        params['fst_vt:turb_config:OverHang']   = float(f.readline().split()[0])
        params['fst_vt:turb_config:ShftGagL']   = float(f.readline().split()[0])
        params['fst_vt:turb_config:ShftTilt']   = float(f.readline().split()[0])
        params['fst_vt:turb_config:NacCMxn']    = float(f.readline().split()[0])
        params['fst_vt:turb_config:NacCMyn']    = float(f.readline().split()[0])
        params['fst_vt:turb_config:NacCMzn']    = float(f.readline().split()[0])
        params['fst_vt:turb_config:NcIMUxn']    = float(f.readline().split()[0])
        params['fst_vt:turb_config:NcIMUyn']    = float(f.readline().split()[0])
        params['fst_vt:turb_config:NcIMUzn']    = float(f.readline().split()[0])
        params['fst_vt:turb_config:Twr2Shft']   = float(f.readline().split()[0])
        params['fst_vt:turb_config:TowerHt']    = float(f.readline().split()[0])
        params['fst_vt:turb_config:TowerBsHt']  = float(f.readline().split()[0])
        params['fst_vt:turb_config:PtfmCMxt']   = float(f.readline().split()[0])
        params['fst_vt:turb_config:PtfmCMyt']   = float(f.readline().split()[0])
        params['fst_vt:turb_config:PtfmCMzt']   = float(f.readline().split()[0])
        params['fst_vt:turb_config:PtfmRefzt']  = float(f.readline().split()[0])

        # Mass and Inertia (mass_inertia)
        f.readline()
        params['fst_vt:mass_inertia:TipMass1']   = float(f.readline().split()[0])
        params['fst_vt:mass_inertia:TipMass2']   = float(f.readline().split()[0])
        params['fst_vt:mass_inertia:TipMass3']   = float(f.readline().split()[0])
        params['fst_vt:mass_inertia:HubMass']    = float(f.readline().split()[0])
        params['fst_vt:mass_inertia:HubIner']    = float(f.readline().split()[0])
        params['fst_vt:mass_inertia:GenIner']    = float(f.readline().split()[0])
        params['fst_vt:mass_inertia:NacMass']    = float(f.readline().split()[0])
        params['fst_vt:mass_inertia:NacYIner']   = float(f.readline().split()[0])
        params['fst_vt:mass_inertia:YawBrMass']  = float(f.readline().split()[0])
        params['fst_vt:mass_inertia:PtfmMass']   = float(f.readline().split()[0])
        params['fst_vt:mass_inertia:PtfmRIner']  = float(f.readline().split()[0])
        params['fst_vt:mass_inertia:PtfmPIner']  = float(f.readline().split()[0])
        params['fst_vt:mass_inertia:PtfmYIner']  = float(f.readline().split()[0])

        # ElastoDyn Blade (blade_struc)
        f.readline()
        params['fst_vt:blade_struc:BldNodes'] = int(f.readline().split()[0])
        params['fst_vt:blade_struc:BldFile1'] = f.readline().split()[0][1:-1]
        params['fst_vt:blade_struc:BldFile2'] = f.readline().split()[0][1:-1]
        params['fst_vt:blade_struc:BldFile3'] = f.readline().split()[0][1:-1]

        # Rotor-Teeter (rotor_teeter)
        f.readline()
        params['fst_vt:rotor_teeter:TeetMod']  = int(f.readline().split()[0])
        params['fst_vt:rotor_teeter:TeetDmpP'] = float(f.readline().split()[0])
        params['fst_vt:rotor_teeter:TeetDmp']  = float(f.readline().split()[0])
        params['fst_vt:rotor_teeter:TeetCDmp'] = float(f.readline().split()[0])
        params['fst_vt:rotor_teeter:TeetSStP'] = float(f.readline().split()[0])
        params['fst_vt:rotor_teeter:TeetHStP'] = float(f.readline().split()[0])
        params['fst_vt:rotor_teeter:TeetSSSp'] = float(f.readline().split()[0])
        params['fst_vt:rotor_teeter:TeetHSSp'] = float(f.readline().split()[0])

        # Drivetrain (drivetrain)
        f.readline()
        params['fst_vt:drivetrain:GBoxEff']  = float(f.readline().split()[0])
        params['fst_vt:drivetrain:GBRatio']  = float(f.readline().split()[0])
        params['fst_vt:drivetrain:DTTorSpr'] = float(f.readline().split()[0])
        params['fst_vt:drivetrain:DTTorDmp'] = float(f.readline().split()[0])

        # Furling (furling)
        f.readline()
        boolflag = f.readline().split()[0]
        if boolflag == 'False':
            params['fst_vt:furling:Furling'] = False
        else:
            params['fst_vt:furling:Furling'] = True
        params['fst_vt:furling:FurlFile'] = f.readline().split()[0][1:-1]

        # Tower (tower)
        f.readline()
        params['fst_vt:tower:TwrNodes'] = int(f.readline().split()[0])
        params['fst_vt:tower:TwrFile'] = f.readline().split()[0][1:-1]

        # ED Output Parameters (ed_out_params)
        f.readline()
        boolflag = f.readline().split()[0]
        if boolflag == 'False':
            params['fst_vt:ed_out_params:SumPrint'] = False
        else:
            params['fst_vt:ed_out_params:SumPrint'] = True
        params['fst_vt:ed_out_params:OutFile']  = int(f.readline().split()[0])
        boolflag = f.readline().split()[0]
        if boolflag == 'False':
            params['fst_vt:ed_out_params:TabDelim'] = False
        else:
            params['fst_vt:ed_out_params:TabDelim'] = True
        params['fst_vt:ed_out_params:OutFmt']   = f.readline().split()[0][1:-1]
        params['fst_vt:ed_out_params:TStart']   = float(f.readline().split()[0])
        params['fst_vt:ed_out_params:DecFact']  = int(f.readline().split()[0])
        params['fst_vt:ed_out_params:NTwGages'] = int(f.readline().split()[0])
        twrg = f.readline().split(',')
        if params['fst_vt:ed_out_params:NTwGages'] != 0: #loop over elements if there are gauges to be added, otherwise assign directly
            for i in range(params['fst_vt:ed_out_params:NTwGages']):
                params['fst_vt:ed_out_params:TwrGagNd'].append(twrg[i])
            params['fst_vt:ed_out_params:TwrGagNd'][-1] = params['fst_vt:ed_out_params:TwrGagNd'][-1][:-1]   #remove last (newline) character
        else:
            params['fst_vt:ed_out_params:TwrGagNd'] = twrg
            params['fst_vt:ed_out_params:TwrGagNd'][-1] = params['fst_vt:ed_out_params:TwrGagNd'][-1][:-1]
        params['fst_vt:ed_out_params:NBlGages'] = int(f.readline().split()[0])
        blg = f.readline().split(',')
        if params['fst_vt:ed_out_params:NBlGages'] != 0:
            for i in range(params['fst_vt:ed_out_params:NBlGages']):
                params['fst_vt:ed_out_params:BldGagNd'].append(blg[i])
            params['fst_vt:ed_out_params:BldGagNd'][-1] = params['fst_vt:ed_out_params:BldGagNd'][-1][:-1]
        else:
            params['fst_vt:ed_out_params:BldGagNd'] = blg
            params['fst_vt:ed_out_params:BldGagNd'][-1] = params['fst_vt:ed_out_params:BldGagNd'][-1][:-1]

        # Outlist (TODO - detailed categorization)
        f.readline()
        data = f.readline()
        while data.split()[0] != 'END':
            channels = data.split('"')
            channel_list = channels[1].split(',')
            for variable in channel_list:
                for param in params.keys():
                    if ':outlist:' in param:
                       params[param] = True
            #for i in range(len(channel_list)):
            #    channel_list[i] = channel_list[i].replace(' ','')
            #    if channel_list[i] in params['fst_vt:outlist:wind_mot_vt'].__dict__.keys():
            #        params['fst_vt:outlist:wind_mot_vt'].__dict__[channel_list[i]] = True
            #for i in range(len(channel_list)):
            #    channel_list[i] = channel_list[i].replace(' ','')
            #    if channel_list[i] in params['fst_vt:outlist:blade_mot_vt'].__dict__.keys():
            #        params['fst_vt:outlist:blade_mot_vt'].__dict__[channel_list[i]] = True
            #for i in range(len(channel_list)):
            #    channel_list[i] = channel_list[i].replace(' ','')
            #    if channel_list[i] in params['fst_vt:outlist:hub_nacelle_mot_vt'].__dict__.keys():
            #        params['fst_vt:outlist:hub_nacelle_mot_vt'].__dict__[channel_list[i]] = True
            #for i in range(len(channel_list)):
            #    channel_list[i] = channel_list[i].replace(' ','')
            #    if channel_list[i] in params['fst_vt:outlist:tower_support_mot_vt'].__dict__.keys():
            #        params['fst_vt:outlist:tower_support_mot_vt'].__dict__[channel_list[i]] = True
            #for i in range(len(channel_list)):
            #    channel_list[i] = channel_list[i].replace(' ','')
            #    if channel_list[i] in params['fst_vt:outlist:wave_mot_vt'].__dict__.keys():
            #        params['fst_vt:outlist:wave_mot_vt'].__dict__[channel_list[i]] = True
            #for i in range(len(channel_list)):
            #    channel_list[i] = channel_list[i].replace(' ','')
            #    if channel_list[i] in params['fst_vt:outlist:blade_loads_vt'].__dict__.keys():
            #        params['fst_vt:outlist:blade_loads_vt'].__dict__[channel_list[i]] = True
            #for i in range(len(channel_list)):
            #    channel_list[i] = channel_list[i].replace(' ','')
            #    if channel_list[i] in params['fst_vt:outlist:hub_nacelle_loads_vt'].__dict__.keys():
            #        params['fst_vt:outlist:hub_nacelle_loads_vt'].__dict__[channel_list[i]] = True
            #for i in range(len(channel_list)):
            #    channel_list[i] = channel_list[i].replace(' ','')
            #    if channel_list[i] in params['fst_vt:outlist:tower_support_loads_vt'].__dict__.keys():
            #        params['fst_vt:outlist:tower_support_loads_vt'].__dict__[channel_list[i]] = True
            #for i in range(len(channel_list)):
            #    channel_list[i] = channel_list[i].replace(' ','')
            #    if channel_list[i] in params['fst_vt:outlist:dof_vt'].__dict__.keys():
            #        params['fst_vt:outlist:dof_vt'].__dict__[channel_list[i]] = True
            data = f.readline()

        f.close()
        return params

    def BladeStrucReader(self, params):
        # All in blade_struc vartree

        blade_file = os.path.join(params['fst_vt:fst_directory'], params['fst_vt:blade_struc:BldFile1'])
        f = open(blade_file)
        
        f.readline()
        f.readline()
        f.readline()
        
        # Blade Parameters
        params['fst_vt:blade_struc:NBlInpSt'] = int(f.readline().split()[0])
        params['fst_vt:blade_struc:BldFlDmp1'] = float(f.readline().split()[0])
        params['fst_vt:blade_struc:BldFlDmp2'] = float(f.readline().split()[0])
        params['fst_vt:blade_struc:BldEdDmp1'] = float(f.readline().split()[0])
        
        # Blade Adjustment Factors
        f.readline()
        params['fst_vt:blade_struc:FlStTunr1'] = float(f.readline().split()[0])
        params['fst_vt:blade_struc:FlStTunr2'] = float(f.readline().split()[0])
        params['fst_vt:blade_struc:AdjBlMs'] = float(f.readline().split()[0])
        params['fst_vt:blade_struc:AdjFlSt'] = float(f.readline().split()[0])
        params['fst_vt:blade_struc:AdjEdSt'] = float(f.readline().split()[0])
        
        # Distrilbuted Blade Properties
        f.readline()
        f.readline()
        f.readline()
        params['fst_vt:blade_struc:BlFract'] = [None] * params['fst_vt:blade_struc:NBlInpSt']
        params['fst_vt:blade_struc:PitchAxis'] = [None] * params['fst_vt:blade_struc:NBlInpSt']
        params['fst_vt:blade_struc:StrcTwst'] = [None] * params['fst_vt:blade_struc:NBlInpSt']
        params['fst_vt:blade_struc:BMassDen'] = [None] * params['fst_vt:blade_struc:NBlInpSt']
        params['fst_vt:blade_struc:FlpStff'] = [None] * params['fst_vt:blade_struc:NBlInpSt']
        params['fst_vt:blade_struc:EdgStff'] = [None] * params['fst_vt:blade_struc:NBlInpSt']
        # self.fst_vt.blade_struc.GJStff = [None] * self.fst_vt.blade_struc.NBlInpSt
        # self.fst_vt.blade_struc.EAStff = [None] * self.fst_vt.blade_struc.NBlInpSt
        # self.fst_vt.blade_struc.Alpha = [None] * self.fst_vt.blade_struc.NBlInpSt
        # self.fst_vt.blade_struc.FlpIner = [None] * self.fst_vt.blade_struc.NBlInpSt
        # self.fst_vt.blade_struc.EdgIner = [None] * self.fst_vt.blade_struc.NBlInpSt
        # self.fst_vt.blade_struc.PrecrvRef = [None] * self.fst_vt.blade_struc.NBlInpSt
        # self.fst_vt.blade_struc.PreswpRef = [None] * self.fst_vt.blade_struc.NBlInpSt
        # self.fst_vt.blade_struc.FlpcgOf = [None] * self.fst_vt.blade_struc.NBlInpSt
        # self.fst_vt.blade_struc.Edgcgof = [None] * self.fst_vt.blade_struc.NBlInpSt
        # self.fst_vt.blade_struc.FlpEAOf = [None] * self.fst_vt.blade_struc.NBlInpSt
        # self.fst_vt.blade_struc.EdgEAOf = [None] * self.fst_vt.blade_struc.NBlInpSt
        for i in range(params['fst_vt:blade_struc:NBlInpSt']):
            data = f.readline().split()          
            params['fst_vt:blade_struc:BlFract'][i] = float(data[0])
            params['fst_vt:blade_struc:PitchAxis'][i] = float(data[1])
            params['fst_vt:blade_struc:StrcTwst'][i] = float(data[2])
            params['fst_vt:blade_struc:BMassDen'][i] = float(data[3])
            params['fst_vt:blade_struc:FlpStff'][i] = float(data[4])
            params['fst_vt:blade_struc:EdgStff'][i] = float(data[5])
            # self.fst_vt.blade_struc.GJStff[i] = float(data[6])
            # self.fst_vt.blade_struc.EAStff[i] = float(data[7])
            # self.fst_vt.blade_struc.Alpha[i] = float(data[8])
            # self.fst_vt.blade_struc.FlpIner[i] = float(data[9])
            # self.fst_vt.blade_struc.EdgIner[i] = float(data[10])
            # self.fst_vt.blade_struc.PrecrvRef[i] = float(data[11])
            # self.fst_vt.blade_struc.PreswpRef[i] = float(data[12])
            # self.fst_vt.blade_struc.FlpcgOf[i] = float(data[13])
            # self.fst_vt.blade_struc.Edgcgof[i] = float(data[14])
            # self.fst_vt.blade_struc.FlpEAOf[i] = float(data[15])
            # self.fst_vt.blade_struc.EdgEAOf[i] = float(data[16])

        f.readline()
        params['fst_vt:blade_struc:BldFl1Sh'] = [None] * 5
        params['fst_vt:blade_struc:BldFl2Sh'] = [None] * 5        
        params['fst_vt:blade_struc:BldEdgSh'] = [None] * 5
        for i in range(5):
            params['fst_vt:blade_struc:BldFl1Sh'][i] = float(f.readline().split()[0])
        for i in range(5):
            params['fst_vt:blade_struc:BldFl2Sh'][i] = float(f.readline().split()[0])            
        for i in range(5):
            params['fst_vt:blade_struc:BldEdgSh'][i] = float(f.readline().split()[0])        

        f.close()
        return params


    def TowerReader(self, params):

        tower_file = os.path.join(params['fst_vt:fst_directory'], params['fst_vt:tower:TwrFile']) 
        f = open(tower_file)

        f.readline()
        f.readline()

        # General Tower Paramters
        f.readline()
        params['fst_vt:tower:NTwInptSt'] = int(f.readline().split()[0])
        params['fst_vt:tower:TwrFADmp1'] = float(f.readline().split()[0])
        params['fst_vt:tower:TwrFADmp2'] = float(f.readline().split()[0])
        params['fst_vt:tower:TwrSSDmp1'] = float(f.readline().split()[0])
        params['fst_vt:tower:TwrSSDmp2'] = float(f.readline().split()[0])
    
        # Tower Adjustment Factors
        f.readline()
        params['fst_vt:tower:FAStTunr1'] = float(f.readline().split()[0])
        params['fst_vt:tower:FAStTunr2'] = float(f.readline().split()[0])
        params['fst_vt:tower:SSStTunr1'] = float(f.readline().split()[0])
        params['fst_vt:tower:SSStTunr2'] = float(f.readline().split()[0])
        params['fst_vt:tower:AdjTwMa'] = float(f.readline().split()[0])
        params['fst_vt:tower:AdjFASt'] = float(f.readline().split()[0])
        params['fst_vt:tower:AdjSSSt'] = float(f.readline().split()[0])
     
        # Distributed Tower Properties   
        f.readline()
        f.readline()
        f.readline()
        params['fst_vt:tower:HtFract'] = [None] * params['fst_vt:tower:NTwInptSt']
        params['fst_vt:tower:TMassDen'] = [None] * params['fst_vt:tower:NTwInptSt']
        params['fst_vt:tower:TwFAStif'] = [None] * params['fst_vt:tower:NTwInptSt']
        params['fst_vt:tower:TwSSStif'] = [None] * params['fst_vt:tower:NTwInptSt']
        # self.fst_vt.tower.TwGJStif = [None] * self.fst_vt.tower.NTwInptSt
        # self.fst_vt.tower.TwEAStif = [None] * self.fst_vt.tower.NTwInptSt
        # self.fst_vt.tower. TwFAIner = [None] * self.fst_vt.tower.NTwInptSt
        # self.fst_vt.tower.TwSSIner = [None] * self.fst_vt.tower.NTwInptSt
        # self.fst_vt.tower.TwFAcgOf = [None] * self.fst_vt.tower.NTwInptSt
        # self.fst_vt.tower.TwSScgOf = [None] * self.fst_vt.tower.NTwInptSt
        for i in range(params['fst_vt:tower:NTwInptSt']):
            data = f.readline().split()
            params['fst_vt:tower:HtFract'][i] = float(data[0])
            params['fst_vt:tower:TMassDen'][i] = float(data[1])
            params['fst_vt:tower:TwFAStif'][i] = float(data[2])
            params['fst_vt:tower:TwSSStif'][i] = float(data[3])
            # self.fst_vt.tower.TwGJStif[i] = float(data[4])
            # self.fst_vt.tower.TwEAStif[i] = float(data[5])
            # self.fst_vt.tower. TwFAIner[i] = float(data[6])
            # self.fst_vt.tower.TwSSIner[i] = float(data[7])
            # self.fst_vt.tower.TwFAcgOf[i] = float(data[8])
            # self.fst_vt.tower.TwSScgOf[i] = float(data[9])           
        
        # Tower Mode Shapes
        f.readline()
        params['fst_vt:tower:TwFAM1Sh'] = [None] * 5
        params['fst_vt:tower:TwFAM2Sh'] = [None] * 5
        for i in range(5):
            params['fst_vt:tower:TwFAM1Sh'][i] = float(f.readline().split()[0])
        for i in range(5):
            params['fst_vt:tower:TwFAM2Sh'][i] = float(f.readline().split()[0])        
        f.readline()
        params['fst_vt:tower:TwSSM1Sh'] = [None] * 5
        params['fst_vt:tower:TwSSM2Sh'] = [None] * 5          
        for i in range(5):
            params['fst_vt:tower:TwSSM1Sh'][i] = float(f.readline().split()[0])
        for i in range(5):
            params['fst_vt:tower:TwSSM2Sh'][i] = float(f.readline().split()[0]) 

        f.close()
        return params


    def InflowWindReader(self, params):

        inflow_file = os.path.join(params['fst_vt:fst_directory'], params['fst_vt:input_files:InflowFile'])
        f = open(inflow_file)
        
        f.readline()
        f.readline()
        f.readline()

        # Inflow wind header parameters (inflow_wind)
        boolflag = f.readline().split()[0]
        if boolflag == 'False':
            params['fst_vt:inflow_wind:Echo'] = False
        else:
            params['fst_vt:inflow_wind:Echo'] = True
        params['fst_vt:inflow_wind:WindType']       = int(f.readline().split()[0])
        params['fst_vt:inflow_wind:PropogationDir'] = float(f.readline().split()[0])
        params['fst_vt:inflow_wind:NWindVel']       = int(f.readline().split()[0])
        params['fst_vt:inflow_wind:WindVxiList']    = float(f.readline().split()[0])
        params['fst_vt:inflow_wind:WindVyiList']    = float(f.readline().split()[0])
        params['fst_vt:inflow_wind:WindVziList']    = float(f.readline().split()[0])

        # Parameters for Steady Wind Conditions [used only for WindType = 1] (steady_wind_params)
        f.readline()
        params['fst_vt:steady_wind_params:HWindSpeed'] = float(f.readline().split()[0])
        params['fst_vt:steady_wind_params:RefHt'] = float(f.readline().split()[0])
        params['fst_vt:steady_wind_params:PLexp'] = float(f.readline().split()[0])

        # Parameters for Uniform wind file   [used only for WindType = 2] (uniform_wind_params)
        f.readline()
        params['fst_vt:uniform_wind_params:Filename'] = f.readline().split()[0][1:-1]
        params['fst_vt:uniform_wind_params:RefHt'] = float(f.readline().split()[0])
        params['fst_vt:uniform_wind_params:RefLength'] = float(f.readline().split()[0])

        # Parameters for Binary TurbSim Full-Field files   [used only for WindType = 3] (turbsim_wind_params)
        f.readline()
        params['fst_vt:turbsim_wind_params:Filename'] = f.readline().split()[0][1:-1]

        # Parameters for Binary Bladed-style Full-Field files   [used only for WindType = 4] (bladed_wind_params)
        f.readline()
        params['fst_vt:bladed_wind_params:FilenameRoot'] = f.readline().split()[0][1:-1]       
        boolflag = f.readline().split()[0]
        if boolflag == 'False':
            params['fst_vt:bladed_wind_params:TowerFile'] = False
        else:
            params['fst_vt:bladed_wind_params:TowerFile'] = True

        # Parameters for HAWC-format binary files  [Only used with WindType = 5] (hawc_wind_params)
        f.readline()
        params['fst_vt:hawc_wind_params:FileName_u'] = f.readline().split()[0][1:-1]
        params['fst_vt:hawc_wind_params:FileName_v'] = f.readline().split()[0][1:-1]
        params['fst_vt:hawc_wind_params:FileName_w'] = f.readline().split()[0][1:-1]
        params['fst_vt:hawc_wind_params:nx']    = int(f.readline().split()[0])
        params['fst_vt:hawc_wind_params:ny']    = int(f.readline().split()[0])
        params['fst_vt:hawc_wind_params:nz']    = int(f.readline().split()[0])
        params['fst_vt:hawc_wind_params:dx']    = float(f.readline().split()[0])
        params['fst_vt:hawc_wind_params:dy']    = float(f.readline().split()[0])
        params['fst_vt:hawc_wind_params:dz']    = float(f.readline().split()[0])
        params['fst_vt:hawc_wind_params:RefHt'] = float(f.readline().split()[0])

        # Scaling parameters for turbulence (still hawc_wind_params)
        f.readline()
        params['fst_vt:hawc_wind_params:ScaleMethod'] = int(f.readline().split()[0])
        params['fst_vt:hawc_wind_params:SFx']         = float(f.readline().split()[0])
        params['fst_vt:hawc_wind_params:SFy']         = float(f.readline().split()[0])
        params['fst_vt:hawc_wind_params:SFz']         = float(f.readline().split()[0])
        params['fst_vt:hawc_wind_params:SigmaFx']     = float(f.readline().split()[0])
        params['fst_vt:hawc_wind_params:SigmaFy']     = float(f.readline().split()[0])
        params['fst_vt:hawc_wind_params:SigmaFz']     = float(f.readline().split()[0])

        # Mean wind profile parameters (added to HAWC-format files) (still hawc_wind_params)
        f.readline()
        params['fst_vt:hawc_wind_params:URef']        = float(f.readline().split()[0])
        params['fst_vt:hawc_wind_params:WindProfile'] = int(f.readline().split()[0])
        params['fst_vt:hawc_wind_params:PLExp']       = float(f.readline().split()[0])
        params['fst_vt:hawc_wind_params:Z0']          = float(f.readline().split()[0])

        # Inflow Wind Output Parameters (inflow_out_params)
        f.readline()
        boolflag = f.readline().split()[0]
        if boolflag == 'False':
            params['fst_vt:inflow_out_params:SumPrint'] = False
        else:
            params['fst_vt:inflow_out_params:SumPrint'] = True
        
        # NO INFLOW WIND OUTPUT PARAMETERS YET DEFINED IN FAST
        # f.readline()
        # data = f.readline()
        # while data.split()[0] != 'END':
        #     channels = data.split('"')
        #     channel_list = channels[1].split(',')
        #     for i in range(len(channel_list)):
        #         channel_list[i] = channel_list[i].replace(' ','')
        #         if channel_list[i] in self.fst_vt.outlist.inflow_wind_vt.__dict__.keys():
        #             self.fst_vt.outlist.inflow_wind_vt.__dict__[channel_list[i]] = True
        #     data = f.readline()

        f.close()
        return params


    def WndWindReader(self, wndfile, params):

        wind_file = os.path.join(params['fst_vt:fst_directory'], wndfile)
        f = open(wind_file)

        data = []
        while 1:
            line = f.readline()
            if not line:
                break
            line_split = line.split()
            if line_split[0] != '!':
                data.append(line.split())

        params['fst_vt:wnd_wind:TimeSteps'] = len(data)

        params['fst_vt:wnd_wind:Time'] = [None] * len(data)
        params['fst_vt:wnd_wind:HorSpd'] = [None] * len(data)
        params['fst_vt:wnd_wind:WindDir'] = [None] * len(data)
        params['fst_vt:wnd_wind:VerSpd'] = [None] * len(data)
        params['fst_vt:wnd_wind:HorShr'] = [None] * len(data)
        params['fst_vt:wnd_wind:VerShr'] = [None] * len(data)
        params['fst_vt:wnd_wind:LnVShr'] = [None] * len(data)
        params['fst_vt:wnd_wind:GstSpd'] = [None] * len(data)        
        for i in range(len(data)):
            params['fst_vt:wnd_wind:Time'][i] = float(data[i][0])
            params['fst_vt:wnd_wind:HorSpd'][i] = float(data[i][1])
            params['fst_vt:wnd_wind:WindDir'][i] = float(data[i][2])
            params['fst_vt:wnd_wind:VerSpd'][i] = float(data[i][3])
            params['fst_vt:wnd_wind:HorShr'][i] = float(data[i][4])
            params['fst_vt:wnd_wind:VerShr'][i] = float(data[i][5])
            params['fst_vt:wnd_wind:LnVShr'][i] = float(data[i][6])
            params['fst_vt:wnd_wind:GstSpd'][i] = float(data[i][7])

        f.close()
        return params

    def AeroDynReader(self, params):

        #from airfoil import PolarByRe # only if creating airfoil variable trees

        ad_file = os.path.join(self.fst_directory, self.fst_vt.input_files.AeroFile)
        f = open(ad_file)

        # AeroDyn file header (aerodyn)
        f.readline()
        f.readline()
        params['fst_vt:aerodyn:StallMod'] = f.readline().split()[0]
        params['fst_vt:aerodyn:UseCm'] = f.readline().split()[0]
        params['fst_vt:aerodyn:InfModel'] = f.readline().split()[0]
        params['fst_vt:aerodyn:IndModel'] = f.readline().split()[0]
        params['fst_vt:aerodyn:AToler'] = float(f.readline().split()[0])
        params['fst_vt:aerodyn:TLModel'] = f.readline().split()[0]
        params['fst_vt:aerodyn:HLModel'] = f.readline().split()[0]
        params['fst_vt:aerodyn:TwrShad'] = float(f.readline().split()[0])
        params['fst_vt:aerodyn:ShadHWid'] = float(f.readline().split()[0])
        params['fst_vt:aerodyn:T_Shad_Refpt'] = float(f.readline().split()[0])
        params['fst_vt:aerodyn:AirDens'] = float(f.readline().split()[0])
        params['fst_vt:aerodyn:KinVisc'] = float(f.readline().split()[0])
        params['fst_vt:aerodyn:DTAero'] = float(f.readline().split()[0])

        # AeroDyn Blade Properties (blade_aero)
        params['fst_vt:blade_aero:NumFoil'] = int(f.readline().split()[0])
        params['fst_vt:blade_aero:FoilNm'] = [None] * params['fst_vt:blade_aero:NumFoil']
        for i in range(self.fst_vt.blade_aero.NumFoil):
            af_filename = f.readline().split()[0]
            af_filename = fix_path(af_filename)
            # print af_filename
            params['fst_vt:blade_aero:FoilNm'][i] = af_filename[1:-1]
        
        params['fst_vt:blade_aero:BldNodes'] = int(f.readline().split()[0])
        f.readline()
        params['fst_vt:blade_aero:RNodes'] = [None] * params['fst_vt:blade_aero:BldNodes']
        params['fst_vt:blade_aero:AeroTwst'] = [None] * params['fst_vt:blade_aero:BldNodes']
        params['fst_vt:blade_aero:DRNodes'] = [None] * params['fst_vt:blade_aero:BldNodes']
        params['fst_vt:blade_aero:Chord'] = [None] * params['fst_vt:blade_aero:BldNodes']
        params['fst_vt:blade_aero:NFoil'] = [None] * params['fst_vt:blade_aero:BldNodes']
        params['fst_vt:blade_aero:PrnElm'] = [None] * params['fst_vt:blade_aero:BldNodes']       
        for i in range(self.fst_vt.blade_aero.BldNodes):
            data = f.readline().split()
            params['fst_vt:blade_aero:RNodes'][i] = float(data[0])
            params['fst_vt:blade_aero:AeroTwst'][i] = float(data[1])
            params['fst_vt:blade_aero:DRNodes'][i] = float(data[2])
            params['fst_vt:blade_aero:Chord'][i] = float(data[3])
            params['fst_vt:blade_aero:NFoil'][i] = int(data[4])
            params['fst_vt:blade_aero:PrnElm'][i] = data[5]

        f.close()

        # create airfoil objects
        for i in range(params['fst_vt:blade_aero:NumFoil']):
             params['fst_vt:blade_aero:af_data'].append(self.initFromAerodynFile(os.path.join(params['fst_directory'], params['fst_vt:blade_aero:FoilNm'][i]), params['fst_vt:ad_file_type']))
        return params


    def initFromAerodynFile(self, aerodynFile, mode, params): # kld - added for fast noise
        """
        Construct array of polars from old-style Aerodyn file
        Use this method for FAST (which can't read the new format) 2012 11 12

        Arguments:
        aerodynFile - path/name of a properly formatted old-style Aerodyn file
        """
        # open aerodyn file
        f = open(aerodynFile, 'r')
        
        airfoil = ADAirfoil()

        # skip through header
        airfoil.description = f.readline().rstrip()  # remove newline
        f.readline()
        if mode == 0: 
            f.readline()        
        airfoil.number_tables = int(f.readline().split()[0])

        # loop through tables
        for i in range(airfoil.number_tables):
 
            polar = ADAirfoilPolar()

            polar.IDParam = float(f.readline().split()[0])
            if mode == 0:
                f.readline()
            polar.StallAngle = float(f.readline().split()[0])
            if mode == 1:
                f.readline()
                f.readline()
                f.readline()
            polar.ZeroCn = float(f.readline().split()[0])
            polar.CnSlope = float(f.readline().split()[0])
            polar.CnPosStall = float(f.readline().split()[0])
            polar.CnNegStall = float(f.readline().split()[0])
            polar.alphaCdMin = float(f.readline().split()[0])
            polar.CdMin = float(f.readline().split()[0])

            alpha = []
            cl = []
            cd = []
            cm = []
            # read polar information line by line
            while True:
                line = f.readline()
                if 'EOT' in line:
                    break
                data = [float(s) for s in line.split()]
                if len(data) < 1:
                    break
                alpha.append(data[0])
                cl.append(data[1])
                cd.append(data[2])
                # cm.append(data[3]) [AH] does not appear to be used in current version...
            polar.alpha = alpha
            polar.cl = cl
            polar.cd = cd
            polar.cm = cm
            airfoil.af_tables.append(polar)

        f.close()

        return airfoil, params


    def ServoDynReader(self, params):

        sd_file = os.path.join(params['fst_vt:fst_directory'], params['fst_vt:input_files:ServoFile'])
        f = open(sd_file)

        f.readline()
        f.readline()

        # Simulation Control (sd_sim_ctrl)
        f.readline()
        boolflag = f.readline().split()[0]
        if boolflag == 'False':
            params['fst_vt:sd_sim_ctrl:Echo'] = False
        else:
            params['fst_vt:sd_sim_ctrl:Echo'] = True
        params['fst_vt:sd_sim_ctrl:DT'] = float(f.readline().split()[0])

        # Pitch Control (pitch_ctrl)
        f.readline()
        params['fst_vt:pitch_ctrl:PCMode']       = int(f.readline().split()[0])
        params['fst_vt:pitch_ctrl:TPCOn']        = float(f.readline().split()[0])
        params['fst_vt:pitch_ctrl:TPitManS1']    = float(f.readline().split()[0])
        params['fst_vt:pitch_ctrl:TPitManS2']    = float(f.readline().split()[0])
        params['fst_vt:pitch_ctrl:TPitManS3']    = float(f.readline().split()[0])
        params['fst_vt:pitch_ctrl:PitManRat1']   = float(f.readline().split()[0])
        params['fst_vt:pitch_ctrl:PitManRat2']   = float(f.readline().split()[0])
        params['fst_vt:pitch_ctrl:PitManRat3']   = float(f.readline().split()[0])
        params['fst_vt:pitch_ctrl:BlPitchF1']    = float(f.readline().split()[0])
        params['fst_vt:pitch_ctrl:BlPitchF2']    = float(f.readline().split()[0])
        params['fst_vt:pitch_ctrl:BlPitchF3']    = float(f.readline().split()[0])

        # Geneartor and Torque Control (gen_torq_ctrl)
        f.readline()
        separams['fst_vt:gen_torq_ctrl:VSContrl'] = int(f.readline().split()[0])
        params['fst_vt:gen_torq_ctrl:GenModel'] = int(f.readline().split()[0])
        params['fst_vt:gen_torq_ctrl:GenEff']   = float(f.readline().split()[0])
        boolflag = f.readline().split()[0]
        if boolflag == 'False':
            params['fst_vt:gen_torq_ctrl:GenTiStr'] = False
        else:
            params['fst_vt:gen_torq_ctrl:GenTiStr'] = True
        boolflag = f.readline().split()[0]
        if boolflag == 'False':
            params['fst_vt:gen_torq_ctrl:GenTiStp'] = False
        else:
            params['fst_vt:gen_torq_ctrl:GenTiStp'] = True
        params['fst_vt:gen_torq_ctrl:SpdGenOn'] = float(f.readline().split()[0])
        params['fst_vt:gen_torq_ctrl:TimGenOn'] = float(f.readline().split()[0])
        params['fst_vt:gen_torq_ctrl:TimGenOf'] = float(f.readline().split()[0])

        # Simple Variable-Speed Torque Control (var_speed_torq_ctrl)
        f.readline()
        params['fst_vt:var_speed_torq_ctrl:VS_RtGnSp'] = float(f.readline().split()[0])
        params['fst_vt:var_speed_torq_ctrl:VS_RtTq']   = float(f.readline().split()[0])
        params['fst_vt:var_speed_torq_ctrl:VS_Rgn2K']  = float(f.readline().split()[0])
        params['fst_vt:var_speed_torq_ctrl:VS_SlPc']   = float(f.readline().split()[0])

        # Simple Induction Generator (induct_gen)
        f.readline()
        params['fst_vt:induct_gen:SIG_SlPc'] = float(f.readline().split()[0])
        params['fst_vt:induct_gen:SIG_SySp'] = float(f.readline().split()[0])
        params['fst_vt:induct_gen:SIG_RtTq'] = float(f.readline().split()[0])
        params['fst_vt:induct_gen:SIG_PORt'] = float(f.readline().split()[0])

        # Thevenin-Equivalent Induction Generator (theveq_induct_gen)
        f.readline()
        params['fst_vt:theveq_induct_gen:TEC_Freq'] = float(f.readline().split()[0])
        params['fst_vt:theveq_induct_gen:TEC_NPol'] = int(f.readline().split()[0])
        params['fst_vt:theveq_induct_gen:TEC_SRes'] = float(f.readline().split()[0])
        params['fst_vt:theveq_induct_gen:TEC_RRes'] = float(f.readline().split()[0])
        params['fst_vt:theveq_induct_gen:TEC_VLL']  = float(f.readline().split()[0])
        params['fst_vt:theveq_induct_gen:TEC_SLR']  = float(f.readline().split()[0])
        params['fst_vt:theveq_induct_gen:TEC_RLR']  = float(f.readline().split()[0])
        params['fst_vt:theveq_induct_gen:TEC_MR']   = float(f.readline().split()[0])

        # High-Speed Shaft Brake (shaft_brake)
        f.readline()
        params['fst_vt:shaft_brake:HSSBrMode'] = int(f.readline().split()[0])
        params['fst_vt:shaft_brake:THSSBrDp']  = float(f.readline().split()[0])
        params['fst_vt:shaft_brake:HSSBrDT']   = float(f.readline().split()[0])
        params['fst_vt:shaft_brake:HSSBrTqF']  = float(f.readline().split()[0])

        # Nacelle-Yaw Control (nac_yaw_ctrl)
        f.readline()
        params['fst_vt:nac_yaw_ctrl:YCMode']    = int(f.readline().split()[0])
        params['fst_vt:nac_yaw_ctrl:TYCOn']     = float(f.readline().split()[0])
        params['fst_vt:nac_yaw_ctrl:YawNeut']   = float(f.readline().split()[0])
        params['fst_vt:nac_yaw_ctrl:YawSpr']    = float(f.readline().split()[0])
        params['fst_vt:nac_yaw_ctrl:YawDamp']   = float(f.readline().split()[0])
        params['fst_vt:nac_yaw_ctrl:TYawManS']  = float(f.readline().split()[0])
        params['fst_vt:nac_yaw_ctrl:YawManRat'] = float(f.readline().split()[0])
        params['fst_vt:nac_yaw_ctrl:NacYawF']   = float(f.readline().split()[0])

        # Tuned Mass Damper (tuned_mass_damper)
        f.readline()
        boolflag = f.readline().split()[0]
        if boolflag == 'False':
            params['fst_vt:tuned_mass_damper:CompNTMD'] = False
        else:
            params['fst_vt:tuned_mass_damper:CompNTMD'] = True
        params['fst_vt:tuned_mass_damper:NTMDfile'] = f.readline().split()[0][1:-1]
        boolflag = f.readline().split()[0]
        if boolflag == 'False':
            params['fst_vt:tuned_mass_damper:CompTTMD'] = False
        else:
            params['fst_vt:tuned_mass_damper:CompTTMD'] = True
        params['fst_vt:tuned_mass_damper:TTMDfile'] = f.readline().split()[0][1:-1]

        # Bladed Interface and Torque-Speed Look-Up Table (bladed_interface)
        f.readline()
        params['fst_vt:bladed_interface:DLL_FileName'] = f.readline().split()[0][1:-1]
        params['fst_vt:bladed_interface:DLL_InFile']   = f.readline().split()[0][1:-1]
        params['fst_vt:bladed_interface:DLL_ProcName'] = f.readline().split()[0][1:-1]
        dll_dt_line = f.readline().split()[0]
        try:
            params['fst_vt:bladed_interface:DLL_DT'] = float(dll_dt_line)
        except:
            params['fst_vt:bladed_interface:DLL_DT'] = dll_dt_line[1:-1]
        boolflag = f.readline().split()[0]
        if boolflag == 'False':
            params['fst_vt:bladed_interface:DLL_Ramp'] = False
        else:
            params['fst_vt:bladed_interface:DLL_Ramp'] = True
        params['fst_vt:bladed_interface:BPCutoff']     = float(f.readline().split()[0])
        params['fst_vt:bladed_interface:NacYaw_North'] = float(f.readline().split()[0])
        params['fst_vt:bladed_interface:Ptch_Cntrl']   = int(f.readline().split()[0])
        params['fst_vt:bladed_interface:Ptch_SetPnt']  = float(f.readline().split()[0])
        params['fst_vt:bladed_interface:Ptch_Min']     = float(f.readline().split()[0])
        params['fst_vt:bladed_interface:Ptch_Max']     = float(f.readline().split()[0])
        params['fst_vt:bladed_interface:PtchRate_Min'] = float(f.readline().split()[0])
        params['fst_vt:bladed_interface:PtchRate_Max'] = float(f.readline().split()[0])
        params['fst_vt:bladed_interface:Gain_OM']      = float(f.readline().split()[0])
        params['fst_vt:bladed_interface:GenSpd_MinOM'] = float(f.readline().split()[0])
        params['fst_vt:bladed_interface:GenSpd_MaxOM'] = float(f.readline().split()[0])
        params['fst_vt:bladed_interface:GenSpd_Dem']   = float(f.readline().split()[0])
        params['fst_vt:bladed_interface:GenTrq_Dem']   = float(f.readline().split()[0])
        params['fst_vt:bladed_interface:GenPwr_Dem']   = float(f.readline().split()[0])

        f.readline()

        params['fst_vt:bladed_interface:DLL_NumTrq'] = int(f.readline().split()[0])
        f.readline()
        f.readline()
        params['fst_vt:bladed_interface:GenSpd_TLU'] = [None] * params['fst_vt:bladed_interface:DLL_NumTrq']
        params['fst_vt:bladed_interface:GenTrq_TLU'] = [None] * params['fst_vt:bladed_interface:DLL_NumTrq']
        for i in range(self.fst_vt.bladed_interface.DLL_NumTrq):
            data = f.readline().split()
            params['fst_vt:bladed_interface:GenSpd_TLU'][i] = float(data[0])
            params['fst_vt:bladed_interface:GenTrq_TLU'][i] = float(data[0])

        # ServoDyn Output Params (sd_out_params)
        f.readline()
        boolflag = f.readline().split()[0]
        if boolflag == 'False':
            params['fst_vt:sd_out_params:SumPrint'] = False
        else:
            params['fst_vt:sd_out_params:SumPrint'] = True
        params['fst_vt:sd_out_params:OutFile']  = int(f.readline().split()[0])
        boolflag = f.readline().split()[0]
        if boolflag == 'False':
            params['fst_vt:sd_out_params:TabDelim'] = False
        else:
            params['fst_vt:sd_out_params:TabDelim'] = True
        params['fst_vt:sd_out_params:OutFmt']   = f.readline().split()[0][1:-1]
        params['fst_vt:sd_out_params:TStart']   = float(f.readline().split()[0])

        # ServoDyn Outlist
        f.readline()
        data = f.readline()
        while data.split()[0] != 'END':
            channels = data.split('"')
            channel_list = channels[1].split(',')
            for i in range(len(channel_list)):
                channel_list[i] = channel_list[i].replace(' ','')
                if channel_list[i] in params['fst_vt:outlist:servodyn_vt'].__dict__.keys():
                    params['fst_vt:outlist:servodyn_vt'].__dict__[channel_list[i]] = True
            data = f.readline()

        f.close()
        return params


if __name__=="__main__":
    path = "this\\was\\a\\windows\\path"
    new = fix_path(path)
    print "path, newpath", path, new
    path = "this/was/a/linux/path"
    new = fix_path(path)
    print "path, newpath", path, new

