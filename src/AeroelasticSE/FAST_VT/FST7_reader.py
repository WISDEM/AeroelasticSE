
import os,re

from FST_vartrees_new import FstModel, ADAirfoil, ADAirfoilPolar

def fix_path(name):
    """ split a path, then reconstruct it using os.path.join """
    name = re.split("\\\|/", name)
    new = name[0]
    for i in range(1,len(name)):
        new = os.path.join(new, name[i])
    return new

class Fst7InputBase(object):

    model_name = 'FAST Model'

class Fst7InputReader(Fst7InputBase):


    def __init__(self):

        self.fst_infile = ''   #Master FAST file
        self.fst_directory = ''   #Directory of master FAST file set
        self.fst_file_type = 0   #Enum(0, (0,1), desc='Fst file type, 0=old FAST, 1 = new FAST')    
        self.ad_file_type = 0   #Enum(0, (0,1), desc='Aerodyn file type, 0=old Aerodyn, 1 = new Aerdyn')

        self.fst_vt = FstModel()
    
    def execute(self):
    	  
    	  self.read_input_file()

    def read_input_file(self):

        fst_file = os.path.join(self.fst_directory, self.fst_infile)
        f = open(fst_file)

        # FAST Inputs
        f.readline()
        f.readline()
        self.fst_vt.description = f.readline().rstrip()
        f.readline()
        f.readline()
        boolflag = f.readline().split()[0]
        if boolflag == 'False':
            self.fst_vt.fst_sim_ctrl.Echo = False
        else:
            self.fst_vt.fst_sim_ctrl.Echo = True
        ap = f.readline().split()[0]
        if ap == '1':
            self.fst_vt.fst_sim_ctrl.ADAMSPrep = 1
        elif ap == '2':
            self.fst_vt.fst_sim_ctrl.ADAMSPrep = 2
        else:
            self.fst_vt.fst_sim_ctrl.ADAMSPrep = 3
        am = f.readline().split()[0]
        if am == '1':
            self.fst_vt.fst_sim_ctrl.AnalMode = 1
        else:
            self.fst_vt.fst_sim_ctrl.AnalMode = 2
        self.fst_vt.turb_config.NumBl = int(f.readline().split()[0])
        self.fst_vt.fst_sim_ctrl.TMax = float(f.readline().split()[0])
        self.fst_vt.fst_sim_ctrl.DT  = float(f.readline().split()[0])
        f.readline()
        ym = f.readline().split()[0]
        if ym == '0':
            self.fst_vt.nac_yaw_ctrl.YCMode = 0
        elif ym == '1':
            self.fst_vt.nac_yaw_ctrl.YCMode = 1
        else:
            self.fst_vt.nac_yaw_ctrl.YCMode = 2
        self.fst_vt.nac_yaw_ctrl.TYCOn = float(f.readline().split()[0])
        pm = f.readline().split()[0]
        if pm == '0':
            self.fst_vt.pitch_ctrl.PCMode = 0
        elif pm == '1':
            self.fst_vt.pitch_ctrl.PCMode = 1
        else:
            self.fst_vt.pitch_ctrl.PCMode = 2
        self.fst_vt.pitch_ctrl.TPCOn = float(f.readline().split()[0])
        vs = f.readline().split()[0]
        if vs == '0':
            self.fst_vt.gen_torq_ctrl.VSContrl = 0
        elif vs == '1':
            self.fst_vt.gen_torq_ctrl.VSContrl = 1
        elif vs == '2':
            self.fst_vt.gen_torq_ctrl.VSContrl = 2
        else:
            self.fst_vt.gen_torq_ctrl.VSContrl = 3
        self.fst_vt.var_speed_torq_ctrl.VS_RtGnSp  = float(f.readline().split()[0])
        self.fst_vt.var_speed_torq_ctrl.VS_RtTq  = float(f.readline().split()[0])
        self.fst_vt.var_speed_torq_ctrl.VS_Rgn2K  = float(f.readline().split()[0])
        self.fst_vt.var_speed_torq_ctrl.VS_SlPc  = float(f.readline().split()[0])
        gm = f.readline().split()[0]
        if gm == '1':
            self.fst_vt.gen_torq_ctrl.GenModel = 1
        elif gm == '2':
            self.fst_vt.gen_torq_ctrl.GenModel = 2
        else:
            self.fst_vt.gen_torq_ctrl.GenModel = 3
        self.fst_vt.gen_torq_ctrl.GenTiStr = bool(f.readline().split()[0])
        self.fst_vt.gen_torq_ctrl.GenTiStp = bool(f.readline().split()[0])
        self.fst_vt.gen_torq_ctrl.SpdGenOn = float(f.readline().split()[0])
        self.fst_vt.gen_torq_ctrl.TimGenOn = float(f.readline().split()[0])
        self.fst_vt.gen_torq_ctrl.TimGenOf = float(f.readline().split()[0])
        hss = f.readline().split()[0]
        if hss == '1':
            self.fst_vt.shaft_brake.HSSBrMode = 1
        else:
            self.fst_vt.shaft_brake.HSSBrMode = 2
        self.fst_vt.shaft_brake.THSSBrDp = float(f.readline().split()[0])
        self.fst_vt.tip_brake.TiDynBrk = float(f.readline().split()[0])
        self.fst_vt.tip_brake.TTpBrDp1 = float(f.readline().split()[0])
        self.fst_vt.tip_brake.TTpBrDp2 = float(f.readline().split()[0])
        self.fst_vt.tip_brake.TTpBrDp3 = float(f.readline().split()[0])
        self.fst_vt.tip_brake.TBDepISp1 = float(f.readline().split()[0])
        self.fst_vt.tip_brake.TBDepISp2 = float(f.readline().split()[0])
        self.fst_vt.tip_brake.TBDepISp3 = float(f.readline().split()[0])
        self.fst_vt.nac_yaw_ctrl.TYawManS = float(f.readline().split()[0])
        self.fst_vt.nac_yaw_ctrl.TYawManE = float(f.readline().split()[0])
        self.fst_vt.nac_yaw_ctrl.NacYawF = float(f.readline().split()[0])
        self.fst_vt.pitch_ctrl.TPitManS1 = float(f.readline().split()[0])
        self.fst_vt.pitch_ctrl.TPitManS2 = float(f.readline().split()[0])
        self.fst_vt.pitch_ctrl.TPitManS3 = float(f.readline().split()[0])
        self.fst_vt.pitch_ctrl.TPitManE1 = float(f.readline().split()[0])
        self.fst_vt.pitch_ctrl.TPitManE2 = float(f.readline().split()[0])
        self.fst_vt.pitch_ctrl.TPitManE3 = float(f.readline().split()[0])
        self.fst_vt.pitch_ctrl.BlPitch1  = float(f.readline().split()[0])
        self.fst_vt.pitch_ctrl.BlPitch2  = float(f.readline().split()[0])
        self.fst_vt.pitch_ctrl.BlPitch3  = float(f.readline().split()[0])
        self.fst_vt.pitch_ctrl.B1PitchF1 = float(f.readline().split()[0])
        self.fst_vt.pitch_ctrl.B1PitchF2 = float(f.readline().split()[0])
        self.fst_vt.pitch_ctrl.B1PitchF3 = float(f.readline().split()[0])
        f.readline()
        self.fst_vt.envir_cond.Gravity = float(f.readline().split()[0])
        f.readline()
        boolflag = f.readline().split()[0]
        if boolflag == 'False':
            self.fst_vt.dof.FlapDOF1 = False
        else:
            self.fst_vt.dof.FlapDOF1 = True
        boolflag = f.readline().split()[0]
        if boolflag == 'False':
            self.fst_vt.dof.FlapDOF2 = False
        else:
            self.fst_vt.dof.FlapDOF2 = True
        boolflag = f.readline().split()[0]
        if boolflag == 'False':
            self.fst_vt.dof.EdgeDOF = False
        else:
            self.fst_vt.dof.EdgeDOF = True
        boolflag = f.readline().split()[0]
        if boolflag == 'False':
            self.fst_vt.dof.TeetDOF = False
        else:
            self.fst_vt.dof.TeetDOF = True
        boolflag = f.readline().split()[0]
        if boolflag == 'False':
            self.fst_vt.dof.DrTrDOF = False
        else:
            self.fst_vt.dof.DrTrDOF = True
        boolflag = f.readline().split()[0]
        if boolflag == 'False':
            self.fst_vt.dof.GenDOF = False
        else:
            self.fst_vt.dof.GenDOF = True
        boolflag = f.readline().split()[0]
        if boolflag == 'False':
            self.fst_vt.dof.YawDOF = False
        else:
            self.fst_vt.dof.YawDOF = True
        boolflag = f.readline().split()[0]
        if boolflag == 'False':
            self.fst_vt.dof.TwFADOF1 = False
        else:
            self.fst_vt.dof.TwFADOF1 = True
        boolflag = f.readline().split()[0]
        if boolflag == 'False':
            self.fst_vt.dof.TwFADOF2 = False
        else:
            self.fst_vt.dof.TwFADOF2 = True
        boolflag = f.readline().split()[0]
        if boolflag == 'False':
            self.fst_vt.dof.TwSSDOF1 = False
        else:
            self.fst_vt.dof.TwSSDOF1 = True
        boolflag = f.readline().split()[0]
        if boolflag == 'False':
            self.fst_vt.dof.TwSSDOF2 = False
        else:
            self.fst_vt.dof.TwSSDOF2 = True
        boolflag = f.readline().split()[0]
        if boolflag == 'False':
            self.fst_vt.ftr_swtchs_flgs.CompAero = False
        else:
            self.fst_vt.ftr_swtchs_flgs.CompAero = True
        boolflag = f.readline().split()[0]
        if boolflag == 'False':
            self.fst_vt.ftr_swtchs_flgs.CompNoise = False
        else:
            self.fst_vt.ftr_swtchs_flgs.CompNoise = True
        f.readline()
        self.fst_vt.init_conds.OoPDefl = float(f.readline().split()[0])
        self.fst_vt.init_conds.IPDefl = float(f.readline().split()[0])
        self.fst_vt.init_conds.TeetDefl = float(f.readline().split()[0])
        self.fst_vt.init_conds.Azimuth = float(f.readline().split()[0])
        self.fst_vt.init_conds.RotSpeed = float(f.readline().split()[0])
        self.fst_vt.init_conds.NacYaw = float(f.readline().split()[0])
        self.fst_vt.init_conds.TTDspFA = float(f.readline().split()[0])
        self.fst_vt.init_conds.TTDspSS = float(f.readline().split()[0])
        f.readline()
        self.fst_vt.turb_config.TipRad = float(f.readline().split()[0])
        self.fst_vt.turb_config.HubRad = float(f.readline().split()[0])
        self.fst_vt.turb_config.PSpnElN = int(f.readline().split()[0])
        self.fst_vt.turb_config.UndSling = float(f.readline().split()[0])
        self.fst_vt.turb_config.HubCM = float(f.readline().split()[0])
        self.fst_vt.turb_config.OverHang = float(f.readline().split()[0])
        self.fst_vt.turb_config.NacCMxn = float(f.readline().split()[0])
        self.fst_vt.turb_config.NacCMyn = float(f.readline().split()[0])
        self.fst_vt.turb_config.NacCMzn = float(f.readline().split()[0])
        self.fst_vt.turb_config.TowerHt = float(f.readline().split()[0])
        self.fst_vt.turb_config.Twr2Shft = float(f.readline().split()[0])
        self.fst_vt.turb_config.TwrRBHt = float(f.readline().split()[0])
        self.fst_vt.turb_config.ShftTilt = float(f.readline().split()[0])
        self.fst_vt.turb_config.Delta3 = float(f.readline().split()[0])
        self.fst_vt.turb_config.PreCone1 = float(f.readline().split()[0])
        self.fst_vt.turb_config.PreCone2 = float(f.readline().split()[0])
        self.fst_vt.turb_config.PreCone3 = float(f.readline().split()[0])
        self.fst_vt.turb_config.AzimB1Up = float(f.readline().split()[0])
        f.readline()
        self.fst_vt.mass_inertia.YawBrMass = float(f.readline().split()[0])
        self.fst_vt.mass_inertia.NacMass = float(f.readline().split()[0])
        self.fst_vt.mass_inertia.HubMass = float(f.readline().split()[0])
        self.fst_vt.mass_inertia.TipMass1 = float(f.readline().split()[0])
        self.fst_vt.mass_inertia.TipMass2 = float(f.readline().split()[0])
        self.fst_vt.mass_inertia.TipMass3 = float(f.readline().split()[0])
        self.fst_vt.mass_inertia.NacYIner = float(f.readline().split()[0])
        self.fst_vt.mass_inertia.GenIner = float(f.readline().split()[0])
        self.fst_vt.mass_inertia.HubIner = float(f.readline().split()[0])
        f.readline()
        self.fst_vt.drivetrain.GBoxEff = float(f.readline().split()[0])
        self.fst_vt.gen_torq_ctrl.GenEff = float(f.readline().split()[0])
        self.fst_vt.drivetrain.GBRatio = float(f.readline().split()[0])
        boolflag = f.readline().split()[0]
        if boolflag == 'False':
            self.fst_vt.drivetrain.GBRevers = False
        else:
            self.fst_vt.drivetrain.GBRevers = True
        self.fst_vt.shaft_brake.HSSBrTqF = float(f.readline().split()[0])
        self.fst_vt.shaft_brake.HSSBrDT = float(f.readline().split()[0])
        self.fst_vt.drivetrain.DynBrkFi = f.readline().split()[0]
        self.fst_vt.drivetrain.DTTorSpr = float(f.readline().split()[0])
        self.fst_vt.drivetrain.DTTorDmp = float(f.readline().split()[0])
        f.readline()
        self.fst_vt.induct_gen.SIG_SlPc = float(f.readline().split()[0])
        self.fst_vt.induct_gen.SIG_SySp = float(f.readline().split()[0])
        self.fst_vt.induct_gen.SIG_RtTq = float(f.readline().split()[0])
        self.fst_vt.induct_gen.SIG_PORt = float(f.readline().split()[0])
        f.readline()
        self.fst_vt.theveq_induct_gen.TEC_Freq = float(f.readline().split()[0])
        self.fst_vt.theveq_induct_gen.TEC_NPol = int(f.readline().split()[0])
        self.fst_vt.theveq_induct_gen.TEC_SRes = float(f.readline().split()[0])
        self.fst_vt.theveq_induct_gen.TEC_RRes = float(f.readline().split()[0])
        self.fst_vt.theveq_induct_gen.TEC_VLL = float(f.readline().split()[0])
        self.fst_vt.theveq_induct_gen.TEC_SLR = float(f.readline().split()[0])
        self.fst_vt.theveq_induct_gen.TEC_RLR = float(f.readline().split()[0])
        self.fst_vt.theveq_induct_gen.TEC_MR = float(f.readline().split()[0])
        f.readline()
        pm = f.readline().split()[0]
        if pm == '0':
            self.fst_vt.platform.PtfmModel = 0
        elif pm == '1':
            self.fst_vt.platform.PtfmModel = 1
        elif pm == '2':
            self.fst_vt.platform.PtfmModel = 2
        else:
            self.fst_vt.platform.PtfmModel = 3
        self.fst_vt.platform.PtfmFile = f.readline().split()[0][1:-1]
        f.readline()
        self.fst_vt.tower.TwrNodes = int(f.readline().split()[0])
        self.fst_vt.tower.TwrFile = f.readline().split()[0][1:-1]
        f.readline()
        self.fst_vt.nac_yaw_ctrl.YawSpr = float(f.readline().split()[0])
        self.fst_vt.nac_yaw_ctrl.YawDamp = float(f.readline().split()[0])
        self.fst_vt.nac_yaw_ctrl.YawNeut = float(f.readline().split()[0])
        f.readline()
        boolflag = f.readline().split()[0]
        if boolflag == 'False':
            self.fst_vt.furling.Furling = False
        else:
            self.fst_vt.furling.Furling = True
        self.fst_vt.furling.FurlFile = f.readline().split()[0]
        f.readline() 
        tm = f.readline().split()[0]
        if tm == '0':
            self.fst_vt.rotor_teeter.TeetMod = 0
        elif tm == '1':
            self.fst_vt.rotor_teeter.TeetMod = 1
        else:
            self.fst_vt.rotor_teeter.TeetMod = 2
        self.fst_vt.rotor_teeter.TeetDmpP = float(f.readline().split()[0])
        self.fst_vt.rotor_teeter.TeetDmp = float(f.readline().split()[0])
        self.fst_vt.rotor_teeter.TeetCDmp = float(f.readline().split()[0])
        self.fst_vt.rotor_teeter.TeetSStP = float(f.readline().split()[0])
        self.fst_vt.rotor_teeter.TeetHStP = float(f.readline().split()[0])
        self.fst_vt.rotor_teeter.TeetSSSp = float(f.readline().split()[0])
        self.fst_vt.rotor_teeter.TeetHSSp = float(f.readline().split()[0])
        f.readline()
        self.fst_vt.tip_brake.TBDrConN = float(f.readline().split()[0])
        self.fst_vt.tip_brake.TBDrConD = float(f.readline().split()[0])
        self.fst_vt.tip_brake.TpBrDT = float(f.readline().split()[0])
        f.readline()
        self.fst_vt.blade_struc.BldFile1 = f.readline().split()[0][1:-1] # TODO - different blade files
        self.fst_vt.blade_struc.BldFile2 = f.readline().split()[0][1:-1]
        self.fst_vt.blade_struc.BldFile3 = f.readline().split()[0][1:-1]
        f.readline() 
        self.fst_vt.input_files.ADFile = f.readline().split()[0][1:-1]
        f.readline()
        self.fst_vt.input_files.NoiseFile = f.readline().split()[0]
        f.readline()
        self.fst_vt.input_files.ADAMSFile = f.readline().split()[0]
        f.readline()
        self.fst_vt.input_files.LinFile = f.readline().split()[0]
        f.readline()
        boolflag = f.readline().split()[0]
        if boolflag == 'False':
            self.fst_vt.fst_out_params.SumPrint = False
        else:
            self.fst_vt.fst_out_params.SumPrint = True
        if self.fst_file_type == 0:
            ff = f.readline().split()[0]
            if ff == '1':
                self.fst_vt.fst_out_params.OutFileFmt = 1
            else:
                self.fst_vt.fst_out_params.OutFileFmt = 2
        boolflag = f.readline().split()[0]
        if boolflag == 'False':
            self.fst_vt.fst_out_params.TabDelim = False
        else:
            self.fst_vt.fst_out_params.TabDelim = True

        self.fst_vt.fst_out_params.OutFmt = f.readline().split()[0]
        self.fst_vt.fst_out_params.TStart = float(f.readline().split()[0])
        self.fst_vt.ed_out_params.DecFact = int(f.readline().split()[0])
        self.fst_vt.fst_out_params.SttsTime = float(f.readline().split()[0])
        self.fst_vt.turb_config.NcIMUxn = float(f.readline().split()[0])
        self.fst_vt.turb_config.NcIMUyn = float(f.readline().split()[0])
        self.fst_vt.turb_config.NcIMUzn = float(f.readline().split()[0])
        self.fst_vt.turb_config.ShftGagL = float(f.readline().split()[0])
        self.fst_vt.ed_out_params.NTwGages = int(f.readline().split()[0])
        twrg = f.readline().split(',')
        if self.fst_vt.ed_out_params.NTwGages != 0: #loop over elements if there are gauges to be added, otherwise assign directly
            for i in range(self.fst_vt.ed_out_params.NTwGages):
                self.fst_vt.ed_out_params.TwrGagNd.append(twrg[i])
            self.fst_vt.ed_out_params.TwrGagNd[-1] = self.fst_vt.ed_out_params.TwrGagNd[-1][0:2]
        else:
            self.fst_vt.ed_out_params.TwrGagNd = twrg
            self.fst_vt.ed_out_params.TwrGagNd[-1] = self.fst_vt.ed_out_params.TwrGagNd[-1][0:4]
        self.fst_vt.ed_out_params.NBlGages = int(f.readline().split()[0])
        blg = f.readline().split(',')
        if self.fst_vt.ed_out_params.NBlGages != 0:
            for i in range(self.fst_vt.ed_out_params.NBlGages):
                self.fst_vt.ed_out_params.BldGagNd.append(blg[i])
            self.fst_vt.ed_out_params.BldGagNd[-1] = self.fst_vt.ed_out_params.BldGagNd[-1][0:2]
        else:
            self.fst_vt.ed_out_params.BldGagNd = blg
            self.fst_vt.ed_out_params.BldGagNd[-1] = self.fst_vt.ed_out_params.BldGagNd[-1][0:4]
    
        # Outlist (TODO - detailed categorization)
        f.readline()
        data = f.readline()
        while data.split()[0] != 'END':
            channels = data.split('"')
            channel_list = channels[1].split(',')
            for i in range(len(channel_list)):
                channel_list[i] = channel_list[i].replace(' ','')
                if channel_list[i] in self.fst_vt.outlist.wind_mot_vt.__dict__.keys():
                    self.fst_vt.outlist.wind_mot_vt.__dict__[channel_list[i]] = True
            for i in range(len(channel_list)):
                channel_list[i] = channel_list[i].replace(' ','')
                if channel_list[i] in self.fst_vt.outlist.blade_mot_vt.__dict__.keys():
                    self.fst_vt.outlist.blade_mot_vt.__dict__[channel_list[i]] = True
            for i in range(len(channel_list)):
                channel_list[i] = channel_list[i].replace(' ','')
                if channel_list[i] in self.fst_vt.outlist.hub_nacelle_mot_vt.__dict__.keys():
                    self.fst_vt.outlist.hub_nacelle_mot_vt.__dict__[channel_list[i]] = True
            for i in range(len(channel_list)):
                channel_list[i] = channel_list[i].replace(' ','')
                if channel_list[i] in self.fst_vt.outlist.tower_support_mot_vt.__dict__.keys():
                    self.fst_vt.outlist.tower_support_mot_vt.__dict__[channel_list[i]] = True
            for i in range(len(channel_list)):
                channel_list[i] = channel_list[i].replace(' ','')
                if channel_list[i] in self.fst_vt.outlist.wave_mot_vt.__dict__.keys():
                    self.fst_vt.outlist.wave_mot_vt.__dict__[channel_list[i]] = True
            for i in range(len(channel_list)):
                channel_list[i] = channel_list[i].replace(' ','')
                if channel_list[i] in self.fst_vt.outlist.blade_loads_vt.__dict__.keys():
                    self.fst_vt.outlist.blade_loads_vt.__dict__[channel_list[i]] = True
            for i in range(len(channel_list)):
                channel_list[i] = channel_list[i].replace(' ','')
                if channel_list[i] in self.fst_vt.outlist.hub_nacelle_loads_vt.__dict__.keys():
                    self.fst_vt.outlist.hub_nacelle_loads_vt.__dict__[channel_list[i]] = True
            for i in range(len(channel_list)):
                channel_list[i] = channel_list[i].replace(' ','')
                if channel_list[i] in self.fst_vt.outlist.tower_support_loads_vt.__dict__.keys():
                    self.fst_vt.outlist.tower_support_loads_vt.__dict__[channel_list[i]] = True
            for i in range(len(channel_list)):
                channel_list[i] = channel_list[i].replace(' ','')
                if channel_list[i] in self.fst_vt.outlist.dof_vt.__dict__.keys():
                    self.fst_vt.outlist.dof_vt.__dict__[channel_list[i]] = True
            data = f.readline()

        self.AeroReader()
        if self.fst_vt.aerodyn.wind_file_type == 'wnd':
            self.WndWindReader()
        else:
            print "TODO: Other wind file type (bts)"
        self.BladeReader()
        self.TowerReader()
        # if self.fst_vt.PtfmFile != 'unused':
        #     self.PlatformReader()
    
    # def PlatformReader(self):

    #     platform_file = os.path.join(self.fst_directory, self.fst_vt.PtfmFile)
    #     f = open(platform_file)

    #     f.readline()
    #     f.readline()
    #     self.fst_vt.platform_vt.description = f.readline().rstrip()

    #     # FEATURE FLAGS (CONT)
    #     f.readline()
    #     boolflag = f.readline().split()[0]
    #     if boolflag == 'False':
    #         self.fst_vt.PtfmSgDOF = False
    #     else:
    #         self.fst_vt.PtfmSgDOF = True
    #     boolflag = f.readline().split()[0]
    #     if boolflag == 'False':
    #         self.fst_vt.PtfmSwDOF = False
    #     else:
    #         self.fst_vt.PtfmSwDOF = True
    #     boolflag = f.readline().split()[0]
    #     if boolflag == 'False':
    #         self.fst_vt.PtfmHvDOF = False
    #     else:
    #         self.fst_vt.PtfmHvDOF = True
    #     boolflag = f.readline().split()[0]
    #     if boolflag == 'False':
    #         self.fst_vt.PtfmRDOF = False
    #     else:
    #         self.fst_vt.PtfmRDOF = True
    #     boolflag = f.readline().split()[0]
    #     if boolflag == 'False':
    #         self.fst_vt.PtfmPDOF = False
    #     else:
    #         self.fst_vt.PtfmPDOF = True
    #     boolflag = f.readline().split()[0]
    #     if boolflag == 'False':
    #         self.fst_vt.PtfmYDOF = False
    #     else:
    #         self.fst_vt.PtfmYDOF = True
        
    #     # INITIAL CONDITIONS (CONT)
    #     f.readline()
    #     self.fst_vt.platform_vt.PtfmSurge = float(f.readline().split()[0])
    #     self.fst_vt.platform_vt.PtfmSway  = float(f.readline().split()[0])
    #     self.fst_vt.platform_vt.PtfmHeave = float(f.readline().split()[0])
    #     self.fst_vt.platform_vt.PtfmRoll  = float(f.readline().split()[0])
    #     self.fst_vt.platform_vt.PtfmPitch = float(f.readline().split()[0])
    #     self.fst_vt.platform_vt.PtfmYaw   = float(f.readline().split()[0])
        
    #     # TURBINE CONFIGURATION (CONT)
    #     f.readline()
    #     self.fst_vt.platform_vt.TwrDraft  = float(f.readline().split()[0])
    #     self.fst_vt.platform_vt.PtfmCM    = float(f.readline().split()[0])
    #     self.fst_vt.platform_vt.PtfmRef   = float(f.readline().split()[0])
        
    #     # MASS AND INERTIA (CONT) 
    #     f.readline()
    #     self.fst_vt.platform_vt.PtfmMass  = float(f.readline().split()[0])
    #     self.fst_vt.platform_vt.PtfmRIner = float(f.readline().split()[0])
    #     self.fst_vt.platform_vt.PtfmPIner = float(f.readline().split()[0])
    #     self.fst_vt.platform_vt.PtfmYIner = float(f.readline().split()[0])
        
    #     # PLATFORM (CONT) 
    #     f.readline()
    #     pltmd = f.readline().split()[0]
    #     if pltmd == '0':
    #         self.fst_vt.platform_vt.PtfmLdMod  = 0
    #     else:
    #         self.fst_vt.platform_vt.PtfmLdMod  = 1
        
    #     # TOWER (CONT) 
    #     f.readline()
    #     twrmd = f.readline().split()[0]
    #     if twrmd == '0':
    #         self.fst_vt.platform_vt.TwrLdMod  = 0
    #     elif twrmd == '1':
    #         self.fst_vt.platform_vt.TwrLdMod  = 1
    #     elif twrmd == '2':
    #         self.fst_vt.platform_vt.TwrLdMod  = 3
    #     self.fst_vt.platform_vt.TwrDiam   = float(f.readline().split()[0])
    #     self.fst_vt.platform_vt.TwrCA     = float(f.readline().split()[0])
    #     self.fst_vt.platform_vt.TwrCD     = float(f.readline().split()[0])
        
    #     # WAVES 
    #     f.readline()
    #     self.fst_vt.platform_vt.WtrDens   = float(f.readline().split()[0])
    #     self.fst_vt.platform_vt.WtrDpth   = float(f.readline().split()[0])
    #     wavemod = f.readline().split()[0]
    #     if wavemod == '0':
    #         self.fst_vt.platform_vt.WaveMod = 0
    #     elif wavemod == '1':
    #         self.fst_vt.platform_vt.WaveMod  = 1  
    #     elif wavemod == '2':
    #         self.fst_vt.platform_vt.WaveMod = 2
    #     elif wavemod == '3':
    #         self.fst_vt.platform_vt.WaveMod  = 3
    #     else:
    #         self.fst_vt.platform_vt.WaveMod  = 4
    #     wavestmod = f.readline().split()[0]
    #     if wavestmod == '0':
    #         self.fst_vt.platform_vt.WaveStMod = 0
    #     elif wavestmod == '1':
    #         self.fst_vt.platform_vt.WaveStMod = 1
    #     elif wavestmod == '2':
    #         self.fst_vt.platform_vt.WaveStMod = 2
    #     elif wavestmod == '3':
    #         self.fst_vt.platform_vt.WaveStMod = 3
    #     self.fst_vt.platform_vt.WaveTMax  = float(f.readline().split()[0])
    #     self.fst_vt.platform_vt.WaveDT    = float(f.readline().split()[0])
    #     self.fst_vt.platform_vt.WaveHs    = float(f.readline().split()[0])
    #     self.fst_vt.platform_vt.WaveTp    = float(f.readline().split()[0])
    #     wvpk = f.readline().split()[0]
    #     if wvpk == 'DEFAULT':
    #         self.fst_vt.platform_vt.WavePkShp = 9999.9
    #     else:
    #         self.fst_vt.platform_vt.WavePkShp = float(wvpk)
    #     self.fst_vt.platform_vt.WaveDir   = float(f.readline().split()[0])
    #     self.fst_vt.platform_vt.WaveSeed1 = int(f.readline().split()[0])
    #     self.fst_vt.platform_vt.WaveSeed2 = int(f.readline().split()[0])
    #     self.fst_vt.platform_vt.GHWvFile  = f.readline().split()[0]
    
    #     # CURRENT
    #     f.readline()
    #     currmod = float(f.readline().split()[0])
    #     if currmod == '0':
    #         self.fst_vt.platform_vt.CurrMod   = 0
    #     elif currmod == '1':
    #         self.fst_vt.platform_vt.CurrMod   = 1
    #     elif currmod == '2':
    #         self.fst_vt.platform_vt.CurrMod   = 2
    #     self.fst_vt.platform_vt.CurrSSV0  = float(f.readline().split()[0])
    #     currs = f.readline().split()[0]
    #     if currs == 'DEFAULT':
    #         self.fst_vt.platform_vt.CurrSSDir = 9999.9
    #     else:
    #         self.fst_vt.platform_vt.CurrSSDir = float(currs)
    #     self.fst_vt.platform_vt.CurrNSRef = float(f.readline().split()[0])
    #     self.fst_vt.platform_vt.CurrNSV0  = float(f.readline().split()[0])
    #     self.fst_vt.platform_vt.CurrNSDir = float(f.readline().split()[0])
    #     self.fst_vt.platform_vt.CurrDIV   = float(f.readline().split()[0])
    #     self.fst_vt.platform_vt.CurrDIDir = float(f.readline().split()[0])
    
    #     # OUTPUT (CONT) 
    #     f.readline()
    #     self.fst_vt.platform_vt.NWaveKin = int(f.readline().split()[0])
    #     if self.fst_vt.platform_vt.NWaveKin != 0:
    #         self.fst_vt.platform_vt.WaveKinNd = str(f.readline().split()[0])


    def TowerReader(self):

        tower_file = os.path.join(self.fst_directory, self.fst_vt.tower.TwrFile)        
        f = open(tower_file)
        
        f.readline()
        f.readline()
        f.readline()

        # General Tower Paramters
        f.readline()
        self.fst_vt.tower.NTwInptSt = int(f.readline().split()[0])
        boolflag = f.readline().split()[0]
        if boolflag == 'False':
            self.fst_vt.CalcTMode = False
        else:
            self.fst_vt.CalcTMode = True
        self.fst_vt.tower.TwrFADmp1 = float(f.readline().split()[0])
        self.fst_vt.tower.TwrFADmp2 = float(f.readline().split()[0])
        self.fst_vt.tower.TwrSSDmp1 = float(f.readline().split()[0])
        self.fst_vt.tower.TwrSSDmp2 = float(f.readline().split()[0])
    
        # Tower Adjustment Factors
        f.readline()
        self.fst_vt.tower.FAStTunr1 = float(f.readline().split()[0])
        self.fst_vt.tower.FAStTunr2 = float(f.readline().split()[0])
        self.fst_vt.tower.SSStTunr1 = float(f.readline().split()[0])
        self.fst_vt.tower.SSStTunr2 = float(f.readline().split()[0])
        self.fst_vt.tower.AdjTwMa = float(f.readline().split()[0])
        self.fst_vt.tower.AdjFASt = float(f.readline().split()[0])
        self.fst_vt.tower.AdjSSSt = float(f.readline().split()[0])
     
        # Distributed Tower Properties   
        x = f.readline()
        y = f.readline()
        z = f.readline()
        self.fst_vt.tower.HtFract = [None] * self.fst_vt.tower.NTwInptSt
        self.fst_vt.tower.TMassDen = [None] * self.fst_vt.tower.NTwInptSt
        self.fst_vt.tower.TwFAStif = [None] * self.fst_vt.tower.NTwInptSt
        self.fst_vt.tower.TwSSStif = [None] * self.fst_vt.tower.NTwInptSt
        self.fst_vt.tower.TwGJStif = [None] * self.fst_vt.tower.NTwInptSt
        self.fst_vt.tower.TwEAStif = [None] * self.fst_vt.tower.NTwInptSt
        self.fst_vt.tower. TwFAIner = [None] * self.fst_vt.tower.NTwInptSt
        self.fst_vt.tower.TwSSIner = [None] * self.fst_vt.tower.NTwInptSt
        self.fst_vt.tower.TwFAcgOf = [None] * self.fst_vt.tower.NTwInptSt
        self.fst_vt.tower.TwSScgOf = [None] * self.fst_vt.tower.NTwInptSt
        for i in range(self.fst_vt.tower.NTwInptSt):
            data = f.readline().split()
            self.fst_vt.tower.HtFract[i] = float(data[0])
            self.fst_vt.tower.TMassDen[i] = float(data[1])
            self.fst_vt.tower.TwFAStif[i] = float(data[2])
            self.fst_vt.tower.TwSSStif[i] = float(data[3])
            self.fst_vt.tower.TwGJStif[i] = float(data[4])
            self.fst_vt.tower.TwEAStif[i] = float(data[5])
            self.fst_vt.tower. TwFAIner[i] = float(data[6])
            self.fst_vt.tower.TwSSIner[i] = float(data[7])
            self.fst_vt.tower.TwFAcgOf[i] = float(data[8])
            self.fst_vt.tower.TwSScgOf[i] = float(data[9])           
        
        # Tower Mode Shapes
        f.readline()
        self.fst_vt.tower.TwFAM1Sh = [None] * 5
        self.fst_vt.tower.TwFAM2Sh = [None] * 5
        for i in range(5):
            self.fst_vt.tower.TwFAM1Sh[i] = float(f.readline().split()[0])
        for i in range(5):
            self.fst_vt.tower.TwFAM2Sh[i] = float(f.readline().split()[0])        
        f.readline()
        self.fst_vt.tower.TwSSM1Sh = [None] * 5
        self.fst_vt.tower.TwSSM2Sh = [None] * 5          
        for i in range(5):
            self.fst_vt.tower.TwSSM1Sh[i] = float(f.readline().split()[0])
        for i in range(5):
            self.fst_vt.tower.TwSSM2Sh[i] = float(f.readline().split()[0]) 
    
    def BladeReader(self):

        blade_file = os.path.join(self.fst_directory, self.fst_vt.blade_struc.BldFile1)
        f = open(blade_file)
        
        f.readline()
        f.readline()
        f.readline()
        f.readline()
        
        self.fst_vt.blade_struc.NBlInpSt = int(f.readline().split()[0])
        boolflag = f.readline().split()[0]
        if boolflag == 'False':
            self.fst_vt.blade_struc.CalcBMode = False
        else:
            self.fst_vt.blade_struc.CalcBMode = True
        self.fst_vt.blade_struc.BldFlDmp1 = float(f.readline().split()[0])
        self.fst_vt.blade_struc.BldFlDmp2 = float(f.readline().split()[0])
        self.fst_vt.blade_struc.BldEdDmp1 = float(f.readline().split()[0])
        f.readline()
        self.fst_vt.blade_struc.FlStTunr1 = float(f.readline().split()[0])
        self.fst_vt.blade_struc.FlStTunr2 = float(f.readline().split()[0])
        self.fst_vt.blade_struc.AdjBlMs = float(f.readline().split()[0])
        self.fst_vt.blade_struc.AdjFlSt = float(f.readline().split()[0])
        self.fst_vt.blade_struc.AdjEdSt = float(f.readline().split()[0])
        
        f.readline()
        f.readline()
        f.readline()
        self.fst_vt.blade_struc.BlFract = [None] * self.fst_vt.blade_struc.NBlInpSt
        self.fst_vt.blade_struc.AeroCent = [None] * self.fst_vt.blade_struc.NBlInpSt
        self.fst_vt.blade_struc.StrcTwst = [None] * self.fst_vt.blade_struc.NBlInpSt
        self.fst_vt.blade_struc.BMassDen = [None] * self.fst_vt.blade_struc.NBlInpSt
        self.fst_vt.blade_struc.FlpStff = [None] * self.fst_vt.blade_struc.NBlInpSt
        self.fst_vt.blade_struc.EdgStff = [None] * self.fst_vt.blade_struc.NBlInpSt
        self.fst_vt.blade_struc.GJStff = [None] * self.fst_vt.blade_struc.NBlInpSt
        self.fst_vt.blade_struc.EAStff = [None] * self.fst_vt.blade_struc.NBlInpSt
        self.fst_vt.blade_struc.Alpha = [None] * self.fst_vt.blade_struc.NBlInpSt
        self.fst_vt.blade_struc.FlpIner = [None] * self.fst_vt.blade_struc.NBlInpSt
        self.fst_vt.blade_struc.EdgIner = [None] * self.fst_vt.blade_struc.NBlInpSt
        self.fst_vt.blade_struc.PrecrvRef = [None] * self.fst_vt.blade_struc.NBlInpSt
        self.fst_vt.blade_struc.PreswpRef = [None] * self.fst_vt.blade_struc.NBlInpSt
        self.fst_vt.blade_struc.FlpcgOf = [None] * self.fst_vt.blade_struc.NBlInpSt
        self.fst_vt.blade_struc.Edgcgof = [None] * self.fst_vt.blade_struc.NBlInpSt
        self.fst_vt.blade_struc.FlpEAOf = [None] * self.fst_vt.blade_struc.NBlInpSt
        self.fst_vt.blade_struc.EdgEAOf = [None] * self.fst_vt.blade_struc.NBlInpSt
        for i in range(self.fst_vt.blade_struc.NBlInpSt):
            data = f.readline().split()          
            self.fst_vt.blade_struc.BlFract[i] = float(data[0])
            self.fst_vt.blade_struc.AeroCent[i] = float(data[1])
            self.fst_vt.blade_struc.StrcTwst[i] = float(data[2])
            self.fst_vt.blade_struc.BMassDen[i] = float(data[3])
            self.fst_vt.blade_struc.FlpStff[i] = float(data[4])
            self.fst_vt.blade_struc.EdgStff[i] = float(data[5])
            self.fst_vt.blade_struc.GJStff[i] = float(data[6])
            self.fst_vt.blade_struc.EAStff[i] = float(data[7])
            self.fst_vt.blade_struc.Alpha[i] = float(data[8])
            self.fst_vt.blade_struc.FlpIner[i] = float(data[9])
            self.fst_vt.blade_struc.EdgIner[i] = float(data[10])
            self.fst_vt.blade_struc.PrecrvRef[i] = float(data[11])
            self.fst_vt.blade_struc.PreswpRef[i] = float(data[12])
            self.fst_vt.blade_struc.FlpcgOf[i] = float(data[13])
            self.fst_vt.blade_struc.Edgcgof[i] = float(data[14])
            self.fst_vt.blade_struc.FlpEAOf[i] = float(data[15])
            self.fst_vt.blade_struc.EdgEAOf[i] = float(data[16])

        f.readline()
        self.fst_vt.blade_struc.BldFl1Sh = [None] * 5
        self.fst_vt.blade_struc.BldFl2Sh = [None] * 5        
        self.fst_vt.blade_struc.BldEdgSh = [None] * 5
        for i in range(5):
            self.fst_vt.blade_struc.BldFl1Sh[i] = float(f.readline().split()[0])
        for i in range(5):
            self.fst_vt.blade_struc.BldFl2Sh[i] = float(f.readline().split()[0])            
        for i in range(5):
            self.fst_vt.blade_struc.BldEdgSh[i] = float(f.readline().split()[0])        
        

    def AeroReader(self):

        #from airfoil import PolarByRe # only if creating airfoil variable trees

        ad_file = os.path.join(self.fst_directory, self.fst_vt.input_files.ADFile)
        f = open(ad_file)

        # skip lines and check if nondimensional
        f.readline()
        self.fst_vt.aerodyn.SysUnits = f.readline().split()[0]
        self.fst_vt.aerodyn.StallMod = f.readline().split()[0]
        self.fst_vt.aerodyn.UseCm = f.readline().split()[0]
        self.fst_vt.aerodyn.InfModel = f.readline().split()[0]
        self.fst_vt.aerodyn.IndModel = f.readline().split()[0]
        self.fst_vt.aerodyn.AToler = float(f.readline().split()[0])
        self.fst_vt.aerodyn.TLModel = f.readline().split()[0]
        self.fst_vt.aerodyn.HLModel = f.readline().split()[0]
        self.fst_vt.aerodyn.WindFile = f.readline().split()[0][1:-1]
        if self.fst_vt.aerodyn.WindFile[-1] == 'h':
            self.fst_vt.aerodyn.wind_file_type = 'hh'
        elif self.fst_vt.aerodyn.WindFile[-1] == 's':
            self.fst_vt.aerodyn.wind_file_type = 'bts'
        else:
            self.fst_vt.aerodyn.wind_file_type = 'wnd'
        self.fst_vt.aerodyn.HH = float(f.readline().split()[0])
        self.fst_vt.aerodyn.TwrShad = float(f.readline().split()[0])
        self.fst_vt.aerodyn.ShadHWid = float(f.readline().split()[0])
        self.fst_vt.aerodyn.T_Shad_Refpt = float(f.readline().split()[0])
        self.fst_vt.aerodyn.AirDens = float(f.readline().split()[0])
        self.fst_vt.aerodyn.KinVisc = float(f.readline().split()[0])
        self.fst_vt.aerodyn.DTAero = float(f.readline().split()[0])

        self.fst_vt.blade_aero.NumFoil = int(f.readline().split()[0])
        self.fst_vt.blade_aero.FoilNm = [None] * self.fst_vt.blade_aero.NumFoil
        for i in range(self.fst_vt.blade_aero.NumFoil):
            af_filename = f.readline().split()[0]
            af_filename = fix_path(af_filename)
            # print af_filename
            self.fst_vt.blade_aero.FoilNm[i] = af_filename[1:-1]
        
        self.fst_vt.blade_aero.BldNodes = int(f.readline().split()[0])
        f.readline()
        self.fst_vt.blade_aero.RNodes = [None] * self.fst_vt.blade_aero.BldNodes
        self.fst_vt.blade_aero.AeroTwst = [None] * self.fst_vt.blade_aero.BldNodes
        self.fst_vt.blade_aero.DRNodes = [None] * self.fst_vt.blade_aero.BldNodes
        self.fst_vt.blade_aero.Chord = [None] * self.fst_vt.blade_aero.BldNodes
        self.fst_vt.blade_aero.NFoil = [None] * self.fst_vt.blade_aero.BldNodes
        self.fst_vt.blade_aero.PrnElm = [None] * self.fst_vt.blade_aero.BldNodes       
        for i in range(self.fst_vt.blade_aero.BldNodes):
            data = f.readline().split()
            self.fst_vt.blade_aero.RNodes[i] = float(data[0])
            self.fst_vt.blade_aero.AeroTwst[i] = float(data[1])
            self.fst_vt.blade_aero.DRNodes[i] = float(data[2])
            self.fst_vt.blade_aero.Chord[i] = float(data[3])
            self.fst_vt.blade_aero.NFoil[i] = int(data[4])
            self.fst_vt.blade_aero.PrnElm[i] = data[5]

        f.close()

        # create airfoil objects
        for i in range(self.fst_vt.blade_aero.NumFoil):
             self.fst_vt.blade_aero.af_data.append(self.initFromAerodynFile(os.path.join(self.fst_directory,self.fst_vt.blade_aero.FoilNm[i]), self.ad_file_type))


    def initFromAerodynFile(self, aerodynFile, mode): # kld - added for fast noise
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

        return airfoil
    
    # def SimpleWindReader(self):

    #     #from airfoil import PolarByRe # only if creating airfoil variable trees

    #     wind_file = os.path.join(self.fst_directory, self.fst_vt.aero_vt.WindFile)
    #     f = open(wind_file)

    #     data = []
    #     while 1:
    #         line = f.readline()
    #         if not line:
    #             break
    #         line_split = line.split()
    #         if line_split[0] != '!':
    #             data.append(line.split())

    #     self.fst_vt.simple_wind_vt.TimeSteps = len(data)

    #     self.fst_vt.simple_wind_vt.Time = [None] * len(data)
    #     self.fst_vt.simple_wind_vt.HorSpd = [None] * len(data)
    #     self.fst_vt.simple_wind_vt.WindDir = [None] * len(data)
    #     self.fst_vt.simple_wind_vt.VerSpd = [None] * len(data)
    #     self.fst_vt.simple_wind_vt.HorShr = [None] * len(data)
    #     self.fst_vt.simple_wind_vt.VerShr = [None] * len(data)
    #     self.fst_vt.simple_wind_vt.LnVShr = [None] * len(data)
    #     self.fst_vt.simple_wind_vt.GstSpd = [None] * len(data)        
    #     for i in range(len(data)):
    #         self.fst_vt.simple_wind_vt.Time[i] = float(data[i][0])
    #         self.fst_vt.simple_wind_vt.HorSpd[i] = float(data[i][1])
    #         self.fst_vt.simple_wind_vt.WindDir[i] = float(data[i][2])
    #         self.fst_vt.simple_wind_vt.VerSpd[i] = float(data[i][3])
    #         self.fst_vt.simple_wind_vt.HorShr[i] = float(data[i][4])
    #         self.fst_vt.simple_wind_vt.VerShr[i] = float(data[i][5])
    #         self.fst_vt.simple_wind_vt.LnVShr[i] = float(data[i][6])
    #         self.fst_vt.simple_wind_vt.GstSpd[i] = float(data[i][7])

    #     f.close()


    def WndWindReader(self):

        wind_file = os.path.join(self.fst_directory, self.fst_vt.aerodyn.WindFile)
        f = open(wind_file)

        data = []
        while 1:
            line = f.readline()
            if not line:
                break
            line_split = line.split()
            if line_split[0] != '!':
                data.append(line.split())

        self.fst_vt.wnd_wind.TimeSteps = len(data)

        self.fst_vt.wnd_wind.Time = [None] * len(data)
        self.fst_vt.wnd_wind.HorSpd = [None] * len(data)
        self.fst_vt.wnd_wind.WindDir = [None] * len(data)
        self.fst_vt.wnd_wind.VerSpd = [None] * len(data)
        self.fst_vt.wnd_wind.HorShr = [None] * len(data)
        self.fst_vt.wnd_wind.VerShr = [None] * len(data)
        self.fst_vt.wnd_wind.LnVShr = [None] * len(data)
        self.fst_vt.wnd_wind.GstSpd = [None] * len(data)        
        for i in range(len(data)):
            self.fst_vt.wnd_wind.Time[i] = float(data[i][0])
            self.fst_vt.wnd_wind.HorSpd[i] = float(data[i][1])
            self.fst_vt.wnd_wind.WindDir[i] = float(data[i][2])
            self.fst_vt.wnd_wind.VerSpd[i] = float(data[i][3])
            self.fst_vt.wnd_wind.HorShr[i] = float(data[i][4])
            self.fst_vt.wnd_wind.VerShr[i] = float(data[i][5])
            self.fst_vt.wnd_wind.LnVShr[i] = float(data[i][6])
            self.fst_vt.wnd_wind.GstSpd[i] = float(data[i][7])

        f.close()

if __name__=="__main__":
    path = "this\\was\\a\\windows\\path"
    new = fix_path(path)
    print "path, newpath", path, new
    path = "this/was/a/linux/path"
    new = fix_path(path)
    print "path, newpath", path, new

