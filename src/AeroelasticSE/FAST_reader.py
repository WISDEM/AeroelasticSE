import os, re, sys, copy
import yaml
import numpy as np
from functools import reduce
import operator

from FAST_vars import FstModel


def fix_path(name):
    """ split a path, then reconstruct it using os.path.join """
    name = re.split("\\\|/", name)
    new = name[0]
    for i in range(1,len(name)):
        new = os.path.join(new, name[i])
    return new

def bool_read(text):
    # convert true/false strings to boolean
    if text.lower() == 'true':
        return True
    else:
        return False

def float_read(text):
    # return float with error handing for "default" values
    if 'default' in text.lower():
        return str(text)
    else:
        return float(text)

def int_read(text):
    # return int with error handing for "default" values
    if 'default' in text.lower():
        return str(text)
    else:
        return int(text)

class InputReader_Common(object):
    """ Methods for reading input files that are (relatively) unchanged across FAST versions."""

    def __init__(self, **kwargs):

        self.FAST_ver = 'OPENFAST'
        self.dev_branch = False      # branch: pullrequest/ganesh : 5b78391
        self.FAST_InputFile = None   # FAST input file (ext=.fst)
        self.FAST_directory = None   # Path to fst directory files
        self.fst_vt = FstModel

        # Optional population class attributes from key word arguments
        for k, w in kwargs.iteritems():
            try:
                setattr(self, k, w)
            except:
                pass

        super(InputReader_Common, self).__init__()

    def read_yaml(self):
        f = open(self.FAST_yamlfile, 'r')
        self.fst_vt = yaml.load(f)

    def set_outlist(self, vartree_head, channel_list):
        """ Loop through a list of output channel names, recursively set them to True in the nested outlist dict """

        # given a list of nested dictionary keys, return the dict at that point
        def get_dict(vartree, branch):
            return reduce(operator.getitem, branch, vartree_head)
        # given a list of nested dictionary keys, set the value of the dict at that point
        def set_dict(vartree, branch, val):
            get_dict(vartree, branch[:-1])[branch[-1]] = val
        # recursively loop through outlist dictionaries to set output channels
        def loop_dict(vartree, search_var, branch):
            for var in vartree.keys():
                branch_i = copy.copy(branch)
                branch_i.append(var)
                if type(vartree[var]) is dict:
                    loop_dict(vartree[var], search_var, branch_i)
                else:
                    if var == search_var:
                        set_dict(vartree_head, branch_i, True)

        # loop through outchannels on this line, loop through outlist dicts to set to True
        for var in channel_list:
            var = var.replace(' ', '')
            loop_dict(vartree_head, var, [])

    def read_ElastoDynBlade(self):
        # ElastoDyn v1.00 Blade Input File
        # Currently no differences between FASTv8.16 and OpenFAST.
        if self.FAST_ver.lower() == 'fast7':
            blade_file = os.path.join(self.FAST_directory, self.fst_vt['Fst7']['BldFile1'])
        else:
            blade_file = os.path.join(self.FAST_directory, self.fst_vt['ElastoDyn']['BldFile1'])

        f = open(blade_file)
        # print blade_file
        f.readline()
        f.readline()
        f.readline()
        if self.FAST_ver.lower() == 'fast7':
            f.readline()
        
        # Blade Parameters
        self.fst_vt['ElastoDynBlade']['NBlInpSt'] = int(f.readline().split()[0])
        if self.FAST_ver.lower() == 'fast7':
            self.fst_vt['ElastoDynBlade']['CalcBMode'] = bool_read(f.readline().split()[0])
        self.fst_vt['ElastoDynBlade']['BldFlDmp1'] = float_read(f.readline().split()[0])
        self.fst_vt['ElastoDynBlade']['BldFlDmp2'] = float_read(f.readline().split()[0])
        self.fst_vt['ElastoDynBlade']['BldEdDmp1'] = float_read(f.readline().split()[0])
        
        # Blade Adjustment Factors
        f.readline()
        self.fst_vt['ElastoDynBlade']['FlStTunr1'] = float_read(f.readline().split()[0])
        self.fst_vt['ElastoDynBlade']['FlStTunr2'] = float_read(f.readline().split()[0])
        self.fst_vt['ElastoDynBlade']['AdjBlMs'] = float_read(f.readline().split()[0])
        self.fst_vt['ElastoDynBlade']['AdjFlSt'] = float_read(f.readline().split()[0])
        self.fst_vt['ElastoDynBlade']['AdjEdSt'] = float_read(f.readline().split()[0])
        
        # Distrilbuted Blade Properties
        f.readline()
        f.readline()
        f.readline()
        self.fst_vt['ElastoDynBlade']['BlFract'] = [None] * self.fst_vt['ElastoDynBlade']['NBlInpSt']
        self.fst_vt['ElastoDynBlade']['PitchAxis'] = [None] * self.fst_vt['ElastoDynBlade']['NBlInpSt']
        self.fst_vt['ElastoDynBlade']['StrcTwst'] = [None] * self.fst_vt['ElastoDynBlade']['NBlInpSt']
        self.fst_vt['ElastoDynBlade']['BMassDen'] = [None] * self.fst_vt['ElastoDynBlade']['NBlInpSt']
        self.fst_vt['ElastoDynBlade']['FlpStff'] = [None] * self.fst_vt['ElastoDynBlade']['NBlInpSt']
        self.fst_vt['ElastoDynBlade']['EdgStff'] = [None] * self.fst_vt['ElastoDynBlade']['NBlInpSt']
        if self.FAST_ver.lower() == 'fast7':
            self.fst_vt['ElastoDynBlade']['GJStff'] = [None] * self.fst_vt['ElastoDynBlade']['NBlInpSt']
            self.fst_vt['ElastoDynBlade']['EAStff'] = [None] * self.fst_vt['ElastoDynBlade']['NBlInpSt']
            self.fst_vt['ElastoDynBlade']['Alpha'] = [None] * self.fst_vt['ElastoDynBlade']['NBlInpSt']
            self.fst_vt['ElastoDynBlade']['FlpIner'] = [None] * self.fst_vt['ElastoDynBlade']['NBlInpSt']
            self.fst_vt['ElastoDynBlade']['EdgIner'] = [None] * self.fst_vt['ElastoDynBlade']['NBlInpSt']
            self.fst_vt['ElastoDynBlade']['PrecrvRef'] = [None] * self.fst_vt['ElastoDynBlade']['NBlInpSt']
            self.fst_vt['ElastoDynBlade']['PreswpRef'] = [None] * self.fst_vt['ElastoDynBlade']['NBlInpSt']
            self.fst_vt['ElastoDynBlade']['FlpcgOf'] = [None] * self.fst_vt['ElastoDynBlade']['NBlInpSt']
            self.fst_vt['ElastoDynBlade']['Edgcgof'] = [None] * self.fst_vt['ElastoDynBlade']['NBlInpSt']
            self.fst_vt['ElastoDynBlade']['FlpEAOf'] = [None] * self.fst_vt['ElastoDynBlade']['NBlInpSt']
            self.fst_vt['ElastoDynBlade']['EdgEAOf'] = [None] * self.fst_vt['ElastoDynBlade']['NBlInpSt']
        for i in range(self.fst_vt['ElastoDynBlade']['NBlInpSt']):
            data = f.readline().split()          
            self.fst_vt['ElastoDynBlade']['BlFract'][i]  = float_read(data[0])
            self.fst_vt['ElastoDynBlade']['PitchAxis'][i]  = float_read(data[1])
            self.fst_vt['ElastoDynBlade']['StrcTwst'][i]  = float_read(data[2])
            self.fst_vt['ElastoDynBlade']['BMassDen'][i]  = float_read(data[3])
            self.fst_vt['ElastoDynBlade']['FlpStff'][i]  = float_read(data[4])
            self.fst_vt['ElastoDynBlade']['EdgStff'][i]  = float_read(data[5])
            if self.FAST_ver.lower() == 'fast7':
                self.fst_vt['ElastoDynBlade']['GJStff'][i]  = float_read(data[6])
                self.fst_vt['ElastoDynBlade']['EAStff'][i]  = float_read(data[7])
                self.fst_vt['ElastoDynBlade']['Alpha'][i]  = float_read(data[8])
                self.fst_vt['ElastoDynBlade']['FlpIner'][i]  = float_read(data[9])
                self.fst_vt['ElastoDynBlade']['EdgIner'][i]  = float_read(data[10])
                self.fst_vt['ElastoDynBlade']['PrecrvRef'][i]  = float_read(data[11])
                self.fst_vt['ElastoDynBlade']['PreswpRef'][i]  = float_read(data[12])
                self.fst_vt['ElastoDynBlade']['FlpcgOf'][i]  = float_read(data[13])
                self.fst_vt['ElastoDynBlade']['Edgcgof'][i]  = float_read(data[14])
                self.fst_vt['ElastoDynBlade']['FlpEAOf'][i]  = float_read(data[15])
                self.fst_vt['ElastoDynBlade']['EdgEAOf'][i]  = float_read(data[16])

        f.readline()
        self.fst_vt['ElastoDynBlade']['BldFl1Sh'] = [None] * 5
        self.fst_vt['ElastoDynBlade']['BldFl2Sh'] = [None] * 5        
        self.fst_vt['ElastoDynBlade']['BldEdgSh'] = [None] * 5
        for i in range(5):
            self.fst_vt['ElastoDynBlade']['BldFl1Sh'][i]  = float_read(f.readline().split()[0])
        for i in range(5):
            self.fst_vt['ElastoDynBlade']['BldFl2Sh'][i]  = float_read(f.readline().split()[0])            
        for i in range(5):
            self.fst_vt['ElastoDynBlade']['BldEdgSh'][i]  = float_read(f.readline().split()[0])        

        f.close()

    def read_ElastoDynTower(self):
        # ElastoDyn v1.00 Tower Input Files
        # Currently no differences between FASTv8.16 and OpenFAST.

        if self.FAST_ver.lower() == 'fast7':
            tower_file = os.path.join(self.FAST_directory, self.fst_vt['Fst7']['TwrFile'])
        else:
            tower_file = os.path.join(self.FAST_directory, self.fst_vt['ElastoDyn']['TwrFile'])  
        
        f = open(tower_file)

        f.readline()
        f.readline()
        if self.FAST_ver.lower() == 'fast7':
            f.readline()

        # General Tower Paramters
        f.readline()
        self.fst_vt['ElastoDynTower']['NTwInptSt'] = int(f.readline().split()[0])
        if self.FAST_ver.lower() == 'fast7':
            self.fst_vt['ElastoDynTower']['CalcTMode'] = bool_read(f.readline().split()[0])
        self.fst_vt['ElastoDynTower']['TwrFADmp1'] = float_read(f.readline().split()[0])
        self.fst_vt['ElastoDynTower']['TwrFADmp2'] = float_read(f.readline().split()[0])
        self.fst_vt['ElastoDynTower']['TwrSSDmp1'] = float_read(f.readline().split()[0])
        self.fst_vt['ElastoDynTower']['TwrSSDmp2'] = float_read(f.readline().split()[0])
    
        # Tower Adjustment Factors
        f.readline()
        self.fst_vt['ElastoDynTower']['FAStTunr1'] = float_read(f.readline().split()[0])
        self.fst_vt['ElastoDynTower']['FAStTunr2'] = float_read(f.readline().split()[0])
        self.fst_vt['ElastoDynTower']['SSStTunr1'] = float_read(f.readline().split()[0])
        self.fst_vt['ElastoDynTower']['SSStTunr2'] = float_read(f.readline().split()[0])
        self.fst_vt['ElastoDynTower']['AdjTwMa'] = float_read(f.readline().split()[0])
        self.fst_vt['ElastoDynTower']['AdjFASt'] = float_read(f.readline().split()[0])
        self.fst_vt['ElastoDynTower']['AdjSSSt'] = float_read(f.readline().split()[0])
     
        # Distributed Tower Properties   
        f.readline()
        f.readline()
        f.readline()
        self.fst_vt['ElastoDynTower']['HtFract'] = [None] * self.fst_vt['ElastoDynTower']['NTwInptSt']
        self.fst_vt['ElastoDynTower']['TMassDen'] = [None] * self.fst_vt['ElastoDynTower']['NTwInptSt']
        self.fst_vt['ElastoDynTower']['TwFAStif'] = [None] * self.fst_vt['ElastoDynTower']['NTwInptSt']
        self.fst_vt['ElastoDynTower']['TwSSStif'] = [None] * self.fst_vt['ElastoDynTower']['NTwInptSt']
        if self.FAST_ver.lower() == 'fast7':
            self.fst_vt['ElastoDynTower']['TwGJStif'] = [None] * self.fst_vt['ElastoDynTower']['NTwInptSt']
            self.fst_vt['ElastoDynTower']['TwEAStif'] = [None] * self.fst_vt['ElastoDynTower']['NTwInptSt']
            self.fst_vt['ElastoDynTower']['TwFAIner'] = [None] * self.fst_vt['ElastoDynTower']['NTwInptSt']
            self.fst_vt['ElastoDynTower']['TwSSIner'] = [None] * self.fst_vt['ElastoDynTower']['NTwInptSt']
            self.fst_vt['ElastoDynTower']['TwFAcgOf'] = [None] * self.fst_vt['ElastoDynTower']['NTwInptSt']
            self.fst_vt['ElastoDynTower']['TwSScgOf'] = [None] * self.fst_vt['ElastoDynTower']['NTwInptSt']

        for i in range(self.fst_vt['ElastoDynTower']['NTwInptSt']):
            data = f.readline().split()
            self.fst_vt['ElastoDynTower']['HtFract'][i]  = float_read(data[0])
            self.fst_vt['ElastoDynTower']['TMassDen'][i]  = float_read(data[1])
            self.fst_vt['ElastoDynTower']['TwFAStif'][i]  = float_read(data[2])
            self.fst_vt['ElastoDynTower']['TwSSStif'][i]  = float_read(data[3])
            if self.FAST_ver.lower() == 'fast7':
                self.fst_vt['ElastoDynTower']['TwGJStif'][i]  = float_read(data[4])
                self.fst_vt['ElastoDynTower']['TwEAStif'][i]  = float_read(data[5])
                self.fst_vt['ElastoDynTower']['TwFAIner'][i]  = float_read(data[6])
                self.fst_vt['ElastoDynTower']['TwSSIner'][i]  = float_read(data[7])
                self.fst_vt['ElastoDynTower']['TwFAcgOf'][i]  = float_read(data[8])
                self.fst_vt['ElastoDynTower']['TwSScgOf'][i]  = float_read(data[9])           
        
        # Tower Mode Shapes
        f.readline()
        self.fst_vt['ElastoDynTower']['TwFAM1Sh'] = [None] * 5
        self.fst_vt['ElastoDynTower']['TwFAM2Sh'] = [None] * 5
        for i in range(5):
            self.fst_vt['ElastoDynTower']['TwFAM1Sh'][i]  = float_read(f.readline().split()[0])
        for i in range(5):
            self.fst_vt['ElastoDynTower']['TwFAM2Sh'][i]  = float_read(f.readline().split()[0])        
        f.readline()
        self.fst_vt['ElastoDynTower']['TwSSM1Sh'] = [None] * 5
        self.fst_vt['ElastoDynTower']['TwSSM2Sh'] = [None] * 5          
        for i in range(5):
            self.fst_vt['ElastoDynTower']['TwSSM1Sh'][i]  = float_read(f.readline().split()[0])
        for i in range(5):
            self.fst_vt['ElastoDynTower']['TwSSM2Sh'][i]  = float_read(f.readline().split()[0]) 

        f.close()

    def read_AeroDyn14Polar(self, aerodynFile):
        # AeroDyn v14 Airfoil Polar Input File

        # open aerodyn file
        f = open(aerodynFile, 'r')
                
        airfoil = copy.copy(self.fst_vt['AeroDynPolar'])

        # skip through header
        airfoil['description'] = f.readline().rstrip()  # remove newline
        f.readline()
        airfoil['number_tables'] = int(f.readline().split()[0])

        IDParam = [float_read(val) for val in f.readline().split()[0:airfoil['number_tables']]]
        StallAngle = [float_read(val) for val in f.readline().split()[0:airfoil['number_tables']]]
        f.readline()
        f.readline()
        f.readline()
        ZeroCn = [float_read(val) for val in f.readline().split()[0:airfoil['number_tables']]]
        CnSlope = [float_read(val) for val in f.readline().split()[0:airfoil['number_tables']]]
        CnPosStall = [float_read(val) for val in f.readline().split()[0:airfoil['number_tables']]]
        CnNegStall = [float_read(val) for val in f.readline().split()[0:airfoil['number_tables']]]
        alphaCdMin = [float_read(val) for val in f.readline().split()[0:airfoil['number_tables']]]
        CdMin = [float_read(val) for val in f.readline().split()[0:airfoil['number_tables']]]

        data = []
        airfoil['af_tables'] = []
        while True:
            line = f.readline()
            if 'EOT' in line:
                break
            line = [float_read(s) for s in line.split()]
            if len(line) < 1:
                break
            data.append(line)

        # loop through tables
        for i in range(airfoil['number_tables']):
            polar = {}
            polar['IDParam'] = IDParam[i]
            polar['StallAngle'] = StallAngle[i]
            polar['ZeroCn'] = ZeroCn[i]
            polar['CnSlope'] = CnSlope[i]
            polar['CnPosStall'] = CnPosStall[i]
            polar['CnNegStall'] = CnNegStall[i]
            polar['alphaCdMin'] = alphaCdMin[i]
            polar['CdMin'] = CdMin[i]

            alpha = []
            cl = []
            cd = []
            cm = []
            # read polar information line by line
            for datai in data:
                if len(datai) == airfoil['number_tables']*3+1:
                    alpha.append(datai[0])
                    cl.append(datai[1 + 3*i])
                    cd.append(datai[2 + 3*i])
                    cm.append(datai[3 + 3*i])
                elif len(datai) == airfoil['number_tables']*2+1:
                    alpha.append(datai[0])
                    cl.append(datai[1 + 2*i])
                    cd.append(datai[2 + 2*i])

            polar['alpha'] = alpha
            polar['cl'] = cl
            polar['cd'] = cd
            polar['cm'] = cm
            airfoil['af_tables'].append(polar)

        f.close()

        return airfoil

    # def WndWindReader(self, wndfile):
    #     # .Wnd Wind Input File for Inflow
    #     wind_file = os.path.join(self.FAST_directory, wndfile)
    #     f = open(wind_file)

    #     data = []
    #     while 1:
    #         line = f.readline()
    #         if not line:
    #             break
    #         if line.strip().split()[0] != '!' and line[0] != '!':
    #             data.append(line.split())

    #     self.fst_vt['wnd_wind']['TimeSteps'] = len(data)
    #     self.fst_vt['wnd_wind']['Time'] = [None] * len(data)
    #     self.fst_vt['wnd_wind']['HorSpd'] = [None] * len(data)
    #     self.fst_vt['wnd_wind']['WindDir'] = [None] * len(data)
    #     self.fst_vt['wnd_wind']['VerSpd'] = [None] * len(data)
    #     self.fst_vt['wnd_wind']['HorShr'] = [None] * len(data)
    #     self.fst_vt['wnd_wind']['VerShr'] = [None] * len(data)
    #     self.fst_vt['wnd_wind']['LnVShr'] = [None] * len(data)
    #     self.fst_vt['wnd_wind']['GstSpd'] = [None] * len(data)        
    #     for i in range(len(data)):
    #         self.fst_vt['wnd_wind']['Time'][i]  = float_read(data[i][0])
    #         self.fst_vt['wnd_wind']['HorSpd'][i]  = float_read(data[i][1])
    #         self.fst_vt['wnd_wind']['WindDir'][i]  = float_read(data[i][2])
    #         self.fst_vt['wnd_wind']['VerSpd'][i]  = float_read(data[i][3])
    #         self.fst_vt['wnd_wind']['HorShr'][i]  = float_read(data[i][4])
    #         self.fst_vt['wnd_wind']['VerShr'][i]  = float_read(data[i][5])
    #         self.fst_vt['wnd_wind']['LnVShr'][i]  = float_read(data[i][6])
    #         self.fst_vt['wnd_wind']['GstSpd'][i]  = float_read(data[i][7])

    #     f.close()


class InputReader_OpenFAST(InputReader_Common):
    """ OpenFAST / FAST 8.16 input file reader """
    
    def execute(self):
    	  
    	self.read_MainInput()
        self.read_ElastoDyn()
        self.read_ElastoDynBlade()
        self.read_ElastoDynTower()
        self.read_InflowWind()
        # if file_wind.split('.')[1] == 'wnd':
        #     self.WndWindReader(file_wind)
        # else:
        #     print 'Wind reader for file type .%s not implemented yet.' % file_wind.split('.')[1]
        # AeroDyn version selection
        if self.fst_vt['Fst']['CompAero'] == 1:
            self.read_AeroDyn14()
        elif self.fst_vt['Fst']['CompAero'] == 2:
            self.read_AeroDyn15()
        self.read_ServoDyn()

    def read_MainInput(self):
        # Main FAST v8.16-v8.17 Input File
        # Currently no differences between FASTv8.16 and OpenFAST.

        fst_file = os.path.join(self.FAST_directory, self.FAST_InputFile)
        f = open(fst_file)

        # Header of .fst file
        f.readline()
        self.fst_vt['description'] = f.readline().rstrip()

        # Simulation Control (fst_sim_ctrl)
        f.readline()
        self.fst_vt['Fst']['Echo'] = bool_read(f.readline().split()[0])
        self.fst_vt['Fst']['AbortLevel'] = f.readline().split()[0][1:-1]
        self.fst_vt['Fst']['TMax'] = float_read(f.readline().split()[0])
        self.fst_vt['Fst']['DT']  = float_read(f.readline().split()[0])
        self.fst_vt['Fst']['InterpOrder']  = int(f.readline().split()[0])
        self.fst_vt['Fst']['NumCrctn']  = int(f.readline().split()[0])
        self.fst_vt['Fst']['DT_UJac']  = float_read(f.readline().split()[0])
        self.fst_vt['Fst']['UJacSclFact']  = float_read(f.readline().split()[0])

        # Feature Switches and Flags (ftr_swtchs_flgs)
        f.readline()
        self.fst_vt['Fst']['CompElast'] = int(f.readline().split()[0])
        self.fst_vt['Fst']['CompInflow'] = int(f.readline().split()[0])
        self.fst_vt['Fst']['CompAero'] = int(f.readline().split()[0])
        self.fst_vt['Fst']['CompServo'] = int(f.readline().split()[0])
        self.fst_vt['Fst']['CompHydro'] = int(f.readline().split()[0])
        self.fst_vt['Fst']['CompSub'] = int(f.readline().split()[0])
        self.fst_vt['Fst']['CompMooring'] = int(f.readline().split()[0])
        self.fst_vt['Fst']['CompIce'] = int(f.readline().split()[0])

        # Input Files (input_files)
        f.readline()
        self.fst_vt['Fst']['EDFile'] = f.readline().split()[0][1:-1]
        self.fst_vt['Fst']['BDBldFile1'] = f.readline().split()[0][1:-1]
        self.fst_vt['Fst']['BDBldFile2'] = f.readline().split()[0][1:-1]
        self.fst_vt['Fst']['BDBldFile3'] = f.readline().split()[0][1:-1]
        self.fst_vt['Fst']['InflowFile'] = f.readline().split()[0][1:-1]
        self.fst_vt['Fst']['AeroFile'] = f.readline().split()[0][1:-1]
        self.fst_vt['Fst']['ServoFile'] = f.readline().split()[0][1:-1]
        self.fst_vt['Fst']['HydroFile'] = f.readline().split()[0][1:-1]
        self.fst_vt['Fst']['SubFile'] = f.readline().split()[0][1:-1]
        self.fst_vt['Fst']['MooringFile'] = f.readline().split()[0][1:-1]
        self.fst_vt['Fst']['IceFile'] = f.readline().split()[0][1:-1]

        # FAST Output Parameters (fst_output_params)
        f.readline()
        self.fst_vt['Fst']['SumPrint'] = bool_read(f.readline().split()[0])
        self.fst_vt['Fst']['SttsTime'] = float_read(f.readline().split()[0])
        self.fst_vt['Fst']['ChkptTime'] = float_read(f.readline().split()[0])
        self.fst_vt['Fst']['DT_Out'] = float_read(f.readline().split()[0])
        self.fst_vt['Fst']['TStart'] = float_read(f.readline().split()[0])
        self.fst_vt['Fst']['OutFileFmt'] = int(f.readline().split()[0])
        self.fst_vt['Fst']['TabDelim'] = bool_read(f.readline().split()[0])
        self.fst_vt['Fst']['OutFmt'] = f.readline().split()[0][1:-1]

        # Fst
        f.readline()
        self.fst_vt['Fst']['linearize'] = f.readline().split()[0]
        self.fst_vt['Fst']['NLinTimes'] = f.readline().split()[0]
        self.fst_vt['Fst']['LinTimes'] = re.findall(r'[^,\s]+', f.readline())[0:2]
        self.fst_vt['Fst']['LinInputs'] = f.readline().split()[0]
        self.fst_vt['Fst']['LinOutputs'] = f.readline().split()[0]
        self.fst_vt['Fst']['LinOutJac'] = f.readline().split()[0]
        self.fst_vt['Fst']['LinOutMod'] = f.readline().split()[0]

        # Visualization ()
        f.readline()
        self.fst_vt['Fst']['WrVTK'] = int(f.readline().split()[0])
        self.fst_vt['Fst']['VTK_type'] = int(f.readline().split()[0])
        self.fst_vt['Fst']['VTK_fields'] = bool_read(f.readline().split()[0])
        self.fst_vt['Fst']['VTK_fps'] = float_read(f.readline().split()[0])

    def read_ElastoDyn(self):
        # ElastoDyn v1.03 Input File
        # Currently no differences between FASTv8.16 and OpenFAST.

        ed_file = os.path.join(self.FAST_directory, self.fst_vt['Fst']['EDFile'])
        f = open(ed_file)

        f.readline()
        f.readline()

        # Simulation Control (ed_sim_ctrl)
        f.readline()
        self.fst_vt['ElastoDyn']['Echo'] = bool_read(f.readline().split()[0])
        self.fst_vt['ElastoDyn']['Method']  = int(f.readline().split()[0])
        self.fst_vt['ElastoDyn']['DT'] = float_read(f.readline().split()[0])

        # Environmental Condition (envir_cond)
        f.readline()
        self.fst_vt['ElastoDyn']['Gravity'] = float_read(f.readline().split()[0])

        # Degrees of Freedom (dof)
        f.readline()
        self.fst_vt['ElastoDyn']['FlapDOF1'] = bool_read(f.readline().split()[0])
        self.fst_vt['ElastoDyn']['FlapDOF2'] = bool_read(f.readline().split()[0])
        self.fst_vt['ElastoDyn']['EdgeDOF'] = bool_read(f.readline().split()[0])
        self.fst_vt['ElastoDyn']['TeetDOF'] = bool_read(f.readline().split()[0])
        self.fst_vt['ElastoDyn']['DrTrDOF'] = bool_read(f.readline().split()[0])
        self.fst_vt['ElastoDyn']['GenDOF'] = bool_read(f.readline().split()[0])
        self.fst_vt['ElastoDyn']['YawDOF'] = bool_read(f.readline().split()[0])
        self.fst_vt['ElastoDyn']['TwFADOF1'] = bool_read(f.readline().split()[0])
        self.fst_vt['ElastoDyn']['TwFADOF2'] = bool_read(f.readline().split()[0])
        self.fst_vt['ElastoDyn']['TwSSDOF1'] = bool_read(f.readline().split()[0])
        self.fst_vt['ElastoDyn']['TwSSDOF2'] = bool_read(f.readline().split()[0])
        self.fst_vt['ElastoDyn']['PtfmSgDOF'] = bool_read(f.readline().split()[0])
        self.fst_vt['ElastoDyn']['PtfmSwDOF'] = bool_read(f.readline().split()[0])
        self.fst_vt['ElastoDyn']['PtfmHvDOF'] = bool_read(f.readline().split()[0])
        self.fst_vt['ElastoDyn']['PtfmRDOF'] = bool_read(f.readline().split()[0])
        self.fst_vt['ElastoDyn']['PtfmPDOF'] = bool_read(f.readline().split()[0])
        self.fst_vt['ElastoDyn']['PtfmYDOF'] = bool_read(f.readline().split()[0])

        # Initial Conditions (init_conds)
        f.readline()
        self.fst_vt['ElastoDyn']['OoPDefl']    = float_read(f.readline().split()[0])
        self.fst_vt['ElastoDyn']['IPDefl']     = float_read(f.readline().split()[0])
        self.fst_vt['ElastoDyn']['BlPitch1']   = float_read(f.readline().split()[0])
        self.fst_vt['ElastoDyn']['BlPitch2']   = float_read(f.readline().split()[0])
        self.fst_vt['ElastoDyn']['BlPitch3']   = float_read(f.readline().split()[0])
        self.fst_vt['ElastoDyn']['TeetDefl']   = float_read(f.readline().split()[0])
        self.fst_vt['ElastoDyn']['Azimuth']    = float_read(f.readline().split()[0])
        self.fst_vt['ElastoDyn']['RotSpeed']   = float_read(f.readline().split()[0])
        self.fst_vt['ElastoDyn']['NacYaw']     = float_read(f.readline().split()[0])
        self.fst_vt['ElastoDyn']['TTDspFA']    = float_read(f.readline().split()[0])
        self.fst_vt['ElastoDyn']['TTDspSS']    = float_read(f.readline().split()[0])
        self.fst_vt['ElastoDyn']['PtfmSurge']  = float_read(f.readline().split()[0])
        self.fst_vt['ElastoDyn']['PtfmSway']   = float_read(f.readline().split()[0])
        self.fst_vt['ElastoDyn']['PtfmHeave']  = float_read(f.readline().split()[0])
        self.fst_vt['ElastoDyn']['PtfmRoll']   = float_read(f.readline().split()[0])
        self.fst_vt['ElastoDyn']['PtfmPitch']  = float_read(f.readline().split()[0])
        self.fst_vt['ElastoDyn']['PtfmYaw']    = float_read(f.readline().split()[0])


        # Turbine Configuration (turb_config)
        f.readline()
        self.fst_vt['ElastoDyn']['NumBl']      = int(f.readline().split()[0])
        self.fst_vt['ElastoDyn']['TipRad']     = float_read(f.readline().split()[0])
        self.fst_vt['ElastoDyn']['HubRad']     = float_read(f.readline().split()[0])
        self.fst_vt['ElastoDyn']['PreCone1']   = float_read(f.readline().split()[0])
        self.fst_vt['ElastoDyn']['PreCone2']   = float_read(f.readline().split()[0])
        self.fst_vt['ElastoDyn']['PreCone3']   = float_read(f.readline().split()[0])
        self.fst_vt['ElastoDyn']['HubCM']      = float_read(f.readline().split()[0])
        self.fst_vt['ElastoDyn']['UndSling']   = float_read(f.readline().split()[0])
        self.fst_vt['ElastoDyn']['Delta3']     = float_read(f.readline().split()[0])
        self.fst_vt['ElastoDyn']['AzimB1Up']   = float_read(f.readline().split()[0])
        self.fst_vt['ElastoDyn']['OverHang']   = float_read(f.readline().split()[0])
        self.fst_vt['ElastoDyn']['ShftGagL']   = float_read(f.readline().split()[0])
        self.fst_vt['ElastoDyn']['ShftTilt']   = float_read(f.readline().split()[0])
        self.fst_vt['ElastoDyn']['NacCMxn']    = float_read(f.readline().split()[0])
        self.fst_vt['ElastoDyn']['NacCMyn']    = float_read(f.readline().split()[0])
        self.fst_vt['ElastoDyn']['NacCMzn']    = float_read(f.readline().split()[0])
        self.fst_vt['ElastoDyn']['NcIMUxn']    = float_read(f.readline().split()[0])
        self.fst_vt['ElastoDyn']['NcIMUyn']    = float_read(f.readline().split()[0])
        self.fst_vt['ElastoDyn']['NcIMUzn']    = float_read(f.readline().split()[0])
        self.fst_vt['ElastoDyn']['Twr2Shft']   = float_read(f.readline().split()[0])
        self.fst_vt['ElastoDyn']['TowerHt']    = float_read(f.readline().split()[0])
        self.fst_vt['ElastoDyn']['TowerBsHt']  = float_read(f.readline().split()[0])
        self.fst_vt['ElastoDyn']['PtfmCMxt']   = float_read(f.readline().split()[0])
        self.fst_vt['ElastoDyn']['PtfmCMyt']   = float_read(f.readline().split()[0])
        self.fst_vt['ElastoDyn']['PtfmCMzt']   = float_read(f.readline().split()[0])
        self.fst_vt['ElastoDyn']['PtfmRefzt']  = float_read(f.readline().split()[0])

        # Mass and Inertia (mass_inertia)
        f.readline()
        self.fst_vt['ElastoDyn']['TipMass1']   = float_read(f.readline().split()[0])
        self.fst_vt['ElastoDyn']['TipMass2']   = float_read(f.readline().split()[0])
        self.fst_vt['ElastoDyn']['TipMass3']   = float_read(f.readline().split()[0])
        self.fst_vt['ElastoDyn']['HubMass']    = float_read(f.readline().split()[0])
        self.fst_vt['ElastoDyn']['HubIner']    = float_read(f.readline().split()[0])
        self.fst_vt['ElastoDyn']['GenIner']    = float_read(f.readline().split()[0])
        self.fst_vt['ElastoDyn']['NacMass']    = float_read(f.readline().split()[0])
        self.fst_vt['ElastoDyn']['NacYIner']   = float_read(f.readline().split()[0])
        self.fst_vt['ElastoDyn']['YawBrMass']  = float_read(f.readline().split()[0])
        self.fst_vt['ElastoDyn']['PtfmMass']   = float_read(f.readline().split()[0])
        self.fst_vt['ElastoDyn']['PtfmRIner']  = float_read(f.readline().split()[0])
        self.fst_vt['ElastoDyn']['PtfmPIner']  = float_read(f.readline().split()[0])
        self.fst_vt['ElastoDyn']['PtfmYIner']  = float_read(f.readline().split()[0])

        # ElastoDyn Blade (blade_struc)
        f.readline()
        self.fst_vt['ElastoDyn']['BldNodes'] = int(f.readline().split()[0])
        self.fst_vt['ElastoDyn']['BldFile1'] = f.readline().split()[0][1:-1]
        self.fst_vt['ElastoDyn']['BldFile2'] = f.readline().split()[0][1:-1]
        self.fst_vt['ElastoDyn']['BldFile3'] = f.readline().split()[0][1:-1]

        # Rotor-Teeter (rotor_teeter)
        f.readline()
        self.fst_vt['ElastoDyn']['TeetMod']  = int(f.readline().split()[0])
        self.fst_vt['ElastoDyn']['TeetDmpP'] = float_read(f.readline().split()[0])
        self.fst_vt['ElastoDyn']['TeetDmp']  = float_read(f.readline().split()[0])
        self.fst_vt['ElastoDyn']['TeetCDmp'] = float_read(f.readline().split()[0])
        self.fst_vt['ElastoDyn']['TeetSStP'] = float_read(f.readline().split()[0])
        self.fst_vt['ElastoDyn']['TeetHStP'] = float_read(f.readline().split()[0])
        self.fst_vt['ElastoDyn']['TeetSSSp'] = float_read(f.readline().split()[0])
        self.fst_vt['ElastoDyn']['TeetHSSp'] = float_read(f.readline().split()[0])

        # Drivetrain (drivetrain)
        f.readline()
        self.fst_vt['ElastoDyn']['GBoxEff']  = float_read(f.readline().split()[0])
        self.fst_vt['ElastoDyn']['GBRatio']  = float_read(f.readline().split()[0])
        self.fst_vt['ElastoDyn']['DTTorSpr'] = float_read(f.readline().split()[0])
        self.fst_vt['ElastoDyn']['DTTorDmp'] = float_read(f.readline().split()[0])

        # Furling (furling)
        f.readline()
        self.fst_vt['ElastoDyn']['Furling'] = bool_read(f.readline().split()[0])
        self.fst_vt['ElastoDyn']['FurlFile'] = f.readline().split()[0][1:-1]

        # Tower (tower)
        f.readline()
        self.fst_vt['ElastoDyn']['TwrNodes'] = int(f.readline().split()[0])
        self.fst_vt['ElastoDyn']['TwrFile'] = f.readline().split()[0][1:-1]

        # ED Output Parameters (ed_out_params)
        f.readline()
        self.fst_vt['ElastoDyn']['SumPrint'] = bool_read(f.readline().split()[0])
        self.fst_vt['ElastoDyn']['OutFile']  = int(f.readline().split()[0])
        self.fst_vt['ElastoDyn']['TabDelim'] = bool_read(f.readline().split()[0])
        self.fst_vt['ElastoDyn']['OutFmt']   = f.readline().split()[0][1:-1]
        self.fst_vt['ElastoDyn']['TStart']   = float_read(f.readline().split()[0])
        self.fst_vt['ElastoDyn']['DecFact']  = int(f.readline().split()[0])
        self.fst_vt['ElastoDyn']['NTwGages'] = int(f.readline().split()[0])
        twrg = f.readline().split(',')
        if self.fst_vt['ElastoDyn']['NTwGages'] != 0: #loop over elements if there are gauges to be added, otherwise assign directly
            for i in range(self.fst_vt['ElastoDyn']['NTwGages']):
                self.fst_vt['ElastoDyn']['TwrGagNd'].append(twrg[i])
            self.fst_vt['ElastoDyn']['TwrGagNd'][-1]  = self.fst_vt['ElastoDyn']['TwrGagNd'][-1][:-1]   #remove last (newline) character
        else:
            self.fst_vt['ElastoDyn']['TwrGagNd'] = twrg
            self.fst_vt['ElastoDyn']['TwrGagNd'][-1]  = self.fst_vt['ElastoDyn']['TwrGagNd'][-1][:-1]
        self.fst_vt['ElastoDyn']['NBlGages'] = int(f.readline().split()[0])
        blg = f.readline().split(',')
        if self.fst_vt['ElastoDyn']['NBlGages'] != 0:
            for i in range(self.fst_vt['ElastoDyn']['NBlGages']):
                self.fst_vt['ElastoDyn']['BldGagNd'].append(blg[i])
            self.fst_vt['ElastoDyn']['BldGagNd'][-1]  = self.fst_vt['ElastoDyn']['BldGagNd'][-1][:-1]
        else:
            self.fst_vt['ElastoDyn']['BldGagNd'] = blg
            self.fst_vt['ElastoDyn']['BldGagNd'][-1]  = self.fst_vt['ElastoDyn']['BldGagNd'][-1][:-1]

        # Loop through output channel lines
        f.readline()
        data = f.readline()
        while data.split()[0] != 'END':
            channels = data.split('"')
            channel_list = channels[1].split(',')
            self.set_outlist(self.fst_vt['outlist']['ElastoDyn'], channel_list)

            data = f.readline()

        f.close()


    def read_InflowWind(self):
        # InflowWind v3.01
        # Currently no differences between FASTv8.16 and OpenFAST.
        inflow_file = os.path.normpath(os.path.join(self.FAST_directory, self.fst_vt['Fst']['InflowFile']))
        f = open(inflow_file)
        
        f.readline()
        f.readline()
        f.readline()

        # Inflow wind header parameters (inflow_wind)
        self.fst_vt['InflowWind']['Echo']           = bool_read(f.readline().split()[0])
        self.fst_vt['InflowWind']['WindType']       = int(f.readline().split()[0])
        self.fst_vt['InflowWind']['PropogationDir'] = float_read(f.readline().split()[0])
        self.fst_vt['InflowWind']['NWindVel']       = int(f.readline().split()[0])
        self.fst_vt['InflowWind']['WindVxiList']    = float_read(f.readline().split()[0])
        self.fst_vt['InflowWind']['WindVyiList']    = float_read(f.readline().split()[0])
        self.fst_vt['InflowWind']['WindVziList']    = float_read(f.readline().split()[0])

        # Parameters for Steady Wind Conditions [used only for WindType = 1] (steady_wind_params)
        f.readline()
        self.fst_vt['InflowWind']['HWindSpeed'] = float_read(f.readline().split()[0])
        self.fst_vt['InflowWind']['RefHt'] = float_read(f.readline().split()[0])
        self.fst_vt['InflowWind']['PLexp'] = float_read(f.readline().split()[0])

        # Parameters for Uniform wind file   [used only for WindType = 2] (uniform_wind_params)
        f.readline()
        self.fst_vt['InflowWind']['Filename'] = os.path.join(os.path.split(inflow_file)[0], f.readline().split()[0][1:-1])
        self.fst_vt['InflowWind']['RefHt'] = float_read(f.readline().split()[0])
        self.fst_vt['InflowWind']['RefLength'] = float_read(f.readline().split()[0])

        # Parameters for Binary TurbSim Full-Field files   [used only for WindType = 3] (turbsim_wind_params)
        f.readline()
        self.fst_vt['InflowWind']['Filename'] = os.path.join(os.path.split(inflow_file)[0], f.readline().split()[0][1:-1])

        # Parameters for Binary Bladed-style Full-Field files   [used only for WindType = 4] (bladed_wind_params)
        f.readline()
        self.fst_vt['InflowWind']['FilenameRoot'] = f.readline().split()[0][1:-1]       
        self.fst_vt['InflowWind']['TowerFile'] = bool_read(f.readline().split()[0])

        # Parameters for HAWC-format binary files  [Only used with WindType = 5] (hawc_wind_params)
        f.readline()
        self.fst_vt['InflowWind']['FileName_u'] = os.path.normpath(os.path.join(os.path.split(inflow_file)[0], f.readline().split()[0][1:-1]))
        self.fst_vt['InflowWind']['FileName_v'] = os.path.normpath(os.path.join(os.path.split(inflow_file)[0], f.readline().split()[0][1:-1]))
        self.fst_vt['InflowWind']['FileName_w'] = os.path.normpath(os.path.join(os.path.split(inflow_file)[0], f.readline().split()[0][1:-1]))
        self.fst_vt['InflowWind']['nx']    = int(f.readline().split()[0])
        self.fst_vt['InflowWind']['ny']    = int(f.readline().split()[0])
        self.fst_vt['InflowWind']['nz']    = int(f.readline().split()[0])
        self.fst_vt['InflowWind']['dx']    = float_read(f.readline().split()[0])
        self.fst_vt['InflowWind']['dy']    = float_read(f.readline().split()[0])
        self.fst_vt['InflowWind']['dz']    = float_read(f.readline().split()[0])
        self.fst_vt['InflowWind']['RefHt'] = float_read(f.readline().split()[0])

        # Scaling parameters for turbulence (still hawc_wind_params)
        f.readline()
        self.fst_vt['InflowWind']['ScaleMethod'] = int(f.readline().split()[0])
        self.fst_vt['InflowWind']['SFx']         = float_read(f.readline().split()[0])
        self.fst_vt['InflowWind']['SFy']         = float_read(f.readline().split()[0])
        self.fst_vt['InflowWind']['SFz']         = float_read(f.readline().split()[0])
        self.fst_vt['InflowWind']['SigmaFx']     = float_read(f.readline().split()[0])
        self.fst_vt['InflowWind']['SigmaFy']     = float_read(f.readline().split()[0])
        self.fst_vt['InflowWind']['SigmaFz']     = float_read(f.readline().split()[0])

        # Mean wind profile parameters (added to HAWC-format files) (still hawc_wind_params)
        f.readline()
        self.fst_vt['InflowWind']['URef']        = float_read(f.readline().split()[0])
        self.fst_vt['InflowWind']['WindProfile'] = int(f.readline().split()[0])
        self.fst_vt['InflowWind']['PLExp']       = float_read(f.readline().split()[0])
        self.fst_vt['InflowWind']['Z0']          = float_read(f.readline().split()[0])

        # Inflow Wind Output Parameters (inflow_out_params)
        f.readline()
        self.fst_vt['InflowWind']['SumPrint'] = bool_read(f.readline().split()[0])
        
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

    def read_AeroDyn14(self):
        # AeroDyn v14.04

        ad_file = os.path.join(self.FAST_directory, self.fst_vt['Fst']['AeroFile'])
        f = open(ad_file)
        # AeroDyn file header (aerodyn)
        f.readline()
        f.readline()
        self.fst_vt['AeroDyn14']['StallMod'] = f.readline().split()[0]
        self.fst_vt['AeroDyn14']['UseCm'] = f.readline().split()[0]
        self.fst_vt['AeroDyn14']['InfModel'] = f.readline().split()[0]
        self.fst_vt['AeroDyn14']['IndModel'] = f.readline().split()[0]
        self.fst_vt['AeroDyn14']['AToler'] = float_read(f.readline().split()[0])
        self.fst_vt['AeroDyn14']['TLModel'] = f.readline().split()[0]
        self.fst_vt['AeroDyn14']['HLModel'] = f.readline().split()[0]
        self.fst_vt['AeroDyn14']['TwrShad'] = f.readline().split()[0]
        self.fst_vt['AeroDyn14']['TwrPotent'] = bool_read(f.readline().split()[0])
        self.fst_vt['AeroDyn14']['TwrShadow'] = bool_read(f.readline().split()[0])
        self.fst_vt['AeroDyn14']['TwrFile'] = f.readline().split()[0].replace('"','').replace("'",'')
        self.fst_vt['AeroDyn14']['CalcTwrAero'] = bool_read(f.readline().split()[0])
        self.fst_vt['AeroDyn14']['AirDens'] = float_read(f.readline().split()[0])
        self.fst_vt['AeroDyn14']['KinVisc'] = float_read(f.readline().split()[0])
        self.fst_vt['AeroDyn14']['DTAero'] = float_read(f.readline().split()[0])

        # AeroDyn Blade Properties (blade_aero)
        self.fst_vt['AeroDyn14']['NumFoil'] = int(f.readline().split()[0])
        self.fst_vt['AeroDyn14']['FoilNm'] = [None] * self.fst_vt['AeroDyn14']['NumFoil']
        for i in range(self.fst_vt['AeroDyn14']['NumFoil']):
            af_filename = f.readline().split()[0]
            af_filename = fix_path(af_filename)
            self.fst_vt['AeroDyn14']['FoilNm'][i]  = af_filename[1:-1]
        
        self.fst_vt['AeroDynBlade']['BldNodes'] = int(f.readline().split()[0])
        f.readline()
        self.fst_vt['AeroDynBlade']['RNodes'] = [None] * self.fst_vt['AeroDynBlade']['BldNodes']
        self.fst_vt['AeroDynBlade']['AeroTwst'] = [None] * self.fst_vt['AeroDynBlade']['BldNodes']
        self.fst_vt['AeroDynBlade']['DRNodes'] = [None] * self.fst_vt['AeroDynBlade']['BldNodes']
        self.fst_vt['AeroDynBlade']['Chord'] = [None] * self.fst_vt['AeroDynBlade']['BldNodes']
        self.fst_vt['AeroDynBlade']['NFoil'] = [None] * self.fst_vt['AeroDynBlade']['BldNodes']
        self.fst_vt['AeroDynBlade']['PrnElm'] = [None] * self.fst_vt['AeroDynBlade']['BldNodes']       
        for i in range(self.fst_vt['AeroDynBlade']['BldNodes']):
            data = f.readline().split()
            self.fst_vt['AeroDynBlade']['RNodes'][i]  = float_read(data[0])
            self.fst_vt['AeroDynBlade']['AeroTwst'][i]  = float_read(data[1])
            self.fst_vt['AeroDynBlade']['DRNodes'][i]  = float_read(data[2])
            self.fst_vt['AeroDynBlade']['Chord'][i]  = float_read(data[3])
            self.fst_vt['AeroDynBlade']['NFoil'][i]  = int(data[4])
            self.fst_vt['AeroDynBlade']['PrnElm'][i]  = data[5]

        f.close()

        # create airfoil objects
        self.fst_vt['AeroDynBlade']['af_data'] = []
        for i in range(self.fst_vt['AeroDynBlade']['NumFoil']):
             self.fst_vt['AeroDynBlade']['af_data'].append(self.read_AeroDyn14Polar(os.path.join(self.FAST_directory,self.fst_vt['AeroDyn14']['FoilNm'][i])))

        # tower
        self.read_AeroDyn14Tower()

    def read_AeroDyn14Tower(self):
        # AeroDyn v14.04 Tower

        ad_tower_file = os.path.join(self.FAST_directory, self.fst_vt['aerodyn']['TwrFile'])
        f = open(ad_tower_file)

        f.readline()
        f.readline()
        self.fst_vt['AeroDynTower']['NTwrHt'] = int(f.readline().split()[0])
        self.fst_vt['AeroDynTower']['NTwrRe'] = int(f.readline().split()[0])
        self.fst_vt['AeroDynTower']['NTwrCD'] = int(f.readline().split()[0])
        self.fst_vt['AeroDynTower']['Tower_Wake_Constant'] = float_read(f.readline().split()[0])
        
        f.readline()
        f.readline()
        self.fst_vt['AeroDynTower']['TwrHtFr'] = [None]*self.fst_vt['AeroDynTower']['NTwrHt']
        self.fst_vt['AeroDynTower']['TwrWid'] = [None]*self.fst_vt['AeroDynTower']['NTwrHt']
        self.fst_vt['AeroDynTower']['NTwrCDCol'] = [None]*self.fst_vt['AeroDynTower']['NTwrHt']
        for i in range(self.fst_vt['AeroDynTower']['NTwrHt']):
            data = [float(val) for val in f.readline().split()]
            self.fst_vt['AeroDynTower']['TwrHtFr'][i]  = data[0] 
            self.fst_vt['AeroDynTower']['TwrWid'][i]  = data[1]
            self.fst_vt['AeroDynTower']['NTwrCDCol'][i]  = data[2]

        f.readline()
        f.readline()
        self.fst_vt['AeroDynTower']['TwrRe'] = [None]*self.fst_vt['AeroDynTower']['NTwrRe']
        self.fst_vt['AeroDynTower']['TwrCD'] = np.zeros((self.fst_vt['AeroDynTower']['NTwrRe'], self.fst_vt['AeroDynTower']['NTwrCD']))
        for i in range(self.fst_vt['AeroDynTower']['NTwrRe']):
            data = [float(val) for val in f.readline().split()]
            self.fst_vt['AeroDynTower']['TwrRe'][i]  = data[0]
            self.fst_vt['AeroDynTower']['TwrCD'][i,:]  = data[1:]


    def read_AeroDyn15(self):
        # AeroDyn v15.03

        ad_file = os.path.join(self.FAST_directory, self.fst_vt['Fst']['AeroFile'])
        f = open(ad_file)

        # General Option
        f.readline()
        f.readline()
        f.readline()
        self.fst_vt['AeroDyn15']['Echo']          = bool_read(f.readline().split()[0])
        self.fst_vt['AeroDyn15']['DTAero']        = float_read(f.readline().split()[0])
        self.fst_vt['AeroDyn15']['WakeMod']       = int(f.readline().split()[0])
        self.fst_vt['AeroDyn15']['AFAeroMod']     = int(f.readline().split()[0])
        self.fst_vt['AeroDyn15']['TwrPotent']     = int(f.readline().split()[0])
        self.fst_vt['AeroDyn15']['TwrShadow']     = bool_read(f.readline().split()[0])
        self.fst_vt['AeroDyn15']['TwrAero']       = bool_read(f.readline().split()[0])
        self.fst_vt['AeroDyn15']['FrozenWake']    = bool_read(f.readline().split()[0])
        if self.FAST_ver.lower() != 'fast8':
                self.fst_vt['AeroDyn15']['CavitCheck']    = bool_read(f.readline().split()[0])

        # Environmental Conditions
        f.readline()
        self.fst_vt['AeroDyn15']['AirDens']        = float_read(f.readline().split()[0])
        self.fst_vt['AeroDyn15']['KinVisc']        = float_read(f.readline().split()[0])
        self.fst_vt['AeroDyn15']['SpdSound']       = float_read(f.readline().split()[0])
        if self.FAST_ver.lower() != 'fast8':
            self.fst_vt['AeroDyn15']['Patm']           = float_read(f.readline().split()[0])
            self.fst_vt['AeroDyn15']['Pvap']           = float_read(f.readline().split()[0])
            self.fst_vt['AeroDyn15']['FluidDepth']     = float_read(f.readline().split()[0])

        # Blade-Element/Momentum Theory Options
        f.readline()
        self.fst_vt['AeroDyn15']['SkewMod']               = int(f.readline().split()[0])
        if self.dev_branch:
            self.fst_vt['AeroDyn15']['SkewModFactor']     = float_read(f.readline().split()[0])
        self.fst_vt['AeroDyn15']['TipLoss']               = bool_read(f.readline().split()[0])
        self.fst_vt['AeroDyn15']['HubLoss']               = bool_read(f.readline().split()[0])
        self.fst_vt['AeroDyn15']['TanInd']                = bool_read(f.readline().split()[0])
        self.fst_vt['AeroDyn15']['AIDrag']                = bool_read(f.readline().split()[0])
        self.fst_vt['AeroDyn15']['TIDrag']                = bool_read(f.readline().split()[0])
        self.fst_vt['AeroDyn15']['IndToler']              = float_read(f.readline().split()[0])
        self.fst_vt['AeroDyn15']['MaxIter']               = int(f.readline().split()[0])

        # Dynamic Blade-Element/Momentum Theory Options 
        if self.dev_branch:
            f.readline()
            self.fst_vt['AeroDyn15']['DBEMT_Mod']          = int(f.readline().split()[0])
            self.fst_vt['AeroDyn15']['tau1_const']         = int(f.readline().split()[0])

        # Beddoes-Leishman Unsteady Airfoil Aerodynamics Options
        f.readline()
        self.fst_vt['AeroDyn15']['UAMod']                  = int(f.readline().split()[0])
        self.fst_vt['AeroDyn15']['FLookup']                = bool_read(f.readline().split()[0])

        # Airfoil Information
        f.readline()
        self.fst_vt['AeroDyn15']['InCol_Alfa']       = int(f.readline().split()[0])
        self.fst_vt['AeroDyn15']['InCol_Cl']         = int(f.readline().split()[0])
        self.fst_vt['AeroDyn15']['InCol_Cd']         = int(f.readline().split()[0])
        self.fst_vt['AeroDyn15']['InCol_Cm']         = int(f.readline().split()[0])
        self.fst_vt['AeroDyn15']['InCol_Cpmin']      = int(f.readline().split()[0])
        self.fst_vt['AeroDyn15']['NumAFfiles']       = int(f.readline().split()[0])
        self.fst_vt['AeroDyn15']['AFNames']          = [None] * self.fst_vt['AeroDyn15']['NumAFfiles']
        for i in range(self.fst_vt['AeroDyn15']['NumAFfiles']):
            af_filename = fix_path(f.readline().split()[0])[1:-1]
            self.fst_vt['AeroDyn15']['AFNames'][i]   = os.path.abspath(os.path.join(self.FAST_directory, af_filename))

        # Rotor/Blade Properties
        f.readline()
        self.fst_vt['AeroDyn15']['UseBlCm']        = bool_read(f.readline().split()[0])
        self.fst_vt['AeroDyn15']['ADBlFile1']      = f.readline().split()[0][1:-1]
        self.fst_vt['AeroDyn15']['ADBlFile2']      = f.readline().split()[0][1:-1]
        self.fst_vt['AeroDyn15']['ADBlFile3']      = f.readline().split()[0][1:-1]

        # Tower Influence and Aerodynamics
        f.readline()
        self.fst_vt['AeroDyn15']['NumTwrNds']      = int(f.readline().split()[0])
        f.readline()
        f.readline()
        self.fst_vt['AeroDyn15']['TwrElev']        = [None]*self.fst_vt['AeroDyn15']['NumTwrNds']
        self.fst_vt['AeroDyn15']['TwrDiam']        = [None]*self.fst_vt['AeroDyn15']['NumTwrNds']
        self.fst_vt['AeroDyn15']['TwrCd']          = [None]*self.fst_vt['AeroDyn15']['NumTwrNds']
        for i in range(self.fst_vt['AeroDyn15']['NumTwrNds']):
            data = [float(val) for val in f.readline().split()]
            self.fst_vt['AeroDyn15']['TwrElev'][i] = data[0] 
            self.fst_vt['AeroDyn15']['TwrDiam'][i] = data[1] 
            self.fst_vt['AeroDyn15']['TwrCd'][i]   = data[2]

        # Outputs
        f.readline()
        self.fst_vt['AeroDyn15']['SumPrint']    = bool_read(f.readline().split()[0])
        self.fst_vt['AeroDyn15']['NBlOuts']     = int(f.readline().split()[0])
        self.fst_vt['AeroDyn15']['BlOutNd']     = [idx.strip() for idx in f.readline().split('BlOutNd')[0].split(',')]
        self.fst_vt['AeroDyn15']['NTwOuts']     = int(f.readline().split()[0])
        self.fst_vt['AeroDyn15']['TwOutNd']     = [idx.strip() for idx in f.readline().split('TwOutNd')[0].split(',')]

        # AeroDyn15 Outlist
        f.readline()
        data = f.readline()
        while data.split()[0] != 'END':
            channels = data.split('"')
            channel_list = channels[1].split(',')
            self.set_outlist(self.fst_vt['outlist']['AeroDyn'], channel_list)
            data = f.readline()

        f.close()

        self.read_AeroDyn15Blade()
        self.read_AeroDyn15Polar()

    def read_AeroDyn15Blade(self):
        # AeroDyn v5.00 Blade Definition File

        ad_blade_file = os.path.join(self.FAST_directory, self.fst_vt['AeroDyn15']['ADBlFile1'])
        f = open(ad_blade_file)

        f.readline()
        f.readline()
        f.readline()
        # Blade Properties
        self.fst_vt['AeroDynBlade']['NumBlNds']       = int(f.readline().split()[0])
        f.readline()
        f.readline()
        self.fst_vt['AeroDynBlade']['BlSpn']          = [None]*self.fst_vt['AeroDynBlade']['NumBlNds']
        self.fst_vt['AeroDynBlade']['BlCrvAC']        = [None]*self.fst_vt['AeroDynBlade']['NumBlNds']
        self.fst_vt['AeroDynBlade']['BlSwpAC']        = [None]*self.fst_vt['AeroDynBlade']['NumBlNds']
        self.fst_vt['AeroDynBlade']['BlCrvAng']       = [None]*self.fst_vt['AeroDynBlade']['NumBlNds']
        self.fst_vt['AeroDynBlade']['BlTwist']        = [None]*self.fst_vt['AeroDynBlade']['NumBlNds']
        self.fst_vt['AeroDynBlade']['BlChord']        = [None]*self.fst_vt['AeroDynBlade']['NumBlNds']
        self.fst_vt['AeroDynBlade']['BlAFID']         = [None]*self.fst_vt['AeroDynBlade']['NumBlNds']
        for i in range(self.fst_vt['AeroDynBlade']['NumBlNds']):
            data = [float(val) for val in f.readline().split()]
            self.fst_vt['AeroDynBlade']['BlSpn'][i]   = data[0] 
            self.fst_vt['AeroDynBlade']['BlCrvAC'][i] = data[1] 
            self.fst_vt['AeroDynBlade']['BlSwpAC'][i] = data[2]
            self.fst_vt['AeroDynBlade']['BlCrvAng'][i]= data[3]
            self.fst_vt['AeroDynBlade']['BlTwist'][i] = data[4]
            self.fst_vt['AeroDynBlade']['BlChord'][i] = data[5]
            self.fst_vt['AeroDynBlade']['BlAFID'][i]  = data[6]


    def read_AeroDyn15Polar(self):
        # AirfoilInfo v1.01

        def readline_filterComments(f):
            read = True
            while read:
                line = f.readline().strip()
                if len(line)>0:
                    if line[0] != '!':
                        read = False
            return line


        self.fst_vt['AeroDyn15']['af_data'] = [None]*self.fst_vt['AeroDyn15']['NumAFfiles']

        for afi, af_filename in enumerate(self.fst_vt['AeroDyn15']['AFNames']):
            f = open(af_filename)
            # print af_filename

            polar = {}

            polar['InterpOrd']      = int_read(readline_filterComments(f).split()[0])
            polar['NonDimArea']     = int_read(readline_filterComments(f).split()[0])
            polar['NumCoords']      = readline_filterComments(f).split()[0]
            polar['NumTabs']        = int_read(readline_filterComments(f).split()[0])
            polar['Re']             = float_read(readline_filterComments(f).split()[0])
            polar['Ctrl']           = int_read(readline_filterComments(f).split()[0])
            polar['InclUAdata']     = bool_read(readline_filterComments(f).split()[0])

            # Unsteady Aero Data
            if polar['InclUAdata']:
                polar['alpha0']     = float_read(readline_filterComments(f).split()[0])
                polar['alpha1']     = float_read(readline_filterComments(f).split()[0])
                polar['alpha2']     = float_read(readline_filterComments(f).split()[0])
                polar['eta_e']      = float_read(readline_filterComments(f).split()[0])
                polar['C_nalpha']   = float_read(readline_filterComments(f).split()[0])
                polar['T_f0']       = float_read(readline_filterComments(f).split()[0])
                polar['T_V0']       = float_read(readline_filterComments(f).split()[0])
                polar['T_p']        = float_read(readline_filterComments(f).split()[0])
                polar['T_VL']       = float_read(readline_filterComments(f).split()[0])
                polar['b1']         = float_read(readline_filterComments(f).split()[0])
                polar['b2']         = float_read(readline_filterComments(f).split()[0])
                polar['b5']         = float_read(readline_filterComments(f).split()[0])
                polar['A1']         = float_read(readline_filterComments(f).split()[0])
                polar['A2']         = float_read(readline_filterComments(f).split()[0])
                polar['A5']         = float_read(readline_filterComments(f).split()[0])
                polar['S1']         = float_read(readline_filterComments(f).split()[0])
                polar['S2']         = float_read(readline_filterComments(f).split()[0])
                polar['S3']         = float_read(readline_filterComments(f).split()[0])
                polar['S4']         = float_read(readline_filterComments(f).split()[0])
                polar['Cn1']        = float_read(readline_filterComments(f).split()[0])
                polar['Cn2']        = float_read(readline_filterComments(f).split()[0])
                polar['St_sh']      = float_read(readline_filterComments(f).split()[0])
                polar['Cd0']        = float_read(readline_filterComments(f).split()[0])
                polar['Cm0']        = float_read(readline_filterComments(f).split()[0])
                polar['k0']         = float_read(readline_filterComments(f).split()[0])
                polar['k1']         = float_read(readline_filterComments(f).split()[0])
                polar['k2']         = float_read(readline_filterComments(f).split()[0])
                polar['k3']         = float_read(readline_filterComments(f).split()[0])
                polar['k1_hat']     = float_read(readline_filterComments(f).split()[0])
                polar['x_cp_bar']   = float_read(readline_filterComments(f).split()[0])
                polar['UACutout']   = float_read(readline_filterComments(f).split()[0])
                polar['filtCutOff'] = float_read(readline_filterComments(f).split()[0])

            # Polar Data
            polar['NumAlf']         = int_read(readline_filterComments(f).split()[0])
            polar['Alpha']          = [None]*polar['NumAlf']
            polar['Cl']             = [None]*polar['NumAlf']
            polar['Cd']             = [None]*polar['NumAlf']
            polar['Cm']             = [None]*polar['NumAlf']
            polar['Cpmin']          = [None]*polar['NumAlf']
            for i in range(polar['NumAlf']):
                data = [float(val) for val in readline_filterComments(f).split()]
                if self.fst_vt['AeroDyn15']['InCol_Alfa'] > 0:
                    polar['Alpha'][i] = data[self.fst_vt['AeroDyn15']['InCol_Alfa']-1]
                if self.fst_vt['AeroDyn15']['InCol_Cl'] > 0:
                    polar['Cl'][i]    = data[self.fst_vt['AeroDyn15']['InCol_Cl']-1]
                if self.fst_vt['AeroDyn15']['InCol_Cd'] > 0:
                    polar['Cd'][i]    = data[self.fst_vt['AeroDyn15']['InCol_Cd']-1]
                if self.fst_vt['AeroDyn15']['InCol_Cm'] > 0:
                    polar['Cm'][i]    = data[self.fst_vt['AeroDyn15']['InCol_Cm']-1]
                if self.fst_vt['AeroDyn15']['InCol_Cpmin'] > 0:
                    polar['Cpmin'][i] = data[self.fst_vt['AeroDyn15']['InCol_Cpmin']-1]

            self.fst_vt['AeroDyn15']['af_data'][afi] = polar


    def read_ServoDyn(self):
        # ServoDyn v1.05 Input File
        # Currently no differences between FASTv8.16 and OpenFAST.


        sd_file = os.path.normpath(os.path.join(self.FAST_directory, self.fst_vt['Fst']['ServoFile']))
        f = open(sd_file)

        f.readline()
        f.readline()

        # Simulation Control (sd_sim_ctrl)
        f.readline()
        self.fst_vt['ServoDyn']['Echo'] = bool_read(f.readline().split()[0])
        self.fst_vt['ServoDyn']['DT'] = float_read(f.readline().split()[0])

        # Pitch Control (pitch_ctrl)
        f.readline()
        self.fst_vt['ServoDyn']['PCMode']       = int(f.readline().split()[0])
        self.fst_vt['ServoDyn']['TPCOn']        = float_read(f.readline().split()[0])
        self.fst_vt['ServoDyn']['TPitManS1']    = float_read(f.readline().split()[0])
        self.fst_vt['ServoDyn']['TPitManS2']    = float_read(f.readline().split()[0])
        self.fst_vt['ServoDyn']['TPitManS3']    = float_read(f.readline().split()[0])
        self.fst_vt['ServoDyn']['PitManRat1']   = float_read(f.readline().split()[0])
        self.fst_vt['ServoDyn']['PitManRat2']   = float_read(f.readline().split()[0])
        self.fst_vt['ServoDyn']['PitManRat3']   = float_read(f.readline().split()[0])
        self.fst_vt['ServoDyn']['BlPitchF1']    = float_read(f.readline().split()[0])
        self.fst_vt['ServoDyn']['BlPitchF2']    = float_read(f.readline().split()[0])
        self.fst_vt['ServoDyn']['BlPitchF3']    = float_read(f.readline().split()[0])

        # Geneartor and Torque Control (gen_torq_ctrl)
        f.readline()
        self.fst_vt['ServoDyn']['VSContrl'] = int(f.readline().split()[0])
        self.fst_vt['ServoDyn']['GenModel'] = int(f.readline().split()[0])
        self.fst_vt['ServoDyn']['GenEff']   = float_read(f.readline().split()[0])
        self.fst_vt['ServoDyn']['GenTiStr'] = bool_read(f.readline().split()[0])
        self.fst_vt['ServoDyn']['GenTiStp'] = bool_read(f.readline().split()[0])
        self.fst_vt['ServoDyn']['SpdGenOn'] = float_read(f.readline().split()[0])
        self.fst_vt['ServoDyn']['TimGenOn'] = float_read(f.readline().split()[0])
        self.fst_vt['ServoDyn']['TimGenOf'] = float_read(f.readline().split()[0])

        # Simple Variable-Speed Torque Control (var_speed_torq_ctrl)
        f.readline()
        self.fst_vt['ServoDyn']['VS_RtGnSp'] = float_read(f.readline().split()[0])
        self.fst_vt['ServoDyn']['VS_RtTq']   = float_read(f.readline().split()[0])
        self.fst_vt['ServoDyn']['VS_Rgn2K']  = float_read(f.readline().split()[0])
        self.fst_vt['ServoDyn']['VS_SlPc']   = float_read(f.readline().split()[0])

        # Simple Induction Generator (induct_gen)
        f.readline()
        self.fst_vt['ServoDyn']['SIG_SlPc'] = float_read(f.readline().split()[0])
        self.fst_vt['ServoDyn']['SIG_SySp'] = float_read(f.readline().split()[0])
        self.fst_vt['ServoDyn']['SIG_RtTq'] = float_read(f.readline().split()[0])
        self.fst_vt['ServoDyn']['SIG_PORt'] = float_read(f.readline().split()[0])

        # Thevenin-Equivalent Induction Generator (theveq_induct_gen)
        f.readline()
        self.fst_vt['ServoDyn']['TEC_Freq'] = float_read(f.readline().split()[0])
        self.fst_vt['ServoDyn']['TEC_NPol'] = int(f.readline().split()[0])
        self.fst_vt['ServoDyn']['TEC_SRes'] = float_read(f.readline().split()[0])
        self.fst_vt['ServoDyn']['TEC_RRes'] = float_read(f.readline().split()[0])
        self.fst_vt['ServoDyn']['TEC_VLL']  = float_read(f.readline().split()[0])
        self.fst_vt['ServoDyn']['TEC_SLR']  = float_read(f.readline().split()[0])
        self.fst_vt['ServoDyn']['TEC_RLR']  = float_read(f.readline().split()[0])
        self.fst_vt['ServoDyn']['TEC_MR']   = float_read(f.readline().split()[0])

        # High-Speed Shaft Brake (shaft_brake)
        f.readline()
        self.fst_vt['ServoDyn']['HSSBrMode'] = int(f.readline().split()[0])
        self.fst_vt['ServoDyn']['THSSBrDp']  = float_read(f.readline().split()[0])
        self.fst_vt['ServoDyn']['HSSBrDT']   = float_read(f.readline().split()[0])
        self.fst_vt['ServoDyn']['HSSBrTqF']  = float_read(f.readline().split()[0])

        # Nacelle-Yaw Control (nac_yaw_ctrl)
        f.readline()
        self.fst_vt['ServoDyn']['YCMode']    = int(f.readline().split()[0])
        self.fst_vt['ServoDyn']['TYCOn']     = float_read(f.readline().split()[0])
        self.fst_vt['ServoDyn']['YawNeut']   = float_read(f.readline().split()[0])
        self.fst_vt['ServoDyn']['YawSpr']    = float_read(f.readline().split()[0])
        self.fst_vt['ServoDyn']['YawDamp']   = float_read(f.readline().split()[0])
        self.fst_vt['ServoDyn']['TYawManS']  = float_read(f.readline().split()[0])
        self.fst_vt['ServoDyn']['YawManRat'] = float_read(f.readline().split()[0])
        self.fst_vt['ServoDyn']['NacYawF']   = float_read(f.readline().split()[0])

        # Tuned Mass Damper (tuned_mass_damper)
        f.readline()
        self.fst_vt['ServoDyn']['CompNTMD'] = bool_read(f.readline().split()[0])
        self.fst_vt['ServoDyn']['NTMDfile'] = f.readline().split()[0][1:-1]
        self.fst_vt['ServoDyn']['CompTTMD'] = bool_read(f.readline().split()[0])
        self.fst_vt['ServoDyn']['TTMDfile'] = f.readline().split()[0][1:-1]

        # Bladed Interface and Torque-Speed Look-Up Table (bladed_interface)
        f.readline()
        self.fst_vt['ServoDyn']['DLL_FileName'] = os.path.normpath(os.path.join(os.path.split(sd_file)[0], f.readline().split()[0][1:-1]))
        self.fst_vt['ServoDyn']['DLL_InFile']   = f.readline().split()[0][1:-1]
        self.fst_vt['ServoDyn']['DLL_ProcName'] = f.readline().split()[0][1:-1]
        dll_dt_line = f.readline().split()[0]
        try:
            self.fst_vt['ServoDyn']['DLL_DT'] = float_read(dll_dt_line)
        except:
            self.fst_vt['ServoDyn']['DLL_DT'] = dll_dt_line[1:-1]
        self.fst_vt['ServoDyn']['DLL_Ramp']     = bool_read(f.readline().split()[0])
        self.fst_vt['ServoDyn']['BPCutoff']     = float_read(f.readline().split()[0])
        self.fst_vt['ServoDyn']['NacYaw_North'] = float_read(f.readline().split()[0])
        self.fst_vt['ServoDyn']['Ptch_Cntrl']   = int(f.readline().split()[0])
        self.fst_vt['ServoDyn']['Ptch_SetPnt']  = float_read(f.readline().split()[0])
        self.fst_vt['ServoDyn']['Ptch_Min']     = float_read(f.readline().split()[0])
        self.fst_vt['ServoDyn']['Ptch_Max']     = float_read(f.readline().split()[0])
        self.fst_vt['ServoDyn']['PtchRate_Min'] = float_read(f.readline().split()[0])
        self.fst_vt['ServoDyn']['PtchRate_Max'] = float_read(f.readline().split()[0])
        self.fst_vt['ServoDyn']['Gain_OM']      = float_read(f.readline().split()[0])
        self.fst_vt['ServoDyn']['GenSpd_MinOM'] = float_read(f.readline().split()[0])
        self.fst_vt['ServoDyn']['GenSpd_MaxOM'] = float_read(f.readline().split()[0])
        self.fst_vt['ServoDyn']['GenSpd_Dem']   = float_read(f.readline().split()[0])
        self.fst_vt['ServoDyn']['GenTrq_Dem']   = float_read(f.readline().split()[0])
        self.fst_vt['ServoDyn']['GenPwr_Dem']   = float_read(f.readline().split()[0])

        f.readline()

        self.fst_vt['ServoDyn']['DLL_NumTrq'] = int(f.readline().split()[0])
        f.readline()
        f.readline()
        self.fst_vt['ServoDyn']['GenSpd_TLU'] = [None] * self.fst_vt['ServoDyn']['DLL_NumTrq']
        self.fst_vt['ServoDyn']['GenTrq_TLU'] = [None] * self.fst_vt['ServoDyn']['DLL_NumTrq']
        for i in range(self.fst_vt['ServoDyn']['DLL_NumTrq']):
            data = f.readline().split()
            self.fst_vt['ServoDyn']['GenSpd_TLU'][i]  = float_read(data[0])
            self.fst_vt['ServoDyn']['GenTrq_TLU'][i]  = float_read(data[0])

        # ServoDyn Output Params (sd_out_params)
        f.readline()
        self.fst_vt['ServoDyn']['SumPrint'] = bool_read(f.readline().split()[0])
        self.fst_vt['ServoDyn']['OutFile']  = int(f.readline().split()[0])
        self.fst_vt['ServoDyn']['TabDelim'] = bool_read(f.readline().split()[0])
        self.fst_vt['ServoDyn']['OutFmt']   = f.readline().split()[0][1:-1]
        self.fst_vt['ServoDyn']['TStart']   = float_read(f.readline().split()[0])

        # ServoDyn Outlist
        f.readline()
        data = f.readline()
        while data.split()[0] != 'END':
            channels = data.split('"')
            channel_list = channels[1].split(',')
            self.set_outlist(self.fst_vt['outlist']['ServoDyn'], channel_list)
            data = f.readline()

        f.close()


class InputReader_FAST7(InputReader_Common):
    """ FASTv7.02 input file reader """
    
    def execute(self):
        self.read_MainInput()
        self.read_AeroDyn_FAST7()
        # if self.fst_vt['aerodyn']['wind_file_type'][1]  == 'wnd':
        #     self.WndWindReader(self.fst_vt['aerodyn']['WindFile'])
        # else:
        #     print 'Wind reader for file type .%s not implemented yet.' % self.fst_vt['aerodyn']['wind_file_type'][1]
        self.read_ElastoDynBlade()
        self.read_ElastoDynTower()

    def read_MainInput(self):

        fst_file = os.path.join(self.FAST_directory, self.FAST_InputFile)
        f = open(fst_file)

        # FAST Inputs
        f.readline()
        f.readline()
        self.fst_vt['description'] = f.readline().rstrip()
        f.readline()
        f.readline()
        self.fst_vt['Fst7']['Echo'] = bool_read(f.readline().split()[0])
        self.fst_vt['Fst7']['ADAMSPrep'] = int(f.readline().split()[0])
        self.fst_vt['Fst7']['AnalMode'] = int(f.readline().split()[0])
        self.fst_vt['Fst7']['NumBl'] = int(f.readline().split()[0])
        self.fst_vt['Fst7']['TMax'] = float_read(f.readline().split()[0])
        self.fst_vt['Fst7']['DT']  = float_read(f.readline().split()[0])
        f.readline()
        self.fst_vt['Fst7']['YCMode'] = int(f.readline().split()[0])
        self.fst_vt['Fst7']['TYCOn'] = float_read(f.readline().split()[0])
        self.fst_vt['Fst7']['PCMode'] = int(f.readline().split()[0])
        self.fst_vt['Fst7']['TPCOn'] = float_read(f.readline().split()[0])
        self.fst_vt['Fst7']['VSContrl'] = int(f.readline().split()[0])
        self.fst_vt['Fst7']['VS_RtGnSp']  = float_read(f.readline().split()[0])
        self.fst_vt['Fst7']['VS_RtTq']  = float_read(f.readline().split()[0])
        self.fst_vt['Fst7']['VS_Rgn2K']  = float_read(f.readline().split()[0])
        self.fst_vt['Fst7']['VS_SlPc']  = float_read(f.readline().split()[0])
        self.fst_vt['Fst7']['GenModel'] = int(f.readline().split()[0])
        self.fst_vt['Fst7']['GenTiStr'] = bool(f.readline().split()[0])
        self.fst_vt['Fst7']['GenTiStp'] = bool(f.readline().split()[0])
        self.fst_vt['Fst7']['SpdGenOn'] = float_read(f.readline().split()[0])
        self.fst_vt['Fst7']['TimGenOn'] = float_read(f.readline().split()[0])
        self.fst_vt['Fst7']['TimGenOf'] = float_read(f.readline().split()[0])
        self.fst_vt['Fst7']['HSSBrMode'] = int(f.readline().split()[0])
        self.fst_vt['Fst7']['THSSBrDp'] = float_read(f.readline().split()[0])
        self.fst_vt['Fst7']['TiDynBrk'] = float_read(f.readline().split()[0])
        self.fst_vt['Fst7']['TTpBrDp1'] = float_read(f.readline().split()[0])
        self.fst_vt['Fst7']['TTpBrDp2'] = float_read(f.readline().split()[0])
        self.fst_vt['Fst7']['TTpBrDp3'] = float_read(f.readline().split()[0])
        self.fst_vt['Fst7']['TBDepISp1'] = float_read(f.readline().split()[0])
        self.fst_vt['Fst7']['TBDepISp2'] = float_read(f.readline().split()[0])
        self.fst_vt['Fst7']['TBDepISp3'] = float_read(f.readline().split()[0])
        self.fst_vt['Fst7']['TYawManS'] = float_read(f.readline().split()[0])
        self.fst_vt['Fst7']['TYawManE'] = float_read(f.readline().split()[0])
        self.fst_vt['Fst7']['NacYawF'] = float_read(f.readline().split()[0])
        self.fst_vt['Fst7']['TPitManS1'] = float_read(f.readline().split()[0])
        self.fst_vt['Fst7']['TPitManS2'] = float_read(f.readline().split()[0])
        self.fst_vt['Fst7']['TPitManS3'] = float_read(f.readline().split()[0])
        self.fst_vt['Fst7']['TPitManE1'] = float_read(f.readline().split()[0])
        self.fst_vt['Fst7']['TPitManE2'] = float_read(f.readline().split()[0])
        self.fst_vt['Fst7']['TPitManE3'] = float_read(f.readline().split()[0])
        self.fst_vt['Fst7']['BlPitch1']  = float_read(f.readline().split()[0])
        self.fst_vt['Fst7']['BlPitch2']  = float_read(f.readline().split()[0])
        self.fst_vt['Fst7']['BlPitch3']  = float_read(f.readline().split()[0])
        self.fst_vt['Fst7']['B1PitchF1'] = float_read(f.readline().split()[0])
        self.fst_vt['Fst7']['B1PitchF2'] = float_read(f.readline().split()[0])
        self.fst_vt['Fst7']['B1PitchF3'] = float_read(f.readline().split()[0])
        f.readline()
        self.fst_vt['Fst7']['Gravity'] = float_read(f.readline().split()[0])
        f.readline()
        self.fst_vt['Fst7']['FlapDOF1'] = bool_read(f.readline().split()[0])
        self.fst_vt['Fst7']['FlapDOF2'] = bool_read(f.readline().split()[0])
        self.fst_vt['Fst7']['EdgeDOF'] = bool_read(f.readline().split()[0])
        self.fst_vt['Fst7']['TeetDOF'] = bool_read(f.readline().split()[0])
        self.fst_vt['Fst7']['DrTrDOF'] = bool_read(f.readline().split()[0])
        self.fst_vt['Fst7']['GenDOF'] = bool_read(f.readline().split()[0])
        self.fst_vt['Fst7']['YawDOF'] = bool_read(f.readline().split()[0])
        self.fst_vt['Fst7']['TwFADOF1'] = bool_read(f.readline().split()[0])
        self.fst_vt['Fst7']['TwFADOF2'] = bool_read(f.readline().split()[0])
        self.fst_vt['Fst7']['TwSSDOF1'] = bool_read(f.readline().split()[0])
        self.fst_vt['Fst7']['TwSSDOF2'] = bool_read(f.readline().split()[0])
        self.fst_vt['Fst7']['CompAero'] = bool_read(f.readline().split()[0])
        self.fst_vt['Fst7']['CompNoise'] = bool_read(f.readline().split()[0])
        f.readline()
        self.fst_vt['Fst7']['OoPDefl'] = float_read(f.readline().split()[0])
        self.fst_vt['Fst7']['IPDefl'] = float_read(f.readline().split()[0])
        self.fst_vt['Fst7']['TeetDefl'] = float_read(f.readline().split()[0])
        self.fst_vt['Fst7']['Azimuth'] = float_read(f.readline().split()[0])
        self.fst_vt['Fst7']['RotSpeed'] = float_read(f.readline().split()[0])
        self.fst_vt['Fst7']['NacYaw'] = float_read(f.readline().split()[0])
        self.fst_vt['Fst7']['TTDspFA'] = float_read(f.readline().split()[0])
        self.fst_vt['Fst7']['TTDspSS'] = float_read(f.readline().split()[0])
        f.readline()
        self.fst_vt['Fst7']['TipRad'] = float_read(f.readline().split()[0])
        self.fst_vt['Fst7']['HubRad'] = float_read(f.readline().split()[0])
        self.fst_vt['Fst7']['PSpnElN'] = int(f.readline().split()[0])
        self.fst_vt['Fst7']['UndSling'] = float_read(f.readline().split()[0])
        self.fst_vt['Fst7']['HubCM'] = float_read(f.readline().split()[0])
        self.fst_vt['Fst7']['OverHang'] = float_read(f.readline().split()[0])
        self.fst_vt['Fst7']['NacCMxn'] = float_read(f.readline().split()[0])
        self.fst_vt['Fst7']['NacCMyn'] = float_read(f.readline().split()[0])
        self.fst_vt['Fst7']['NacCMzn'] = float_read(f.readline().split()[0])
        self.fst_vt['Fst7']['TowerHt'] = float_read(f.readline().split()[0])
        self.fst_vt['Fst7']['Twr2Shft'] = float_read(f.readline().split()[0])
        self.fst_vt['Fst7']['TwrRBHt'] = float_read(f.readline().split()[0])
        self.fst_vt['Fst7']['ShftTilt'] = float_read(f.readline().split()[0])
        self.fst_vt['Fst7']['Delta3'] = float_read(f.readline().split()[0])
        self.fst_vt['Fst7']['PreCone1'] = float_read(f.readline().split()[0])
        self.fst_vt['Fst7']['PreCone2'] = float_read(f.readline().split()[0])
        self.fst_vt['Fst7']['PreCone3'] = float_read(f.readline().split()[0])
        self.fst_vt['Fst7']['AzimB1Up'] = float_read(f.readline().split()[0])
        f.readline()
        self.fst_vt['Fst7']['YawBrMass'] = float_read(f.readline().split()[0])
        self.fst_vt['Fst7']['NacMass'] = float_read(f.readline().split()[0])
        self.fst_vt['Fst7']['HubMass'] = float_read(f.readline().split()[0])
        self.fst_vt['Fst7']['TipMass1'] = float_read(f.readline().split()[0])
        self.fst_vt['Fst7']['TipMass2'] = float_read(f.readline().split()[0])
        self.fst_vt['Fst7']['TipMass3'] = float_read(f.readline().split()[0])
        self.fst_vt['Fst7']['NacYIner'] = float_read(f.readline().split()[0])
        self.fst_vt['Fst7']['GenIner'] = float_read(f.readline().split()[0])
        self.fst_vt['Fst7']['HubIner'] = float_read(f.readline().split()[0])
        f.readline()
        self.fst_vt['Fst7']['GBoxEff'] = float_read(f.readline().split()[0])
        self.fst_vt['Fst7']['GenEff'] = float_read(f.readline().split()[0])
        self.fst_vt['Fst7']['GBRatio'] = float_read(f.readline().split()[0])
        self.fst_vt['Fst7']['GBRevers'] = bool_read(f.readline().split()[0])
        self.fst_vt['Fst7']['HSSBrTqF'] = float_read(f.readline().split()[0])
        self.fst_vt['Fst7']['HSSBrDT'] = float_read(f.readline().split()[0])
        self.fst_vt['Fst7']['DynBrkFi'] = f.readline().split()[0]
        self.fst_vt['Fst7']['DTTorSpr'] = float_read(f.readline().split()[0])
        self.fst_vt['Fst7']['DTTorDmp'] = float_read(f.readline().split()[0])
        f.readline()
        self.fst_vt['Fst7']['SIG_SlPc'] = float_read(f.readline().split()[0])
        self.fst_vt['Fst7']['SIG_SySp'] = float_read(f.readline().split()[0])
        self.fst_vt['Fst7']['SIG_RtTq'] = float_read(f.readline().split()[0])
        self.fst_vt['Fst7']['SIG_PORt'] = float_read(f.readline().split()[0])
        f.readline()
        self.fst_vt['Fst7']['TEC_Freq'] = float_read(f.readline().split()[0])
        self.fst_vt['Fst7']['TEC_NPol'] = int(f.readline().split()[0])
        self.fst_vt['Fst7']['TEC_SRes'] = float_read(f.readline().split()[0])
        self.fst_vt['Fst7']['TEC_RRes'] = float_read(f.readline().split()[0])
        self.fst_vt['Fst7']['TEC_VLL'] = float_read(f.readline().split()[0])
        self.fst_vt['Fst7']['TEC_SLR'] = float_read(f.readline().split()[0])
        self.fst_vt['Fst7']['TEC_RLR'] = float_read(f.readline().split()[0])
        self.fst_vt['Fst7']['TEC_MR'] = float_read(f.readline().split()[0])
        f.readline()
        self.fst_vt['Fst7']['PtfmModel'] = int(f.readline().split()[0])
        self.fst_vt['Fst7']['PtfmFile'] = f.readline().split()[0][1:-1]
        f.readline()
        self.fst_vt['Fst7']['TwrNodes'] = int(f.readline().split()[0])
        self.fst_vt['Fst7']['TwrFile'] = f.readline().split()[0][1:-1]
        f.readline()
        self.fst_vt['Fst7']['YawSpr'] = float_read(f.readline().split()[0])
        self.fst_vt['Fst7']['YawDamp'] = float_read(f.readline().split()[0])
        self.fst_vt['Fst7']['YawNeut'] = float_read(f.readline().split()[0])
        f.readline()
        self.fst_vt['Fst7']['Furling'] = bool_read(f.readline().split()[0])
        self.fst_vt['Fst7']['FurlFile'] = f.readline().split()[0]
        f.readline() 
        self.fst_vt['Fst7']['TeetMod'] = int(f.readline().split()[0])
        self.fst_vt['Fst7']['TeetDmpP'] = float_read(f.readline().split()[0])
        self.fst_vt['Fst7']['TeetDmp'] = float_read(f.readline().split()[0])
        self.fst_vt['Fst7']['TeetCDmp'] = float_read(f.readline().split()[0])
        self.fst_vt['Fst7']['TeetSStP'] = float_read(f.readline().split()[0])
        self.fst_vt['Fst7']['TeetHStP'] = float_read(f.readline().split()[0])
        self.fst_vt['Fst7']['TeetSSSp'] = float_read(f.readline().split()[0])
        self.fst_vt['Fst7']['TeetHSSp'] = float_read(f.readline().split()[0])
        f.readline()
        self.fst_vt['Fst7']['TBDrConN'] = float_read(f.readline().split()[0])
        self.fst_vt['Fst7']['TBDrConD'] = float_read(f.readline().split()[0])
        self.fst_vt['Fst7']['TpBrDT'] = float_read(f.readline().split()[0])
        f.readline()
        self.fst_vt['Fst7']['BldFile1'] = f.readline().split()[0][1:-1] # TODO - different blade files
        self.fst_vt['Fst7']['BldFile2'] = f.readline().split()[0][1:-1]
        self.fst_vt['Fst7']['BldFile3'] = f.readline().split()[0][1:-1]
        f.readline() 
        self.fst_vt['Fst7']['ADFile'] = f.readline().split()[0][1:-1]
        f.readline()
        self.fst_vt['Fst7']['NoiseFile'] = f.readline().split()[0]
        f.readline()
        self.fst_vt['Fst7']['ADAMSFile'] = f.readline().split()[0]
        f.readline()
        self.fst_vt['Fst7']['LinFile'] = f.readline().split()[0]
        f.readline()
        self.fst_vt['Fst7']['SumPrint'] = bool_read(f.readline().split()[0])
        self.fst_vt['Fst7']['OutFileFmt'] = int(f.readline().split()[0])
        self.fst_vt['Fst7']['TabDelim'] = bool_read(f.readline().split()[0])

        self.fst_vt['Fst7']['OutFmt'] = f.readline().split()[0]
        self.fst_vt['Fst7']['TStart'] = float_read(f.readline().split()[0])
        self.fst_vt['Fst7']['DecFact'] = int(f.readline().split()[0])
        self.fst_vt['Fst7']['SttsTime'] = float_read(f.readline().split()[0])
        self.fst_vt['Fst7']['NcIMUxn'] = float_read(f.readline().split()[0])
        self.fst_vt['Fst7']['NcIMUyn'] = float_read(f.readline().split()[0])
        self.fst_vt['Fst7']['NcIMUzn'] = float_read(f.readline().split()[0])
        self.fst_vt['Fst7']['ShftGagL'] = float_read(f.readline().split()[0])
        self.fst_vt['Fst7']['NTwGages'] = int(f.readline().split()[0])
        twrg = f.readline().split(',')
        if self.fst_vt['Fst7']['NTwGages'] != 0: #loop over elements if there are gauges to be added, otherwise assign directly
            for i in range(self.fst_vt['Fst7']['NTwGages']):
                self.fst_vt['Fst7']['TwrGagNd'].append(twrg[i])
            self.fst_vt['Fst7']['TwrGagNd'][-1]  = self.fst_vt['Fst7']['TwrGagNd'][-1][0:2]
        else:
            self.fst_vt['Fst7']['TwrGagNd'] = twrg
            self.fst_vt['Fst7']['TwrGagNd'][-1]  = self.fst_vt['Fst7']['TwrGagNd'][-1][0:4]
        self.fst_vt['Fst7']['NBlGages'] = int(f.readline().split()[0])
        blg = f.readline().split(',')
        if self.fst_vt['Fst7']['NBlGages'] != 0:
            for i in range(self.fst_vt['Fst7']['NBlGages']):
                self.fst_vt['Fst7']['BldGagNd'].append(blg[i])
            self.fst_vt['Fst7']['BldGagNd'][-1]  = self.fst_vt['Fst7']['BldGagNd'][-1][0:2]
        else:
            self.fst_vt['Fst7']['BldGagNd'] = blg
            self.fst_vt['Fst7']['BldGagNd'][-1]  = self.fst_vt['Fst7']['BldGagNd'][-1][0:4]
    
        # Outlist (TODO - detailed categorization)
        f.readline()
        data = f.readline()
        while data.split()[0] != 'END':
            channels = data.split('"')
            channel_list = channels[1].split(',')
            self.set_outlist(self.fst_vt['outlist7'], channel_list)
            data = f.readline()

    def read_AeroDyn_FAST7(self):

        ad_file = os.path.join(self.FAST_directory, self.fst_vt['Fst7']['ADFile'])
        f = open(ad_file)

        # skip lines and check if nondimensional
        f.readline()
        self.fst_vt['AeroDyn14']['SysUnits'] = f.readline().split()[0]
        self.fst_vt['AeroDyn14']['StallMod'] = f.readline().split()[0]
        self.fst_vt['AeroDyn14']['UseCm'] = f.readline().split()[0]
        self.fst_vt['AeroDyn14']['InfModel'] = f.readline().split()[0]
        self.fst_vt['AeroDyn14']['IndModel'] = f.readline().split()[0]
        self.fst_vt['AeroDyn14']['AToler'] = float_read(f.readline().split()[0])
        self.fst_vt['AeroDyn14']['TLModel'] = f.readline().split()[0]
        self.fst_vt['AeroDyn14']['HLModel'] = f.readline().split()[0]
        self.fst_vt['AeroDyn14']['WindFile'] = os.path.normpath(os.path.join(os.path.split(ad_file)[0], f.readline().split()[0][1:-1]))
        self.fst_vt['AeroDyn14']['wind_file_type'] = self.fst_vt['AeroDyn14']['WindFile'].split('.')
        self.fst_vt['AeroDyn14']['HH'] = float_read(f.readline().split()[0])
        self.fst_vt['AeroDyn14']['TwrShad'] = float_read(f.readline().split()[0])
        self.fst_vt['AeroDyn14']['ShadHWid'] = float_read(f.readline().split()[0])
        self.fst_vt['AeroDyn14']['T_Shad_Refpt'] = float_read(f.readline().split()[0])
        self.fst_vt['AeroDyn14']['AirDens'] = float_read(f.readline().split()[0])
        self.fst_vt['AeroDyn14']['KinVisc'] = float_read(f.readline().split()[0])
        self.fst_vt['AeroDyn14']['DTAero'] = float_read(f.readline().split()[0])

        self.fst_vt['AeroDyn14']['NumFoil'] = int(f.readline().split()[0])
        self.fst_vt['AeroDyn14']['FoilNm'] = [None] * self.fst_vt['AeroDyn14']['NumFoil']
        for i in range(self.fst_vt['AeroDyn14']['NumFoil']):
            af_filename = f.readline().split()[0]
            af_filename = fix_path(af_filename)
            self.fst_vt['AeroDyn14']['FoilNm'][i]  = af_filename[1:-1]
        
        self.fst_vt['AeroDynBlade']['BldNodes'] = int(f.readline().split()[0])
        f.readline()
        self.fst_vt['AeroDynBlade']['RNodes'] = [None] * self.fst_vt['AeroDynBlade']['BldNodes']
        self.fst_vt['AeroDynBlade']['AeroTwst'] = [None] * self.fst_vt['AeroDynBlade']['BldNodes']
        self.fst_vt['AeroDynBlade']['DRNodes'] = [None] * self.fst_vt['AeroDynBlade']['BldNodes']
        self.fst_vt['AeroDynBlade']['Chord'] = [None] * self.fst_vt['AeroDynBlade']['BldNodes']
        self.fst_vt['AeroDynBlade']['NFoil'] = [None] * self.fst_vt['AeroDynBlade']['BldNodes']
        self.fst_vt['AeroDynBlade']['PrnElm'] = [None] * self.fst_vt['AeroDynBlade']['BldNodes']       
        for i in range(self.fst_vt['AeroDynBlade']['BldNodes']):
            data = f.readline().split()
            self.fst_vt['AeroDynBlade']['RNodes'][i]  = float_read(data[0])
            self.fst_vt['AeroDynBlade']['AeroTwst'][i]  = float_read(data[1])
            self.fst_vt['AeroDynBlade']['DRNodes'][i]  = float_read(data[2])
            self.fst_vt['AeroDynBlade']['Chord'][i]  = float_read(data[3])
            self.fst_vt['AeroDynBlade']['NFoil'][i]  = int(data[4])
            self.fst_vt['AeroDynBlade']['PrnElm'][i]  = data[5]

        f.close()

        # create airfoil objects
        self.fst_vt['AeroDynBlade']['af_data'] = []
        for i in range(self.fst_vt['AeroDyn14']['NumFoil']):
             self.fst_vt['AeroDynBlade']['af_data'].append(self.read_AeroDyn14Polar(os.path.join(self.FAST_directory,self.fst_vt['AeroDyn14']['FoilNm'][i])))


if __name__=="__main__":
    
    FAST_ver = 'OpenFAST'
    read_yaml = True

    if read_yaml:
        fast = InputReader_Common(FAST_ver=FAST_ver)
        fast.FAST_yamlfile = 'temp/OpenFAST/test.yaml'
        fast.read_yaml()

    else:
        if FAST_ver.lower() == 'fast7':
            fast = InputReader_FAST7(FAST_ver=FAST_ver)
            fast.FAST_InputFile = 'Test16.fst'   # FAST input file (ext=.fst)
            fast.FAST_directory = 'C:/Users/egaertne/WT_Codes/models/FAST_v7.02.00d-bjj/CertTest/'   # Path to fst directory files

        elif FAST_ver.lower() == 'fast8':
            fast = InputReader_OpenFAST(FAST_ver=FAST_ver)
            fast.FAST_InputFile = 'NREL5MW_onshore.fst'   # FAST input file (ext=.fst)
            fast.FAST_directory = 'C:/Users/egaertne/WT_Codes/models/FAST_v8.16.00a-bjj/ref/5mw_onshore/'   # Path to fst directory files

        elif FAST_ver.lower() == 'openfast':
            fast = InputReader_OpenFAST(FAST_ver=FAST_ver)
            fast.FAST_InputFile = '5MW_Land_DLL_WTurb.fst'   # FAST input file (ext=.fst)
            fast.FAST_directory = 'C:/Users/egaertne/WT_Codes/models/openfast/glue-codes/fast/5MW_Land_DLL_WTurb'   # Path to fst directory files

        fast.execute()
