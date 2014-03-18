
import os

from fusedwind.runSuite.runCase import GenericRunCaseTable
from fusedwind.runSuite.runBatch import get_options, parse_input, CaseAnalyzer

#from peregrineallocators import ClusterAllocator
from openmdao.main.resource import ResourceAllocationManager as RAM

from FusedFAST import openFAST 

# this is a callback function used in processing output.
# see runBatch.py "output_operations"
def rf(col):
    # import python version of rainflow algorithm
    from rainflow import rain_one
    # wrapper for rainflow algorithm
    # rain_one(column of data, exponent in final load calculation)
    val = rain_one(col, 5)
    return val

## main function that opens input, runs cases, writes output, ie. whole thing.
def rundlcs():
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
    """    

    options, arg = get_options()
    ctrl = parse_input(options)
    # ctrl will be just the input, but broken up into separate categories, e.g.
    # ctrl.cases, ctrl.app, ctrl.dispatch, ...

    # work in progress; running efficiently at NREL.
    if (options.cluster_allocator):
        cluster=ClusterAllocator()
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

