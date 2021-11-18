DESCRIPTION = "study class"

import os
from glob import glob
import pydicom
import numpy as np
import shutil
from nipype.interfaces.dcm2nii import Dcm2niix
import pickle


class Study(): 

	def __init__(self, path=None):
		if path is not None:
			self._set_path(path)
			self._check_depth()
			self._set_dcm_files()
		else:
			self.path = None
			self.dcm_files = None
		self.metadata = None
		self.seriesDescriptions = None

	def process_study(self):
		return None

	def read_all_metadata(self):
		metadata = {}
		for n, f in enumerate(self.dcm_files):
			meta_ = {}
			dcm_ = pydicom.read_file(f)
			meta_['StudyDate'] = dcm_.StudyDate
			meta_['Manufacturer'] = dcm_.Manufacturer
			meta_['StudyDescription'] = dcm_.StudyDescription
			meta_['SeriesDescription'] = dcm_.SeriesDescription
			meta_['StudyID'] = dcm_.StudyID 
			meta_['SeriesNumber'] = dcm_.SeriesNumber

			try:
				meta_['AcquisitionNumber'] = dcm_.AcquisitionNumber
			except AttributeError:
				meta_['AcquisitionNumber'] = None

			meta_['InstanceNumber'] = dcm_.InstanceNumber

			try:
				meta_['PixelSpacing'] = dcm_.PixelSpacing
			except AttributeError:
				meta_['PixelSpacing'] = None

			try:
				meta_['WindowCenter'] = dcm_.WindowCenter
			except AttributeError:
				meta_['WindowCenter'] = None

			try:
				meta_['WindowWidth'] = dcm_.WindowWidth
			except AttributeError:
				meta_['WindowWidth'] = None

			metadata[f] = meta_
			print('\r{}% complete'.format(np.round(n/len(self.dcm_files)*100,2)), end='')
		self.metadata = metadata
		self._set_series_names()

	def get_series_names(self):
		if self.seriesDescriptions is None:
			self.set_series_descriptions()
		return set(list(self.seriesDescriptions.keys()))

	def convert_series_to_nifti(self, series_description, output_path=None, output_file=None):
		assert series_description in self.get_series_names(), "The series specified does not match a series description"
		tmp_path = os.path.join(os.path.split(self.path)[0], 'tmp')
		if output_path is None:
			output_path = os.path.split(self.path)[0]
		if output_file is None:
			out_name = series_description.replace('.','')
			out_name = out_name.replace(' ','')
			os.mkdir(os.path.join(output_path, out_name))
		if os.path.isdir(tmp_path) and len(os.listdir(tmp_path)) > 0:
			shutil.rmtree(tmp_path)
		os.mkdir(tmp_path)
		for f in self.seriesDescriptions[series_description]:
			shutil.copy(f, tmp_path)
		converter = Dcm2niix()
		converter.inputs.source_dir = tmp_path
		converter.inputs.output_dir = os.path.join(output_path, out_name)
		converter.cmdline
		converter.run() 
		shutil.rmtree(tmp_path)

	def save_object(self, path):
		with open(path, 'wb') as f:
			pickle.dump(self, f)
		print('File saved to {}'.format(path))

	def load_object(self, path):
		with open(path, 'rb') as f:
			obj = pickle.load(f)
		for attr in vars(obj):
			setattr(self, attr, getattr(obj, attr))
		print('Opened object from file {}'.format(path))

	def copy_series_dcm_to_directory(self, series_description, newDir):
		assert series_description in self.get_series_names(), "The series specified does not match a series description"
		assert os.path.isdir(newDir) is False, "newDir already exists"
		for f in self.seriesDescriptions[series_description]:
			shutil.copy(f, newDir)

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
		# creates list of dicom files
		self.dcm_files = glob(os.path.join(self.path, "*/*"))

	def _set_series_names(self):
		series = {}
		for f, meta_ in self.metadata.items():
			seriesDescription_ = meta_['SeriesDescription']
			if seriesDescription_ not in series.keys():
				series[seriesDescription_] = [f]
			else:
				series[seriesDescription_].append(f)
		self.seriesDescriptions = series






	




