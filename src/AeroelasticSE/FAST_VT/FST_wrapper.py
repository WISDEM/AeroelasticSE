import os
import sys
from openmdao.lib.components.external_code import ExternalCode
from openmdao.lib.datatypes.api import Str

from FST_writer import FstInputWriter
from FST_reader import FstInputReader
from FST_vartrees import FstModel

class FstExternalCode(ExternalCode):

    pass


class FstWrapper(FstExternalCode):

    FSTexe = Str(io_type='in', desc='Path to executable')
    FSTInputFile = Str(iotype='in', desc='FAST input file (ext=.fst)')
    fst_directory = Str(iotype='in', desc='Path to fst directory files')

    def __init__(self):
        super(FstWrapper, self).__init__()

    def execute(self):

        self.input_file = os.path.join(self.fst_directory, self.FSTInputFile)

        if (not os.path.exists(self.FSTexe)):
            sys.stderr.write("Can't find FAST executable: {:}\n".format(self.FSTexe))
            return 0
        print "calling ", self.FSTexe
        print "input file=", self.input_file

        self.command.append(self.FSTexe)
        self.command.append(self.input_file)
        
        super(FstWrapper,self).execute()


if __name__=="__main__":

    fst = FstWrapper()
    fst.FSTexe = 'C:/Models/FAST/FAST.exe'
    #fst.FSTInputFile = 'C:/Models/FAST/ModelFiles/FASTmodel.fst'
    #fst.execute()

    # OC3 Example
    fst_input = FstInputReader()
    fst_writer = FstInputWriter()

    FAST_DIR = os.path.dirname(os.path.realpath(__file__))

    fst_input.fst_infile = 'NRELOffshrBsline5MW_Monopile_RF.fst'
    fst_input.fst_directory = os.path.join(FAST_DIR,"OC3_Files")
    fst_input.ad_file_type = 1
    fst_input.fst_file_type = 1
    fst_input.execute() 

    fst_writer.fst_vt = fst_input.fst_vt
    fst_writer.fst_infile = 'FAST_Model.fst'
    fst_writer.fst_directory = os.path.join(FAST_DIR,"tmp")
    fst_writer.fst_vt.PtfmFile = "Platform.dat"
    fst_writer.fst_vt.TwrFile = "Tower.dat"
    fst_writer.fst_vt.BldFile1 = "Blade.dat"
    fst_writer.fst_vt.BldFile2 = fst_writer.fst_vt.BldFile1 
    fst_writer.fst_vt.BldFile3 = fst_writer.fst_vt.BldFile1 
    fst_writer.fst_vt.ADFile = "Aerodyn.ipt"
    fst_writer.execute()
    
    fst.FSTInputFile = fst_writer.fst_infile
    fst.fst_directory = fst_writer.fst_directory
    fst.execute()