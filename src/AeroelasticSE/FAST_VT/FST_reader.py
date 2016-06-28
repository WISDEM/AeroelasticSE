
# from openmdao.main.api import VariableTree, Container, Component
# from openmdao.lib.datatypes.api import Int, Str, Float, List, Array, Enum, Bool, VarTree, Dict
import os,re

from FST_vartrees import FstModel, ADAirfoil, ADAirfoilPolar

def fix_path(name):
    """ split a path, then reconstruct it using os.path.join """
    name = re.split("\\\|/", name)
    new = name[0]
    for i in range(1,len(name)):
        new = os.path.join(new, name[i])
    return new

class FstInputBase(object):

    model_name = 'FAST Model'

class FstInputReader(FstInputBase):

    fst_infile = ''   #Master FAST file
    fst_directory = ''   #Directory of master FAST file set
    fst_file_type = 0   #Enum(0, (0,1), desc='Fst file type, 0=old FAST, 1 = new FAST')    
    ad_file_type = 0   #Enum(0, (0,1), desc='Aerodyn file type, 0=old Aerodyn, 1 = new Aerdyn')

    fst_vt = FstModel()

    def __init__(self):
        super(FstInputReader, self).__init__()
    
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
            self.fst_vt.Echo = False
        else:
            self.fst_vt.Echo = True
        ap = f.readline().split()[0]
        if ap == '1':
            self.fst_vt.ADAMSPrep = 1
        elif ap == '2':
            self.fst_vt.ADAMSPrep = 2
        else:
            self.fst_vt.ADAMSPrep = 3
        am = f.readline().split()[0]
        if am == '1':
            self.fst_vt.AnalMode = 1
        else:
            self.fst_vt.AnalMode = 2
        self.fst_vt.NumBl = int(f.readline().split()[0])
        self.fst_vt.TMax = float(f.readline().split()[0])
        self.fst_vt.DT  = float(f.readline().split()[0])
        f.readline()
        ym = f.readline().split()[0]
        if ym == '0':
            self.fst_vt.YCMode = 0
        elif ym == '1':
            self.fst_vt.YCMode = 1
        else:
            self.fst_vt.YCMode = 2
        self.fst_vt.TYCOn = float(f.readline().split()[0])
        pm = f.readline().split()[0]
        if pm == '0':
            self.fst_vt.PCMode = 0
        elif pm == '1':
            self.fst_vt.PCMode = 1
        else:
            self.fst_vt.PCMode = 2
        self.fst_vt.TPCOn = float(f.readline().split()[0])
        vs = f.readline().split()[0]
        if vs == '0':
            self.fst_vt.VSContrl = 0
        elif vs == '1':
            self.fst_vt.VSContrl = 1
        elif vs == '2':
            self.fst_vt.VSContrl = 2
        else:
            self.fst_vt.VSContrl = 3
        self.fst_vt.VS_RtGnSp  = float(f.readline().split()[0])
        self.fst_vt.VS_RtTq  = float(f.readline().split()[0])
        self.fst_vt.VS_Rgn2K  = float(f.readline().split()[0])
        self.fst_vt.VS_SlPc  = float(f.readline().split()[0])
        gm = f.readline().split()[0]
        if gm == '1':
            self.fst_vt.GenModel = 1
        elif gm == '2':
            self.fst_vt.GenModel = 2
        else:
            self.fst_vt.GenModel = 3
        self.fst_vt.GenTiStr = bool(f.readline().split()[0])
        self.fst_vt.GenTiStp = bool(f.readline().split()[0])
        self.fst_vt.SpdGenOn = float(f.readline().split()[0])
        self.fst_vt.TimGenOn = float(f.readline().split()[0])
        self.fst_vt.TimGenOf = float(f.readline().split()[0])
        hss = f.readline().split()[0]
        if hss == '1':
            self.fst_vt.HSSBrMode = 1
        else:
            self.fst_vt.HSSBrMode = 2
        self.fst_vt.THSSBrDp = float(f.readline().split()[0])
        self.fst_vt.TiDynBrk = float(f.readline().split()[0])
        self.fst_vt.TTpBrDp1 = float(f.readline().split()[0])
        self.fst_vt.TTpBrDp2 = float(f.readline().split()[0])
        self.fst_vt.TTpBrDp3 = float(f.readline().split()[0])
        self.fst_vt.TBDepISp1 = float(f.readline().split()[0])
        self.fst_vt.TBDepISp2 = float(f.readline().split()[0])
        self.fst_vt.TBDepISp3 = float(f.readline().split()[0])
        self.fst_vt.TYawManS = float(f.readline().split()[0])
        self.fst_vt.TYawManE = float(f.readline().split()[0])
        self.fst_vt.NacYawF = float(f.readline().split()[0])
        self.fst_vt.TPitManS1 = float(f.readline().split()[0])
        self.fst_vt.TPitManS2 = float(f.readline().split()[0])
        self.fst_vt.TPitManS3 = float(f.readline().split()[0])
        self.fst_vt.TPitManE1 = float(f.readline().split()[0])
        self.fst_vt.TPitManE2 = float(f.readline().split()[0])
        self.fst_vt.TPitManE3 = float(f.readline().split()[0])
        self.fst_vt.BlPitch1  = float(f.readline().split()[0])
        self.fst_vt.BlPitch2  = float(f.readline().split()[0])
        self.fst_vt.BlPitch3  = float(f.readline().split()[0])
        self.fst_vt.B1PitchF1 = float(f.readline().split()[0])
        self.fst_vt.B1PitchF2 = float(f.readline().split()[0])
        self.fst_vt.B1PitchF3 = float(f.readline().split()[0])
        f.readline()
        self.fst_vt.Gravity = float(f.readline().split()[0])
        f.readline()
        boolflag = f.readline().split()[0]
        if boolflag == 'False':
            self.fst_vt.FlapDOF1 = False
        else:
            self.fst_vt.FlapDOF1 = True
        boolflag = f.readline().split()[0]
        if boolflag == 'False':
            self.fst_vt.FlapDOF2 = False
        else:
            self.fst_vt.FlapDOF2 = True
        boolflag = f.readline().split()[0]
        if boolflag == 'False':
            self.fst_vt.EdgeDOF = False
        else:
            self.fst_vt.EdgeDOF = True
        boolflag = f.readline().split()[0]
        if boolflag == 'False':
            self.fst_vt.TeetDOF = False
        else:
            self.fst_vt.TeetDOF = True
        boolflag = f.readline().split()[0]
        if boolflag == 'False':
            self.fst_vt.DrTrDOF = False
        else:
            self.fst_vt.DrTrDOF = True
        boolflag = f.readline().split()[0]
        if boolflag == 'False':
            self.fst_vt.GenDOF = False
        else:
            self.fst_vt.GenDOF = True
        boolflag = f.readline().split()[0]
        if boolflag == 'False':
            self.fst_vt.YawDOF = False
        else:
            self.fst_vt.YawDOF = True
        boolflag = f.readline().split()[0]
        if boolflag == 'False':
            self.fst_vt.TwFADOF1 = False
        else:
            self.fst_vt.TwFADOF1 = True
        boolflag = f.readline().split()[0]
        if boolflag == 'False':
            self.fst_vt.TwFADOF2 = False
        else:
            self.fst_vt.TwFADOF2 = True
        boolflag = f.readline().split()[0]
        if boolflag == 'False':
            self.fst_vt.TwSSDOF1 = False
        else:
            self.fst_vt.TwSSDOF1 = True
        boolflag = f.readline().split()[0]
        if boolflag == 'False':
            self.fst_vt.TwSSDOF2 = False
        else:
            self.fst_vt.TwSSDOF2 = True
        boolflag = f.readline().split()[0]
        if boolflag == 'False':
            self.fst_vt.CompAero = False
        else:
            self.fst_vt.CompAero = True
        boolflag = f.readline().split()[0]
        if boolflag == 'False':
            self.fst_vt.CompNoise = False
        else:
            self.fst_vt.CompNoise = True
        f.readline()
        self.fst_vt.OoPDefl = float(f.readline().split()[0])
        self.fst_vt.IPDefl = float(f.readline().split()[0])
        self.fst_vt.TeetDefl = float(f.readline().split()[0])
        self.fst_vt.Azimuth = float(f.readline().split()[0])
        self.fst_vt.RotSpeed = float(f.readline().split()[0])
        self.fst_vt.NacYaw = float(f.readline().split()[0])
        self.fst_vt.TTDspFA = float(f.readline().split()[0])
        self.fst_vt.TTDspSS = float(f.readline().split()[0])
        f.readline()
        self.fst_vt.TipRad = float(f.readline().split()[0])
        self.fst_vt.HubRad = float(f.readline().split()[0])
        self.fst_vt.PSpnElN = int(f.readline().split()[0])
        self.fst_vt.UndSling = float(f.readline().split()[0])
        self.fst_vt.HubCM = float(f.readline().split()[0])
        self.fst_vt.OverHang = float(f.readline().split()[0])
        self.fst_vt.NacCMxn = float(f.readline().split()[0])
        self.fst_vt.NacCMyn = float(f.readline().split()[0])
        self.fst_vt.NacCMzn = float(f.readline().split()[0])
        self.fst_vt.TowerHt = float(f.readline().split()[0])
        self.fst_vt.Twr2Shft = float(f.readline().split()[0])
        self.fst_vt.TwrRBHt = float(f.readline().split()[0])
        self.fst_vt.ShftTilt = float(f.readline().split()[0])
        self.fst_vt.Delta3 = float(f.readline().split()[0])
        self.fst_vt.PreCone1 = float(f.readline().split()[0])
        self.fst_vt.PreCone2 = float(f.readline().split()[0])
        self.fst_vt.PreCone3 = float(f.readline().split()[0])
        self.fst_vt.AzimB1Up = float(f.readline().split()[0])
        f.readline()
        self.fst_vt.YawBrMass = float(f.readline().split()[0])
        self.fst_vt.NacMass = float(f.readline().split()[0])
        self.fst_vt.HubMass = float(f.readline().split()[0])
        self.fst_vt.TipMass1 = float(f.readline().split()[0])
        self.fst_vt.TipMass2 = float(f.readline().split()[0])
        self.fst_vt.TipMass3 = float(f.readline().split()[0])
        self.fst_vt.NacYIner = float(f.readline().split()[0])
        self.fst_vt.GenIner = float(f.readline().split()[0])
        self.fst_vt.HubIner = float(f.readline().split()[0])
        f.readline()
        self.fst_vt.GBoxEff = float(f.readline().split()[0])
        self.fst_vt.GenEff = float(f.readline().split()[0])
        self.fst_vt.GBRatio = float(f.readline().split()[0])
        boolflag = f.readline().split()[0]
        if boolflag == 'False':
            self.fst_vt.GBRevers = False
        else:
            self.fst_vt.GBRevers = True
        self.fst_vt.HSSBrTqF = float(f.readline().split()[0])
        self.fst_vt.HSSBrDT = float(f.readline().split()[0])
        self.fst_vt.DynBrkFi = f.readline().split()[0]
        self.fst_vt.DTTorSpr = float(f.readline().split()[0])
        self.fst_vt.DTTorDmp = float(f.readline().split()[0])
        f.readline()
        self.fst_vt.SIG_SlPc = float(f.readline().split()[0])
        self.fst_vt.SIG_SySp = float(f.readline().split()[0])
        self.fst_vt.SIG_RtTq = float(f.readline().split()[0])
        self.fst_vt.SIG_PORt = float(f.readline().split()[0])
        f.readline()
        self.fst_vt.TEC_Freq = float(f.readline().split()[0])
        self.fst_vt.TEC_NPol = int(f.readline().split()[0])
        self.fst_vt.TEC_SRes = float(f.readline().split()[0])
        self.fst_vt.TEC_RRes = float(f.readline().split()[0])
        self.fst_vt.TEC_VLL = float(f.readline().split()[0])
        self.fst_vt.TEC_SLR = float(f.readline().split()[0])
        self.fst_vt.TEC_RLR = float(f.readline().split()[0])
        self.fst_vt.TEC_MR = float(f.readline().split()[0])
        f.readline()
        pm = f.readline().split()[0]
        if pm == '0':
            self.fst_vt.PtfmModel = 0
        elif pm == '1':
            self.fst_vt.PtfmModel = 1
        elif pm == '2':
            self.fst_vt.PtfmModel = 2
        else:
            self.fst_vt.PtfmModel = 3
        self.fst_vt.PtfmFile = f.readline().split()[0][1:-1]
        f.readline()
        self.fst_vt.TwrNodes = int(f.readline().split()[0])
        self.fst_vt.TwrFile = f.readline().split()[0][1:-1]
        f.readline()
        self.fst_vt.YawSpr = float(f.readline().split()[0])
        self.fst_vt.YawDamp = float(f.readline().split()[0])
        self.fst_vt.YawNeut = float(f.readline().split()[0])
        f.readline()
        boolflag = f.readline().split()[0]
        if boolflag == 'False':
            self.fst_vt.Furling = False
        else:
            self.fst_vt.Furling = True
        self.fst_vt.FurlFile = f.readline().split()[0]
        f.readline() 
        tm = f.readline().split()[0]
        if tm == '0':
            self.fst_vt.TeetMod = 0
        elif tm == '1':
            self.fst_vt.TeetMod = 1
        else:
            self.fst_vt.TeetMod = 2
        self.fst_vt.TeetDmpP = float(f.readline().split()[0])
        self.fst_vt.TeetDmp = float(f.readline().split()[0])
        self.fst_vt.TeetCDmp = float(f.readline().split()[0])
        self.fst_vt.TeetSStP = float(f.readline().split()[0])
        self.fst_vt.TeetHStP = float(f.readline().split()[0])
        self.fst_vt.TeetSSSp = float(f.readline().split()[0])
        self.fst_vt.TeetHSSp = float(f.readline().split()[0])
        f.readline()
        self.fst_vt.TBDrConN = float(f.readline().split()[0])
        self.fst_vt.TBDrConD = float(f.readline().split()[0])
        self.fst_vt.TpBrDT = float(f.readline().split()[0])
        f.readline()
        self.fst_vt.BldFile1 = f.readline().split()[0][1:-1] # TODO - different blade files
        self.fst_vt.BldFile2 = f.readline().split()[0][1:-1]
        self.fst_vt.BldFile3 = f.readline().split()[0][1:-1]
        f.readline() 
        self.fst_vt.ADFile = f.readline().split()[0][1:-1]
        f.readline()
        self.fst_vt.NoiseFile = f.readline().split()[0]
        f.readline()
        self.fst_vt.ADAMSFile = f.readline().split()[0]
        f.readline()
        self.fst_vt.LinFile = f.readline().split()[0]
        f.readline()
        boolflag = f.readline().split()[0]
        if boolflag == 'False':
            self.fst_vt.SumPrint = False
        else:
            self.fst_vt.SumPrint = True
        if self.fst_file_type == 0:
            ff = f.readline().split()[0]
            if ff == '1':
                self.fst_vt.OutFileFmt = 1
            else:
                self.fst_vt.OutFileFmt = 2
        boolflag = f.readline().split()[0]
        if boolflag == 'False':
            self.fst_vt.TabDelim = False
        else:
            self.fst_vt.TabDelim = True

        self.fst_vt.OutFmt = f.readline().split()[0]
        self.fst_vt.TStart = float(f.readline().split()[0])
        self.fst_vt.DecFact = int(f.readline().split()[0])
        self.fst_vt.SttsTime = float(f.readline().split()[0])
        self.fst_vt.NcIMUxn = float(f.readline().split()[0])
        self.fst_vt.NcIMUyn = float(f.readline().split()[0])
        self.fst_vt.NcIMUzn = float(f.readline().split()[0])
        self.fst_vt.ShftGagL = float(f.readline().split()[0])
        self.fst_vt.NTwGages = int(f.readline().split()[0])
        twrg = f.readline().split(',')
        for i in range(self.fst_vt.NTwGages):
            self.fst_vt.TwrGagNd.append(twrg[i])
        # self.fst_vt.TwrGagNd[-1] = self.fst_vt.TwrGagNd[-1][0:2]   # [AH] Commented out (also line 5 down), was causing errors. What does this line do?
        self.fst_vt.NBlGages = int(f.readline().split()[0])
        blg = f.readline().split(',')
        for i in range(self.fst_vt.NBlGages):
            self.fst_vt.BldGagNd.append(blg[i])
        # self.fst_vt.BldGagNd[-1] = self.fst_vt.BldGagNd[-1][0:2]
    
        # Outlist (TODO - detailed categorization)
        f.readline()
        data = f.readline()
        while data.split()[0] != 'END':
            channels = data.split('"')
            channel_list = channels[1].split(',')
            for i in range(len(channel_list)):
                channel_list[i] = channel_list[i].replace(' ','')
                if channel_list[i] in self.fst_vt.fst_output_vt.wind_mot_vt.__dict__.keys():
                    self.fst_vt.fst_output_vt.wind_mot_vt.__dict__[channel_list[i]] = True
            for i in range(len(channel_list)):
                channel_list[i] = channel_list[i].replace(' ','')
                if channel_list[i] in self.fst_vt.fst_output_vt.blade_mot_vt.__dict__.keys():
                    self.fst_vt.fst_output_vt.blade_mot_vt.__dict__[channel_list[i]] = True
            for i in range(len(channel_list)):
                channel_list[i] = channel_list[i].replace(' ','')
                if channel_list[i] in self.fst_vt.fst_output_vt.hub_nacelle_mot_vt.__dict__.keys():
                    self.fst_vt.fst_output_vt.hub_nacelle_mot_vt.__dict__[channel_list[i]] = True
            for i in range(len(channel_list)):
                channel_list[i] = channel_list[i].replace(' ','')
                if channel_list[i] in self.fst_vt.fst_output_vt.tower_support_mot_vt.__dict__.keys():
                    self.fst_vt.fst_output_vt.tower_support_mot_vt.__dict__[channel_list[i]] = True
            for i in range(len(channel_list)):
                channel_list[i] = channel_list[i].replace(' ','')
                if channel_list[i] in self.fst_vt.fst_output_vt.wave_mot_vt.__dict__.keys():
                    self.fst_vt.fst_output_vt.wave_mot_vt.__dict__[channel_list[i]] = True
            for i in range(len(channel_list)):
                channel_list[i] = channel_list[i].replace(' ','')
                if channel_list[i] in self.fst_vt.fst_output_vt.blade_loads_vt.__dict__.keys():
                    self.fst_vt.fst_output_vt.blade_loads_vt.__dict__[channel_list[i]] = True
            for i in range(len(channel_list)):
                channel_list[i] = channel_list[i].replace(' ','')
                if channel_list[i] in self.fst_vt.fst_output_vt.hub_nacelle_loads_vt.__dict__.keys():
                    self.fst_vt.fst_output_vt.hub_nacelle_loads_vt.__dict__[channel_list[i]] = True
            for i in range(len(channel_list)):
                channel_list[i] = channel_list[i].replace(' ','')
                if channel_list[i] in self.fst_vt.fst_output_vt.tower_support_loads_vt.__dict__.keys():
                    self.fst_vt.fst_output_vt.tower_support_loads_vt.__dict__[channel_list[i]] = True
            for i in range(len(channel_list)):
                channel_list[i] = channel_list[i].replace(' ','')
                if channel_list[i] in self.fst_vt.fst_output_vt.dof_vt.__dict__.keys():
                    self.fst_vt.fst_output_vt.dof_vt.__dict__[channel_list[i]] = True
            data = f.readline()

        self.AeroReader()
        if self.fst_vt.aero_vt.wind_file_type == 'hh':
            self.SimpleWindReader()
        else:
            print "TODO: not simple wind file"
        self.BladeReader()
        self.TowerReader()
        if self.fst_vt.PtfmFile != 'unused':
            self.PlatformReader()
    
    def PlatformReader(self):

        platform_file = os.path.join(self.fst_directory, self.fst_vt.PtfmFile)
        f = open(platform_file)

        f.readline()
        f.readline()
        self.fst_vt.platform_vt.description = f.readline().rstrip()

        # FEATURE FLAGS (CONT)
        f.readline()
        boolflag = f.readline().split()[0]
        if boolflag == 'False':
            self.fst_vt.PtfmSgDOF = False
        else:
            self.fst_vt.PtfmSgDOF = True
        boolflag = f.readline().split()[0]
        if boolflag == 'False':
            self.fst_vt.PtfmSwDOF = False
        else:
            self.fst_vt.PtfmSwDOF = True
        boolflag = f.readline().split()[0]
        if boolflag == 'False':
            self.fst_vt.PtfmHvDOF = False
        else:
            self.fst_vt.PtfmHvDOF = True
        boolflag = f.readline().split()[0]
        if boolflag == 'False':
            self.fst_vt.PtfmRDOF = False
        else:
            self.fst_vt.PtfmRDOF = True
        boolflag = f.readline().split()[0]
        if boolflag == 'False':
            self.fst_vt.PtfmPDOF = False
        else:
            self.fst_vt.PtfmPDOF = True
        boolflag = f.readline().split()[0]
        if boolflag == 'False':
            self.fst_vt.PtfmYDOF = False
        else:
            self.fst_vt.PtfmYDOF = True
        
        # INITIAL CONDITIONS (CONT)
        f.readline()
        self.fst_vt.platform_vt.PtfmSurge = float(f.readline().split()[0])
        self.fst_vt.platform_vt.PtfmSway  = float(f.readline().split()[0])
        self.fst_vt.platform_vt.PtfmHeave = float(f.readline().split()[0])
        self.fst_vt.platform_vt.PtfmRoll  = float(f.readline().split()[0])
        self.fst_vt.platform_vt.PtfmPitch = float(f.readline().split()[0])
        self.fst_vt.platform_vt.PtfmYaw   = float(f.readline().split()[0])
        
        # TURBINE CONFIGURATION (CONT)
        f.readline()
        self.fst_vt.platform_vt.TwrDraft  = float(f.readline().split()[0])
        self.fst_vt.platform_vt.PtfmCM    = float(f.readline().split()[0])
        self.fst_vt.platform_vt.PtfmRef   = float(f.readline().split()[0])
        
        # MASS AND INERTIA (CONT) 
        f.readline()
        self.fst_vt.platform_vt.PtfmMass  = float(f.readline().split()[0])
        self.fst_vt.platform_vt.PtfmRIner = float(f.readline().split()[0])
        self.fst_vt.platform_vt.PtfmPIner = float(f.readline().split()[0])
        self.fst_vt.platform_vt.PtfmYIner = float(f.readline().split()[0])
        
        # PLATFORM (CONT) 
        f.readline()
        pltmd = f.readline().split()[0]
        if pltmd == '0':
            self.fst_vt.platform_vt.PtfmLdMod  = 0
        else:
            self.fst_vt.platform_vt.PtfmLdMod  = 1
        
        # TOWER (CONT) 
        f.readline()
        twrmd = f.readline().split()[0]
        if twrmd == '0':
            self.fst_vt.platform_vt.TwrLdMod  = 0
        elif twrmd == '1':
            self.fst_vt.platform_vt.TwrLdMod  = 1
        elif twrmd == '2':
            self.fst_vt.platform_vt.TwrLdMod  = 3
        self.fst_vt.platform_vt.TwrDiam   = float(f.readline().split()[0])
        self.fst_vt.platform_vt.TwrCA     = float(f.readline().split()[0])
        self.fst_vt.platform_vt.TwrCD     = float(f.readline().split()[0])
        
        # WAVES 
        f.readline()
        self.fst_vt.platform_vt.WtrDens   = float(f.readline().split()[0])
        self.fst_vt.platform_vt.WtrDpth   = float(f.readline().split()[0])
        wavemod = f.readline().split()[0]
        if wavemod == '0':
            self.fst_vt.platform_vt.WaveMod = 0
        elif wavemod == '1':
            self.fst_vt.platform_vt.WaveMod  = 1  
        elif wavemod == '2':
            self.fst_vt.platform_vt.WaveMod = 2
        elif wavemod == '3':
            self.fst_vt.platform_vt.WaveMod  = 3
        else:
            self.fst_vt.platform_vt.WaveMod  = 4
        wavestmod = f.readline().split()[0]
        if wavestmod == '0':
            self.fst_vt.platform_vt.WaveStMod = 0
        elif wavestmod == '1':
            self.fst_vt.platform_vt.WaveStMod = 1
        elif wavestmod == '2':
            self.fst_vt.platform_vt.WaveStMod = 2
        elif wavestmod == '3':
            self.fst_vt.platform_vt.WaveStMod = 3
        self.fst_vt.platform_vt.WaveTMax  = float(f.readline().split()[0])
        self.fst_vt.platform_vt.WaveDT    = float(f.readline().split()[0])
        self.fst_vt.platform_vt.WaveHs    = float(f.readline().split()[0])
        self.fst_vt.platform_vt.WaveTp    = float(f.readline().split()[0])
        wvpk = f.readline().split()[0]
        if wvpk == 'DEFAULT':
            self.fst_vt.platform_vt.WavePkShp = 9999.9
        else:
            self.fst_vt.platform_vt.WavePkShp = float(wvpk)
        self.fst_vt.platform_vt.WaveDir   = float(f.readline().split()[0])
        self.fst_vt.platform_vt.WaveSeed1 = int(f.readline().split()[0])
        self.fst_vt.platform_vt.WaveSeed2 = int(f.readline().split()[0])
        self.fst_vt.platform_vt.GHWvFile  = f.readline().split()[0]
    
        # CURRENT
        f.readline()
        currmod = float(f.readline().split()[0])
        if currmod == '0':
            self.fst_vt.platform_vt.CurrMod   = 0
        elif currmod == '1':
            self.fst_vt.platform_vt.CurrMod   = 1
        elif currmod == '2':
            self.fst_vt.platform_vt.CurrMod   = 2
        self.fst_vt.platform_vt.CurrSSV0  = float(f.readline().split()[0])
        currs = f.readline().split()[0]
        if currs == 'DEFAULT':
            self.fst_vt.platform_vt.CurrSSDir = 9999.9
        else:
            self.fst_vt.platform_vt.CurrSSDir = float(currs)
        self.fst_vt.platform_vt.CurrNSRef = float(f.readline().split()[0])
        self.fst_vt.platform_vt.CurrNSV0  = float(f.readline().split()[0])
        self.fst_vt.platform_vt.CurrNSDir = float(f.readline().split()[0])
        self.fst_vt.platform_vt.CurrDIV   = float(f.readline().split()[0])
        self.fst_vt.platform_vt.CurrDIDir = float(f.readline().split()[0])
    
        # OUTPUT (CONT) 
        f.readline()
        self.fst_vt.platform_vt.NWaveKin = int(f.readline().split()[0])
        if self.fst_vt.platform_vt.NWaveKin != 0:
            self.fst_vt.platform_vt.WaveKinNd = str(f.readline().split()[0])


    def TowerReader(self):

        tower_file = os.path.join(self.fst_directory, self.fst_vt.TwrFile)        
        f = open(tower_file)
        

        f.readline()
        f.readline()
        self.fst_vt.fst_tower_vt.description = f.readline().rstrip()

        # General Tower Paramters
        f.readline()
        self.fst_vt.fst_tower_vt.NTwInptSt = int(f.readline().split()[0])
        boolflag = f.readline().split()[0]
        if boolflag == 'False':
            self.fst_vt.CalcTMode = False
        else:
            self.fst_vt.CalcTMode = True
        self.fst_vt.fst_tower_vt.TwrFADmp1 = float(f.readline().split()[0])
        self.fst_vt.fst_tower_vt.TwrFADmp2 = float(f.readline().split()[0])
        self.fst_vt.fst_tower_vt.TwrSSDmp1 = float(f.readline().split()[0])
        self.fst_vt.fst_tower_vt.TwrSSDmp2 = float(f.readline().split()[0])
    
        # Tower Adjustment Factors
        f.readline()
        self.fst_vt.fst_tower_vt.FAStTunr1 = float(f.readline().split()[0])
        self.fst_vt.fst_tower_vt.FAStTunr2 = float(f.readline().split()[0])
        self.fst_vt.fst_tower_vt.SSStTunr1 = float(f.readline().split()[0])
        self.fst_vt.fst_tower_vt.SSStTunr2 = float(f.readline().split()[0])
        self.fst_vt.fst_tower_vt.AdjTwMa = float(f.readline().split()[0])
        self.fst_vt.fst_tower_vt.AdjFASt = float(f.readline().split()[0])
        self.fst_vt.fst_tower_vt.AdjSSSt = float(f.readline().split()[0])
     
        # Distributed Tower Properties   
        x = f.readline()
        y = f.readline()
        z = f.readline()
        self.fst_vt.fst_tower_vt.HtFract = [None] * self.fst_vt.fst_tower_vt.NTwInptSt
        self.fst_vt.fst_tower_vt.TMassDen = [None] * self.fst_vt.fst_tower_vt.NTwInptSt
        self.fst_vt.fst_tower_vt.TwFAStif = [None] * self.fst_vt.fst_tower_vt.NTwInptSt
        self.fst_vt.fst_tower_vt.TwSSStif = [None] * self.fst_vt.fst_tower_vt.NTwInptSt
        self.fst_vt.fst_tower_vt.TwGJStif = [None] * self.fst_vt.fst_tower_vt.NTwInptSt
        self.fst_vt.fst_tower_vt.TwEAStif = [None] * self.fst_vt.fst_tower_vt.NTwInptSt
        self.fst_vt.fst_tower_vt. TwFAIner = [None] * self.fst_vt.fst_tower_vt.NTwInptSt
        self.fst_vt.fst_tower_vt.TwSSIner = [None] * self.fst_vt.fst_tower_vt.NTwInptSt
        self.fst_vt.fst_tower_vt.TwFAcgOf = [None] * self.fst_vt.fst_tower_vt.NTwInptSt
        self.fst_vt.fst_tower_vt.TwSScgOf = [None] * self.fst_vt.fst_tower_vt.NTwInptSt
        for i in range(self.fst_vt.fst_tower_vt.NTwInptSt):
            data = f.readline().split()
            self.fst_vt.fst_tower_vt.HtFract[i] = float(data[0])
            self.fst_vt.fst_tower_vt.TMassDen[i] = float(data[1])
            self.fst_vt.fst_tower_vt.TwFAStif[i] = float(data[2])
            self.fst_vt.fst_tower_vt.TwSSStif[i] = float(data[3])
            self.fst_vt.fst_tower_vt.TwGJStif[i] = float(data[4])
            self.fst_vt.fst_tower_vt.TwEAStif[i] = float(data[5])
            self.fst_vt.fst_tower_vt. TwFAIner[i] = float(data[6])
            self.fst_vt.fst_tower_vt.TwSSIner[i] = float(data[7])
            self.fst_vt.fst_tower_vt.TwFAcgOf[i] = float(data[8])
            self.fst_vt.fst_tower_vt.TwSScgOf[i] = float(data[9])           
        
        # Tower Mode Shapes
        f.readline()
        self.fst_vt.fst_tower_vt.TwFAM1Sh = [None] * 5
        self.fst_vt.fst_tower_vt.TwFAM2Sh = [None] * 5
        for i in range(5):
            self.fst_vt.fst_tower_vt.TwFAM1Sh[i] = float(f.readline().split()[0])
        for i in range(5):
            self.fst_vt.fst_tower_vt.TwFAM2Sh[i] = float(f.readline().split()[0])        
        f.readline()
        self.fst_vt.fst_tower_vt.TwSSM1Sh = [None] * 5
        self.fst_vt.fst_tower_vt.TwSSM2Sh = [None] * 5          
        for i in range(5):
            self.fst_vt.fst_tower_vt.TwSSM1Sh[i] = float(f.readline().split()[0])
        for i in range(5):
            self.fst_vt.fst_tower_vt.TwSSM2Sh[i] = float(f.readline().split()[0]) 
    
    def BladeReader(self):

        blade_file = os.path.join(self.fst_directory, self.fst_vt.BldFile1)
        f = open(blade_file)
        
        f.readline()
        f.readline()
        self.fst_vt.fst_blade_vt.description = f.readline().rstrip()
        f.readline()
        
        self.fst_vt.fst_blade_vt.NBlInpSt = int(f.readline().split()[0])
        boolflag = f.readline().split()[0]
        if boolflag == 'False':
            self.fst_vt.CalcBMode = False
        else:
            self.fst_vt.CalcBMode = True
        self.fst_vt.fst_blade_vt.BldFlDmp1 = float(f.readline().split()[0])
        self.fst_vt.fst_blade_vt.BldFlDmp2 = float(f.readline().split()[0])
        self.fst_vt.fst_blade_vt.BldEdDmp1 = float(f.readline().split()[0])
        f.readline()
        self.fst_vt.fst_blade_vt.FlStTunr1 = float(f.readline().split()[0])
        self.fst_vt.fst_blade_vt.FlStTunr2 = float(f.readline().split()[0])
        self.fst_vt.fst_blade_vt.AdjBlMs = float(f.readline().split()[0])
        self.fst_vt.fst_blade_vt.AdjFlSt = float(f.readline().split()[0])
        self.fst_vt.fst_blade_vt.AdjEdSt = float(f.readline().split()[0])
        
        f.readline()
        f.readline()
        f.readline()
        self.fst_vt.fst_blade_vt.BlFract = [None] * self.fst_vt.fst_blade_vt.NBlInpSt
        self.fst_vt.fst_blade_vt.AeroCent = [None] * self.fst_vt.fst_blade_vt.NBlInpSt
        self.fst_vt.fst_blade_vt.StrcTwst = [None] * self.fst_vt.fst_blade_vt.NBlInpSt
        self.fst_vt.fst_blade_vt.BMassDen = [None] * self.fst_vt.fst_blade_vt.NBlInpSt
        self.fst_vt.fst_blade_vt.FlpStff = [None] * self.fst_vt.fst_blade_vt.NBlInpSt
        self.fst_vt.fst_blade_vt.EdgStff = [None] * self.fst_vt.fst_blade_vt.NBlInpSt
        self.fst_vt.fst_blade_vt.GJStff = [None] * self.fst_vt.fst_blade_vt.NBlInpSt
        self.fst_vt.fst_blade_vt.EAStff = [None] * self.fst_vt.fst_blade_vt.NBlInpSt
        self.fst_vt.fst_blade_vt.Alpha = [None] * self.fst_vt.fst_blade_vt.NBlInpSt
        self.fst_vt.fst_blade_vt.FlpIner = [None] * self.fst_vt.fst_blade_vt.NBlInpSt
        self.fst_vt.fst_blade_vt.EdgIner = [None] * self.fst_vt.fst_blade_vt.NBlInpSt
        self.fst_vt.fst_blade_vt.PrecrvRef = [None] * self.fst_vt.fst_blade_vt.NBlInpSt
        self.fst_vt.fst_blade_vt.FlpcgOf = [None] * self.fst_vt.fst_blade_vt.NBlInpSt
        self.fst_vt.fst_blade_vt.Edgcgof = [None] * self.fst_vt.fst_blade_vt.NBlInpSt
        self.fst_vt.fst_blade_vt.FlpEAOf = [None] * self.fst_vt.fst_blade_vt.NBlInpSt
        self.fst_vt.fst_blade_vt.EdgEAOf = [None] * self.fst_vt.fst_blade_vt.NBlInpSt
        for i in range(self.fst_vt.fst_blade_vt.NBlInpSt):
            data = f.readline().split()          
            self.fst_vt.fst_blade_vt.BlFract[i] = float(data[0])
            self.fst_vt.fst_blade_vt.AeroCent[i] = float(data[1])
            self.fst_vt.fst_blade_vt.StrcTwst[i] = float(data[2])
            self.fst_vt.fst_blade_vt.BMassDen[i] = float(data[3])
            self.fst_vt.fst_blade_vt.FlpStff[i] = float(data[4])
            self.fst_vt.fst_blade_vt.EdgStff[i] = float(data[5])
            self.fst_vt.fst_blade_vt.GJStff[i] = float(data[6])
            self.fst_vt.fst_blade_vt.EAStff[i] = float(data[7])
            self.fst_vt.fst_blade_vt.Alpha[i] = float(data[8])
            self.fst_vt.fst_blade_vt.FlpIner[i] = float(data[9])
            self.fst_vt.fst_blade_vt.EdgIner[i] = float(data[10])
            self.fst_vt.fst_blade_vt.PrecrvRef[i] = float(data[11])
            self.fst_vt.fst_blade_vt.FlpcgOf[i] = float(data[12])
            self.fst_vt.fst_blade_vt.Edgcgof[i] = float(data[13])
            self.fst_vt.fst_blade_vt.FlpEAOf[i] = float(data[14])
            self.fst_vt.fst_blade_vt.EdgEAOf[i] = float(data[15])
        
        f.readline()
        self.fst_vt.fst_blade_vt.BldFl1Sh = [None] * 5
        self.fst_vt.fst_blade_vt.BldFl2Sh = [None] * 5        
        self.fst_vt.fst_blade_vt.BldEdgSh = [None] * 5
        for i in range(5):
            self.fst_vt.fst_blade_vt.BldFl1Sh[i] = float(f.readline().split()[0])
        for i in range(5):
            self.fst_vt.fst_blade_vt.BldFl2Sh[i] = float(f.readline().split()[0])            
        for i in range(5):
            self.fst_vt.fst_blade_vt.BldEdgSh[i] = float(f.readline().split()[0])        
        

    def AeroReader(self):

        #from airfoil import PolarByRe # only if creating airfoil variable trees

        ad_file = os.path.join(self.fst_directory, self.fst_vt.ADFile)
        f = open(ad_file)

        # skip lines and check if nondimensional
        f.readline()
        self.fst_vt.aero_vt.SysUnits = f.readline().split()[0]
        self.fst_vt.aero_vt.StallMod = f.readline().split()[0]
        self.fst_vt.aero_vt.UseCm = f.readline().split()[0]
        self.fst_vt.aero_vt.InfModel = f.readline().split()[0]
        self.fst_vt.aero_vt.IndModel = f.readline().split()[0]
        self.fst_vt.aero_vt.AToler = float(f.readline().split()[0])
        self.fst_vt.aero_vt.TLModel = f.readline().split()[0]
        self.fst_vt.aero_vt.HLModel = f.readline().split()[0]
        self.fst_vt.aero_vt.WindFile = f.readline().split()[0][1:-1]
        if self.fst_vt.aero_vt.WindFile[-1] == 'h':
            self.fst_vt.aero_vt.wind_file_type = 'hh'
        elif self.fst_vt.aero_vt.WindFile[-1] == 's':
            self.fst_vt.aero_vt.wind_file_type = 'bts'
        else:
            self.fst_vt.aero_vt.wind_file_type = 'wnd'
        self.fst_vt.aero_vt.HH = float(f.readline().split()[0])
        self.fst_vt.aero_vt.TwrShad = float(f.readline().split()[0])
        self.fst_vt.aero_vt.ShadHWid = float(f.readline().split()[0])
        self.fst_vt.aero_vt.T_Shad_Refpt = float(f.readline().split()[0])
        self.fst_vt.aero_vt.AirDens = float(f.readline().split()[0])
        self.fst_vt.aero_vt.KinVisc = float(f.readline().split()[0])
        self.fst_vt.aero_vt.DTAero = float(f.readline().split()[0])

        self.fst_vt.aero_vt.blade_vt.NumFoil = int(f.readline().split()[0])
        self.fst_vt.aero_vt.blade_vt.FoilNm = [None] * self.fst_vt.aero_vt.blade_vt.NumFoil
        for i in range(self.fst_vt.aero_vt.blade_vt.NumFoil):
            af_filename = f.readline().split()[0]
            af_filename = fix_path(af_filename)
            print af_filename
            self.fst_vt.aero_vt.blade_vt.FoilNm[i] = af_filename[1:-1]
        
        self.fst_vt.aero_vt.blade_vt.BldNodes = int(f.readline().split()[0])
        f.readline()
        self.fst_vt.aero_vt.blade_vt.RNodes = [None] * self.fst_vt.aero_vt.blade_vt.BldNodes
        self.fst_vt.aero_vt.blade_vt.AeroTwst = [None] * self.fst_vt.aero_vt.blade_vt.BldNodes
        self.fst_vt.aero_vt.blade_vt.DRNodes = [None] * self.fst_vt.aero_vt.blade_vt.BldNodes
        self.fst_vt.aero_vt.blade_vt.Chord = [None] * self.fst_vt.aero_vt.blade_vt.BldNodes
        self.fst_vt.aero_vt.blade_vt.NFoil = [None] * self.fst_vt.aero_vt.blade_vt.BldNodes
        self.fst_vt.aero_vt.blade_vt.PrnElm = [None] * self.fst_vt.aero_vt.blade_vt.BldNodes       
        for i in range(self.fst_vt.aero_vt.blade_vt.BldNodes):
            data = f.readline().split()
            self.fst_vt.aero_vt.blade_vt.RNodes[i] = float(data[0])
            self.fst_vt.aero_vt.blade_vt.AeroTwst[i] = float(data[1])
            self.fst_vt.aero_vt.blade_vt.DRNodes[i] = float(data[2])
            self.fst_vt.aero_vt.blade_vt.Chord[i] = float(data[3])
            self.fst_vt.aero_vt.blade_vt.NFoil[i] = int(data[4])
            self.fst_vt.aero_vt.blade_vt.PrnElm[i] = data[5]

        f.close()

        # create airfoil objects
        for i in range(self.fst_vt.aero_vt.blade_vt.NumFoil):
             self.fst_vt.aero_vt.blade_vt.af_data.append(self.initFromAerodynFile(os.path.join(self.fst_directory,self.fst_vt.aero_vt.blade_vt.FoilNm[i]), self.ad_file_type))


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
    
    def SimpleWindReader(self):

        #from airfoil import PolarByRe # only if creating airfoil variable trees

        wind_file = os.path.join(self.fst_directory, self.fst_vt.aero_vt.WindFile)
        f = open(wind_file)

        data = []
        while 1:
            line = f.readline()
            if not line:
                break
            line_split = line.split()
            if line_split[0] != '!':
                data.append(line.split())

        self.fst_vt.simple_wind_vt.TimeSteps = len(data)

        self.fst_vt.simple_wind_vt.Time = [None] * len(data)
        self.fst_vt.simple_wind_vt.HorSpd = [None] * len(data)
        self.fst_vt.simple_wind_vt.WindDir = [None] * len(data)
        self.fst_vt.simple_wind_vt.VerSpd = [None] * len(data)
        self.fst_vt.simple_wind_vt.HorShr = [None] * len(data)
        self.fst_vt.simple_wind_vt.VerShr = [None] * len(data)
        self.fst_vt.simple_wind_vt.LnVShr = [None] * len(data)
        self.fst_vt.simple_wind_vt.GstSpd = [None] * len(data)        
        for i in range(len(data)):
            self.fst_vt.simple_wind_vt.Time[i] = float(data[i][0])
            self.fst_vt.simple_wind_vt.HorSpd[i] = float(data[i][1])
            self.fst_vt.simple_wind_vt.WindDir[i] = float(data[i][2])
            self.fst_vt.simple_wind_vt.VerSpd[i] = float(data[i][3])
            self.fst_vt.simple_wind_vt.HorShr[i] = float(data[i][4])
            self.fst_vt.simple_wind_vt.VerShr[i] = float(data[i][5])
            self.fst_vt.simple_wind_vt.LnVShr[i] = float(data[i][6])
            self.fst_vt.simple_wind_vt.GstSpd[i] = float(data[i][7])

        f.close()

if __name__=="__main__":
    path = "this\\was\\a\\windows\\path"
    new = fix_path(path)
    print "path, newpath", path, new
    path = "this/was/a/linux/path"
    new = fix_path(path)
    print "path, newpath", path, new

