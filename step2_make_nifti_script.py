DESCRIPTION = "script to process all of the nifti files"

import argparse
import os
from imagetool.study import Study
from glob import glob


if __name__ == "__main__": 

	parser = argparse.ArgumentParser(description=DESCRIPTION)
	mode = parser.add_mutually_exclusive_group()
	mode.add_argument("--studies-path", '-sp', dest='path',
		default=None, help="full path to directory containing dicom studies")
	mode.add_argument("--study-object-path", "-sop", dest='study_object_path', 
		default=None, help="full path to single study object")

	args = parser.parse_args()
	path = args.path
	study_object_path = args.study_object_path

	assert (path is None) or (study_object_path is None), "Cannot specify both --studies-path and --study-path"
	if path is not None:
		import pdb; pbd.set_trace()
		assert os.path.isdir(path), "Provided field for --studies-path is not directory"
	if study_object_path is not None:
		assert os.path.isfile(study_object_path), "Provided path for --study-object-path is not a file"

	if path is not None:
		#get list of patient folders
		pts = os.listdir(path)

		#loop through folders, processing mri and ct studies
		for pt in pts:
			study_obj_files = glob(os.path.join(path, pt, '*.pickle'))
			for study_obj_path in study_obj_files:
				s = Study()
				s.load_object(study_obj_path)
				series_names_ = s.get_series_names()
				for series_ in series_names_:
					s.convert_series_to_nifti(series_)

	if study_object_path is not None:
		s = Study()
		s.load_object(study_object_path)
		series_names_ = s.get_series_names()
		for series_ in series_names_:
			s.convert_series_to_nifti(series_)