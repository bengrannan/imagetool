#!/bin/bash

# simple function to make matlab call for VTA calculation

matlab -nodisplay -nodesktop -r "lead_dbs_register_normalize('$directory', '$earoot', \
	'$dbdir', '$slicerDir', '$connectomeDir', '$elmodel'); exit;"