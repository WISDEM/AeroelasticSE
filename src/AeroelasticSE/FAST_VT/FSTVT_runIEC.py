
from openmdao.lib.datatypes.api import Slot, Str

import numpy as np
import os
import matplotlib.pylab as plt
import copy

from openmdao.main.api import Component, Assembly
from openmdao.lib.datatypes.api import Str, Slot, Bool, VarTree
from FST_vartrees import FstModel
from FST_reader import FstInputReader
from FST_writer import FstInputWriter, FstInputBuilder, FUSEDWindInputBuilder
from FST_wrapper import FstWrapper

from fusedwind.runSuite.runAero import FUSEDIECBase


class FUSEDFSTCaseRunner(FUSEDIECBase):

    FSTexe = Str(iotype='in', desc='Path to executable')

    def __init__(self):
        super(FUSEDFSTCaseRunner, self).__init__()

    def configure(self):

        self.force_execute = True

        self.add('reader', FstInputReader())
        self.driver.workflow.add('reader')
        #self.connect('fst_infile_vt', 'reader.fst_infile_vt')
        #OC3 Example
        FAST_DIR = os.path.dirname(os.path.realpath(__file__))
    
        self.reader.fst_infile = 'NRELOffshrBsline5MW_Monopile_RF.fst' #replace with master fast file
        self.reader.fst_directory = os.path.join(FAST_DIR,"OC3_Files")
        self.reader.ad_file_type = 1
        self.reader.fst_file_type = 1

        self.reader.read_input_file()

        self.add('builder', FUSEDWindInputBuilder())
        self.driver.workflow.add('builder')
        #self.connect('reader.fst_vt', 'builder.fstIn') #TODO: why can't these be connected like a normal workflow?
        #self.builder.force_execute = True

        self.connect('inputs', 'builder.inputs')
        self.builder.fstIn = self.reader.fst_vt.copy()
        self.builder.initialize_inputs()
        self.builder.execute()
        self.builder.force_execute = True

        self.add('writer', FstInputWriter())
        self.driver.workflow.add('writer')
        self.writer.fst_infile = 'FAST_Model.fst'
        self.writer.fst_directory = os.path.join(FAST_DIR,self.inputs.case_name)
        if not os.path.isdir(self.writer.fst_directory):
            os.mkdir(self.writer.fst_directory)
        self.connect('builder.fstOut', 'writer.fst_vt') #TODO; why can't i do direct connect?
        self.connect('inputs.case_name', ['writer.case_id'])
        self.writer.force_execute = True

        self.add('wrapper', FstWrapper())
        self.driver.workflow.add('wrapper')
        #self.connect('FSTexe', 'wrapper.FSTexe') #TODO: why isn't connect working?
        # Set up input files
        self.wrapper.FSTexe = 'C:/Models/FAST/FAST.exe'
        self.connect('writer.fst_directory', 'wrapper.fst_directory')
        self.connect('writer.fst_file', 'wrapper.FSTInputFile')

if __name__ == '__main__':
    
    pass