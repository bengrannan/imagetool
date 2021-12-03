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
		self.seriesIdentifiers = None

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
		self._set_series_identifiers()

	def get_series_identifiers(self):
		if self.seriesIdentifiers is None:
			self.set_series_identifiers()
		return set(list(self.seriesIdentifiers.keys()))

	def convert_series_to_nifti(self, series_identifier, output_path=None):
		assert series_identifier in self.get_series_identifiers(), "The identifier specified does not match \
			a series (seriesDescription, seriesNumber) tuple"
		# set nifti path	
		nifti_path = os.path.join(os.path.split(self.path)[0], 'nifti_'+os.path.split(self.path)[1])
		if not os.path.isdir(nifti_path):
			os.mkdir(nifti_path)
		# set output path
		if output_path is None:
			out_name = series_identifier[0].replace('.','')+'_'+str(series_identifier[1])
			out_name = out_name.replace(' ','')
			output_path = os.path.join(nifti_path, out_name)
		if not os.path.isdir(output_path):
			os.mkdir(output_path)
		# convert dicom
		converter = Dcm2niix()
		converter.inputs.source_names = self.seriesIdentifiers[series_identifier]
		converter.inputs.compress = 'n'
		converter.inputs.output_dir = output_path
		try:
			converter.run()
		except RuntimeError:
			print('\nRuntimeError for {}... skipping.\n'.format(series_identifier)) 

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

	def _set_series_identifiers(self):
		series = {}
		for f, meta_ in self.metadata.items():
			seriesDescription_ = meta_['SeriesDescription']
			seriesNumber_ = meta_['SeriesNumber']
			identifier_ = (seriesDescription_, seriesNumber_)
			if identifier_ not in series.keys():
				series[identifier_] = [f]
			else:
				series[identifier_].append(f)
		self.seriesIdentifiers = series






	




