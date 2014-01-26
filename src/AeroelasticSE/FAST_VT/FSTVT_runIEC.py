
from openmdao.lib.datatypes.api import Slot, Str

import numpy as np
import os
import matplotlib.pylab as plt

from openmdao.main.api import Component, Assembly
from openmdao.lib.datatypes.api import Str, Slot, Bool, VarTree #, Instance
from FST_vartrees import FSTModel
from FST_reader import FSTInputReader
from FST_writer import FSTInputWriter
from FST_wrapper import FSTWrapper


class FUSEDFSTCaseRunner(FUSEDIECBase):

    def __init__(self):
        super(FUSEDFSTCaseRunner, self).__init__()

    def configure(self):

        self.force_execute = True

        self.add('reader', FSTInputReader())
        self.driver.workflow.add('reader')
        self.reader.force_execute = True

        self.add('builder', FSTInputBuilder())
        self.driver.workflow.add('builder')
        self.connect('reader.fst_vt', 'builder.fstIn')
        self.builder.force_execute = True

        self.add('writer', FSTInputWriter())
        self.driver.workflow.add('writer')
        self.connect('builder.fstOut', 'writer.fst_vt')
        self.writer.force_execute = True

        self.add('wrapper', FSTWrapper())
        self.driver.workflow.add('wrapper')
        self.wrapper.FSTexe = 'C:/Models/FAST/FAST.exe'


if __name__ == '__main__':
    
    pass