#!/bin/bash
#
shopt -s expand_aliases
#
echo "======================================================================="
echo "            Setting up the MoEDAL Simulations (CVFMS running)          "
echo "======================================================================="
echo "* HOME is         : "$HOME
#
## The current working directory for the MoEDAL simulations.
export MOEDALDIR=`pwd`
echo "* MOEDALDIR is    : "$MOEDALDIR
#
## The Configuration Management Tool architecture/SL/compiler flag.
export CMTCONFIG="x86_64-slc6-gcc49-opt"
echo "*"
echo "* CMTCONFIG is    : "$CMTCONFIG
#
#
# Now, rather than getting our LHCb software environment from
# AFS, we can do it all through CVMFS (providing our machine
# has CVMFS enabled, of course).
#
## The Location of the LHCb software on CVMFS.
export VO_LHCB_SW_DIR=/cvmfs/lhcb.cern.ch
echo "* VO_LHCB_SW_DIR is : "$VO_LHCB_SW_DIR
echo "*"
#
# Source the LHCb environmemt from CVMFS (rather than AFS).
echo "Sourcing the LHCb environment with LbLogin.sh"
source $VO_LHCB_SW_DIR/lib/LbLogin.sh -c x86_64-slc6-gcc49-opt
echo "...done."
#
echo "Running 'SetupProject Gauss v49r8'"
SetupProject Gauss v49r8
echo "...done."
#
echo "Running 'setenvProject.sh Gauss v49r8 --user-area \$MOEDALDIR'"
setenvProject.sh Gauss v49r8 --user-area $MOEDALDIR
echo "...done."
#
## The location of the Gauss project.
echo "Declaring  NEWPROJECTPATH=$MOEDALDIR/Gauss_v49r8"
NEWPROJECTPATH=$MOEDALDIR/Gauss_v49r8
echo "...done."
#
# Now, rather than check out and build the modifications to Gauss
# required by MoEDAL, we can copy the pre-built packages from the
# MoEDAL CVMFS repository to our Gauss project directory.
#
## The location of the MoEDAL CVMFS repository.
export VO_MOEDAL_SW_DIR=/cvmfs/moedal.cern.ch
echo "* VO_MOEDAL_SW_DIR is : "$VO_MOEDAL_SW_DIR
echo "...done."
#
# Copy the pre-built packages to our Gauss project area.
cd ${NEWPROJECTPATH}
if [ -d "InstallArea" ]; then echo "<InstallArea> already exists"; else cp -r ${VO_MOEDAL_SW_DIR}/Gauss/Gauss_v49r8/InstallArea/ InstallArea; fi
if [ -d "Sim" ]; then echo "<Sim> already exists"; else cp -r ${VO_MOEDAL_SW_DIR}/Gauss/Gauss_v49r8/Sim/ Sim; fi
if [ -d "Gen" ]; then echo "<Gen> already exists"; else cp -r ${VO_MOEDAL_SW_DIR}/Gauss/Gauss_v49r8/Gen/ Gen; fi

# The following commands run the package setup scripts, but
# we comment out the 'make' commands because we don't need to build
# them each time.

# GaussMoEDAL depends on GaussMonopoles, need to build GaussMonopoles first
echo "* Preparing the GaussMonopoles package..."
cd Sim/GaussMonopoles/cmt
cmt config
source setup.sh
#make
echo "* ...done."
cd ${NEWPROJECTPATH}

echo "* Preparing the GaussMoEDAL package..."
cd Sim/GaussMoEDAL/cmt
cmt config
source setup.sh
#make
echo "* ...done."
cd ${NEWPROJECTPATH}

echo "* Preparing the (modified) Gauss package..."
cd Sim/Gauss/cmt
cmt config
source setup.sh
#make
echo "*...done."
cd ${NEWPROJECTPATH}

echo "* Preparing the (modified) LbPythia package..."
cd Gen/LbPythia/cmt
cmt config
source setup.sh
#make
echo "*...done."
cd ${NEWPROJECTPATH}

# Return to the working directory.
cd ..

# Setup the right version of ROOT for the ntuples.
source $VO_LHCB_SW_DIR/lib/lcg/releases/ROOT/6.04.02-a6f71/x86_64-slc6-gcc49-opt/bin/thisroot.sh

echo "* Setup complete!"
echo
#
echo "======================================================================="
echo "                          Prepare the LHE file                         "
echo "======================================================================="
#
if [ -f unweighted_events.lhe.gz ]; then
  echo "Unzipping unweighted_events.lhe.gz..."
  gunzip unweighted_events.lhe.gz
  echo "...done. Now we have:"
  ls
  echo
fi
#
echo "======================================================================="
echo "                     Running a MoEDAL simulation job                   "
echo "======================================================================="
#
# USAGE: See README.md.
#

## The start time of the job.
BEGIN=$(date +%s)

# Run the simulation using. All options are supplied in the Python
# files listed below.
gaudirun.py \
CFGNAME \
${GAUSSOPTS}/Gauss-2016.py \
&> LOGNAME

# One may choose between: ${GAUSSOPTS}/Gauss-2015.py \  and  ${GAUSSOPTS}/Gauss-2016.py \
# The 2015 and 2016 configurations include a commented option: EnableSpillover

# Update the user via the log file.
echo "JOB_FINISHED" >> LOGNAME
echo "* Run complete!"
#
# Calculate the length of time the job took.
NOW=$(date +%s)
DIFF=$(($NOW - $BEGIN))
HOURS=$(($DIFF / 3600))
MINS=$(($DIFF / 60))
MINS=$(($MINS % 60))
SECS=$(($DIFF % 60))
echo "JOB TOOK:  ${HOURS} : ${MINS} : ${SECS}" >> LOGNAME
echo "*"
echo "* Total running time :  ${HOURS} h : ${MINS} m : ${SECS} s"
echo "*"
echo "* View the output messages with:"
echo "$ vim LOGNAME"
echo "*"
echo "* or inspect the results histograms with:"
echo "$ root -l ROOTFILE"
echo "*"
echo
