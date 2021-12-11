#!/bin/bash

# simple function to make matlab call from bash shell

directory=$1
earoot=$2
dbdir=$3
slicerDir=$4
connectomeDir=$5
elmodel=$6

matlab -nodisplay -nodesktop -r "lead_dbs_register_normalize('$directory', '$earoot', \
	'$dbdir', '$slicerDir', '$connectomeDir', '$elmodel'); exit;"
echo ""
echo "This job is complete."