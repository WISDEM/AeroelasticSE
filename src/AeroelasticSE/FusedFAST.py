import os,glob,shutil

from openmdao.main.api import Component, Assembly, FileMetadata
from openmdao.lib.components.external_code import ExternalCode
from openmdao.main.datatypes.slot import Slot
from openmdao.main.datatypes.instance import Instance
from openmdao.main.datatypes.api import Array, Float, Str


from newrunFAST import runFAST
from runTurbSim import runTurbSim

from FusedFASTrunCase import FASTRunCaseBuilder, FASTRunCase, FASTRunResult

from fusedwind.runSuite.runAero import openAeroCode
from fusedwind.runSuite.runCase import GenericRunCase, RunCase, RunResult, IECRunCaseBaseVT




class openFAST(openAeroCode):
    
    code_input = Instance(FASTRunCase, iotype='in')

    def __init__(self, filedict):
        self.runfast = runFASText(filedict)
        self.runts = runTurbSimext(filedict)

        ## this is repeated in runFASText, should consolodate
        self.basedir = os.path.join(os.getcwd(),"all_runs")
        if 'run_dir' in filedict:
            self.basedir = os.path.join(os.getcwd(),filedict['run_dir'])

        super(openFAST, self).__init__()
        print "openFAST __init__"

    def getRunCaseBuilder(self):
        return FASTRunCaseBuilder()

    def configure(self):
        print "openFAST configure"
        self.add('tsrunner', self.runts)
        self.driver.workflow.add(['tsrunner'])
        self.add('runner', self.runfast)
        self.driver.workflow.add(['runner'])
        self.connect('code_input', 'runner.inputs')
        self.connect('code_input', 'tsrunner.inputs')
        self.connect('runner.outputs', 'outputs')        
        self.connect('tsrunner.tswind_file', 'runner.tswind_file')

    def execute(self):
        print "openFAST.execute(), case = ", self.inputs
        run_case_builder = self.getRunCaseBuilder()
        dlc = self.inputs 
#        print "executing", dlc.case_name
        self.code_input = run_case_builder.buildRunCase(dlc)
        super(openFAST, self).execute()

    def getResults(self, keys, results_dir, operation=max):
        myfast = self.runfast.rawfast        
        col = myfast.getOutputValues(keys, results_dir)
#        print "getting output for keys=", keys
        vals = []
        for i in range(len(col)):
            c = col[i]
            try:
                val = operation(c)
            except:
                val = None
            vals.append(val)
        return vals

    def setOutput(self, output_params):
        self.runfast.set_fast_outputs(output_params['output_keys'])
        print "set FAST output:", output_params['output_keys']


class runTurbSimext(Component):
    """ a component to run TurbSim.
        will try to make it aware of whether the wind file already exists"""
    
    inputs = Instance(IECRunCaseBaseVT, iotype='in')
    tswind_file = Str(iotype='out')

    def __init__(self, filedict):
        super(runTurbSimext,self).__init__()
        self.rawts = runTurbSim()
    
        self.rawts.ts_exe = filedict['ts_exe']
        self.rawts.ts_dir = filedict['ts_dir']
        self.rawts.ts_file = filedict['ts_file']
#        self.rawts.run_name = self.run_name

        self.basedir = os.path.join(os.getcwd(),"allts_runs")
        if 'run_dir' in filedict:
            self.basedir = os.path.join(os.getcwd(),filedict['run_dir'])
        if (not os.path.exists(self.basedir)):
            os.mkdir(self.basedir)

    def execute(self):
        case = self.inputs
        ws=case.fst_params['Vhub']
        tmax = 2  ## should not be hard default ##
        if ('TMax' in case.fst_params):  ## Note, this gets set via "AnalTime" in input files--FAST peculiarity ? ##
            tmax = case.fst_params['TMax']

        # run TurbSim to generate the wind:        
        # for now, turbsim params we mess with are possibly: TMax, RandomSeed, Tmax.  These should generate
        # new runs, otherwise we should just use wind file we already have
            # for now, just differentiate by wind speed
        ts_case_name = "TurbSim-Vhub%.4f" % ws

        run_dir = os.path.join(self.basedir, ts_case_name)
        print "running TurbSim in " , run_dir
        self.rawts.run_dir = run_dir
        self.rawts.set_dict({"URef": ws, "AnalysisTime":tmax, "UsableTime":tmax})
        tsoutname = self.rawts.ts_file.replace("inp", "wnd")
        tsoutname = os.path.join(run_dir, tsoutname)
        reused_run = False
        if (os.path.isfile(tsoutname)):
            # maybe there's an old results we can use:
            tssumname = tsoutname.replace("wnd", "sum")
            ln = file(tssumname).readlines()[-1]
            if (ln != None and ln != "" and len(ln) > 0 and ln.split(".")[0] == "Processing complete"):
                print "re-using previous TurbSim output %s for ws = %f" % (tsoutname, ws)
                reused_run = True
        
        if (not reused_run):
            self.rawts.execute() 

        # here we link turbsim -> fast
        self.tswind_file = tsoutname


class runFASText(Component):
    """ 
        this used to be an ExternalCode class to take advantage of file copying stuff.
        But now it relies on the global file system instead.
        it finally calls the real (openMDAO-free) FAST wrapper 
    """
    inputs = Instance(IECRunCaseBaseVT, iotype='in')
#    input = Instance(GenericRunCase, iotype='in')
    outputs = Instance(RunResult, iotype='out')  ## never used, never even set
    tswind_file = Str(iotype='in')

    ## just a template, meant to be reset by caller
    fast_outputs = ['WindVxi','RotSpeed', 'RotPwr', 'GenPwr', 'RootMxc1', 'RootMyc1', 'LSSGagMya', 'LSSGagMza', 'YawBrMxp', 'YawBrMyp','TwrBsMxt',
                    'TwrBsMyt', 'Fair1Ten', 'Fair2Ten', 'Fair3Ten', 'Anch1Ten', 'Anch2Ten', 'Anch3Ten'] 

    def __init__(self, filedict):
        super(runFASText,self).__init__()
        self.rawfast = runFAST()

        print "runFASText init(), filedict = ", filedict

        # probably overridden by caller
        self.rawfast.setOutputs(self.fast_outputs)

        # if True, results will be copied back to basedir+casename.
        # In context of global file system, this is not necessary.  Instead, leave False and postprocess directly from run_dirs.
        self.copyback_files = False
 
        have_tags = all([tag in filedict for tag in ["fst_exe", "fst_dir", "fst_file", "ts_exe", "ts_dir", "ts_file"]])
        if (not have_tags):
            print "Failed to provide all necessary files/paths: fst_exe, fst_dir, fst_file, ts_exe, ts_dir, ts_file  needed to run FAST"
            raise ValueError, "Failed to provide all necessary files/paths: fst_exe, fst_dir, fst_file, ts_exe, ts_dir, ts_file  needed to run FAST"

        self.rawfast.fst_exe = filedict['fst_exe']
        self.rawfast.fst_dir = filedict['fst_dir']
        self.rawfast.fst_file = filedict['fst_file']
        self.run_name = self.rawfast.fst_file.split(".")[0]
        self.rawfast.run_name = self.run_name

        self.basedir = os.path.join(os.getcwd(),"all_runs")
        if 'run_dir' in filedict:
            self.basedir = os.path.join(os.getcwd(),filedict['run_dir'])
        if (not os.path.exists(self.basedir)):
            os.mkdir(self.basedir)

    def set_fast_outputs(self,fst_out):
        self.fast_outputs = fst_out
        self.rawfast.setOutputs(self.fast_outputs)
                
    def execute(self):
        case = self.inputs

        ws=case.fst_params['Vhub']
        tmax = 2  ## should not be hard default ##
        if ('TMax' in case.fst_params):  ## Note, this gets set via "AnalTime" in input files--FAST peculiarity ? ##
            tmax = case.fst_params['TMax']

        # TurbSim has already been run to generate the wind, it's output is
        # connected as tswind_file
        self.rawfast.set_wind_file(self.tswind_file)

        run_dir = os.path.join(self.basedir, case.case_name)
        print "running FASTFASTFAST in " , run_dir, case.case_name

        ### actually execute FAST (!!) 
        print "RUNNING FAST WITH RUN_DIR", run_dir
        self.rawfast.run_dir = run_dir
        self.rawfast.set_dict(case.fst_params)
        # FAST object write its inputs in execute()
        self.rawfast.execute()
        ###

        # gather output directly
        self.output = FASTRunResult(self)
        
        # also, copy all the output and input back "home"
        if (self.copyback_files):
            self.results_dir = os.path.join(self.basedir, case.case_name)
            try:
                os.mkdir(self.results_dir)
            except:
                # print 'error creating directory', results_dir
                # print 'it probably already exists, so no problem'
                pass

            # Is this supposed to do what we're doing by hand here?
            # self.copy_results_dirs(results_dir, '', overwrite=True)

            files = glob.glob( "%s.*" % os.path.join(self.rawfast.run_dir, self.rawfast.run_name))
            files += glob.glob( "%s.*" % os.path.join(self.rawts.run_dir, self.rawts.run_name))
            
            for filename in files:
#                print "wanting to copy %s to %s" % (filename, results_dir) ## for debugging, don't clobber stuff you care about!
                shutil.copy(filename, self.results_dir)



class designFAST(openFAST):        
    """ base class for cases where we have parametric design (e.g. dakota),
    corresponding to a driver that are for use within a Driver that "has_parameters" """
    x = Array(iotype='in')   ## exact size of this gets filled in study.setup_cases(), which call create_x, below
    f = Float(iotype='out')
    # need some mapping back and forth
    param_names = []

    def __init__(self,geom,atm,filedict):
        super(designFAST, self).__init__(geom,atm,filedict)

    def create_x(self, size):
        """ just needs to exist and be right size to use has_parameters stuff """
        self.x = [0 for i in range(size)]

    def dlc_from_params(self,x):
        print x, self.param_names, self.dlc.case_name
        case = FASTRunCaseBuilder.buildRunCase_x(x, self.param_names, self.dlc)
        print case.fst_params
        return case

    def execute(self):
        # build DLC from x, if we're using it
        print "in design code. execute()", self.x
        self.inputs = self.dlc_from_params(self.x)
        super(designFAST, self).execute()
        myfast = self.runfast.rawfast
        self.f = myfast.getMaxOutputValue('TwrBsMxt', directory=os.getcwd())



def designFAST_test():
    w = designFAST()

    ## sort of hacks to save this info
    w.param_names = ['Vhub']
    w.dlc = FASTRunCase("runAero-testcase", {}, None)
    print "set aerocode dlc"
    ##

    res = []
    for x in range(10,16,2):
        w.x = [x]
        w.execute()
        res.append([ w.dlc.case_name, w.param_names, w.x, w.f])
    for r in res:
        print r


def openFAST_test():
    # in real life these come from an input file:
    filedict = {'ts_exe' : "/Users/pgraf/opt/windcode-7.31.13/TurbSim/build/TurbSim_glin64",
                'ts_dir' : "/Users/pgraf/work/wese/fatigue12-13/from_gordie/SparFAST3.orig/TurbSim",
                'ts_file' : "TurbSim.inp",
                'fst_exe' : "/Users/pgraf/opt/windcode-7.31.13/build/FAST_glin64",
                'fst_dir' : "/Users/pgraf/work/wese/fatigue12-13/from_gordie/SparFAST3.orig",
                'fst_file' : "NRELOffshrBsline5MW_Floating_OC3Hywind.fst",
                'run_dir' : "run_dir"}

    w = openFAST(filedict)
    tmax = 5
    res = []
    for x in [10,16,20]:
        dlc = GenericRunCase("runAero-testcase%d" % x, ['Vhub','AnalTime'], [x,tmax])
#        dlc = FASTRunCase("runAero-testcase%d" % x, {'Vhub':x, 'AnalTime':tmax}, {})
        w.inputs = dlc
        w.execute()



if __name__=="__main__":
    openFAST_test()
#    designFAST_test()
