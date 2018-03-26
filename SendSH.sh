#! /bin/bash

sftp asantra@lxplus6.cern.ch << EOF
put make_dirac_lhe_job.py /afs/cern.ch/user/a/asantra/public/MoEDALSim/moedal-run-simulations/ganga
put run_lhe_v49r8_TEMPLATE.sh /afs/cern.ch/user/a/asantra/public/MoEDALSim/moedal-run-simulations/ganga
put configuration_LHE_TEMPLATE.py /afs/cern.ch/user/a/asantra/public/MoEDALSim/moedal-run-simulations/ganga
EOF