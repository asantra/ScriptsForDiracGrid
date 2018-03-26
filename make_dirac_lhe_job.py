#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#=============================================================================
# Make Ganga jobs for MoEDAL simulations - LHE running on DIRAC
#=============================================================================
#

# For the operating system stuff.
import os

# For copying files in Python.
from shutil import copyfile

def replace_text(filename, stringtomatch, stringtoreplace):
    import fileinput
    for line in fileinput.input(filename, inplace = 1):
        print line.replace(stringtomatch, stringtoreplace),

print("*")
print("* Generating the MoEDAL simulation (LHE) configuration file for Ganga (DIRAC)")
print("*")
print("*")

## The run number (determines the random seed).
run_number = 1082

## The basename of the LHE events file.
lhe_file_basename = "unweighted_events.lhe"

## The base LHE file directory.
lfn_path = '/vo.moedal.org/sim/13TEVYY/FilesByArka/SecondTryMarch22/MoEDAL_LHEFiles'

## The geometry DB file location in CVMFS.
geometry_db_file_location = "/cvmfs/moedal.cern.ch/Gauss/Geometry/2-0-0"
#geometry_db_file_location = "/cvmfs/moedal.cern.ch/Gauss/Geometry/2-2-0"

## The magnetic monopole electric charge [e].
monopole_electric_charge = 0

## The Centre-of-Mass energy.
com_energy = '13TeV'

## The magnetic monopole spin.







############## modified by Arka  #####################


betaName                  = ['betaIndependent', 'betaDependent']

magnetic_monopole_spin    = ['SpinZero', 'SpinHalf', 'SpinOne']

monopole_magnetic_charges = ['q10', 'q20', 'q30', 'q40', 'q50', 'q60']

monopole_masses           = {200: 'run_01',  \
                             500: 'run_02',  \
                             1000: 'run_03', \
                             1500: 'run_04', \
                             2000: 'run_05', \
                             2500: 'run_06', \
                             3000: 'run_07', \
                             4000: 'run_08', \
                             5000: 'run_09', \
                             6000: 'run_10'}
                             

## A dictionary of geometry names to geometry files .
geometries = {                       \
    'default':'geometry_default.db', \
    'maximal':'geometry_maximal.db', \
    'minimal':'geometry_minimal.db'}




for n in xrange(0, len(betaName)):
    beta = betaName[n]
    if n == 0:
        prefix = 'No'
    else:
        prefix = ''
        
    ### loop over the spins
    for k in xrange(0, len(magnetic_monopole_spin)):
        spin = magnetic_monopole_spin[k]
        
        ### loop over the charges
        for i in xrange(0, len(monopole_magnetic_charges)):
            charge = monopole_magnetic_charges[i]
            
            ### loop over the monopole masses
            for keyMass in monopole_masses:
                
                ### loop over the different geometries
                for keyGeom in geometries:
                    run = monopole_masses[keyMass]
                    ## The batch name.
                    batch_name = 'myRun_'+beta+'_'+spin+'_'+charge+'_'+run+'_'+keyGeom

                    # Global configuration variables.

                    ## The first event number.
                    first_event_number = 1

                    ## The number of events to run.
                    number_of_events = 10000
                    

                    ## The monopole mass [GeV]
                    monopole_mass = keyMass

                    ## The LHE generation run name.
                    #lhe_run_name = 'run_01'
                    lhe_run_name   = 'RunName_'+beta+'_'+spin+'_'+charge+'_'+run+'_'+keyGeom  ### modified by Arka
                    outputmonopole = 'MonopoleData_'+beta+'_'+spin+'_'+charge+'_'+run+'_'+keyGeom+'.root'
                    outputgen      = 'GenData_'+beta+'_'+spin+'_'+charge+'_'+run+'_'+keyGeom+'.root'
                    outputlog      = 'log.run.'+beta+'.'+spin+'.'+charge+'.'+run+'.'+keyGeom+'.txt'

                    ## The monopole magnetic charge [q_D].
                    monopole_magnetic_charge = i+1

                    ## The magnetic charge label used in the file name.
                    monopole_magnetic_charge_label = charge

                    ## The geometry name.
                    geometry_name = keyGeom

                    ## The geometry filename.
                    geometry_filename = geometries[keyGeom]

                    # Shorten the variable names for convenience...
                    com      = com_energy
                    geo      = geometry_name
                    mag_chrg = monopole_magnetic_charge_label
                    mass     = "m%d" % (monopole_mass)
                    #spin     = magnetic_monopole_spin

                    ## The job name.
                    job_name = "%s_PhotonFusion_%s" % (com, batch_name)

                    ## The name of the configuration.
                    cfg_name = "cfg_" + job_name
                    #
                    print("* Configuration filename: '%s'" % (cfg_name))

                    ## The path of the configuration file.
                    cfg_path = cfg_name + ".py"

                    ## The location of the LHE file on the DIRAC File Catalog.

                    lhe_location = 'LFN:%s/%s/%s/%s/%s/unweighted_events.lhe' % (lfn_path, beta, spin, charge, run) ## done by Arka
                    
                    # Add the LFN to the inputfiles list (DiracFile).
                    
                    cfg_ganga_lhe_name = 'cfg_ganga_lhe_run_'+beta+'_'+spin+'_'+charge+'_'+run+'_'+keyGeom+'.py'
                    

                    #
                    print 'LHE sample LFN: ', lhe_location
                    print 'cfg path: ', cfg_path
                    print 'first event number: ', first_event_number
                    print 'run number: ', run_number
                    print 'lhe_file_basename: ', lhe_file_basename
                    print 'geometry_db_file_location: ', geometry_db_file_location
                    print 'geometry_filename: ', geometry_filename
                    print 'monopole_mass: ', monopole_mass
                    print 'monopole_electric_charge: ', monopole_electric_charge
                    print 'monopole_magnetic_charge: ', monopole_magnetic_charge
                    print 'number_of_events: ', number_of_events
                    print 'monopoleData: ', outputmonopole
                    print 'genData: ', outputgen
                    print 'logFile: ', outputlog
                    print 'cfg_ganga_lhe_name: ', cfg_ganga_lhe_name
                    print 'cfg_path: ', cfg_path
                    print("*********************************")

                    

                    # Create a copy of the configuration file from the template.
                    copyfile('configuration_LHE_TEMPLATE.py', cfg_path)

                    # Replace the first event number variable.
                    replace_text(cfg_path, "FIRST_EVENT_NUMBER", "%d" % (first_event_number))

                    # Replace the run number variable.
                    replace_text(cfg_path, "RUN_NUMBER", "%d" % (run_number))

                    # Replace the LHE file basename.
                    replace_text(cfg_path, "LHE_FILE_BASENAME", lhe_file_basename)

                    replace_text(cfg_path, "GEOMETRY_DB_FILE_LOCATION", geometry_db_file_location)

                    replace_text(cfg_path, "GEOMETRY_DB_FILENAME", geometry_filename)

                    replace_text(cfg_path, "MONOPOLE_MASS_GEV", "%d" % (monopole_mass))

                    replace_text(cfg_path, "MONOPOLE_ELECTRIC_CHARGE", "%d" % (monopole_electric_charge))

                    replace_text(cfg_path, "MONOPOLE_MAGNETIC_CHARGE", "%d" % (monopole_magnetic_charge))

                    replace_text(cfg_path, "NUMBER_OF_EVENTS", "%d" % (number_of_events))
                    
                    replace_text(cfg_path, "MONOPOLE_DATA_ROOT", "%s" % (outputmonopole))
                    
                    replace_text(cfg_path, "GEN_DATA_ROOT", "%s" % (outputgen))

                    # Add config to the inputfiles list (LocalFile).

                    

                    # Create a copy of the configuration file to use in the job.
                    copyfile(cfg_path, cfg_ganga_lhe_name)

                    exit()
                    # Create the job.
                    j = Job()
                    # Set the job name (using the cfg name).
                    j.name = job_name
                    j.application = Executable()
                    #j.application.exe = File('run_lhe_v48r1.sh')
                    j.application.exe = File('run_lhe_v49r7.sh')
                    j.application.args = []

                    # DIRAC running
                    j.inputfiles = [LocalFile(cfg_path), LocalFile(cfg_ganga_lhe_name), DiracFile(lhe_location)]

                    # Output files will be remotely stored, and can be retrieved from vo.moedal.org/user/...
                    j.outputfiles = [ DiracFile(outputmonopole), DiracFile(outputgen), DiracFile('ParticlePropertySvc_Monopole.txt'), DiracFile(outputlog), DiracFile(cfg_path) ]

                    # Output files will be locally stored, in $HOME/gangadir/workspace/gridpp/LocalXML
                    #j.outputfiles = [ LocalFile('MonopoleData.root'), LocalFile('GenData.root'), LocalFile('ParticlePropertySvc_Monopole.txt'), LocalFile('log.run.txt'), LocalFile(cfg_path) ]

                    j.backend = Dirac()

                    # Uncomment when ready to submit automatically.
                    #j.submit()





