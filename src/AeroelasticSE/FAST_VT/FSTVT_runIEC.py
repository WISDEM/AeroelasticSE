
from openmdao.lib.datatypes.api import Slot, Str

import numpy as np
import os
import matplotlib.pylab as plt

from openmdao.main.api import Component, Assembly
from openmdao.lib.datatypes.api import Str, Slot, Bool, VarTree, Slot
from FST_vartrees import FstModel
from FST_reader import FstInputReader
from FST_writer import FstInputWriter, FstInputBuilder
from FST_wrapper import FstWrapper

from fusedwind.runSuite.runAero import FUSEDIECBase

class FUSEDFSTCaseRunner(FUSEDIECBase):

    def __init__(self):
        super(FUSEDFSTCaseRunner, self).__init__()

    def configure(self):

        self.force_execute = True

        self.add('reader', FstInputReader())
        self.driver.workflow.add('reader')
        self.reader.force_execute = True

        self.add('builder', FstInputBuilder())
        self.driver.workflow.add('builder')
        self.connect('reader.fst_vt', 'builder.fstIn')
        self.builder.force_execute = True

        self.add('writer', FstInputWriter())
        self.driver.workflow.add('writer')
        self.connect('builder.fstOut', 'writer.fst_vt')
        self.writer.force_execute = True

        self.add('wrapper', FstWrapper())
        self.driver.workflow.add('wrapper')

if __name__ == '__main__':
    
    pass