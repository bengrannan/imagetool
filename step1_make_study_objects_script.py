DESCRIPTION = "step 1: script to process process study \
objects for all imaging studies"

import argparse
import os
from imagetool.study import Study


if __name__ == "__main__": 

	parser = argparse.ArgumentParser(description=DESCRIPTION)
	mode = parser.add_mutually_exclusive_group()
	mode.add_argument("--study-path", '-sp', dest='path',
		default=None, help="full path to directory containing dicom studies")

	args = parser.parse_args()
	path = args.path

	assert os.path.isdir(path), "Provided field for study path is not directory"

	#get list of patient folders
	pts = os.listdir(path)

	#loop through folders, processing mri and ct studies
	print("Processing {}".format(path))
	s = Study(path)
	s.read_all_metadata()
	save_path = os.path.join(os.path.split(path)[0], \
		'{}_StudyObject.pickle'.format(os.path.split(path)[1]))
	s.save_object(save_path)