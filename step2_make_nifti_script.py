DESCRIPTION = "script to process all of the nifti files using study object files"

import argparse
import os
from imagetool.study import Study
from glob import glob


if __name__ == "__main__": 

	parser = argparse.ArgumentParser(description=DESCRIPTION)
	mode = parser.add_mutually_exclusive_group()
	mode.add_argument("-p", "--path", default=None, dest='path',
		help="full path to single study object file")

	args = parser.parse_args()
	path = args.path

	assert os.path.isfile(path), "Provided path for --study-object-path is not a file"

	s = Study()
	s.load_object(path)
	series_identifiers = s.get_series_identifiers()
	for identifier in series_identifiers:
		#import pdb; pdb.set_trace()
		s.convert_series_to_nifti(identifier)