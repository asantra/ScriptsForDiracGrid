#!/usr/bin/env python
# -*- coding: utf-8 -*-

############################################################################
# Import statements
############################################################################

from Gauss.Configuration import *

from Gaudi.Configuration import *

from Configurables import Generation

from Configurables import Special

from Configurables import FixedNInteractions

from Configurables import ReadLHEfileProduction

from Configurables import Gauss, GiGa, GiGaPhysListModular, GiGaPhysConstructorMonopole

from Configurables import LHCb__ParticlePropertySvc

from Configurables import GaudiSequencer, MonopoleTupleAlg, GenTupleAlg

from Configurables import GiGaPhysConstructorOp, GiGaPhysConstructorHpd

from Configurables import LHCbApp

from Configurables import CondDB, CondDBAccessSvc, GiGaInputStream

from Configurables import GetMMTHitsAlg, GetNTDHitsAlg

from GaudiKernel import SystemOfUnits

from Configurables import LHCb__ParticlePropertySvc

from Configurables import MonopoleTupleAlg, GenTupleAlg


##############################################################################

#-----------------------------------------------------------------------------
# Generator phase
#-----------------------------------------------------------------------------
GaussGen = GenInit("GaussGen")
#
# Set the random numbers - these fix the random seed.
#
GaussGen.FirstEventNumber = 1
GaussGen.RunNumber        = 1082

# The output is managed below, so we disable the standard Gauss output.
Gauss().OutputType = 'NONE'
Gauss().Histograms = 'NONE'

# Switch off pileup (recommended!).
Generation().addTool(FixedNInteractions, name="FixedNInteractions")
Generation().FixedNInteractions.NInteractions = 0
Generation().PileUpTool = "FixedNInteractions"

# Define "special" production.
Generation().addTool(Special,"Special")
Generation().SampleGenerationTool = "Special"

# No cuts.
Generation().Special.CutTool = ""

# Define the production tool
Generation().Special.addTool(ReadLHEfileProduction, name="ReadLHEfileProduction")
Generation().Special.ProductionTool = "ReadLHEfileProduction"

## Define the input file in LHE xml format.
Generation().Special.ReadLHEfileProduction.InputFile = "unweighted_events.lhe"

##############################################################################
# Monopole physics
##############################################################################

# Set add monopole physics constructor from GaussMonopoles to the GiGa
# physics list.
giga = GiGa()
giga.addTool( GiGaPhysListModular("ModularPL") , name="ModularPL" )
giga.ModularPL.addTool( GiGaPhysConstructorMonopole, name = "GiGaPhysConstructorMonopole" )


############################################################################
## Add the Ntuple writer to the Simulation Monitor

## Kind of a hack, but works
monopoleTupleAlg = MonopoleTupleAlg()
GaudiSequencer("SimMonitor").Members+= [ monopoleTupleAlg ]
genTupleAlg = GenTupleAlg()
GaudiSequencer("GenMonitor").Members+= [ genTupleAlg ]

############################################################################
## Switch off RICH physics (leave geometry)
giga.ModularPL.addTool( GiGaPhysConstructorOp,  name = "GiGaPhysConstructorOp"  )
giga.ModularPL.addTool( GiGaPhysConstructorHpd, name = "GiGaPhysConstructorHpd" )
giga.ModularPL.GiGaPhysConstructorOp.RichOpticalPhysicsProcessActivate = False
giga.ModularPL.GiGaPhysConstructorHpd.RichHpdPhysicsProcessActivate = False

## Note that the options and the tags will be used directly from ${GAUSSOPTS}
# Pick beam conditions as set in AppConfig. 
#importOptions("$APPCONFIGOPTS/Gauss/Beam6500GeV-md100-nu1.6.py")
#importOptions("$APPCONFIGOPTS/Gauss/DataType-2015.py")
# Set the database tags using those for Sim08.
#LHCbApp().DDDBtag   = "dddb-20140729"
#LHCbApp().CondDBtag = "sim-20140730-vc-md100"

############################################################################
# Database options
############################################################################

# Add sqlite database to CondDB and turn on MoEDAL geometry

############################################################################
## Add geometry data
## Two options:
## Overwrite entire DDDB with file contents
#cdb = CondDB()
#cbd.PartitionConnectionString["DDDB"] = "sqlite_file:$HOME/LHCb_software/mkingtest.db/DDDB"
#cdb.Tags[DDDB] = "DC06"

## Add file contents as layer (should overwrite existing entries in same location)
CondDB(). addLayer(
    CondDBAccessSvc("MoEDAL_DDDB",
        ConnectionString = "sqlite_file:/cvmfs/moedal.cern.ch/Gauss/Geometry/2-0-0/geometry_default.db/DDDB",
        DefaultTAG = "HEAD"))

############################################################################
## Switch on geometry for MoEDAL detectors
geo = GiGaInputStream('Geo')

geo.StreamItems += [ "/dd/Structure/LHCb/BeforeMagnetRegion/MoEDAL/VacTankCoverPipes" ]
geo.StreamItems += [ "/dd/Structure/LHCb/BeforeMagnetRegion/MoEDAL/VacTankCoverHead" ]

## When using tag 2.2.0, please activate the VacTankTopFlanges
#geo.StreamItems += [ "/dd/Structure/LHCb/BeforeMagnetRegion/MoEDAL/VacTankTopFlanges" ]

geo.StreamItems += [ "/dd/Structure/LHCb/BeforeMagnetRegion/MoEDAL/DetectorVacuum" ]
geo.StreamItems += [ "/dd/Structure/LHCb/BeforeMagnetRegion/MoEDAL/VacuumPump" ]
geo.StreamItems += [ "/dd/Structure/LHCb/BeforeMagnetRegion/MoEDAL/VeloDustCover" ]
geo.StreamItems += [ "/dd/Structure/LHCb/BeforeMagnetRegion/MoEDAL/ExtraMaterial" ]

geo.StreamItems += [ "/dd/Structure/LHCb/BeforeMagnetRegion/MoEDAL/VacuumManifolds" ]

geo.StreamItems += [ "/dd/Structure/LHCb/BeforeMagnetRegion/MoEDAL/MMT1" ]
geo.StreamItems += [ "/dd/Structure/LHCb/BeforeMagnetRegion/MoEDAL/MMT2" ]
geo.StreamItems += [ "/dd/Structure/LHCb/BeforeMagnetRegion/MoEDAL/MMT3" ]
geo.StreamItems += [ "/dd/Structure/LHCb/BeforeMagnetRegion/MoEDAL/HCC2015" ]
geo.StreamItems += [ "/dd/Structure/LHCb/BeforeMagnetRegion/MoEDAL/NTD2015" ]


##############################################################################
# Subdetector management
##############################################################################

# Activate MMT, HCC, and NTD sensitive detectors

getMMTHits = GetMMTHitsAlg("GetMMTHits")
getMMTHits.CollectionName = "MMT/Hits"
getMMTHits.MCHitsLocation = "/Event/MC/MMT/Hits"
getMMTHits.Detectors      = [ "/dd/Structure/LHCb/BeforeMagnetRegion/MoEDAL/MMT1" ]
GaudiSequencer("DetectorsHits").Members += [ getMMTHits ]

getMMTHits = GetMMTHitsAlg("GetMMTHits")
getMMTHits.CollectionName = "MMT/Hits"
getMMTHits.MCHitsLocation = "/Event/MC/MMT/Hits"
getMMTHits.Detectors      = [ "/dd/Structure/LHCb/BeforeMagnetRegion/MoEDAL/MMT2" ]
GaudiSequencer("DetectorsHits").Members += [ getMMTHits ]

getMMTHits = GetMMTHitsAlg("GetMMTHits")
getMMTHits.CollectionName = "MMT/Hits"
getMMTHits.MCHitsLocation = "/Event/MC/MMT/Hits"
getMMTHits.Detectors      = [ "/dd/Structure/LHCb/BeforeMagnetRegion/MoEDAL/MMT3" ]
GaudiSequencer("DetectorsHits").Members += [ getMMTHits ]

getNTDHits = GetNTDHitsAlg("GetNTDHits")
getNTDHits.CollectionName = "NTD/Hits"
getNTDHits.MCHitsLocation = "/Event/MC/NTD/Hits"
getNTDHits.Detectors      = [ "/dd/Structure/LHCb/BeforeMagnetRegion/MoEDAL/HCC2015" ]
## Disable NTD hit retrieval when NTDs are disabled in geometry
GaudiSequencer("DetectorsHits").Members += [ getNTDHits ]

getNTDHits = GetNTDHitsAlg("GetNTDHits")
getNTDHits.CollectionName = "NTD/Hits"
getNTDHits.MCHitsLocation = "/Event/MC/NTD/Hits"
getNTDHits.Detectors      = [ "/dd/Structure/LHCb/BeforeMagnetRegion/MoEDAL/NTD2015" ]
## Disable NTD hit retrieval when NTDs are disabled in geometry
GaudiSequencer("DetectorsHits").Members += [ getNTDHits ]


##############################################################################
# Define the MoEDAL option variables
##############################################################################

# Define the monopole properties.

## The magnetic monopole PDG ID.
monopole_pdg       = 4110000 #shouldn't coincide with other particles

#monopole_mass      = 1000 # [GeV]

## The magnetic monopole mass [GeV].
monopole_mass      = 2000 # [GeV]

## The magnetic monopole electric charge [e].
monopole_elcharge  = 0 # [e]

## The magnetic monopole magnetic charge [g_D].
monopole_magcharge = 1 # [g_D]

# Define the monopole behavior.

## Use fields?
monopole_usefields = True

## The minimum beta for the magnetic monopoles.
monopole_minbeta   = 1.0e-3

## nint/step:  q =    0,   1,   2,   3,   4,   5,   6

nintpersteparray = [  1,  10,  20,  40,  80, 160, 320]

nintperstep = nintpersteparray[ int(monopole_magcharge) ]


##############################################################################
# Gauss controls
##############################################################################

## The number of events to process.
LHCbApp().EvtMax = 10000

# Define input file in LHE xml format
# This should have been specified in cfg_lhe.py file.
#Generation().Special.ReadLHEfileProduction.InputFile = "events.lhe"

##############################################################################
# Output files
##############################################################################

## The output filename.
MonopoleTupleAlg().OutputNtupleFilename = "MonopoleData_betaIndependent_SpinZero_q10_run_05_default.root"

## Should we read the NTD hits?
MonopoleTupleAlg().ReadNTDHits = True

## The generator information output filename.
GenTupleAlg().OutputNtupleFilename = "GenData_betaIndependent_SpinZero_q10_run_05_default.root"


##############################################################################
# Apply variables to MoEDAL options
##############################################################################

GiGa().ModularPL.GiGaPhysConstructorMonopole.PdgId     = monopole_pdg
GiGa().ModularPL.GiGaPhysConstructorMonopole.Mass      = monopole_mass
GiGa().ModularPL.GiGaPhysConstructorMonopole.ElCharge  = monopole_elcharge
GiGa().ModularPL.GiGaPhysConstructorMonopole.MagCharge = monopole_magcharge

GiGa().ModularPL.GiGaPhysConstructorMonopole.UseFields = monopole_usefields
GiGa().ModularPL.GiGaPhysConstructorMonopole.MinBeta   = monopole_minbeta
GiGa().ModularPL.GiGaPhysConstructorMonopole.NumberOfInteractionsPerStep = nintperstep


############################################################################
## Add monopole information to Ntuple writer
## (should retrieve particle information from ParticlePropertySvc, but no magnetic charge field available)
MonopoleTupleAlg().MonopolePdgs  = [ monopole_pdg,       -monopole_pdg       ]
MonopoleTupleAlg().MonopoleQmags = [ monopole_magcharge, -monopole_magcharge ]
GenTupleAlg().MonopolePdgs       = [ monopole_pdg,       -monopole_pdg       ]
GenTupleAlg().MonopoleQmags      = [ monopole_magcharge, -monopole_magcharge ]


##############################################################################
# Patch ParticlePropertySvc to include the monopole details.
# It's not yet entirely clear what uses this and what uses the (i.e. mass)
# definitions in GiGaPhysConstructorMonopole.
# - Either the simulation or generation phases in Gauss definitely use these
# values.
ParticlePropertyFile = open("ParticlePropertySvc_Monopole.txt", 'w')
ParticlePropertyFile.write("\# ParticlePropertySvc file automatically generated by MoEDAL_options.py\n")
ParticlePropertyFile.write("PARTICLE")

ParticlePropertyFile.write('\n')
ParticlePropertyFile.write('magnetic_monopole')           # PARTICLE NAME
ParticlePropertyFile.write('\t' + str(monopole_pdg))      # GEANTID
ParticlePropertyFile.write('\t' + str(monopole_pdg))      # PDGID
ParticlePropertyFile.write('\t' + str(monopole_elcharge)) # CHARGE
ParticlePropertyFile.write('\t' + str(monopole_mass))     # MASS(GeV)
ParticlePropertyFile.write('\t-1')                        # TLIFE(s)
ParticlePropertyFile.write('\tmagnetic_monopole')         # EVTGENNAME
ParticlePropertyFile.write('\t' + str(monopole_pdg))      # PYTHIAID
ParticlePropertyFile.write('\t0.00000000')                # MAXWIDTH

ParticlePropertyFile.write('\n')
ParticlePropertyFile.write('antimagnetic_monopole')        # PARTICLE NAME
ParticlePropertyFile.write('\t' + str(-monopole_pdg))      # GEANTID
ParticlePropertyFile.write('\t' + str(-monopole_pdg))      # PDGID
ParticlePropertyFile.write('\t' + str(-monopole_elcharge)) # CHARGE
ParticlePropertyFile.write('\t' + str(monopole_mass))      # MASS(GeV)
ParticlePropertyFile.write('\t-1')                         # TLIFE(s)
ParticlePropertyFile.write('\tantimagnetic_monopole')      # EVTGENNAME
ParticlePropertyFile.write('\t' + str(-monopole_pdg))      # PYTHIAID
ParticlePropertyFile.write('\t0.00000000')                 # MAXWIDTH

LHCb__ParticlePropertySvc().OtherFiles = [ "ParticlePropertySvc_Monopole.txt" ]
