import os
import sys
import subprocess

from FST7_writer import Fst7InputWriter
from FST7_reader import Fst7InputReader
from FST_vartrees_new import FstModel

class Fst7ExternalCode(object):

    pass
    

class Fst7Wrapper(Fst7ExternalCode):

    FSTexe = ''   #Path to executable
    FSTInputFile = ''   #FAST input file (ext=.fst)
    fst_directory = ''   #Path to fst directory files

    def __init__(self):
        super(Fst7Wrapper, self).__init__()

    def execute(self):


        print "Executing FAST"
        self.input_file = os.path.join(self.fst_directory, self.FSTInputFile)

        if (not os.path.exists(self.FSTexe)):
            sys.stderr.write("Can't find FAST executable: {:}\n".format(self.FSTexe))
            return 0
        
        print "Calling ", self.FSTexe
        print "Input file = ", self.input_file

        exec_str = []
        exec_str.append(self.FSTexe)
        exec_str.append(self.input_file)

        subprocess.call(exec_str)#, stdin=None, stdout=None, stderr=None, shell=False)
        

if __name__=="__main__":

   pass