"""
A basic python script that demonstrates how to use the FST7 reader, writer, and wrapper in a purely
python setting. These functions are constructed to provide a simple interface for controlling FAST
programmatically with minimal additional dependencies.
"""
# Hacky way of doing relative imports
import os, sys
sys.path.insert(0, os.path.abspath(".."))

from FST7_reader import Fst7InputReader
from FST7_writer import Fst7InputWriter
from FST7_wrapper import Fst7Wrapper

reader = Fst7InputReader()   #Initialize reader
writer = Fst7InputWriter()   #Initialize writer
wrapper = Fst7Wrapper()   #Initialize wrapper

reader.fst_infile = 'Test01.fst'   #Master FAST file to base test on
reader.fst_directory = './FST7inputfiles/'   #Directory of master FAST file set
reader.fst_file_type = 0   #Enum(0, (0,1), desc='Fst file type, 0=old FAST, 1 = new FAST')    
reader.ad_file_type = 1   #Enum(0, (0,1), desc='Aerodyn file type, 0=old Aerodyn, 1 = new Aerdyn')
reader.execute()

writer.fst_vt = reader.fst_vt   #Pass properties from reader to writer
writer.fst_infile = 'Test01_Case1.fst'   #Name for new .fst file
writer.fst_directory = './rundir/'   #Running directory
writer.execute()   #Write new files

wrapper.FSTexe = '../../../../../FAST_v7/bin/FAST_glin32'
wrapper.FSTInputFile = writer.fst_infile
wrapper.fst_directory = writer.fst_directory
wrapper.execute()   #Execute actual FAST analysis