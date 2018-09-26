import os, sys, copy
import operator
import yaml
import numpy as np

from FAST_reader import InputReader_Common, InputReader_OpenFAST, InputReader_FAST7
from FAST_vars import FstModel



# Builder


def auto_format(f, var):
    # Error handling for variables with 'Default' options
    if isinstance(var, str):
        f.write('{:}\n'.format(var))
    elif isinstance(var, int):
        f.write('{:3}\n'.format(var))
    elif isinstance(var, int):
        f.write('{: 2.15e}\n'.format(var))

# given a list of nested dictionary keys, return the dict at that point
def get_dict(vartree, branch):
    return reduce(operator.getitem, branch, vartree)

class InputWriter_Common(object):
    """ Methods for writing input files that are (relatively) unchanged across FAST versions."""

    def __init__(self, **kwargs):

        self.FAST_ver = 'OPENFAST'
        self.FAST_namingOut = None    #Master FAST file
        self.FAST_runDirectory = None #Output directory
        self.fst_vt = FstModel
        self.fst_update = {}

        # Optional population class attributes from key word arguments
        for k, w in kwargs.iteritems():
            try:
                setattr(self, k, w)
            except:
                pass

        super(InputWriter_Common, self).__init__()

    def write_yaml(self):
        self.FAST_yamlfile = os.path.join(self.FAST_runDirectory, self.FAST_namingOut+'.yaml')
        f = open(self.FAST_yamlfile, "w")
        yaml.dump(self.fst_vt, f)


    def update(self, fst_update={}):
        """ Change fast variables based on the user supplied values """
        if fst_update:
            self.fst_update = fst_update

        # recursively loop through fast variable levels and set them to their update values
        def loop_dict(vartree, branch):
            for var in vartree.keys():
                branch_i = copy.copy(branch)
                branch_i.append(var)
                if type(vartree[var]) is dict:
                    loop_dict(vartree[var], branch_i)
                else:
                    # try:
                    get_dict(self.fst_vt, branch_i[:-1])[branch_i[-1]] = get_dict(self.fst_update, branch_i[:-1])[branch_i[-1]]
                    # except:
                        # pass

        # make sure update dictionary is not empty
        if self.fst_update:
            # if update dictionary uses list keys, convert to nested dictionaries
            if type(self.fst_update.keys()[0]) in [list, tuple]:
                fst_update = copy.copy(self.fst_update)
                self.fst_update = {}
                for var_list in fst_update.keys():
                    branch = []
                    for i, var in enumerate(var_list[0:-1]):
                        if var not in get_dict(self.fst_update, branch).keys():
                            get_dict(self.fst_update, branch)[var] = {}
                        branch.append(var)

                    get_dict(self.fst_update, branch)[var_list[-1]] = fst_update[var_list]

            # set fast variables to update values
            loop_dict(self.fst_update, [])


    def write_ElastoDynBlade(self):

        self.fst_vt['ElastoDyn']['BldFile1'] = self.FAST_namingOut + '_ElastoDyn_blade.dat'
        self.fst_vt['ElastoDyn']['BldFile2'] = self.fst_vt['ElastoDyn']['BldFile1']
        self.fst_vt['ElastoDyn']['BldFile3'] = self.fst_vt['ElastoDyn']['BldFile1']
        blade_file = os.path.join(self.FAST_runDirectory,self.fst_vt['ElastoDyn']['BldFile1'])
        f = open(blade_file, 'w')
        
        f.write('---\n')
        f.write('---\n')
        f.write('---\n')
        if self.FAST_ver.lower() == 'fast7':
            f.write('---\n')

        f.write('{:4}\n'.format(self.fst_vt['ElastoDynBlade']['NBlInpSt']))
        if self.FAST_ver.lower() == 'fast7':
            f.write('{:}\n'.format(self.fst_vt['ElastoDynBlade']['CalcBMode']))
        f.write('{:.6f}\n'.format(self.fst_vt['ElastoDynBlade']['BldFlDmp1']))
        f.write('{:.6f}\n'.format(self.fst_vt['ElastoDynBlade']['BldFlDmp2']))
        f.write('{:.6f}\n'.format(self.fst_vt['ElastoDynBlade']['BldEdDmp1']))
        f.write('---\n')
        f.write('{:.6f}\n'.format(self.fst_vt['ElastoDynBlade']['FlStTunr1']))
        f.write('{:.6f}\n'.format(self.fst_vt['ElastoDynBlade']['FlStTunr2']))
        f.write('{:.6f}\n'.format(self.fst_vt['ElastoDynBlade']['AdjBlMs']))
        f.write('{:.6f}\n'.format(self.fst_vt['ElastoDynBlade']['AdjFlSt']))
        f.write('{:.6f}\n'.format(self.fst_vt['ElastoDynBlade']['AdjEdSt']))
        f.write('Distributed blade properties\n')
        f.write('---\n')
        f.write('---\n')
        

        bf = self.fst_vt['ElastoDynBlade']['BlFract']
        pa = self.fst_vt['ElastoDynBlade']['PitchAxis']
        st = self.fst_vt['ElastoDynBlade']['StrcTwst']
        bm = self.fst_vt['ElastoDynBlade']['BMassDen']
        fs = self.fst_vt['ElastoDynBlade']['FlpStff']
        es = self.fst_vt['ElastoDynBlade']['EdgStff']
        if self.FAST_ver.lower() == 'fast7':
            gs = self.fst_vt['ElastoDynBlade']['GJStff']
            eas = self.fst_vt['ElastoDynBlade']['EAStff']
            a = self.fst_vt['ElastoDynBlade']['Alpha']
            fi = self.fst_vt['ElastoDynBlade']['FlpIner']
            ei = self.fst_vt['ElastoDynBlade']['EdgIner'] 
            pr = self.fst_vt['ElastoDynBlade']['PrecrvRef']
            ps = self.fst_vt['ElastoDynBlade']['PreswpRef']
            fo = self.fst_vt['ElastoDynBlade']['FlpcgOf']       
            eo = self.fst_vt['ElastoDynBlade']['Edgcgof']
            feo = self.fst_vt['ElastoDynBlade']['FlpEAOf']
            eeo = self.fst_vt['ElastoDynBlade']['EdgEAOf']

        if self.FAST_ver.lower() == 'fast7':
            for a1, a2, a3, a4, a5, a6, a7, a8, a9, a10, a11, a12, a13, a14, a15, a16, a17  in \
                zip(bf, pa, st, bm, fs, es, gs, eas, a, fi, ei, pr, ps, fo, eo, feo, eeo):
                f.write('{:.9e}\t{:.9e}\t{:.9e}\t{:.9e}\t{:.9e}\t{:.9e}\t{:.9e}\t{:.9e}\t{:.9e}\t{:.9e}\t{:.9e}\t{:.9e}\t{:.9e}\t{:.9e}\t{:.9e}\t{:.9e}\t{:.9e}\n'.\
                format(a1, a2, a3, a4, a5, a6, a7, a8, a9, a10, a11, a12, a13, a14, a15, a16, a17))
        else:
            for a1, a2, a3, a4, a5, a6 in \
                zip(bf, pa, st, bm, fs, es):
                f.write('{:.9e}\t{:.9e}\t{:.9e}\t{:.9e}\t{:.9e}\t{:.9e}\n'.\
                format(a1, a2, a3, a4, a5, a6))
 
        f.write('Blade Mode Shapes\n')
        for i in range(5):
            f.write('{:.4f}\n'.format(self.fst_vt['ElastoDynBlade']['BldFl1Sh'][i]))
        for i in range(5):
            f.write('{:.4f}\n'.format(self.fst_vt['ElastoDynBlade']['BldFl2Sh'][i]))           
           
        for i in range(5):
            f.write('{:.4f}\n'.format(self.fst_vt['ElastoDynBlade']['BldEdgSh'][i]))      
      
         
        f.close()


    def write_ElastoDynTower(self):

        self.fst_vt['ElastoDyn']['TwrFile'] = self.FAST_namingOut + '_ElastoDyn_tower.dat'
        tower_file = os.path.join(self.FAST_runDirectory,self.fst_vt['ElastoDyn']['TwrFile'])
        f = open(tower_file, 'w')

        f.write('---\n')
        f.write('---\n')
        f.write('Tower Parameters\n')
        if self.FAST_ver.lower() == 'fast7':
            f.write('---\n')

        f.write('{:4}\n'.format(self.fst_vt['ElastoDynTower']['NTwInptSt']))
        if self.FAST_ver.lower() == 'fast7':
            f.write('{:}\n'.format(self.fst_vt['ElastoDynTower']['CalcTMode']))
        f.write('{:5}\n'.format(self.fst_vt['ElastoDynTower']['TwrFADmp1']))
        f.write('{:5}\n'.format(self.fst_vt['ElastoDynTower']['TwrFADmp2']))
        f.write('{:5}\n'.format(self.fst_vt['ElastoDynTower']['TwrSSDmp1']))
        f.write('{:5}\n'.format(self.fst_vt['ElastoDynTower']['TwrSSDmp2']))
    
        # Tower Adjustment Factors
        f.write('Tower Adjustment Factors\n')
        f.write('{:5}\n'.format(self.fst_vt['ElastoDynTower']['FAStTunr1']))
        f.write('{:5}\n'.format(self.fst_vt['ElastoDynTower']['FAStTunr2']))
        f.write('{:5}\n'.format(self.fst_vt['ElastoDynTower']['SSStTunr1']))
        f.write('{:5}\n'.format(self.fst_vt['ElastoDynTower']['SSStTunr2']))
        f.write('{:5}\n'.format(self.fst_vt['ElastoDynTower']['AdjTwMa']))
        f.write('{:5}\n'.format(self.fst_vt['ElastoDynTower']['AdjFASt']))
        f.write('{:5}\n'.format(self.fst_vt['ElastoDynTower']['AdjSSSt']))
     
        # Distributed Tower Properties   
        f.write('Distributed Tower Properties\n')
        f.write('---\n')
        f.write('---\n')
        hf = self.fst_vt['ElastoDynTower']['HtFract']
        md = self.fst_vt['ElastoDynTower']['TMassDen']
        fs = self.fst_vt['ElastoDynTower']['TwFAStif']
        ss = self.fst_vt['ElastoDynTower']['TwSSStif']
        if self.FAST_ver.lower() == 'fast7':
            gs = self.fst_vt['ElastoDynTower']['TwGJStif']
            es = self.fst_vt['ElastoDynTower']['TwEAStif']
            fi = self.fst_vt['ElastoDynTower']['TwFAIner']
            si = self.fst_vt['ElastoDynTower']['TwSSIner']
            fo = self.fst_vt['ElastoDynTower']['TwFAcgOf']
            so = self.fst_vt['ElastoDynTower']['TwSScgOf']
        if self.FAST_ver.lower() == 'fast7':
            for a1, a2, a3, a4, a5, a6, a7, a8, a9, a10 in zip(hf, md, fs, ss, gs, es, fi, si, fo, so):
                f.write('{:.9e}\t{:.9e}\t{:.9e}\t{:.9e}\t{:.9e}\t{:.9e}\t{:.9e}\t{:.9e}\t{:.9e}\t{:.9e}\n'.\
                format(a1, a2, a3, a4, a5, a6, a7, a8, a9, a10))  
        else:
            for a1, a2, a3, a4 in zip(hf, md, fs, ss):
                f.write('{:.9e}\t{:.9e}\t{:.9e}\t{:.9e}\n'.\
                format(a1, a2, a3, a4))          
        
        # Tower Mode Shapes
        f.write('Tower Fore-Aft Mode Shapes\n')
        for i in range(5):
            f.write('{:5}\n'.format(self.fst_vt['ElastoDynTower']['TwFAM1Sh'][i]))
        for i in range(5):
            f.write('{:5}\n'.format(self.fst_vt['ElastoDynTower']['TwFAM2Sh'][i]))        
        
        f.write('Tower Side-to-Side Mode Shapes\n')         
        for i in range(5):
            f.write('{:5}\n'.format(self.fst_vt['ElastoDynTower']['TwSSM1Sh'][i]))
        for i in range(5):
            f.write('{:5}\n'.format(self.fst_vt['ElastoDynTower']['TwSSM2Sh'][i])) 
 
        
        f.close()

    def write_AeroDyn14Polar(self, filename, a_i):
        # AeroDyn v14 Airfoil Polar Input File

        f = open(filename, 'w')
        f.write('AeroDyn airfoil file, Aerodyn v14.04 formatting\n')
        f.write('AeroElasticSE FAST driver\n')

        f.write('{:9d}\t{:}'.format(self.fst_vt['AeroDynBlade']['af_data'][a_i]['number_tables'], 'Number of airfoil tables in this file\n'))
        for i in range(self.fst_vt['AeroDynBlade']['af_data'][a_i]['number_tables']):
            param = self.fst_vt['AeroDynBlade']['af_data'][a_i]['af_tables'][i]
            f.write('{:9g}\t{:}'.format(i, 'Table ID parameter\n'))
            f.write('{: f}\t{:}'.format(param['StallAngle'], 'Stall angle (deg)\n'))
            f.write('{: f}\t{:}'.format(0, 'No longer used, enter zero\n'))
            f.write('{: f}\t{:}'.format(0, 'No longer used, enter zero\n'))
            f.write('{: f}\t{:}'.format(0, 'No longer used, enter zero\n'))
            f.write('{: f}\t{:}'.format(param['ZeroCn'], 'Angle of attack for zero Cn for linear Cn curve (deg)\n'))
            f.write('{: f}\t{:}'.format(param['CnSlope'], 'Cn slope for zero lift for linear Cn curve (1/rad)\n'))
            f.write('{: f}\t{:}'.format(param['CnPosStall'], 'Cn at stall value for positive angle of attack for linear Cn curve\n'))
            f.write('{: f}\t{:}'.format(param['CnNegStall'], 'Cn at stall value for negative angle of attack for linear Cn curve\n'))
            f.write('{: f}\t{:}'.format(param['alphaCdMin'], 'Angle of attack for minimum CD (deg)\n'))
            f.write('{: f}\t{:}'.format(param['CdMin'], 'Minimum CD value\n'))
            if param['cm']:
                for a, cl, cd, cm in zip(param['alpha'], param['cl'], param['cd'], param['cm']):
                    f.write('{: 6e}  {: 6e}  {: 6e}  {: 6e}\n'.format(a, cl, cd, cm))
            else:
                for a, cl, cd in zip(param['alpha'], param['cl'], param['cd']):
                    f.write('{: 6e}  {: 6e}  {: 6e}\n'.format(a, cl, cd))
        
        f.close()

    def get_outlist(self, vartree_head, channel_list=[]):
        """ Loop through a list of output channel names, recursively find values set to True in the nested outlist dict """

        # recursively search nested dictionaries
        def loop_dict(vartree, outlist_i):
            for var in vartree.keys():
                if type(vartree[var]) is dict:
                    loop_dict(vartree[var], outlist_i)
                else:
                    if vartree[var]:
                        outlist_i.append(var)
            return outlist_i

        # if specific outlist branches are not specified, get all
        if not channel_list:
            channel_list = vartree_head.keys()

        # loop through top level of dictionary
        outlist = []
        for var in channel_list:
            var = var.replace(' ', '')
            outlist_i = []
            outlist_i = loop_dict(vartree_head[var], outlist_i)
            if outlist_i:
                outlist.append(sorted(outlist_i))

        return outlist


class InputWriter_OpenFAST(InputWriter_Common):

    def execute(self):
        
        if not os.path.exists(self.FAST_runDirectory):
            os.makedirs(self.FAST_runDirectory)

        self.write_ElastoDynBlade()
        self.write_ElastoDynTower()
        self.write_ElastoDyn()
        # self.write_WindWnd()
        self.write_InflowWind()
        if self.fst_vt['Fst']['CompAero'] == 1:
            self.write_AeroDyn14()
        elif self.fst_vt['Fst']['CompAero'] == 2:
            self.write_AeroDyn15()
        self.write_ServoDyn()

        self.write_MainInput()


    def write_MainInput(self):
        # Main FAST v8.16-v8.17 Input File
        # Currently no differences between FASTv8.16 and OpenFAST.

        self.FAST_InputFileOut = os.path.join(self.FAST_runDirectory, self.FAST_namingOut+'.fst')

        # Keep simple for now:
        f = open(self.FAST_InputFileOut, 'w')

        # ===== .fst Input File =====
        # Simulation Control (fst_sim_ctrl)
        f.write('---\n')
        f.write('---\n')
        f.write('---\n')
        f.write('{:}\n'.format(self.fst_vt['Fst']['Echo']))
        f.write('"{:}"\n'.format(self.fst_vt['Fst']['AbortLevel']))
        f.write('{: 2.15e}\n'.format(self.fst_vt['Fst']['TMax']))
        f.write('{: 2.15e}\n'.format(self.fst_vt['Fst']['DT']))
        f.write('{:3}\n'.format(self.fst_vt['Fst']['InterpOrder']))
        f.write('{:3}\n'.format(self.fst_vt['Fst']['NumCrctn']))
        f.write('{: 2.15e}\n'.format(self.fst_vt['Fst']['DT_UJac']))
        f.write('{: 2.15e}\n'.format(self.fst_vt['Fst']['UJacSclFact']))
        
        # Features Switches and Flags (ftr_swtchs_flgs)
        f.write('---\n')
        f.write('{:3}\n'.format(self.fst_vt['Fst']['CompElast']))
        f.write('{:3}\n'.format(self.fst_vt['Fst']['CompInflow']))
        f.write('{:3}\n'.format(self.fst_vt['Fst']['CompAero']))
        f.write('{:3}\n'.format(self.fst_vt['Fst']['CompServo']))
        f.write('{:3}\n'.format(self.fst_vt['Fst']['CompHydro']))
        f.write('{:3}\n'.format(self.fst_vt['Fst']['CompSub']))
        f.write('{:3}\n'.format(self.fst_vt['Fst']['CompMooring']))
        f.write('{:3}\n'.format(self.fst_vt['Fst']['CompIce']))

        # Input Files (input_files)
        f.write('---\n')
        f.write('"{:}"\n'.format(self.fst_vt['Fst']['EDFile']))
        f.write('"{:}"\n'.format(self.fst_vt['Fst']['BDBldFile1']))
        f.write('"{:}"\n'.format(self.fst_vt['Fst']['BDBldFile2']))
        f.write('"{:}"\n'.format(self.fst_vt['Fst']['BDBldFile3']))
        f.write('"{:}"\n'.format(self.fst_vt['Fst']['InflowFile']))
        f.write('"{:}"\n'.format(self.fst_vt['Fst']['AeroFile']))
        f.write('"{:}"\n'.format(self.fst_vt['Fst']['ServoFile']))
        f.write('"{:}"\n'.format(self.fst_vt['Fst']['HydroFile']))
        f.write('"{:}"\n'.format(self.fst_vt['Fst']['SubFile']))
        f.write('"{:}"\n'.format(self.fst_vt['Fst']['MooringFile']))
        f.write('"{:}"\n'.format(self.fst_vt['Fst']['IceFile']))

        # Output (fst_out_params)
        f.write('---\n')
        f.write('{:}\n'.format(self.fst_vt['Fst']['SumPrint'])) 
 
        f.write('{: 2.15e}\n'.format(self.fst_vt['Fst']['SttsTime'])) 
 
        f.write('{: 2.15e}\n'.format(self.fst_vt['Fst']['ChkptTime']))
        auto_format(f, self.fst_vt['Fst']['DT_Out'])
        f.write('{: 2.15e}\n'.format(self.fst_vt['Fst']['TStart'])) 
 
        f.write('{:3}\n'.format(self.fst_vt['Fst']['OutFileFmt'])) 
 
        f.write('{:}\n'.format(self.fst_vt['Fst']['TabDelim'])) 
 
        f.write('"{:}"\n'.format(self.fst_vt['Fst']['OutFmt']))

        # Visualization (visualization) 
        f.write('---\n')
        f.write('{}\n'.format(self.fst_vt['Fst']['Linearize']))
        f.write('{}\n'.format(self.fst_vt['Fst']['NLinTimes']))
        f.write('{}\n'.format(', '.join(self.fst_vt['Fst']['LinTimes'])))
        f.write('{}\n'.format(self.fst_vt['Fst']['LinInputs']))
        f.write('{}\n'.format(self.fst_vt['Fst']['LinOutputs']))
        f.write('{}\n'.format(self.fst_vt['Fst']['LinOutJac']))
        f.write('{}\n'.format(self.fst_vt['Fst']['LinOutMod']))

        # Visualization (visualization) 
        f.write('---\n')
        f.write('{:3}\n'.format(self.fst_vt['Fst']['WrVTK']))
        f.write('{:3}\n'.format(self.fst_vt['Fst']['VTK_type']))
        f.write('{:}\n'.format(self.fst_vt['Fst']['VTK_fields']))
        f.write('{: 2.15e}\n'.format(self.fst_vt['Fst']['VTK_fps']))

        f.close()


    def write_ElastoDyn(self):
        self.fst_vt['Fst']['EDFile'] = self.FAST_namingOut + '_ElastoDyn.dat'
        ed_file = os.path.join(self.FAST_runDirectory,self.fst_vt['Fst']['EDFile'])
        f = open(ed_file, 'w')

        f.write('---\n')
        f.write('---\n')

        # ElastoDyn Simulation Control (ed_sim_ctrl)
        f.write('---\n')
        f.write('{:}\n'.format(self.fst_vt['ElastoDyn']['Echo']))
        f.write('{:3}\n'.format(self.fst_vt['ElastoDyn']['Method']))
        auto_format(f, self.fst_vt['ElastoDyn']['DT'])

        # Environmental Condition (envir_cond)
        f.write('---\n')
        f.write('{: 2.15e}\n'.format(self.fst_vt['ElastoDyn']['Gravity']))

        # Degrees of Freedom (dof)
        f.write('---\n')
        f.write('{:}\n'.format(self.fst_vt['ElastoDyn']['FlapDOF1']))
        f.write('{:}\n'.format(self.fst_vt['ElastoDyn']['FlapDOF2']))
        f.write('{:}\n'.format(self.fst_vt['ElastoDyn']['EdgeDOF']))
        f.write('{:}\n'.format(self.fst_vt['ElastoDyn']['TeetDOF']))
        f.write('{:}\n'.format(self.fst_vt['ElastoDyn']['DrTrDOF']))
        f.write('{:}\n'.format(self.fst_vt['ElastoDyn']['GenDOF']))
        f.write('{:}\n'.format(self.fst_vt['ElastoDyn']['YawDOF']))
        f.write('{:}\n'.format(self.fst_vt['ElastoDyn']['TwFADOF1']))
        f.write('{:}\n'.format(self.fst_vt['ElastoDyn']['TwFADOF2']))
        f.write('{:}\n'.format(self.fst_vt['ElastoDyn']['TwSSDOF1']))
        f.write('{:}\n'.format(self.fst_vt['ElastoDyn']['TwSSDOF2']))
        f.write('{:}\n'.format(self.fst_vt['ElastoDyn']['PtfmSgDOF']))
        f.write('{:}\n'.format(self.fst_vt['ElastoDyn']['PtfmSwDOF']))
        f.write('{:}\n'.format(self.fst_vt['ElastoDyn']['PtfmHvDOF']))
        f.write('{:}\n'.format(self.fst_vt['ElastoDyn']['PtfmRDOF']))
        f.write('{:}\n'.format(self.fst_vt['ElastoDyn']['PtfmPDOF']))
        f.write('{:}\n'.format(self.fst_vt['ElastoDyn']['PtfmYDOF']))

        # Initial Conditions (init_conds)
        f.write('---\n')
        f.write('{: 2.15e}\n'.format(self.fst_vt['ElastoDyn']['OoPDefl']))
        f.write('{: 2.15e}\n'.format(self.fst_vt['ElastoDyn']['IPDefl']))
        f.write('{: 2.15e}\n'.format(self.fst_vt['ElastoDyn']['BlPitch1']))
        f.write('{: 2.15e}\n'.format(self.fst_vt['ElastoDyn']['BlPitch2']))
        f.write('{: 2.15e}\n'.format(self.fst_vt['ElastoDyn']['BlPitch3']))
        f.write('{: 2.15e}\n'.format(self.fst_vt['ElastoDyn']['TeetDefl']))
        f.write('{: 2.15e}\n'.format(self.fst_vt['ElastoDyn']['Azimuth']))
        f.write('{: 2.15e}\n'.format(self.fst_vt['ElastoDyn']['RotSpeed']))
        f.write('{: 2.15e}\n'.format(self.fst_vt['ElastoDyn']['NacYaw']))
        f.write('{: 2.15e}\n'.format(self.fst_vt['ElastoDyn']['TTDspFA']))
        f.write('{: 2.15e}\n'.format(self.fst_vt['ElastoDyn']['TTDspSS']))
        f.write('{: 2.15e}\n'.format(self.fst_vt['ElastoDyn']['PtfmSurge']))
        f.write('{: 2.15e}\n'.format(self.fst_vt['ElastoDyn']['PtfmSway']))
        f.write('{: 2.15e}\n'.format(self.fst_vt['ElastoDyn']['PtfmHeave']))
        f.write('{: 2.15e}\n'.format(self.fst_vt['ElastoDyn']['PtfmRoll']))
        f.write('{: 2.15e}\n'.format(self.fst_vt['ElastoDyn']['PtfmPitch']))
        f.write('{: 2.15e}\n'.format(self.fst_vt['ElastoDyn']['PtfmYaw']))

        # Turbine Configuration (turb_config)
        f.write('---\n')
        f.write('{:3}\n'.format(self.fst_vt['ElastoDyn']['NumBl']))
        f.write('{: 2.15e}\n'.format(self.fst_vt['ElastoDyn']['TipRad']))
        f.write('{: 2.15e}\n'.format(self.fst_vt['ElastoDyn']['HubRad']))
        f.write('{: 2.15e}\n'.format(self.fst_vt['ElastoDyn']['PreCone1']))
        f.write('{: 2.15e}\n'.format(self.fst_vt['ElastoDyn']['PreCone2']))
        f.write('{: 2.15e}\n'.format(self.fst_vt['ElastoDyn']['PreCone3']))
        f.write('{: 2.15e}\n'.format(self.fst_vt['ElastoDyn']['HubCM']))
        f.write('{: 2.15e}\n'.format(self.fst_vt['ElastoDyn']['UndSling']))
        f.write('{: 2.15e}\n'.format(self.fst_vt['ElastoDyn']['Delta3']))
        f.write('{: 2.15e}\n'.format(self.fst_vt['ElastoDyn']['AzimB1Up']))
        f.write('{: 2.15e}\n'.format(self.fst_vt['ElastoDyn']['OverHang']))
        f.write('{: 2.15e}\n'.format(self.fst_vt['ElastoDyn']['ShftGagL']))
        f.write('{: 2.15e}\n'.format(self.fst_vt['ElastoDyn']['ShftTilt']))
        f.write('{: 2.15e}\n'.format(self.fst_vt['ElastoDyn']['NacCMxn']))
        f.write('{: 2.15e}\n'.format(self.fst_vt['ElastoDyn']['NacCMyn']))
        f.write('{: 2.15e}\n'.format(self.fst_vt['ElastoDyn']['NacCMzn']))
        f.write('{: 2.15e}\n'.format(self.fst_vt['ElastoDyn']['NcIMUxn']))
        f.write('{: 2.15e}\n'.format(self.fst_vt['ElastoDyn']['NcIMUyn']))
        f.write('{: 2.15e}\n'.format(self.fst_vt['ElastoDyn']['NcIMUzn']))
        f.write('{: 2.15e}\n'.format(self.fst_vt['ElastoDyn']['Twr2Shft']))
        f.write('{: 2.15e}\n'.format(self.fst_vt['ElastoDyn']['TowerHt']))
        f.write('{: 2.15e}\n'.format(self.fst_vt['ElastoDyn']['TowerBsHt']))
        f.write('{: 2.15e}\n'.format(self.fst_vt['ElastoDyn']['PtfmCMxt']))
        f.write('{: 2.15e}\n'.format(self.fst_vt['ElastoDyn']['PtfmCMyt']))
        f.write('{: 2.15e}\n'.format(self.fst_vt['ElastoDyn']['PtfmCMzt']))
        f.write('{: 2.15e}\n'.format(self.fst_vt['ElastoDyn']['PtfmRefzt']))

        # Mass and Inertia (mass_inertia)
        f.write('---\n')
        f.write('{: 2.15e}\n'.format(self.fst_vt['ElastoDyn']['TipMass1']))
        f.write('{: 2.15e}\n'.format(self.fst_vt['ElastoDyn']['TipMass2']))
        f.write('{: 2.15e}\n'.format(self.fst_vt['ElastoDyn']['TipMass3']))
        f.write('{: 2.15e}\n'.format(self.fst_vt['ElastoDyn']['HubMass']))
        f.write('{: 2.15e}\n'.format(self.fst_vt['ElastoDyn']['HubIner']))
        f.write('{: 2.15e}\n'.format(self.fst_vt['ElastoDyn']['GenIner']))
        f.write('{: 2.15e}\n'.format(self.fst_vt['ElastoDyn']['NacMass']))
        f.write('{: 2.15e}\n'.format(self.fst_vt['ElastoDyn']['NacYIner']))
        f.write('{: 2.15e}\n'.format(self.fst_vt['ElastoDyn']['YawBrMass']))
        f.write('{: 2.15e}\n'.format(self.fst_vt['ElastoDyn']['PtfmMass']))
        f.write('{: 2.15e}\n'.format(self.fst_vt['ElastoDyn']['PtfmRIner']))
        f.write('{: 2.15e}\n'.format(self.fst_vt['ElastoDyn']['PtfmPIner']))
        f.write('{: 2.15e}\n'.format(self.fst_vt['ElastoDyn']['PtfmYIner']))

        # Blade (blade_struc)
        f.write('---\n')
        f.write('{:3}\n'.format(self.fst_vt['ElastoDyn']['BldNodes']))
        f.write('"{:}"\n'.format(self.fst_vt['ElastoDyn']['BldFile1']))
        f.write('"{:}"\n'.format(self.fst_vt['ElastoDyn']['BldFile2']))
        f.write('"{:}"\n'.format(self.fst_vt['ElastoDyn']['BldFile3']))

        # Rotor-Teeter (rotor_teeter)
        f.write('---\n')
        f.write('{:3}\n'.format(self.fst_vt['ElastoDyn']['TeetMod']))
        f.write('{: 2.15e}\n'.format(self.fst_vt['ElastoDyn']['TeetDmpP']))
        f.write('{: 2.15e}\n'.format(self.fst_vt['ElastoDyn']['TeetDmp']))
        f.write('{: 2.15e}\n'.format(self.fst_vt['ElastoDyn']['TeetCDmp']))
        f.write('{: 2.15e}\n'.format(self.fst_vt['ElastoDyn']['TeetSStP']))
        f.write('{: 2.15e}\n'.format(self.fst_vt['ElastoDyn']['TeetHStP']))
        f.write('{: 2.15e}\n'.format(self.fst_vt['ElastoDyn']['TeetSSSp']))
        f.write('{: 2.15e}\n'.format(self.fst_vt['ElastoDyn']['TeetHSSp']))

        # Drivetrain (drivetrain)
        f.write('---\n')
        f.write('{: 2.15e}\n'.format(self.fst_vt['ElastoDyn']['GBoxEff']))
        f.write('{: 2.15e}\n'.format(self.fst_vt['ElastoDyn']['GBRatio']))
        f.write('{: 2.15e}\n'.format(self.fst_vt['ElastoDyn']['DTTorSpr']))
        f.write('{: 2.15e}\n'.format(self.fst_vt['ElastoDyn']['DTTorDmp']))

        # Furling (furling)
        f.write('---\n')
        f.write('{:}\n'.format(self.fst_vt['ElastoDyn']['Furling']))
        f.write('"{:}"\n'.format(self.fst_vt['ElastoDyn']['FurlFile']))

        # Tower (tower)
        f.write('---\n')
        f.write('{:3}\n'.format(self.fst_vt['ElastoDyn']['TwrNodes']))
        f.write('"{:}"\n'.format(self.fst_vt['ElastoDyn']['TwrFile']))

        # ElastoDyn Output Params (ed_out_params)
        f.write('---\n')
        f.write('{:}\n'.format(self.fst_vt['ElastoDyn']['SumPrint']))
        f.write('{:3}\n'.format(self.fst_vt['ElastoDyn']['OutFile']))
        f.write('{:}\n'.format(self.fst_vt['ElastoDyn']['TabDelim']))
        f.write('"{:}"\n'.format(self.fst_vt['ElastoDyn']['OutFmt']))
        f.write('{: 2.15e}\n'.format(self.fst_vt['ElastoDyn']['TStart']))
        f.write('{:3}\n'.format(self.fst_vt['ElastoDyn']['DecFact']))
        f.write('{:3}\n'.format(self.fst_vt['ElastoDyn']['NTwGages']))
        for i in range(self.fst_vt['ElastoDyn']['NTwGages']-1):
            f.write('{:3}, '.format(self.fst_vt['ElastoDyn']['TwrGagNd'][i]))
        f.write('{:3}\n'.format(self.fst_vt['ElastoDyn']['TwrGagNd'][-1]))
        f.write('{:3}\n'.format(self.fst_vt['ElastoDyn']['NBlGages']))
        for i in range(self.fst_vt['ElastoDyn']['NBlGages']-1):
            f.write('{:3}, '.format(self.fst_vt['ElastoDyn']['BldGagNd'][i]))
        f.write('{:3}\n'.format(self.fst_vt['ElastoDyn']['BldGagNd'][-1]))
    
        # Outlist 
        f.write('Outlist\n')
        outlist = self.get_outlist(self.fst_vt['outlist'], ['ElastoDyn'])
        for channel_list in outlist:
            f.write('"' + ', '.join(channel_list) + '"\n')
        f.write('END\n')
        f.close()


    def write_InflowWind(self):
        self.fst_vt['Fst']['InflowFile'] = self.FAST_namingOut + '_InflowFile.dat'
        inflow_file = os.path.join(self.FAST_runDirectory,self.fst_vt['Fst']['InflowFile'])
        f = open(inflow_file, 'w')

        # self.fst_vt['InflowWind']['Filename'] = os.path.relpath(self.fst_vt['InflowWind']['Filename'], os.path.abspath(self.FAST_runDirectory))
        # self.fst_vt['InflowWind']['FileName_u'] = os.path.relpath(self.fst_vt['InflowWind']['FileName_u'], os.path.abspath(self.FAST_runDirectory))
        # self.fst_vt['InflowWind']['FileName_v'] = os.path.relpath(self.fst_vt['InflowWind']['FileName_v'], os.path.abspath(self.FAST_runDirectory))
        # self.fst_vt['InflowWind']['FileName_w'] = os.path.relpath(self.fst_vt['InflowWind']['FileName_w'], os.path.abspath(self.FAST_runDirectory))

        f.write('---\n')
        f.write('---\n')
        f.write('---\n')
        f.write('{:}\n'.format(self.fst_vt['InflowWind']['Echo']))
        f.write('{:3}\n'.format(self.fst_vt['InflowWind']['WindType']))
        f.write('{: 2.15e}\n'.format(self.fst_vt['InflowWind']['PropogationDir']))
        f.write('{:3}\n'.format(self.fst_vt['InflowWind']['NWindVel']))
        f.write('{: 2.15e}\n'.format(self.fst_vt['InflowWind']['WindVxiList']))
        f.write('{: 2.15e}\n'.format(self.fst_vt['InflowWind']['WindVyiList']))
        f.write('{: 2.15e}\n'.format(self.fst_vt['InflowWind']['WindVziList']))

        # Parameters for Steady Wind Conditions [used only for WindType = 1] (steady_wind_params)
        f.write('---\n')
        f.write('{: 2.15e}\n'.format(self.fst_vt['InflowWind']['HWindSpeed']))
        f.write('{: 2.15e}\n'.format(self.fst_vt['InflowWind']['RefHt']))
        f.write('{: 2.15e}\n'.format(self.fst_vt['InflowWind']['PLexp']))

        # Parameters for Uniform wind file   [used only for WindType = 2] (uniform_wind_params)
        f.write('---\n')
        f.write('"{:}"\n'.format(self.fst_vt['InflowWind']['Filename']))

        f.write('{: 2.15e}\n'.format(self.fst_vt['InflowWind']['RefHt']))
        f.write('{: 2.15e}\n'.format(self.fst_vt['InflowWind']['RefLength']))

        # Parameters for Binary TurbSim Full-Field files   [used only for WindType = 3] (turbsim_wind_params)
        f.write('---\n')
        f.write('"{:}"\n'.format(self.fst_vt['InflowWind']['Filename']))

        # Parameters for Binary Bladed-style Full-Field files   [used only for WindType = 4] (bladed_wind_params)
        f.write('---\n')
        f.write('"{:}"\n'.format(self.fst_vt['InflowWind']['FilenameRoot']))
        f.write('{:}\n'.format(self.fst_vt['InflowWind']['TowerFile']))

        # Parameters for HAWC-format binary files  [Only used with WindType = 5] (hawc_wind_params)
        f.write('---\n')
        f.write('"{:}"\n'.format(self.fst_vt['InflowWind']['FileName_u']))
        f.write('"{:}"\n'.format(self.fst_vt['InflowWind']['FileName_v']))
        f.write('"{:}"\n'.format(self.fst_vt['InflowWind']['FileName_w']))
        f.write('{:3}\n'.format(self.fst_vt['InflowWind']['nx']))
        f.write('{:3}\n'.format(self.fst_vt['InflowWind']['ny']))
        f.write('{:3}\n'.format(self.fst_vt['InflowWind']['nz']))
        f.write('{: 2.15e}\n'.format(self.fst_vt['InflowWind']['dx']))
        f.write('{: 2.15e}\n'.format(self.fst_vt['InflowWind']['dy']))
        f.write('{: 2.15e}\n'.format(self.fst_vt['InflowWind']['dz']))
        f.write('{: 2.15e}\n'.format(self.fst_vt['InflowWind']['RefHt']))
        f.write('---\n')
        f.write('{:3}\n'.format(self.fst_vt['InflowWind']['ScaleMethod']))
        f.write('{: 2.15e}\n'.format(self.fst_vt['InflowWind']['SFx']))
        f.write('{: 2.15e}\n'.format(self.fst_vt['InflowWind']['SFy']))
        f.write('{: 2.15e}\n'.format(self.fst_vt['InflowWind']['SFz']))
        f.write('{: 2.15e}\n'.format(self.fst_vt['InflowWind']['SigmaFx']))
        f.write('{: 2.15e}\n'.format(self.fst_vt['InflowWind']['SigmaFy']))
        f.write('{: 2.15e}\n'.format(self.fst_vt['InflowWind']['SigmaFz']))
        f.write('---\n')
        f.write('{: 2.15e}\n'.format(self.fst_vt['InflowWind']['URef']))
        f.write('{:3}\n'.format(self.fst_vt['InflowWind']['WindProfile']))
        f.write('{: 2.15e}\n'.format(self.fst_vt['InflowWind']['PLExp']))
        f.write('{: 2.15e}\n'.format(self.fst_vt['InflowWind']['Z0']))

        # InflowWind Output Parameters (inflow_out_params)
        f.write('---\n')
        f.write('{:}\n'.format(self.fst_vt['InflowWind']['SumPrint']))
        f.write('OutList\n')
        # No inflow wind outputs currently implemented in FAST 8
        f.write('END\n')


    # def WndWindWriter(self, wndfile):

    #     wind_file = os.path.join(self.FAST_runDirectory,wndfile)
    #     f = open(wind_file, 'w')

    #     for i in range(self.fst_vt['wnd_wind']['TimeSteps']):
    #         f.write('{: 2.15e}\t{: 2.15e}\t{: 2.15e}\t{: 2.15e}\t{: 2.15e}\t{: 2.15e}\t{: 2.15e}\t{: 2.15e}\n'.format(\
    #                   self.fst_vt['wnd_wind']['Time'][i], self.fst_vt['wnd_wind']['HorSpd'][i], self.fst_vt['wnd_wind']['WindDir'][i],\
    #                   self.fst_vt['wnd_wind']['VerSpd'][i], self.fst_vt['wnd_wind']['HorShr'][i],\
    #                   self.fst_vt['wnd_wind']['VerShr'][i], self.fst_vt['wnd_wind']['LnVShr'][i], self.fst_vt['wnd_wind']['GstSpd'][i]))

    #     f.close()


    def write_AeroDyn14(self):

        # ======= Airfoil Files ========
        # make directory for airfoil files
        if not os.path.isdir(os.path.join(self.FAST_runDirectory,'AeroData')):
            os.mkdir(os.path.join(self.FAST_runDirectory,'AeroData'))

        # create write airfoil objects to files
        for i in range(self.fst_vt['AeroDyn14']['NumFoil']):
             af_name = os.path.join(self.FAST_runDirectory, 'AeroData', 'Airfoil' + str(i) + '.dat')
             self.fst_vt['AeroDyn14']['FoilNm'][i]  = os.path.join('AeroData', 'Airfoil' + str(i) + '.dat')
             self.write_AeroDyn14Polar(af_name, i)

        self.fst_vt['Fst']['AeroFile'] = self.FAST_namingOut + '_AeroDyn14.dat'
        ad_file = os.path.join(self.FAST_runDirectory,self.fst_vt['Fst']['AeroFile'])
        f = open(ad_file,'w')

        # create Aerodyn Tower
        self.write_AeroDyn14Tower()

        # ======= Aerodyn Input File ========
        f.write('AeroDyn v14.04.* INPUT FILE\n\n')
        
        # f.write('{:}\n'.format(self.fst_vt['aerodyn']['SysUnits']))
        f.write('{:}\n'.format(self.fst_vt['AeroDyn14']['StallMod']))        
        
        f.write('{:}\n'.format(self.fst_vt['AeroDyn14']['UseCm']))
        f.write('{:}\n'.format(self.fst_vt['AeroDyn14']['InfModel']))
        f.write('{:}\n'.format(self.fst_vt['AeroDyn14']['IndModel']))
        f.write('{: 2.15e}\n'.format(self.fst_vt['AeroDyn14']['AToler']))
        f.write('{:}\n'.format(self.fst_vt['AeroDyn14']['TLModel']))
        f.write('{:}\n'.format(self.fst_vt['AeroDyn14']['HLModel']))
        f.write('{:}\n'.format(self.fst_vt['AeroDyn14']['TwrShad']))  
  
        f.write('{:}\n'.format(self.fst_vt['AeroDyn14']['TwrPotent']))  
  
        f.write('{:}\n'.format(self.fst_vt['AeroDyn14']['TwrShadow']))
        f.write('{:}\n'.format(self.fst_vt['AeroDyn14']['TwrFile']))
        f.write('{:}\n'.format(self.fst_vt['AeroDyn14']['CalcTwrAero']))  
  
        f.write('{: 2.15e}\n'.format(self.fst_vt['AeroDyn14']['AirDens']))  
  
        f.write('{: 2.15e}\n'.format(self.fst_vt['AeroDyn14']['KinVisc']))  
  
        f.write('{:2}\n'.format(self.fst_vt['AeroDyn14']['DTAero']))        
        

        f.write('{:2}\n'.format(self.fst_vt['AeroDynBlade']['NumFoil']))
        for i in range (self.fst_vt['AeroDynBlade']['NumFoil']):
            f.write('"{:}"\n'.format(self.fst_vt['AeroDynBlade']['FoilNm'][i]))

        f.write('{:2}\n'.format(self.fst_vt['AeroDynBlade']['BldNodes']))
        rnodes = self.fst_vt['AeroDynBlade']['RNodes']
        twist = self.fst_vt['AeroDynBlade']['AeroTwst']
        drnodes = self.fst_vt['AeroDynBlade']['DRNodes']
        chord = self.fst_vt['AeroDynBlade']['Chord']
        nfoil = self.fst_vt['AeroDynBlade']['NFoil']
        prnelm = self.fst_vt['AeroDynBlade']['PrnElm']
        f.write('Nodal properties\n')
        for r, t, dr, c, a, p in zip(rnodes, twist, drnodes, chord, nfoil, prnelm):
            f.write('{: 2.15e}\t{: 2.15e}\t{: 2.15e}\t{: 2.15e}\t{:5}\t{:}\n'.format(r, t, dr, c, a, p))

        f.close()        

    def write_AeroDyn14Tower(self):
        # AeroDyn v14.04 Tower
        self.fst_vt['AeroDyn14']['TwrFile'] = self.FAST_namingOut + '_AeroDyn14_tower.dat'
        filename = os.path.join(self.FAST_runDirectory, self.fst_vt['AeroDyn14']['TwrFile'])
        f = open(filename, 'w')

        f.write('AeroDyn tower file, Aerodyn v14.04 formatting\n')
        f.write('AeroElasticSE FAST driver\n')
        f.write('{:<22d} {:<11} {:}'.format(self.fst_vt['AeroDynTower']['NTwrHt'], 'NTwrHt', '- Number of tower input height stations listed (-)\n'))
        f.write('{:<22d} {:<11} {:}'.format(self.fst_vt['AeroDynTower']['NTwrRe'], 'NTwrRe', '- Number of tower Re values (-)\n'))
        f.write('{:<22d} {:<11} {:}'.format(self.fst_vt['AeroDynTower']['NTwrCD'], 'NTwrCD', '- Number of tower CD columns (-) Note: For current versions, this MUST be 1\n'))
        f.write('{: 2.15e} {:<11} {:}'.format(self.fst_vt['AeroDynTower']['Tower_Wake_Constant'], 'Tower_Wake_Constant', '- Tower wake constant (-) {0.0: full potential flow, 0.1: Bak model}\n'))
        f.write('---------------------- DISTRIBUTED TOWER PROPERTIES ----------------------------\n')
        f.write('TwrHtFr  TwrWid  NTwrCDCol\n')
        for HtFr, Wid, CDId in zip(self.fst_vt['AeroDynTower']['TwrHtFr'], self.fst_vt['AeroDynTower']['TwrWid'], self.fst_vt['AeroDynTower']['NTwrCDCol']):
            f.write('{: 2.15e}  {: 2.15e}   {:d}\n'.format(HtFr, Wid, int(CDId)))
        f.write('---------------------- Re v CD PROPERTIES --------------------------------------\n')
        f.write('TwrRe  '+ '  '.join(['TwrCD%d'%(i+1) for i in range(self.fst_vt['AeroDynTower']['NTwrCD'])]) +'\n')
        for Re, CD in zip(self.fst_vt['AeroDynTower']['TwrRe'], self.fst_vt['AeroDynTower']['TwrCD']):
            f.write('% 2.15e' %Re + '   '.join(['% 2.15e'%cdi for cdi in CD]) + '\n')

    def write_AeroDyn15(self):
        # AeroDyn v15.03

        # Generate AeroDyn v15 blade input file
        self.write_AeroDyn15Blade()

        # Generate AeroDyn v15 polars
        self.write_AeroDyn15Polar()


        # Generate AeroDyn v15.03 input file
        self.fst_vt['Fst']['AeroFile'] = self.FAST_namingOut + '_AeroDyn15.dat'
        ad_file = os.path.join(self.FAST_runDirectory, self.fst_vt['Fst']['AeroFile'])
        f = open(ad_file, 'w')

        f.write('------- AERODYN v15.03.* INPUT FILE ------------------------------------------------\n')
        f.write('AeroElasticSE FAST driver\n')
        f.write('======  General Options  ============================================================================\n')
        f.write('{!s:<22} {:<11} {:}'.format(self.fst_vt['AeroDyn15']['Echo'], 'Echo', '- Echo the input to "<rootname>.AD.ech"?  (flag)\n'))
        f.write('{:<22} {:<11} {:}'.format(self.fst_vt['AeroDyn15']['DTAero'], 'DTAero', '- Time interval for aerodynamic calculations {or "default"} (s)\n'))
        f.write('{:<22d} {:<11} {:}'.format(self.fst_vt['AeroDyn15']['WakeMod'], 'WakeMod', '- Type of wake/induction model (switch) {0=none, 1=BEMT}\n'))
        f.write('{:<22d} {:<11} {:}'.format(self.fst_vt['AeroDyn15']['AFAeroMod'], 'AFAeroMod', '- Type of blade airfoil aerodynamics model (switch) {1=steady model, 2=Beddoes-Leishman unsteady model} [must be 1 when linearizing]\n'))
        f.write('{:<22d} {:<11} {:}'.format(self.fst_vt['AeroDyn15']['TwrPotent'], 'TwrPotent', '- Type tower influence on wind based on potential flow around the tower (switch) {0=none, 1=baseline potential flow, 2=potential flow with Bak correction}\n'))
        f.write('{!s:<22} {:<11} {:}'.format(self.fst_vt['AeroDyn15']['TwrShadow'], 'TwrShadow', '- Calculate tower influence on wind based on downstream tower shadow? (flag)\n'))
        f.write('{!s:<22} {:<11} {:}'.format(self.fst_vt['AeroDyn15']['TwrAero'], 'TwrAero', '- Calculate tower aerodynamic loads? (flag)\n'))
        f.write('{!s:<22} {:<11} {:}'.format(self.fst_vt['AeroDyn15']['FrozenWake'], 'FrozenWake', '- Assume frozen wake during linearization? (flag) [used only when WakeMod=1 and when linearizing]\n'))
        if self.FAST_ver.lower() != 'fast8':
            f.write('{!s:<22} {:<11} {:}'.format(self.fst_vt['AeroDyn15']['CavitCheck'], 'CavitCheck', '- Perform cavitation check? (flag) TRUE will turn off unsteady aerodynamics\n'))
        f.write('======  Environmental Conditions  ===================================================================\n')
        f.write('{: 2.15e} {:<11} {:}'.format(self.fst_vt['AeroDyn15']['AirDens'], 'AirDens', '- Air density (kg/m^3)\n'))
        f.write('{: 2.15e} {:<11} {:}'.format(self.fst_vt['AeroDyn15']['KinVisc'], 'KinVisc', '- Kinematic air viscosity (m^2/s)\n'))
        f.write('{: 2.15e} {:<11} {:}'.format(self.fst_vt['AeroDyn15']['SpdSound'], 'SpdSound', '- Speed of sound (m/s)\n'))
        if self.FAST_ver.lower() != 'fast8':
            f.write('{: 2.15e} {:<11} {:}'.format(self.fst_vt['AeroDyn15']['Patm'], 'Patm', '- Atmospheric pressure (Pa) [used only when CavitCheck=True]\n'))
            f.write('{: 2.15e} {:<11} {:}'.format(self.fst_vt['AeroDyn15']['Pvap'], 'Pvap', '- Vapour pressure of fluid (Pa) [used only when CavitCheck=True]\n'))
            f.write('{: 2.15e} {:<11} {:}'.format(self.fst_vt['AeroDyn15']['FluidDepth'], 'FluidDepth', '- Water depth above mid-hub height (m) [used only when CavitCheck=True]\n'))
        f.write('======  Blade-Element/Momentum Theory Options  ====================================================== [used only when WakeMod=1]\n')
        f.write('{:<22d} {:<11} {:}'.format(self.fst_vt['AeroDyn15']['SkewMod'], 'SkewMod', '- Type of skewed-wake correction model (switch) {1=uncoupled, 2=Pitt/Peters, 3=coupled} [used only when WakeMod=1]\n'))
        f.write('{!s:<22} {:<11} {:}'.format(self.fst_vt['AeroDyn15']['TipLoss'], 'TipLoss', '- Use the Prandtl tip-loss model? (flag) [used only when WakeMod=1]\n'))
        f.write('{!s:<22} {:<11} {:}'.format(self.fst_vt['AeroDyn15']['HubLoss'], 'HubLoss', '- Use the Prandtl hub-loss model? (flag) [used only when WakeMod=1]\n'))
        f.write('{!s:<22} {:<11} {:}'.format(self.fst_vt['AeroDyn15']['TanInd'], 'TanInd', '- Include tangential induction in BEMT calculations? (flag) [used only when WakeMod=1]\n'))
        f.write('{!s:<22} {:<11} {:}'.format(self.fst_vt['AeroDyn15']['AIDrag'], 'AIDrag', '- Include the drag term in the axial-induction calculation? (flag) [used only when WakeMod=1]\n'))
        f.write('{!s:<22} {:<11} {:}'.format(self.fst_vt['AeroDyn15']['TIDrag'], 'TIDrag', '- Include the drag term in the tangential-induction calculation? (flag) [used only when WakeMod=1 and TanInd=TRUE]\n'))
        f.write('{:<22} {:<11} {:}'.format(self.fst_vt['AeroDyn15']['IndToler'], 'IndToler', '- Convergence tolerance for BEMT nonlinear solve residual equation {or "default"} (-) [used only when WakeMod=1]\n'))
        f.write('{:<22d} {:<11} {:}'.format(self.fst_vt['AeroDyn15']['MaxIter'], 'MaxIter', '- Maximum number of iteration steps (-) [used only when WakeMod=1]\n'))
        f.write('======  Beddoes-Leishman Unsteady Airfoil Aerodynamics Options  ===================================== [used only when AFAeroMod=2]\n')
        f.write('{:<22d} {:<11} {:}'.format(self.fst_vt['AeroDyn15']['UAMod'], 'UAMod', "Unsteady Aero Model Switch (switch) {1=Baseline model (Original), 2=Gonzalez's variant (changes in Cn,Cc,Cm), 3=Minemma/Pierce variant (changes in Cc and Cm)} [used only when AFAeroMod=2]\n"))
        f.write('{!s:<22} {:<11} {:}'.format(self.fst_vt['AeroDyn15']['FLookup'], 'FLookup', "Flag to indicate whether a lookup for f' will be calculated (TRUE) or whether best-fit exponential equations will be used (FALSE); if FALSE S1-S4 must be provided in airfoil input files (flag) [used only when AFAeroMod=2]\n"))
        f.write('======  Airfoil Information =========================================================================\n')
        f.write('{:<22d} {:<11} {:}'.format(self.fst_vt['AeroDyn15']['InCol_Alfa'], 'InCol_Alfa', '- The column in the airfoil tables that contains the angle of attack (-)\n'))
        f.write('{:<22d} {:<11} {:}'.format(self.fst_vt['AeroDyn15']['InCol_Cl'], 'InCol_Cl', '- The column in the airfoil tables that contains the lift coefficient (-)\n'))
        f.write('{:<22d} {:<11} {:}'.format(self.fst_vt['AeroDyn15']['InCol_Cd'], 'InCol_Cd', '- The column in the airfoil tables that contains the drag coefficient (-)\n'))
        f.write('{:<22d} {:<11} {:}'.format(self.fst_vt['AeroDyn15']['InCol_Cm'], 'InCol_Cm', '- The column in the airfoil tables that contains the pitching-moment coefficient; use zero if there is no Cm column (-)\n'))
        f.write('{:<22d} {:<11} {:}'.format(self.fst_vt['AeroDyn15']['InCol_Cpmin'], 'InCol_Cpmin', '- The column in the airfoil tables that contains the Cpmin coefficient; use zero if there is no Cpmin column (-)\n'))
        f.write('{:<22d} {:<11} {:}'.format(self.fst_vt['AeroDyn15']['NumAFfiles'], 'NumAFfiles', '- Number of airfoil files used (-)\n'))
        for i in range(self.fst_vt['AeroDyn15']['NumAFfiles']):
            if i == 0:
                f.write('"' + self.fst_vt['AeroDyn15']['AFNames'][i] + '"    AFNames            - Airfoil file names (NumAFfiles lines) (quoted strings)\n')
            else:
                f.write('"' + self.fst_vt['AeroDyn15']['AFNames'][i] + '"\n')
        f.write('======  Rotor/Blade Properties  =====================================================================\n')
        f.write('{!s:<22} {:<11} {:}'.format(self.fst_vt['AeroDyn15']['UseBlCm'], 'UseBlCm', '- Include aerodynamic pitching moment in calculations?  (flag)\n'))
        f.write('"{:<22}" {:<11} {:}'.format(self.fst_vt['AeroDyn15']['ADBlFile1'], 'ADBlFile(1)', '- Name of file containing distributed aerodynamic properties for Blade #1 (-)\n'))
        f.write('"{:<22}" {:<11} {:}'.format(self.fst_vt['AeroDyn15']['ADBlFile2'], 'ADBlFile(2)', '- Name of file containing distributed aerodynamic properties for Blade #2 (-) [unused if NumBl < 2]\n'))
        f.write('"{:<22}" {:<11} {:}'.format(self.fst_vt['AeroDyn15']['ADBlFile3'], 'ADBlFile(3)', '- Name of file containing distributed aerodynamic properties for Blade #3 (-) [unused if NumBl < 3]\n'))
        f.write('======  Tower Influence and Aerodynamics ============================================================= [used only when TwrPotent/=0, TwrShadow=True, or TwrAero=True]\n')
        f.write('{:<22d} {:<11} {:}'.format(self.fst_vt['AeroDyn15']['NumTwrNds'], 'NumTwrNds', '- Number of tower nodes used in the analysis  (-) [used only when TwrPotent/=0, TwrShadow=True, or TwrAero=True]\n'))
        f.write('TwrElev        TwrDiam        TwrCd\n')
        f.write('(m)              (m)           (-)\n')
        for TwrElev, TwrDiam, TwrCd in zip(self.fst_vt['AeroDyn15']['TwrElev'], self.fst_vt['AeroDyn15']['TwrDiam'], self.fst_vt['AeroDyn15']['TwrCd']):
            f.write('{: 2.15e} {: 2.15e} {: 2.15e} \n'.format(TwrElev, TwrDiam, TwrCd))
        f.write('======  Tower Influence and Aerodynamics ============================================================= [used only when TwrPotent/=0, TwrShadow=True, or TwrAero=True]\n')
        f.write('{!s:<22} {:<11} {:}'.format(self.fst_vt['AeroDyn15']['SumPrint'], 'SumPrint', '- Generate a summary file listing input options and interpolated properties to "<rootname>.AD.sum"?  (flag)\n'))
        f.write('{:<22d} {:<11} {:}'.format(self.fst_vt['AeroDyn15']['NBlOuts'], 'NBlOuts', '- Number of blade node outputs [0 - 9] (-)\n'))
        f.write('{:<22} {:<11} {:}'.format(', '.join(self.fst_vt['AeroDyn15']['BlOutNd']), 'BlOutNd', '- Blade nodes whose values will be output  (-)\n'))
        f.write('{:<22d} {:<11} {:}'.format(self.fst_vt['AeroDyn15']['NTwOuts'], 'NTwOuts', '- Number of tower node outputs [0 - 9]  (-)\n'))
        f.write('{:<22} {:<11} {:}'.format(', '.join(self.fst_vt['AeroDyn15']['TwOutNd']), 'TwOutNd', '- Tower nodes whose values will be output  (-)\n'))
        f.write('                   OutList             - The next line(s) contains a list of output parameters.  See OutListParameters.xlsx for a listing of available output channels, (-)\n')

        outlist = self.get_outlist(self.fst_vt['outlist'], ['AeroDyn'])
        for channel_list in outlist:
            f.write('"' + ', '.join(channel_list) + '"\n')
        f.write('END of input file (the word "END" must appear in the first 3 columns of this last OutList line)\n')
        f.write('---------------------------------------------------------------------------------------\n')
        f.close()

    def write_AeroDyn15Blade(self):
        # AeroDyn v15.00 Blade
        self.fst_vt['AeroDyn15']['ADBlFile1'] = self.FAST_namingOut + '_AeroDyn15_blade.dat'
        self.fst_vt['AeroDyn15']['ADBlFile2'] = self.fst_vt['AeroDyn15']['ADBlFile1']
        self.fst_vt['AeroDyn15']['ADBlFile3'] = self.fst_vt['AeroDyn15']['ADBlFile1']
        filename = os.path.join(self.FAST_runDirectory, self.fst_vt['AeroDyn15']['ADBlFile1'])
        f = open(filename, 'w')

        f.write('------- AERODYN v15.00.* BLADE DEFINITION INPUT FILE -------------------------------------\n')
        f.write('AeroElasticSE FAST driver\n')
        f.write('======  Blade Properties =================================================================\n')
        f.write('{:<11d} {:<11} {:}'.format(self.fst_vt['AeroDynBlade']['NumBlNds'], 'NumBlNds', '- Number of blade nodes used in the analysis (-)\n'))
        f.write('    BlSpn        BlCrvAC        BlSwpAC        BlCrvAng       BlTwist        BlChord          BlAFID\n')
        f.write('     (m)           (m)            (m)            (deg)         (deg)           (m)              (-)\n')
        BlSpn    = self.fst_vt['AeroDynBlade']['BlSpn']
        BlCrvAC  = self.fst_vt['AeroDynBlade']['BlCrvAC']
        BlSwpAC  = self.fst_vt['AeroDynBlade']['BlSwpAC']
        BlCrvAng = self.fst_vt['AeroDynBlade']['BlCrvAng']
        BlTwist  = self.fst_vt['AeroDynBlade']['BlTwist']
        BlChord  = self.fst_vt['AeroDynBlade']['BlChord']
        BlAFID   = self.fst_vt['AeroDynBlade']['BlAFID']
        for Spn, CrvAC, SwpAC, CrvAng, Twist, Chord, AFID in zip(BlSpn, BlCrvAC, BlSwpAC, BlCrvAng, BlTwist, BlChord, BlAFID):
            f.write('{: 2.15e} {: 2.15e} {: 2.15e} {: 2.15e} {: 2.15e} {: 2.15e} {: 8d}\n'.format(Spn, CrvAC, SwpAC, CrvAng, Twist, Chord, int(AFID)))

    def write_AeroDyn15Polar(self):
        # Airfoil Info v1.01
        # TODO: Coordinates file not supported currently

        def float_default_out(val):
            # formatted float output when 'default' is an option
            if type(val) is float:
                return '{: 22f}'.format(val)
            else:
                return '{:<22}'.format(val)

        if not os.path.isdir(os.path.join(self.FAST_runDirectory,'Airfoils')):
            os.mkdir(os.path.join(self.FAST_runDirectory,'Airfoils'))

        for afi, af_filename in enumerate(self.fst_vt['AeroDyn15']['AFNames']):

            self.fst_vt['AeroDyn15']['AFNames'][afi] = os.path.join('Airfoils', self.FAST_namingOut + '_AeroDyn15_Polar_%02d.dat'%afi)
            af_file = os.path.join(self.FAST_runDirectory, self.fst_vt['AeroDyn15']['AFNames'][afi])
            f = open(af_file, 'w')

            f.write('! ------------ AirfoilInfo v1.01.x Input File ----------------------------------\n')
            f.write('! AeroElasticSE FAST driver\n')
            f.write('! line\n')
            f.write('! line\n')
            f.write('! ------------------------------------------------------------------------------\n')
            f.write('{:<22}   {:<11} {:}'.format(self.fst_vt['AeroDyn15']['af_data'][afi]['InterpOrd'], 'InterpOrd', '! Interpolation order to use for quasi-steady table lookup {1=linear; 3=cubic spline; "default"} [default=3]\n'))
            f.write('{:<22d}   {:<11} {:}'.format(self.fst_vt['AeroDyn15']['af_data'][afi]['NonDimArea'], 'NonDimArea', '! The non-dimensional area of the airfoil (area/chord^2) (set to 1.0 if unsure or unneeded)\n'))
            f.write('{:<22}   {:<11} {:}'.format(0, 'NumCoords', '! The number of coordinates in the airfoil shape file.  Set to zero if coordinates not included.\n'))
            f.write('{:<22d}   {:<11} {:}'.format(self.fst_vt['AeroDyn15']['af_data'][afi]['NumTabs'], 'NumTabs', '! Number of airfoil tables in this file.  Each table must have lines for Re and Ctrl.\n'))
            f.write('! ------------------------------------------------------------------------------\n')
            f.write('! data for table 1\n')
            f.write('! ------------------------------------------------------------------------------\n')
            f.write('{: 22f}   {:<11} {:}'.format(self.fst_vt['AeroDyn15']['af_data'][afi]['Re'], 'Re', '! Reynolds number in millions\n'))
            f.write('{:<22d}   {:<11} {:}'.format(self.fst_vt['AeroDyn15']['af_data'][afi]['Ctrl'], 'Ctrl', '! Control setting (must be 0 for current AirfoilInfo)\n'))
            f.write('{!s:<22}   {:<11} {:}'.format(self.fst_vt['AeroDyn15']['af_data'][afi]['InclUAdata'], 'InclUAdata', '! Is unsteady aerodynamics data included in this table? If TRUE, then include 30 UA coefficients below this line\n'))
            f.write('!........................................\n')
            if self.fst_vt['AeroDyn15']['af_data'][afi]['InclUAdata']:
                f.write('{: 22f}   {:<11} {:}'.format(self.fst_vt['AeroDyn15']['af_data'][afi]['alpha0'], 'alpha0', '! 0-lift angle of attack, depends on airfoil.\n'))
                f.write('{: 22f}   {:<11} {:}'.format(self.fst_vt['AeroDyn15']['af_data'][afi]['alpha1'], 'alpha1', '! Angle of attack at f=0.7, (approximately the stall angle) for AOA>alpha0. (deg)\n'))
                f.write('{: 22f}   {:<11} {:}'.format(self.fst_vt['AeroDyn15']['af_data'][afi]['alpha2'], 'alpha2', '! Angle of attack at f=0.7, (approximately the stall angle) for AOA<alpha0. (deg)\n'))
                f.write('{: 22f}   {:<11} {:}'.format(self.fst_vt['AeroDyn15']['af_data'][afi]['eta_e'], 'eta_e', '! Recovery factor in the range [0.85 - 0.95] used only for UAMOD=1, it is set to 1 in the code when flookup=True. (-)\n'))
                f.write('{: 22f}   {:<11} {:}'.format(self.fst_vt['AeroDyn15']['af_data'][afi]['C_nalpha'], 'C_nalpha', '! Slope of the 2D normal force coefficient curve. (1/rad)\n'))
                f.write(float_default_out(self.fst_vt['AeroDyn15']['af_data'][afi]['T_f0']) + '   {:<11} {:}'.format('T_f0', '! Initial value of the time constant associated with Df in the expression of Df and f''. [default = 3]\n'))
                f.write(float_default_out(self.fst_vt['AeroDyn15']['af_data'][afi]['T_V0']) + '   {:<11} {:}'.format('T_V0', '! Initial value of the time constant associated with the vortex lift decay process; it is used in the expression of Cvn. It depends on Re,M, and airfoil class. [default = 6]\n'))
                f.write(float_default_out(self.fst_vt['AeroDyn15']['af_data'][afi]['T_p']) + '   {:<11} {:}'.format('T_p', '! Boundary-layer,leading edge pressure gradient time constant in the expression of Dp. It should be tuned based on airfoil experimental data. [default = 1.7]\n'))
                f.write(float_default_out(self.fst_vt['AeroDyn15']['af_data'][afi]['T_VL']) + '   {:<11} {:}'.format('T_VL', '! Initial value of the time constant associated with the vortex advection process; it represents the non-dimensional time in semi-chords, needed for a vortex to travel from LE to trailing edge (TE); it is used in the expression of Cvn. It depends on Re, M (weakly), and airfoil. [valid range = 6 - 13, default = 11]\n'))
                f.write(float_default_out(self.fst_vt['AeroDyn15']['af_data'][afi]['b1']) + '   {:<11} {:}'.format('b1', '! Constant in the expression of phi_alpha^c and phi_q^c.  This value is relatively insensitive for thin airfoils, but may be different for turbine airfoils. [from experimental results, defaults to 0.14]\n'))
                f.write(float_default_out(self.fst_vt['AeroDyn15']['af_data'][afi]['b2']) + '   {:<11} {:}'.format('b2', '! Constant in the expression of phi_alpha^c and phi_q^c.  This value is relatively insensitive for thin airfoils, but may be different for turbine airfoils. [from experimental results, defaults to 0.53]\n'))
                f.write(float_default_out(self.fst_vt['AeroDyn15']['af_data'][afi]['b5']) + '   {:<11} {:}'.format('b5', "! Constant in the expression of K'''_q,Cm_q^nc, and k_m,q.  [from  experimental results, defaults to 5]\n"))
                f.write(float_default_out(self.fst_vt['AeroDyn15']['af_data'][afi]['A1']) + '   {:<11} {:}'.format('A1', '! Constant in the expression of phi_alpha^c and phi_q^c.  This value is relatively insensitive for thin airfoils, but may be different for turbine airfoils. [from experimental results, defaults to 0.3]\n'))
                f.write(float_default_out(self.fst_vt['AeroDyn15']['af_data'][afi]['A2']) + '   {:<11} {:}'.format('A2', '! Constant in the expression of phi_alpha^c and phi_q^c.  This value is relatively insensitive for thin airfoils, but may be different for turbine airfoils. [from experimental results, defaults to 0.7]\n'))
                f.write(float_default_out(self.fst_vt['AeroDyn15']['af_data'][afi]['A5']) + '   {:<11} {:}'.format('A5', "! Constant in the expression of K'''_q,Cm_q^nc, and k_m,q. [from experimental results, defaults to 1]\n"))
                f.write('{: 22f}   {:<11} {:}'.format(self.fst_vt['AeroDyn15']['af_data'][afi]['S1'], 'S1', '! Constant in the f curve best-fit for alpha0<=AOA<=alpha1; by definition it depends on the airfoil. [ignored if UAMod<>1]\n'))
                f.write('{: 22f}   {:<11} {:}'.format(self.fst_vt['AeroDyn15']['af_data'][afi]['S2'], 'S2', '! Constant in the f curve best-fit for         AOA> alpha1; by definition it depends on the airfoil. [ignored if UAMod<>1]\n'))
                f.write('{: 22f}   {:<11} {:}'.format(self.fst_vt['AeroDyn15']['af_data'][afi]['S3'], 'S3', '! Constant in the f curve best-fit for alpha2<=AOA< alpha0; by definition it depends on the airfoil. [ignored if UAMod<>1]\n'))
                f.write('{: 22f}   {:<11} {:}'.format(self.fst_vt['AeroDyn15']['af_data'][afi]['S4'], 'S4', '! Constant in the f curve best-fit for         AOA< alpha2; by definition it depends on the airfoil. [ignored if UAMod<>1]\n'))
                f.write('{: 22f}   {:<11} {:}'.format(self.fst_vt['AeroDyn15']['af_data'][afi]['Cn1'], 'Cn1', '! Critical value of C0n at leading edge separation. It should be extracted from airfoil data at a given Mach and Reynolds number. It can be calculated from the static value of Cn at either the break in the pitching moment or the loss of chord force at the onset of stall. It is close to the condition of maximum lift of the airfoil at low Mach numbers.\n'))
                f.write('{: 22f}   {:<11} {:}'.format(self.fst_vt['AeroDyn15']['af_data'][afi]['Cn2'], 'Cn2', '! As Cn1 for negative AOAs.\n'))
                f.write('{: 22f}   {:<11} {:}'.format(self.fst_vt['AeroDyn15']['af_data'][afi]['St_sh'], 'St_sh', "! Strouhal's shedding frequency constant.  [default = 0.19]\n"))
                f.write('{: 22f}   {:<11} {:}'.format(self.fst_vt['AeroDyn15']['af_data'][afi]['Cd0'], 'Cd0', '! 2D drag coefficient value at 0-lift.\n'))
                f.write('{: 22f}   {:<11} {:}'.format(self.fst_vt['AeroDyn15']['af_data'][afi]['Cm0'], 'Cm0', '! 2D pitching moment coefficient about 1/4-chord location, at 0-lift, positive if nose up. [If the aerodynamics coefficients table does not include a column for Cm, this needs to be set to 0.0]\n'))
                f.write('{: 22f}   {:<11} {:}'.format(self.fst_vt['AeroDyn15']['af_data'][afi]['k0'], 'k0', '! Constant in the \\hat(x)_cp curve best-fit; = (\\hat(x)_AC-0.25).  [ignored if UAMod<>1]\n'))
                f.write('{: 22f}   {:<11} {:}'.format(self.fst_vt['AeroDyn15']['af_data'][afi]['k1'], 'k1', '! Constant in the \\hat(x)_cp curve best-fit.  [ignored if UAMod<>1]\n'))
                f.write('{: 22f}   {:<11} {:}'.format(self.fst_vt['AeroDyn15']['af_data'][afi]['k2'], 'k2', '! Constant in the \\hat(x)_cp curve best-fit.  [ignored if UAMod<>1]\n'))
                f.write('{: 22f}   {:<11} {:}'.format(self.fst_vt['AeroDyn15']['af_data'][afi]['k3'], 'k3', '! Constant in the \\hat(x)_cp curve best-fit.  [ignored if UAMod<>1]\n'))
                f.write('{: 22f}   {:<11} {:}'.format(self.fst_vt['AeroDyn15']['af_data'][afi]['k1_hat'], 'k1_hat', '! Constant in the expression of Cc due to leading edge vortex effects.  [ignored if UAMod<>1]\n'))
                f.write(float_default_out(self.fst_vt['AeroDyn15']['af_data'][afi]['x_cp_bar']) + '   {:<11} {:}'.format('x_cp_bar', '! Constant in the expression of \\hat(x)_cp^v. [ignored if UAMod<>1, default = 0.2]\n'))
                f.write(float_default_out(self.fst_vt['AeroDyn15']['af_data'][afi]['UACutout']) + '   {:<11} {:}'.format('UACutout', '! Angle of attack above which unsteady aerodynamics are disabled (deg). [Specifying the string "Default" sets UACutout to 45 degrees]\n'))
                f.write(float_default_out(self.fst_vt['AeroDyn15']['af_data'][afi]['filtCutOff']) + '   {:<11} {:}'.format('filtCutOff', '! Cut-off frequency (-3 dB corner frequency) for low-pass filtering the AoA input to UA, as well as the 1st and 2nd derivatives (Hz) [default = 20]\n'))

            f.write('!........................................\n')
            f.write('! Table of aerodynamics coefficients\n')
            f.write('"{:<22d}"   {:<11} {:}'.format(self.fst_vt['AeroDyn15']['af_data'][afi]['NumAlf'], 'NumAlf', '! Number of data lines in the following table\n'))
            f.write('!    Alpha      Cl      Cd        Cm\n')
            f.write('!    (deg)      (-)     (-)       (-)\n')

            polar_map = [self.fst_vt['AeroDyn15']['InCol_Alfa'], self.fst_vt['AeroDyn15']['InCol_Cl'], self.fst_vt['AeroDyn15']['InCol_Cd'], self.fst_vt['AeroDyn15']['InCol_Cm'], self.fst_vt['AeroDyn15']['InCol_Cpmin']]
            polar_map.remove(0)
            polar_map = [i-1 for i in polar_map]

            alpha = np.asarray(self.fst_vt['AeroDyn15']['af_data'][afi]['Alpha'])
            cl = np.asarray(self.fst_vt['AeroDyn15']['af_data'][afi]['Cl'])
            cd = np.asarray(self.fst_vt['AeroDyn15']['af_data'][afi]['Cd'])
            cm = np.asarray(self.fst_vt['AeroDyn15']['af_data'][afi]['Cm'])
            cpmin = np.asarray(self.fst_vt['AeroDyn15']['af_data'][afi]['Cpmin'])
            polar = np.column_stack((alpha, cl, cd, cm, cpmin))
            polar = polar[:,polar_map]


            for row in polar:
                f.write(' '.join(['{: 2.15e}'.format(val) for val in row])+'\n')


    def write_ServoDyn(self):
        # ServoDyn v1.05 Input File

        self.fst_vt['Fst']['ServoFile'] = self.FAST_namingOut + '_ServoDyn.dat'
        sd_file = os.path.join(self.FAST_runDirectory,self.fst_vt['Fst']['ServoFile'])
        f = open(sd_file,'w')

        f.write('---\n')
        f.write('---\n')
        
        # ServoDyn Simulation Control (sd_sim_ctrl)
        f.write('---\n')
        f.write('{:}\n'.format(self.fst_vt['ServoDyn']['Echo']))
        auto_format(f, self.fst_vt['ServoDyn']['DT'])

        # Pitch Control (pitch_ctrl)
        f.write('---\n')
        f.write('{:3}\n'.format(self.fst_vt['ServoDyn']['PCMode']))
        f.write('{:.9f}\n'.format(self.fst_vt['ServoDyn']['TPCOn']))
        f.write('{:.9f}\n'.format(self.fst_vt['ServoDyn']['TPitManS1']))
        f.write('{:.9f}\n'.format(self.fst_vt['ServoDyn']['TPitManS2']))
        f.write('{:.9f}\n'.format(self.fst_vt['ServoDyn']['TPitManS3']))
        f.write('{:.9f}\n'.format(self.fst_vt['ServoDyn']['PitManRat1']))
        f.write('{:.9f}\n'.format(self.fst_vt['ServoDyn']['PitManRat2']))
        f.write('{:.9f}\n'.format(self.fst_vt['ServoDyn']['PitManRat3']))
        f.write('{:.9f}\n'.format(self.fst_vt['ServoDyn']['BlPitchF1']))
        f.write('{:.9f}\n'.format(self.fst_vt['ServoDyn']['BlPitchF2']))
        f.write('{:.9f}\n'.format(self.fst_vt['ServoDyn']['BlPitchF3']))

        # Generator and Torque Control (gen_torq_ctrl)
        f.write('---\n')
        f.write('{:3}\n'.format(self.fst_vt['ServoDyn']['VSContrl']))
        f.write('{:3}\n'.format(self.fst_vt['ServoDyn']['GenModel']))
        f.write('{:.9f}\n'.format(self.fst_vt['ServoDyn']['GenEff']))
        f.write('{:}\n'.format(self.fst_vt['ServoDyn']['GenTiStr']))
        f.write('{:}\n'.format(self.fst_vt['ServoDyn']['GenTiStp']))
        f.write('{:.9f}\n'.format(self.fst_vt['ServoDyn']['SpdGenOn']))
        f.write('{:.9f}\n'.format(self.fst_vt['ServoDyn']['TimGenOn']))
        f.write('{:.9f}\n'.format(self.fst_vt['ServoDyn']['TimGenOf']))

        # Simple Variable-Speed Torque Control (var_speed_torq_ctrl)
        f.write('---\n')
        f.write('{:.9f}\n'.format(self.fst_vt['ServoDyn']['VS_RtGnSp']))
        f.write('{:.9f}\n'.format(self.fst_vt['ServoDyn']['VS_RtTq']))
        f.write('{:.9f}\n'.format(self.fst_vt['ServoDyn']['VS_Rgn2K']))
        f.write('{:.5e}\n'.format(self.fst_vt['ServoDyn']['VS_SlPc']))

        # Simple Induction Generator (induct_gen)
        f.write('---\n')
        f.write('{:.9f}\n'.format(self.fst_vt['ServoDyn']['SIG_SlPc']))
        f.write('{:.9f}\n'.format(self.fst_vt['ServoDyn']['SIG_SySp']))
        f.write('{:.9f}\n'.format(self.fst_vt['ServoDyn']['SIG_RtTq']))
        f.write('{:.9f}\n'.format(self.fst_vt['ServoDyn']['SIG_PORt']))

        # Thevenin-Equivalent Induction Generator (theveq_induct_gen)
        f.write('---\n')
        f.write('{:.9f}\n'.format(self.fst_vt['ServoDyn']['TEC_Freq']))
        f.write('{:3}\n'.format(self.fst_vt['ServoDyn']['TEC_NPol']))
        f.write('{:.9f}\n'.format(self.fst_vt['ServoDyn']['TEC_SRes']))
        f.write('{:.9f}\n'.format(self.fst_vt['ServoDyn']['TEC_RRes']))
        f.write('{:.9f}\n'.format(self.fst_vt['ServoDyn']['TEC_VLL']))
        f.write('{:.9f}\n'.format(self.fst_vt['ServoDyn']['TEC_SLR']))
        f.write('{:.9f}\n'.format(self.fst_vt['ServoDyn']['TEC_RLR']))
        f.write('{:.9f}\n'.format(self.fst_vt['ServoDyn']['TEC_MR']))

        # High-Speed Shaft Brake (shaft_brake)
        f.write('---\n')
        f.write('{:3}\n'.format(self.fst_vt['ServoDyn']['HSSBrMode']))
        f.write('{:.9f}\n'.format(self.fst_vt['ServoDyn']['THSSBrDp']))
        f.write('{:.9f}\n'.format(self.fst_vt['ServoDyn']['HSSBrDT']))
        f.write('{:.9f}\n'.format(self.fst_vt['ServoDyn']['HSSBrTqF']))

        # Nacelle-Yaw Control (nac_yaw_ctrl)
        f.write('---\n')
        f.write('{:3}\n'.format(self.fst_vt['ServoDyn']['YCMode']))
        f.write('{:.9f}\n'.format(self.fst_vt['ServoDyn']['TYCOn']))
        f.write('{:.9f}\n'.format(self.fst_vt['ServoDyn']['YawNeut']))
        f.write('{:.9f}\n'.format(self.fst_vt['ServoDyn']['YawSpr']))
        f.write('{:.9f}\n'.format(self.fst_vt['ServoDyn']['YawDamp']))
        f.write('{:.9f}\n'.format(self.fst_vt['ServoDyn']['TYawManS']))
        f.write('{:.9f}\n'.format(self.fst_vt['ServoDyn']['YawManRat']))
        f.write('{:.9f}\n'.format(self.fst_vt['ServoDyn']['NacYawF']))

        # Tuned Mass Damper (tuned_mass_damper)
        f.write('---\n')
        f.write('{:}\n'.format(self.fst_vt['ServoDyn']['CompNTMD']))
        f.write('"{:}"\n'.format(self.fst_vt['ServoDyn']['NTMDfile']))
        f.write('{:}\n'.format(self.fst_vt['ServoDyn']['CompTTMD']))
        f.write('"{:}"\n'.format(self.fst_vt['ServoDyn']['TTMDfile']))

        # Bladed Interface (bladed_interface)
        f.write('---\n')
        # self.fst_vt['ServoDyn']['DLL_FileName'] = os.path.relpath(self.fst_vt['ServoDyn']['DLL_FileName'], self.FAST_runDirectory)
        f.write('"{:}"\n'.format(self.fst_vt['ServoDyn']['DLL_FileName']))
        f.write('"{:}"\n'.format(self.fst_vt['ServoDyn']['DLL_InFile']))
        f.write('"{:}"\n'.format(self.fst_vt['ServoDyn']['DLL_ProcName']))
        auto_format(f, self.fst_vt['ServoDyn']['DLL_DT'])
        f.write('{:}\n'.format(self.fst_vt['ServoDyn']['DLL_Ramp']))
        f.write('{:.9f}\n'.format(self.fst_vt['ServoDyn']['BPCutoff']))
        f.write('{:.9f}\n'.format(self.fst_vt['ServoDyn']['NacYaw_North']))
        f.write('{:3}\n'.format(self.fst_vt['ServoDyn']['Ptch_Cntrl']))
        f.write('{:.9f}\n'.format(self.fst_vt['ServoDyn']['Ptch_SetPnt']))
        f.write('{:.9f}\n'.format(self.fst_vt['ServoDyn']['Ptch_Min']))
        f.write('{:.9f}\n'.format(self.fst_vt['ServoDyn']['Ptch_Max']))
        f.write('{:.9f}\n'.format(self.fst_vt['ServoDyn']['PtchRate_Min']))
        f.write('{:.9f}\n'.format(self.fst_vt['ServoDyn']['PtchRate_Max']))
        f.write('{:.9f}\n'.format(self.fst_vt['ServoDyn']['Gain_OM']))
        f.write('{:.9f}\n'.format(self.fst_vt['ServoDyn']['GenSpd_MinOM']))
        f.write('{:.9f}\n'.format(self.fst_vt['ServoDyn']['GenSpd_MaxOM']))
        f.write('{:.9f}\n'.format(self.fst_vt['ServoDyn']['GenSpd_Dem']))
        f.write('{:.9f}\n'.format(self.fst_vt['ServoDyn']['GenTrq_Dem']))
        f.write('{:.9f}\n'.format(self.fst_vt['ServoDyn']['GenPwr_Dem']))

        # Bladed Interface Torque-Speed Look-Up Table (bladed_interface)
        f.write('---\n')
        f.write('{:3}\n'.format(self.fst_vt['ServoDyn']['DLL_NumTrq']))
        f.write('---\n')
        f.write('---\n')
        for i in range(self.fst_vt['ServoDyn']['DLL_NumTrq']):
            a1 = self.fst_vt['ServoDyn']['GenSpd_TLU'][i]
            a2 = self.fst_vt['ServoDyn']['GenTrq_TLU'][i]
            f.write('{:.9f}\t{:.9f}\n'.format(a1, a2))

        # ServoDyn Output Params (sd_out_params)
        f.write('---\n')
        f.write('{:}\n'.format(self.fst_vt['ServoDyn']['SumPrint']))
        f.write('{:3}\n'.format(self.fst_vt['ServoDyn']['OutFile']))
        f.write('{:}\n'.format(self.fst_vt['ServoDyn']['TabDelim']))
        f.write('"{:}"\n'.format(self.fst_vt['ServoDyn']['OutFmt']))
        f.write('{:.9f}\n'.format(self.fst_vt['ServoDyn']['TStart']))

        # ======== OutList =====
        f.write('Outlist\n')
        outlist = self.get_outlist(self.fst_vt['outlist'], ['ServoDyn'])
        for channel_list in outlist:
            f.write('"' + ', '.join(channel_list) + '"\n')
        f.write('END\n')
        f.close()

class InputWriter_FAST7(InputWriter_Common):

    def execute(self):
        
        if not os.path.exists(self.FAST_runDirectory):
            os.makedirs(self.FAST_runDirectory)

        # self.write_WindWnd()
        self.write_ElastoDynBlade()
        self.write_ElastoDynTower()
        self.write_AeroDyn_FAST7()

        self.write_MainInput()

    def write_MainInput(self):

        self.FAST_InputFileOut = os.path.join(self.FAST_runDirectory, self.FAST_namingOut+'.fst')
        ofh = open(self.FAST_InputFileOut, 'w')

        # FAST Inputs
        ofh.write('---\n')
        ofh.write('---\n')
        ofh.write('{:}\n'.format(self.fst_vt['description']))
        ofh.write('---\n')
        ofh.write('---\n')
        ofh.write('{:}\n'.format(self.fst_vt['Fst7']['Echo']))
        ofh.write('{:3}\n'.format(self.fst_vt['Fst7']['ADAMSPrep']))
        ofh.write('{:3}\n'.format(self.fst_vt['Fst7']['AnalMode']))
        ofh.write('{:3}\n'.format(self.fst_vt['Fst7']['NumBl']))
        ofh.write('{:.9f}\n'.format(self.fst_vt['Fst7']['TMax']))
        ofh.write('{:.9f}\n'.format(self.fst_vt['Fst7']['DT']))
        ofh.write('---\n')
        ofh.write('{:3}\n'.format(self.fst_vt['Fst7']['YCMode']))
        ofh.write('{:.9f}\n'.format(self.fst_vt['Fst7']['TYCOn']))
        ofh.write('{:3}\n'.format(self.fst_vt['Fst7']['PCMode']))
        ofh.write('{:.9f}\n'.format(self.fst_vt['Fst7']['TPCOn']))
        ofh.write('{:3}\n'.format(self.fst_vt['Fst7']['VSContrl']))
        ofh.write('{:.9f}\n'.format(self.fst_vt['Fst7']['VS_RtGnSp']))
        ofh.write('{:.9f}\n'.format(self.fst_vt['Fst7']['VS_RtTq']))
        ofh.write('{:.9f}\n'.format(self.fst_vt['Fst7']['VS_Rgn2K']))
        ofh.write('{:.5e}\n'.format(self.fst_vt['Fst7']['VS_SlPc']))
        ofh.write('{:3}\n'.format(self.fst_vt['Fst7']['GenModel']))
        ofh.write('{:}\n'.format(self.fst_vt['Fst7']['GenTiStr']))
        ofh.write('{:}\n'.format(self.fst_vt['Fst7']['GenTiStp']))
        ofh.write('{:.9f}\n'.format(self.fst_vt['Fst7']['SpdGenOn']))
        ofh.write('{:.9f}\n'.format(self.fst_vt['Fst7']['TimGenOn']))
        ofh.write('{:.9f}\n'.format(self.fst_vt['Fst7']['TimGenOf']))
        ofh.write('{:3}\n'.format(self.fst_vt['Fst7']['HSSBrMode']))
        ofh.write('{:.9f}\n'.format(self.fst_vt['Fst7']['THSSBrDp']))
        ofh.write('{:.9f}\n'.format(self.fst_vt['Fst7']['TiDynBrk']))
        ofh.write('{:.9f}\n'.format(self.fst_vt['Fst7']['TTpBrDp1']))
        ofh.write('{:.9f}\n'.format(self.fst_vt['Fst7']['TTpBrDp2']))
        ofh.write('{:.9f}\n'.format(self.fst_vt['Fst7']['TTpBrDp3']))
        ofh.write('{:.9f}\n'.format(self.fst_vt['Fst7']['TBDepISp1']))
        ofh.write('{:.9f}\n'.format(self.fst_vt['Fst7']['TBDepISp2']))
        ofh.write('{:.9f}\n'.format(self.fst_vt['Fst7']['TBDepISp3']))
        ofh.write('{:.9f}\n'.format(self.fst_vt['Fst7']['TYawManS']))
        ofh.write('{:.9f}\n'.format(self.fst_vt['Fst7']['TYawManE']))
        ofh.write('{:.9f}\n'.format(self.fst_vt['Fst7']['NacYawF']))
        ofh.write('{:.9f}\n'.format(self.fst_vt['Fst7']['TPitManS1']))
        ofh.write('{:.9f}\n'.format(self.fst_vt['Fst7']['TPitManS2']))
        ofh.write('{:.9f}\n'.format(self.fst_vt['Fst7']['TPitManS3']))
        ofh.write('{:.9f}\n'.format(self.fst_vt['Fst7']['TPitManE1']))
        ofh.write('{:.9f}\n'.format(self.fst_vt['Fst7']['TPitManE2']))
        ofh.write('{:.9f}\n'.format(self.fst_vt['Fst7']['TPitManE3']))
        ofh.write('{:.9f}\n'.format(self.fst_vt['Fst7']['BlPitch1']))
        ofh.write('{:.9f}\n'.format(self.fst_vt['Fst7']['BlPitch2']))
        ofh.write('{:.9f}\n'.format(self.fst_vt['Fst7']['BlPitch3']))
        ofh.write('{:.9f}\n'.format(self.fst_vt['Fst7']['B1PitchF1']))
        ofh.write('{:.9f}\n'.format(self.fst_vt['Fst7']['B1PitchF2']))
        ofh.write('{:.9f}\n'.format(self.fst_vt['Fst7']['B1PitchF3']))
        ofh.write('---\n')
        ofh.write('{:.9f}\n'.format(self.fst_vt['Fst7']['Gravity']))
        ofh.write('---\n')
        ofh.write('{:}\n'.format(self.fst_vt['Fst7']['FlapDOF1']))
        ofh.write('{:}\n'.format(self.fst_vt['Fst7']['FlapDOF2']))
        ofh.write('{:}\n'.format(self.fst_vt['Fst7']['EdgeDOF']))
        ofh.write('{:}\n'.format(self.fst_vt['Fst7']['TeetDOF']))
        ofh.write('{:}\n'.format(self.fst_vt['Fst7']['DrTrDOF']))
        ofh.write('{:}\n'.format(self.fst_vt['Fst7']['GenDOF']))
        ofh.write('{:}\n'.format(self.fst_vt['Fst7']['YawDOF']))
        ofh.write('{:}\n'.format(self.fst_vt['Fst7']['TwFADOF1']))
        ofh.write('{:}\n'.format(self.fst_vt['Fst7']['TwFADOF2']))
        ofh.write('{:}\n'.format(self.fst_vt['Fst7']['TwSSDOF1']))
        ofh.write('{:}\n'.format(self.fst_vt['Fst7']['TwSSDOF2']))
        ofh.write('{:}\n'.format(self.fst_vt['Fst7']['CompAero']))
        ofh.write('{:}\n'.format(self.fst_vt['Fst7']['CompNoise']))
        ofh.write('---\n')
        ofh.write('{:.9f}\n'.format(self.fst_vt['Fst7']['OoPDefl']))
        ofh.write('{:.9f}\n'.format(self.fst_vt['Fst7']['IPDefl']))
        ofh.write('{:.9f}\n'.format(self.fst_vt['Fst7']['TeetDefl']))
        ofh.write('{:.9f}\n'.format(self.fst_vt['Fst7']['Azimuth']))
        ofh.write('{:.9f}\n'.format(self.fst_vt['Fst7']['RotSpeed']))
        ofh.write('{:.9f}\n'.format(self.fst_vt['Fst7']['NacYaw']))
        ofh.write('{:.9f}\n'.format(self.fst_vt['Fst7']['TTDspFA']))
        ofh.write('{:.9f}\n'.format(self.fst_vt['Fst7']['TTDspSS']))
        ofh.write('---\n')
        ofh.write('{:.9f}\n'.format(self.fst_vt['Fst7']['TipRad']))
        ofh.write('{:.9f}\n'.format(self.fst_vt['Fst7']['HubRad']))
        ofh.write('{:3}\n'.format(self.fst_vt['Fst7']['PSpnElN']))
        ofh.write('{:.9f}\n'.format(self.fst_vt['Fst7']['UndSling']))
        ofh.write('{:.9f}\n'.format(self.fst_vt['Fst7']['HubCM']))
        ofh.write('{:.9f}\n'.format(self.fst_vt['Fst7']['OverHang']))
        ofh.write('{:.9f}\n'.format(self.fst_vt['Fst7']['NacCMxn']))
        ofh.write('{:.9f}\n'.format(self.fst_vt['Fst7']['NacCMyn']))
        ofh.write('{:.9f}\n'.format(self.fst_vt['Fst7']['NacCMzn']))
        ofh.write('{:.9f}\n'.format(self.fst_vt['Fst7']['TowerHt']))
        ofh.write('{:.9f}\n'.format(self.fst_vt['Fst7']['Twr2Shft']))
        ofh.write('{:.9f}\n'.format(self.fst_vt['Fst7']['TwrRBHt']))
        ofh.write('{:.9f}\n'.format(self.fst_vt['Fst7']['ShftTilt']))
        ofh.write('{:.9f}\n'.format(self.fst_vt['Fst7']['Delta3']))
        ofh.write('{:.9f}\n'.format(self.fst_vt['Fst7']['PreCone1']))
        ofh.write('{:.9f}\n'.format(self.fst_vt['Fst7']['PreCone2']))
        ofh.write('{:.9f}\n'.format(self.fst_vt['Fst7']['PreCone3']))
        ofh.write('{:.9f}\n'.format(self.fst_vt['Fst7']['AzimB1Up']))
        ofh.write('---\n')
        ofh.write('{:.9f}\n'.format(self.fst_vt['Fst7']['YawBrMass']))
        ofh.write('{:.9f}\n'.format(self.fst_vt['Fst7']['NacMass']))
        ofh.write('{:.9f}\n'.format(self.fst_vt['Fst7']['HubMass']))
        ofh.write('{:.9f}\n'.format(self.fst_vt['Fst7']['TipMass1']))
        ofh.write('{:.9f}\n'.format(self.fst_vt['Fst7']['TipMass2']))
        ofh.write('{:.9f}\n'.format(self.fst_vt['Fst7']['TipMass3']))
        ofh.write('{:.9f}\n'.format(self.fst_vt['Fst7']['NacYIner']))
        ofh.write('{:.9f}\n'.format(self.fst_vt['Fst7']['GenIner']))
        ofh.write('{:.9f}\n'.format(self.fst_vt['Fst7']['HubIner']))
        ofh.write('---\n')
        ofh.write('{:.9f}\n'.format(self.fst_vt['Fst7']['GBoxEff']))
        ofh.write('{:.9f}\n'.format(self.fst_vt['Fst7']['GenEff']))
        ofh.write('{:.9f}\n'.format(self.fst_vt['Fst7']['GBRatio']))
        ofh.write('{:}\n'.format(self.fst_vt['Fst7']['GBRevers']))
        ofh.write('{:.9f}\n'.format(self.fst_vt['Fst7']['HSSBrTqF']))
        ofh.write('{:.9f}\n'.format(self.fst_vt['Fst7']['HSSBrDT']))
        ofh.write('{:}\n'.format(self.fst_vt['Fst7']['DynBrkFi']))
        ofh.write('{:.9f}\n'.format(self.fst_vt['Fst7']['DTTorSpr']))
        ofh.write('{:.9f}\n'.format(self.fst_vt['Fst7']['DTTorDmp']))
        ofh.write('---\n')
        ofh.write('{:.9f}\n'.format(self.fst_vt['Fst7']['SIG_SlPc']))
        ofh.write('{:.9f}\n'.format(self.fst_vt['Fst7']['SIG_SySp']))
        ofh.write('{:.9f}\n'.format(self.fst_vt['Fst7']['SIG_RtTq']))
        ofh.write('{:.9f}\n'.format(self.fst_vt['Fst7']['SIG_PORt']))
        ofh.write('---\n')
        ofh.write('{:.9f}\n'.format(self.fst_vt['Fst7']['TEC_Freq']))
        ofh.write('{:5}\n'.format(self.fst_vt['Fst7']['TEC_NPol']))
        ofh.write('{:.9f}\n'.format(self.fst_vt['Fst7']['TEC_SRes']))
        ofh.write('{:.9f}\n'.format(self.fst_vt['Fst7']['TEC_RRes']))
        ofh.write('{:.9f}\n'.format(self.fst_vt['Fst7']['TEC_VLL']))
        ofh.write('{:.9f}\n'.format(self.fst_vt['Fst7']['TEC_SLR']))
        ofh.write('{:.9f}\n'.format(self.fst_vt['Fst7']['TEC_RLR']))
        ofh.write('{:.9f}\n'.format(self.fst_vt['Fst7']['TEC_MR']))
        ofh.write('---\n')
        ofh.write('{:3}\n'.format(self.fst_vt['Fst7']['PtfmModel']))
        ofh.write('"{:}"\n'.format(self.fst_vt['Fst7']['PtfmFile']))
        ofh.write('---\n')
        ofh.write('{:3}\n'.format(self.fst_vt['Fst7']['TwrNodes']))
        ofh.write('"{:}"\n'.format(self.fst_vt['Fst7']['TwrFile']))
        ofh.write('---\n')
        ofh.write('{:.9f}\n'.format(self.fst_vt['Fst7']['YawSpr']))
        ofh.write('{:.9f}\n'.format(self.fst_vt['Fst7']['YawDamp']))
        ofh.write('{:.9f}\n'.format(self.fst_vt['Fst7']['YawNeut']))
        ofh.write('---\n')
        ofh.write('{:}\n'.format(self.fst_vt['Fst7']['Furling']))
        ofh.write('{:}\n'.format(self.fst_vt['Fst7']['FurlFile']))
        ofh.write('---\n') 
        ofh.write('{:}\n'.format(self.fst_vt['Fst7']['TeetMod']))
        ofh.write('{:.9f}\n'.format(self.fst_vt['Fst7']['TeetDmpP']))
        ofh.write('{:.9f}\n'.format(self.fst_vt['Fst7']['TeetDmp']))
        ofh.write('{:.9f}\n'.format(self.fst_vt['Fst7']['TeetCDmp']))
        ofh.write('{:.9f}\n'.format(self.fst_vt['Fst7']['TeetSStP']))
        ofh.write('{:.9f}\n'.format(self.fst_vt['Fst7']['TeetHStP']))
        ofh.write('{:.9f}\n'.format(self.fst_vt['Fst7']['TeetSSSp']))
        ofh.write('{:.9f}\n'.format(self.fst_vt['Fst7']['TeetHSSp']))
        ofh.write('---\n')
        ofh.write('{:.9f}\n'.format(self.fst_vt['Fst7']['TBDrConN']))
        ofh.write('{:.9f}\n'.format(self.fst_vt['Fst7']['TBDrConD']))
        ofh.write('{:.9f}\n'.format(self.fst_vt['Fst7']['TpBrDT']))
        ofh.write('---\n')
        ofh.write('"{:}"\n'.format(self.fst_vt['Fst7']['BldFile1']))
        ofh.write('"{:}"\n'.format(self.fst_vt['Fst7']['BldFile2']))
        ofh.write('"{:}"\n'.format(self.fst_vt['Fst7']['BldFile3']))
        ofh.write('---\n') 
        ofh.write('"{:}"\n'.format(self.fst_vt['Fst7']['ADFile']))
        ofh.write('---\n')
        ofh.write('{:}\n'.format(self.fst_vt['Fst7']['NoiseFile']))
        ofh.write('---\n')
        ofh.write('{:}\n'.format(self.fst_vt['Fst7']['ADAMSFile']))
        ofh.write('---\n')
        ofh.write('{:}\n'.format(self.fst_vt['Fst7']['LinFile']))
        ofh.write('---\n')
        ofh.write('{:}\n'.format(self.fst_vt['Fst7']['SumPrint']))
        ofh.write('{:}\n'.format(self.fst_vt['Fst7']['OutFileFmt']))
        ofh.write('{:}\n'.format(self.fst_vt['Fst7']['TabDelim']))
        ofh.write('{:}\n'.format(self.fst_vt['Fst7']['OutFmt']))
        ofh.write('{:.9f}\n'.format(self.fst_vt['Fst7']['TStart']))
        ofh.write('{:3}\n'.format(self.fst_vt['Fst7']['DecFact']))
        ofh.write('{:.9f}\n'.format(self.fst_vt['Fst7']['SttsTime']))
        ofh.write('{:.9f}\n'.format(self.fst_vt['Fst7']['NcIMUxn']))
        ofh.write('{:.9f}\n'.format(self.fst_vt['Fst7']['NcIMUyn']))
        ofh.write('{:.9f}\n'.format(self.fst_vt['Fst7']['NcIMUzn']))
        ofh.write('{:.9f}\n'.format(self.fst_vt['Fst7']['ShftGagL']))
        ofh.write('{:3}\n'.format(self.fst_vt['Fst7']['NTwGages']))
        for i in range(self.fst_vt['Fst7']['NTwGages']-1):
            ofh.write('{:3}, '.format(self.fst_vt['Fst7']['TwrGagNd'][i]))
        ofh.write('{:3}\n'.format(self.fst_vt['Fst7']['TwrGagNd'][-1]))
        ofh.write('{:3}\n'.format(self.fst_vt['Fst7']['NBlGages']))
        for i in range(self.fst_vt['Fst7']['NBlGages']-1):
            ofh.write('{:3}, '.format(self.fst_vt['Fst7']['BldGagNd'][i]))
        ofh.write('{:3}\n'.format(self.fst_vt['Fst7']['BldGagNd'][-1]))
    
        # Outlist
        ofh.write('Outlist\n')
        outlist = self.get_outlist(self.fst_vt['outlist7'], ['OutList'])
        for channel_list in outlist:
            ofh.write('"' + ', '.join(channel_list) + '"\n')
        ofh.write('END\n')
        ofh.close()
        
        ofh.close()

    def write_AeroDyn_FAST7(self):
        if not os.path.isdir(os.path.join(self.FAST_runDirectory,'AeroData')):
            os.mkdir(os.path.join(self.FAST_runDirectory,'AeroData'))

        # create airfoil objects
        for i in range(self.fst_vt['AeroDyn14']['NumFoil']):
             af_name = os.path.join(self.FAST_runDirectory, 'AeroData', 'Airfoil' + str(i) + '.dat')
             self.fst_vt['AeroDyn14']['FoilNm'][i]  = os.path.join('AeroData', 'Airfoil' + str(i) + '.dat')
             self.write_AeroDyn14Polar(af_name, i)

        self.fst_vt['Fst7']['ADFile'] = self.FAST_namingOut + '_AeroDyn.dat'
        ad_file = os.path.join(self.FAST_runDirectory,self.fst_vt['Fst7']['ADFile'])
        ofh = open(ad_file,'w')
        
        ofh.write('Aerodyn input file for FAST\n')
        
        ofh.write('{:}\n'.format(self.fst_vt['AeroDyn14']['SysUnits']))
        ofh.write('{:}\n'.format(self.fst_vt['AeroDyn14']['StallMod']))        
        
        ofh.write('{:}\n'.format(self.fst_vt['AeroDyn14']['UseCm']))
        ofh.write('{:}\n'.format(self.fst_vt['AeroDyn14']['InfModel']))
        ofh.write('{:}\n'.format(self.fst_vt['AeroDyn14']['IndModel']))
        ofh.write('{:.3f}\n'.format(self.fst_vt['AeroDyn14']['AToler']))
        ofh.write('{:}\n'.format(self.fst_vt['AeroDyn14']['TLModel']))
        ofh.write('{:}\n'.format(self.fst_vt['AeroDyn14']['HLModel']))
        ofh.write('"{:}"\n'.format(self.fst_vt['AeroDyn14']['WindFile']))
        ofh.write('{:f}\n'.format(self.fst_vt['AeroDyn14']['HH']))  
  
        ofh.write('{:.1f}\n'.format(self.fst_vt['AeroDyn14']['TwrShad']))  
  
        ofh.write('{:.1f}\n'.format(self.fst_vt['AeroDyn14']['ShadHWid']))  
  
        ofh.write('{:.1f}\n'.format(self.fst_vt['AeroDyn14']['T_Shad_Refpt']))  
  
        ofh.write('{:.3f}\n'.format(self.fst_vt['AeroDyn14']['AirDens']))  
  
        ofh.write('{:.9f}\n'.format(self.fst_vt['AeroDyn14']['KinVisc']))  
  
        ofh.write('{:2}\n'.format(self.fst_vt['AeroDyn14']['DTAero']))        
        

        ofh.write('{:2}\n'.format(self.fst_vt['AeroDyn14']['NumFoil']))
        for i in range (self.fst_vt['AeroDyn14']['NumFoil']):
            ofh.write('"{:}"\n'.format(self.fst_vt['AeroDyn14']['FoilNm'][i]))

        ofh.write('{:2}\n'.format(self.fst_vt['AeroDynBlade']['BldNodes']))
        rnodes = self.fst_vt['AeroDynBlade']['RNodes']
        twist = self.fst_vt['AeroDynBlade']['AeroTwst']
        drnodes = self.fst_vt['AeroDynBlade']['DRNodes']
        chord = self.fst_vt['AeroDynBlade']['Chord']
        nfoil = self.fst_vt['AeroDynBlade']['NFoil']
        prnelm = self.fst_vt['AeroDynBlade']['PrnElm']
        ofh.write('Nodal properties\n')
        for r, t, dr, c, a, p in zip(rnodes, twist, drnodes, chord, nfoil, prnelm):
            ofh.write('{: 2.15e}\t{:.3f}\t{:.4f}\t{:.3f}\t{:5}\t{:}\n'.format(r, t, dr, c, a, p))

        ofh.close()



if __name__=="__main__":

    FAST_ver = 'openfast'
    read_yaml = False

    fst_update = {}
    fst_update['Fst', 'TMax'] = 20.
    fst_update['AeroDyn15', 'TwrAero'] = False


    if read_yaml:
        fast = InputReader_Common(FAST_ver=FAST_ver)
        fast.FAST_yamlfile = 'temp/OpenFAST/test.yaml'
        fast.read_yaml()

    if FAST_ver.lower() == 'fast7':
        if not read_yaml:
            fast = InputReader_FAST7(FAST_ver=FAST_ver)
            fast.FAST_InputFile = 'Test16.fst'   # FAST input file (ext=.fst)
            fast.FAST_directory = 'C:/Users/egaertne/WT_Codes/models/FAST_v7.02.00d-bjj/CertTest/'   # Path to fst directory files
            fast.execute()
        
        fastout = InputWriter_FAST7(FAST_ver=FAST_ver)
        fastout.fst_vt = fast.fst_vt
        fastout.FAST_runDirectory = 'temp/FAST7'
        fastout.FAST_namingOut = 'test'
        fastout.execute()

    elif FAST_ver.lower() == 'fast8':
        if not read_yaml:
            fast = InputReader_OpenFAST(FAST_ver=FAST_ver)
            fast.FAST_InputFile = 'NREL5MW_onshore.fst'   # FAST input file (ext=.fst)
            fast.FAST_directory = 'C:/Users/egaertne/WT_Codes/models/FAST_v8.16.00a-bjj/ref/5mw_onshore/'   # Path to fst directory files
            fast.execute()
        
        fastout = InputWriter_OpenFAST(FAST_ver=FAST_ver)
        fastout.fst_vt = fast.fst_vt
        fastout.FAST_runDirectory = 'temp/FAST8'
        fastout.FAST_namingOut = 'test'
        fastout.execute()

    elif FAST_ver.lower() == 'openfast':
        if not read_yaml:
            fast = InputReader_OpenFAST(FAST_ver=FAST_ver)
            fast.FAST_InputFile = '5MW_Land_DLL_WTurb.fst'   # FAST input file (ext=.fst)
            fast.FAST_directory = 'C:/Users/egaertne/WT_Codes/models/openfast/glue-codes/fast/5MW_Land_DLL_WTurb'   # Path to fst directory files
            fast.execute()
        
        fastout = InputWriter_OpenFAST(FAST_ver=FAST_ver)
        fastout.fst_vt = fast.fst_vt
        fastout.FAST_runDirectory = 'temp/OpenFAST'
        fastout.FAST_namingOut = 'test'
        fastout.update(fst_update=fst_update)
        fastout.execute()
    
    fastout.write_yaml()

    

