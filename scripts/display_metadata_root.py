# Display graphs stored in .root files recorded at V20 in February 2020
# Copyright(C) 2020 Celine Durniak
#
# This program is free software: you can redistribute it and / or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program. If not, see < https://www.gnu.org / licenses/>.

import os
import uproot
import dataconfig  # to get path to datafiles

# check path to folder with ROOT files
assert os.path.exists(dataconfig.data_root), 'The path does not exist.'

# Create dictionary to generate plots
# Each entry corresponds to the spectrum number, the associated root file and
# the folder to get the data from
dict_root_files = {
    'Spectrum03': ('Spectrum03_DENEX006_1_18-02-05_0000.root', 'Meas_3'),
    'Spectrum08': ('Spectrum08_DENEX006_1_18-02-07_0002.root', 'Meas_2'),
    'Spectrum09': ('Spectrum09_DENEX006_1_18-02-08_0001.root', 'Meas_1'),
    'Spectrum11': ('Spectrum11_DENEX006_1_18-02-09_0001.root', "Meas_1"),
    'Spectrum12': ('Spectrum12_DENEX006_1_18-02-10_0000.root', 'Meas_1')
}

# Display metadata stored in selected ROOT file

ROOTfile, dir_with_data = dict_root_files['Spectrum03']

file_to_open = os.path.join(dataconfig.data_root, ROOTfile)

assert os.path.isfile(file_to_open), 'There is an issue with the file to be opened.'

with uproot.open(file_to_open)[dir_with_data] as myFile:
    for key in myFile.keys():
        if 'BoardParam_run' in str(key):
            myObject = myFile[key]
            nb_xbins = int(myObject.member('fEntries'))
            for i in range(nb_xbins):
                print(f"{myObject.axis(axis=0).labels()[i]}: {myObject.counts(False)[i]}")
