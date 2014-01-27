import os
import sys
from openmdao.lib.components.external_code import ExternalCode
from openmdao.lib.datatypes.api import Str

from FST_writer import FstInputWriter
from FST_reader import FstInputReader
from FST_vartrees import FstModel

class FSTExternalCode(ExternalCode):

    pass


class FSTWrapper(ExternalCode):

    FSTexe = Str(io_type='in', desc='Path to executable')
    FSTInputFile = Str(iotype='in', desc='Path to FAST input file (ext=.fst)')

    def __init__(self):
        super(FSTWrapper, self).__init__()

    def execute(self):

        self.input_file = self.FSTInputFile

        if (not os.path.exists(self.FSTexe)):
            sys.stderr.write("Can't find FAST executable: {:}\n".format(ffname))
            return 0
        print "calling ", self.FSTexe
        print "input file=", self.input_file

        self.command.append(self.FSTexe)
        self.command.append(self.input_file)
        
        super(FSTWrapper,self).execute()


if __name__=="__main__":

    fst = FSTWrapper()
    fst.FSTexe = 'C:/Models/FAST/FAST.exe'
    #fst.FSTInputFile = 'C:/Models/FAST/ModelFiles/FASTmodel.fst'
    #fst.execute()

    #OC3 Example
    fst_input = FstInputReader()
    fst_writer = FstInputWriter()

    ad_file    = 'NRELOffshrBsline5MW_AeroDyn.ipt'
    ad_file_type = 1
    blade_file = 'NRELOffshrBsline5MW_Blade.dat'
    tower_file = 'NRELOffshrBsline5MW_Tower_Monopile_RF.dat'
    platform_file = 'NRELOffshrBsline5MW_Platform_Monopile_RF.dat'
    fst_file = 'NRELOffshrBsline5MW_Monopile_RF.fst'
    fst_file_type = 1
    FAST_DIR = os.path.dirname(os.path.realpath(__file__))
    fst_input.template_path= os.path.join(FAST_DIR,"OC3_Files")
    ad_fname = os.path.join(fst_input.template_path, ad_file)
    bl_fname = os.path.join(fst_input.template_path, blade_file)
    tw_fname = os.path.join(fst_input.template_path, tower_file)
    pl_fname = os.path.join(fst_input.template_path, platform_file)
    fs_fname = os.path.join(fst_input.template_path, fst_file)

    fst_input.ad_file = ad_fname
    fst_input.ad_file_type = ad_file_type
    fst_input.blade_file = bl_fname
    fst_input.tower_file = tw_fname
    fst_input.platform_file = pl_fname
    fst_input.fst_file = fs_fname
    fst_input.fst_file_type = fst_file_type
    fst_input.execute() 

    fst_writer.fst_vt = fst_input.fst_vt
    fst_writer.template_path = os.path.join(FAST_DIR,"tmp")
    fst_writer.execute()        
    fst_file = fst_writer.fst_file
    
    fst.FSTInputFile = os.path.join(fst_input.template_path, fst_file)
    fst.execute()