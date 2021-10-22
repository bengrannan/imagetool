DESCRIPTION = "study class"

import os
from glob import glob
import pydicom


class Study(): 

	def __init__(self, path):
		self._set_path(path)
		self._check_depth()
		self._set_dcm_files()
		self.descriptions = None

	def process_study(self):

	def set_series_descriptions(self):
		descriptions = {}
		for f in self.dcm_files:
			dcm_ = pydicom.read_file(f)
			descriptions[f] = dcm_.StudyDescription
		self.descriptions = descriptions

	def get_series_descriptions(self):
		if self.descriptions is None:
			self.set_series_descriptions()
		return self.descriptions

	def _set_path(self, path):
		assert os.path.isdir(path), "Specified path is not a directory"
		self.path = path

	def _check_depth(self):
		# check that each subdirectory only contains single files 
		# no additional directories permitted
		g = glob(os.path.join(self.path, "*/*"))
		for f in g:
			assert os.path.isfile(f), "{} is not a file. Path must contain \
				directories only containing single files.".format(f)

	def _set_dcm_files(self):
		self.dcm_files = glob(os.path.join(self.path, "*/*"))




