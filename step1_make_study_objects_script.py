DESCRIPTION = "step 1: script to process process study \
objects for all imaging studies"

import argparse
import os
from imagetool.study import Study


if __name__ == "__main__": 

	parser = argparse.ArgumentParser(description=DESCRIPTION)
	mode = parser.add_mutually_exclusive_group()
	mode.add_argument("--studies-path", '-sp', dest='path',
		default=None, help="full path to directory containing dicom studies")

	args = parser.parse_args()
	path = args.path

	assert os.path.isdir(path), "Provided field for studies path is not directory"

	#get list of patient folders
	pts = os.listdir(path)

	#loop through folders, processing mri and ct studies
	for pt in pts:
		for s in ['ct', 'mri']:
			path_ = os.path.join(path, pt, s)
			print("Processing {}".format(path_))
			s_ = Study(path_)
			s_.read_all_metadata()
			save_path_ = os.path.join(path, pt, '{}_{}_StudyObject.pickle'.format(pt, s))
			s_.save_object(save_path_)