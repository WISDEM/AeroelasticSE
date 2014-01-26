import os
import sys
from openmdao.lib.components.external_code import ExternalCode
from openmdao.lib.datatypes.api import Str

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
    fst.FSTInputFile = 'C:/Models/FAST/ModelFiles/FASTmodel.fst'
    fst.execute()
