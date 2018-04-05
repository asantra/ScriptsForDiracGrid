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

## The batch name.
batch_name = 'myrun001'

# Global configuration variables.

## The first event number.
first_event_number = 1

## The number of events to run.
number_of_events = 100

## The run number (determines the random seed).
run_number = 1082

## The basename of the LHE events file.
lhe_file_basename = "unweighted_events.lhe"

## The base LHE file directory.
lfn_path = '/vo.moedal.org/sim/13TEVYY/FilesByArka/SecondTryMarch22/MoEDAL_LHEFiles'

## The geometry DB file location in CVMFS.
#geometry_db_file_location = "/cvmfs/moedal.cern.ch/Gauss/Geometry/2-0-0"
#geometry_db_file_location = "/cvmfs/moedal.cern.ch/Gauss/Geometry/3-0-0"
geometry_db_file_location = "/cvmfs/moedal.cern.ch/Gauss/Geometry/3-1-0"

## The magnetic monopole electric charge [e].
monopole_electric_charge = 0

## The Centre-of-Mass energy.
com_energy = '13TeV'

## The magnetic monopole spin.
magnetic_monopole_spin = 'SpinZero'

# Also available - 'SpinHalf'.

## The monopole mass [GeV]
monopole_mass = 200

## The LHE generation run name.
lhe_run_name = 'run_01'

## The monopole magnetic charge [q_D].
monopole_magnetic_charge = 1

## The magnetic charge label used in the file name.
monopole_magnetic_charge_label = 'q10'

## The geometry name.
geometry_name = 'default'

## The geometry filename.
geometry_filename = 'geometry_default.db'

# Shorten the variable names for convenience...
com      = com_energy
geo      = geometry_name
mag_chrg = monopole_magnetic_charge_label
mass     = "m%d" % (monopole_mass)
spin     = magnetic_monopole_spin
beta     = 'betaIndependent'

## The job name.
job_name = "%s_%s_%s_PhotonFusion_%s_%s_%s" % (com, spin, geo, mag_chrg, mass, batch_name)

## The name of the configuration.
cfg_name = "cfg_" + job_name
#
print("* Configuration filename: '%s'" % (cfg_name))

## The path of the configuration file.
cfg_path = cfg_name + ".py"

## The location of the LHE file on the DIRAC File Catalog.
#lhe_location = 'LFN:%s/%s/%s/Events/%s/unweighted_events.lhe.gz' % (lfn_path, com, spin, lhe_run_name)

lhe_location = 'LFN:%s/%s/%s/%s/%s/unweighted_events.lhe' % (lfn_path, beta, spin, mag_chrg, lhe_run_name) ## done by Arka
#
print("* LHE sample LFN = '%s'" % (lhe_location))
print("*")

outputmonopole = "MonopoleData.root"

outputgen      = "GenData.root"

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

# Add the LFN to the inputfiles list (DiracFile).

# Create a copy of the configuration file to use in the job.
copyfile(cfg_path, 'cfg_ganga_lhe_run.py')

# Create the job.
j = Job()
# Set the job name (using the cfg name).
j.name = job_name
j.application = Executable()
#j.application.exe = File('run_lhe_v48r1.sh')
#j.application.exe = File('run_lhe_v49r7.sh')
j.application.exe = File('run_lhe_v49r8.sh')
j.application.args = []

# DIRAC running
j.inputfiles = [LocalFile(cfg_path), LocalFile('cfg_ganga_lhe_run.py'), DiracFile(lhe_location)]

# Output files will be remotely stored, and can be retrieved from vo.moedal.org/user/...
#j.outputfiles = [ DiracFile('MonopoleData.root'), DiracFile('GenData.root'), DiracFile('ParticlePropertySvc_Monopole.txt'), DiracFile('log.run.txt'), DiracFile(cfg_path) ]

# Output files will be locally stored, in $HOME/gangadir/workspace/gridpp/LocalXML
j.outputfiles = [ LocalFile(outputmonopole), LocalFile(outputgen), LocalFile('ParticlePropertySvc_Monopole.txt'), LocalFile('log.run.txt'), LocalFile(cfg_path) ]

j.backend = Dirac()

# Uncomment when ready to submit automatically.
j.submit()
