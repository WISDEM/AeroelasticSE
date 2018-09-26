"""
A basic python script that demonstrates how to use the FST8 reader, writer, and wrapper in a purely
python setting. These functions are constructed to provide a simple interface for controlling FAST
programmatically with minimal additional dependencies.
"""
# Hacky way of doing relative imports
import os, sys
import multiprocessing as mp
# sys.path.insert(0, os.path.abspath(".."))

from FAST_reader import InputReader_Common, InputReader_OpenFAST, InputReader_FAST7
from FAST_writer import InputWriter_Common, InputWriter_OpenFAST, InputWriter_FAST7
from FAST_wrapper import FastWrapper

class runFAST_pywrapper(object):

    def __init__(self, **kwargs):
        self.FAST_ver = 'OPENFAST' #(FAST7, FAST8, OPENFAST)

        self.FAST_exe = None
        self.FAST_InputFile = None
        self.FAST_directory = None
        self.FAST_runDirectory = None
        self.FAST_namingOut = None
        self.read_yaml = False
        self.write_yaml = False
        self.case = {}

        # Optional population class attributes from key word arguments
        for k, w in kwargs.iteritems():
            try:
                setattr(self, k, w)
            except:
                pass

        super(runFAST_pywrapper, self).__init__()

    def execute(self):

        # FAST version specific initialization
        if self.FAST_ver.lower() == 'fast7':
            reader = InputReader_FAST7(FAST_ver=self.FAST_ver)
            writer = InputWriter_FAST7(FAST_ver=self.FAST_ver)
        elif self.FAST_ver.lower() in ['fast8','openfast']:
            reader = InputReader_OpenFAST(FAST_ver=self.FAST_ver)
            writer = InputWriter_OpenFAST(FAST_ver=self.FAST_ver)
        wrapper = FastWrapper(FAST_ver=self.FAST_ver)

        # Read input model, FAST files or Yaml
        if self.read_yaml:
            reader.FAST_yamlfile = self.FAST_yamlfile_in
            reader.read_yaml()
        else:
            reader.FAST_InputFile = self.FAST_InputFile
            reader.FAST_directory = self.FAST_directory
            reader.execute()
        
        # Initialize writer variables with input model
        writer.fst_vt = reader.fst_vt
        writer.FAST_runDirectory = self.FAST_runDirectory
        writer.FAST_namingOut = self.FAST_namingOut
        # Make any case specific variable changes
        if self.case:
            writer.update(fst_update=self.case)
        # Write out FAST model
        writer.execute()
        if self.write_yaml:
            writer.FAST_yamlfile = self.FAST_yamlfile_out
            writer.write_yaml()

        # Run FAST
        wrapper.FAST_exe = self.FAST_exe
        wrapper.FAST_InputFile = os.path.split(writer.FAST_InputFileOut)[1]
        wrapper.FAST_directory = os.path.split(writer.FAST_InputFileOut)[0]
        wrapper.execute()

class runFAST_pywrapper_batch(object):

    def __init__(self, **kwargs):

        self.FAST_ver           = 'OpenFAST'
        self.FAST_exe           = None
        self.FAST_InputFile     = None
        self.FAST_directory     = None
        self.FAST_runDirectory  = None

        self.read_yaml          = False
        self.FAST_yamlfile_in   = ''
        self.write_yaml         = False
        self.FAST_yamlfile_out  = ''

        self.case_list          = []
        self.case_name_list     = []

        self.post               = None

        # Optional population of class attributes from key word arguments
        for k, w in kwargs.iteritems():
            try:
                setattr(self, k, w)
            except:
                pass

        super(runFAST_pywrapper_batch, self).__init__()

        
    def run_serial(self):
        # Run batch serially

        for case, case_name in zip(self.case_list, self.case_name_list):
            eval(case, case_name, self.FAST_ver, self.FAST_exe, self.FAST_runDirectory, self.FAST_InputFile, self.FAST_directory, self.read_yaml, self.FAST_yamlfile_in, self.write_yaml, self.FAST_yamlfile_out, self.post)

    def run_multi(self, cores=None):
        # Run cases in parallel, threaded with multiprocessing module

        if not cores:
            cores = mp.cpu_count()
        pool = mp.Pool(cores)

        case_data_all = []
        for i in range(len(self.case_list)):
            case_data = []
            case_data.append(self.case_list[i])
            case_data.append(self.case_name_list[i])
            case_data.append(self.FAST_ver)
            case_data.append(self.FAST_exe)
            case_data.append(self.FAST_runDirectory)
            case_data.append(self.FAST_InputFile)
            case_data.append(self.FAST_directory)
            case_data.append(self.read_yaml)
            case_data.append(self.FAST_yamlfile_in)
            case_data.append(self.write_yaml)
            case_data.append(self.FAST_yamlfile_out)
            case_data.append(self.post)

            case_data_all.append(case_data)

        pool.map(eval_multi, case_data_all)

    def run_mpi(self):
        # Run in parallel with mpi, not yet implimented
        print 'MPI interfaced not yet implimented'


def eval(case, case_name, FAST_ver, FAST_exe, FAST_runDirectory, FAST_InputFile, FAST_directory, read_yaml, FAST_yamlfile_in, write_yaml, FAST_yamlfile_out, post):
    # Batch FAST pyWrapper call, as a function outside the runFAST_pywrapper_batch class for pickle-ablility

    fast = runFAST_pywrapper(FAST_ver=FAST_ver)
    fast.FAST_exe           = FAST_exe
    fast.FAST_InputFile     = FAST_InputFile
    fast.FAST_directory     = FAST_directory
    fast.FAST_runDirectory  = FAST_runDirectory

    fast.read_yaml          = read_yaml
    fast.FAST_yamlfile_in   = FAST_yamlfile_in
    fast.write_yaml         = write_yaml
    fast.FAST_yamlfile_out  = FAST_yamlfile_out

    fast.FAST_namingOut     = case_name
    fast.case               = case

    fast.execute()

    # Post process
    if post:
        pass

def eval_multi(data):
    # helper function for running with multiprocessing.Pool.map
    # converts list of arguement values to arguments
    eval(data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8], data[9], data[10], data[11])

def example_runFAST_pywrapper_batch():
    """ 
    Example of running a batch of cases, in serial or in parallel
    """

    fastBatch = runFAST_pywrapper_batch(FAST_ver='OpenFAST')

    fastBatch.FAST_exe = 'C:/Users/egaertne/WT_Codes/openfast/build/glue-codes/fast/openfast.exe'   # Path to executable
    fastBatch.FAST_InputFile = '5MW_Land_DLL_WTurb.fst'   # FAST input file (ext=.fst)
    fastBatch.FAST_directory = 'C:/Users/egaertne/WT_Codes/models/openfast/glue-codes/fast/5MW_Land_DLL_WTurb'   # Path to fst directory files
    fastBatch.FAST_runDirectory = 'temp/OpenFAST'

    ## Define case list explicitly
    # case_list = [{}, {}]
    # case_list[0]['Fst', 'TMax'] = 4.
    # case_list[1]['Fst', 'TMax'] = 5.
    # case_name_list = ['test01', 'test02']

    ## Generate case list using General Case Generator
    ## Specify several variables that change independently or collectly
    case_inputs = {}
    case_inputs[("Fst","TMax")] = {'vals':[10.], 'group':0}
    case_inputs[("InflowWind","WindType")] = {'vals':[1], 'group':0}
    case_inputs[("InflowWind","HWindSpeed")] = {'vals':[8., 9., 10., 11., 12.], 'group':1}
    case_inputs[("ElastoDyn","RotSpeed")] = {'vals':[9.156, 10.296, 11.431, 11.89, 12.1], 'group':1}
    case_inputs[("ElastoDyn","BlPitch1")] = {'vals':[0., 0., 0., 0., 3.823], 'group':1}
    case_inputs[("ElastoDyn","BlPitch2")] = case_inputs[("ElastoDyn","BlPitch1")]
    case_inputs[("ElastoDyn","BlPitch3")] = case_inputs[("ElastoDyn","BlPitch1")]
    case_inputs[("ElastoDyn","GenDOF")] = {'vals':['True','False'], 'group':2}
    
    from CaseGen_General import CaseGen_General
    case_list, case_name_list = CaseGen_General(case_inputs, dir_matrix=fastBatch.FAST_runDirectory, namebase='testing')

    fastBatch.case_list = case_list
    fastBatch.case_name_list = case_name_list

    # fastBatch.run_serial()
    fastBatch.run_multi(2)

    
def example_runFAST_pywrapper():
    """ 
    Example of reading, writing, and running FAST 7, 8 and OpenFAST.
    """

    FAST_ver = 'OpenFAST'
    fast = runFAST_pywrapper(FAST_ver=FAST_ver)

    if FAST_ver.lower() == 'fast7':
        fast.FAST_exe = 'C:/Users/egaertne/WT_Codes/FAST_v7.02.00d-bjj/FAST.exe'   # Path to executable
        fast.FAST_InputFile = 'Test12.fst'   # FAST input file (ext=.fst)
        fast.FAST_directory = 'C:/Users/egaertne/WT_Codes/models/FAST_v7.02.00d-bjj/CertTest/'   # Path to fst directory files
        fast.FAST_runDirectory = 'temp/FAST7'
        fast.FAST_namingOut = 'test'

    elif FAST_ver.lower() == 'fast8':
        fast.FAST_exe = 'C:/Users/egaertne/WT_Codes/FAST_v8.16.00a-bjj/bin/FAST_Win32.exe'   # Path to executable
        fast.FAST_InputFile = 'NREL5MW_onshore.fst'   # FAST input file (ext=.fst)
        fast.FAST_directory = 'C:/Users/egaertne/WT_Codes/models/FAST_v8.16.00a-bjj/ref/5mw_onshore/'   # Path to fst directory files
        fast.FAST_runDirectory = 'temp/FAST8'
        fast.FAST_namingOut = 'test'

    elif FAST_ver.lower() == 'openfast':
        fast.FAST_exe = 'C:/Users/egaertne/WT_Codes/openfast/build/glue-codes/fast/openfast.exe'   # Path to executable
        fast.FAST_InputFile = '5MW_Land_DLL_WTurb.fst'   # FAST input file (ext=.fst)
        fast.FAST_directory = 'C:/Users/egaertne/WT_Codes/models/openfast/glue-codes/fast/5MW_Land_DLL_WTurb'   # Path to fst directory files
        fast.FAST_runDirectory = 'temp/OpenFAST'
        fast.FAST_namingOut = 'test'

        fast.read_yaml = True
        fast.FAST_yamlfile_in = 'temp/OpenFAST/test.yaml'

        fast.write_yaml = False
        fast.FAST_yamlfile_out = 'temp/OpenFAST/test.yaml'


    fast.execute()


if __name__=="__main__":

    # example_runFAST_pywrapper()
    example_runFAST_pywrapper_batch()