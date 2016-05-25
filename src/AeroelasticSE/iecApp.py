
import os

from fusedwind.runSuite.runCase import GenericRunCaseTable
from fusedwind.runSuite.runBatch import get_options, parse_input, CaseAnalyzer

#from peregrineallocators import ClusterAllocator
from openmdao.main.resource import ResourceAllocationManager as RAM

from FusedFAST import openFAST 

# this is a callback function used in processing output.
# see fusedwind.runSuite.runBatch.py, "output_operations"
def rf(col):
    # import python version of rainflow algorithm
    from rainflow import rain_one
    # wrapper for rainflow algorithm
    # rain_one(column of data, exponent in final load calculation)
    val = rain_one(col, 5)
    return val

def rundlcs_bybatch(envcmd, options, args, batch_size):
## this is a workaround for the openmdao parallel running out of memory madness: memory leaks and/or buildups
# in the case iterator driver mean we can only do a couple hundred FAST runs at a time.
# strategy here will be to break the big batch up into many little batches, then do one final "no run" (but collect)
# run for the whole batch at the end
    all_cases = options.cases
    lns = file(all_cases).readlines()
    all_cnt = len(lns)-1  # -1 for header line
    cnt = 0
    batch = 0
    while cnt < all_cnt:
        this_case = "%s.%d" % (all_cases,batch)
        fout = file(this_case, "w")
        fout.write(lns[0])
        end = min(cnt+batch_size, all_cnt)
        for i in range(cnt+1,end+1):
            fout.write(lns[i])
        fout.close()
        options.cases = this_case
        rundlcs(envcmd, options, args)
        cnt += batch_size
        batch += 1
    
    saveit = options.norun
    options.norun = True
    options.cases = all_cases
    rundlcs(envcmd, options, args, batch_size=None)
    options.norun = saveit


def line_count(fname):
    num_lines = sum(1 for line in open(fname))
    return num_lines

## main function that opens input, runs cases, writes output, ie. whole thing.
def rundlcs(envcmd = None, options=None, args=None, batch_size=5):
    """ 
    run the whole process, including startup and shutdown
    to do:
    parse input
    create load cases
    create app assembly
    create dispatcher
    send cases and app to dispatcher
    run cases
    collect and save output

    envcmd: a text string cmd (e.g. 'source env.sh') to set up the environment for the cluster allocator
    """    

    if (batch_size != None and line_count(options.cases)-1 > batch_size):
        rundlcs_bybatch(envcmd, options, args, batch_size)
        return

    if options==None:
        options, args = get_options()
    print options
    ctrl = parse_input(options)
    # ctrl will be just the input, but broken up into separate categories, e.g.
    # ctrl.cases, ctrl.app, ctrl.dispatch, ...

    # work in progress; running efficiently at NREL.
    if (options.cluster_allocator):
#        cluster=ClusterAllocator()
### never had the guts to try this yet!
#        env = os.environ
#        fname = "%s/.env.sh" % (env['HOME'])
#        fout = file(fname, "w")
#        for key in env:
#            fout.write("export %s=%s\n" % (key,env[key]))
#        fout.close()
###
        if envcmd == None:
            cluster=ClusterAllocator()
        else:
            cluster=ClusterAllocator(use_modules=False, beforestart=envcmd)        
#        cluster=ClusterAllocator(use_modules=False, beforestart=". %s;" % fname)        
        RAM.remove_allocator('LocalHost')
        RAM.add_allocator(cluster)
#        RAM.insert_allocator(0,cluster)
            
    ###  using "factory" functions to create specific subclasses (e.g. distinguish between FAST and HAWC2)
    # Then we use these to create the cases...
    case_params = ctrl.cases
    casetab = GenericRunCaseTable()
    casetab.initFromFile(case_params['source_file'], verbose=True, start_at = options.start_at)

    # solver...
    solver = 'FAST'
#    solver = 'HAWC2'
    if solver=='FAST':
        ## TODO, changed when we have a real turbine
        # aero code stuff: for constructors
        aerocode = openFAST(ctrl.output)  ## need better name than output_params
        aerocode.setOutput(ctrl.output)
    elif solver == 'HAWC2':
        aerocoe = openHAWC2(None)
        raise NotImplementedError, "HAWC2 aeroecode wrapper not implemented in runBatch.py yet"
    else:
        raise ValueError, "unknown aerocode: %s" % solver
    
    # case iterator
    dispatcher = CaseAnalyzer(ctrl.dispatcher)

    ### After this point everything should be generic, all appropriate subclass object created
    # # # # # # # # # # #

    dispatcher.presetup_workflow(aerocode, casetab.cases)  # just makes sure parts are there when configure() is called
    dispatcher.configure()
    # Now tell the dispatcher to (setup and ) run the cases using the aerocode on the turbine.
    # calling configure() is done inside run(). but now it is done already (above), too.
    
    # norun does not write directories, but it does set us up to process them if they already exist
    if (not options.norun):
        dispatcher.run()

    # TODO:  more complexity will be needed for difference between "run now" and "run later" cases.
    dispatcher.collect_output(ctrl.output)
    

if __name__=="__main__":
    rundlcs()

