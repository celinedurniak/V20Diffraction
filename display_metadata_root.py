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

import ROOT

path_to_file = '/Users/celinedurniak/Documents/test_root/Diffraction/TBL_Data_DreamTeam_Feb2018/DREAMTeam_Feb2018/DENEX/'

# Create dictionary to generate plots
# Each entry corresponds to the spectrum number, the associated root file and
# the folder to get the data from
dict_root_files = {
    'Spectrum03': ("Spectrum03_DENEX006_1_18-02-05_0000.root", "Meas_3"),
    'Spectrum08': ("Spectrum08_DENEX006_1_18-02-07_0002.root", "Meas_2"),
    'Spectrum09': ("Spectrum09_DENEX006_1_18-02-08_0001.root", "Meas_1"),
    'Spectrum11': ("Spectrum11_DENEX006_1_18-02-09_0001.root", "Meas_1"),
    'Spectrum12': ("Spectrum12_DENEX006_1_18-02-10_0000.root", "Meas_1")
}

# Display metadata stored in selected ROOT file

ROOTfile,  dir_with_data = dict_root_files['Spectrum03']

myFile = ROOT.TFile.Open(path_to_file + ROOTfile, "read")

for keyName in myFile.GetListOfKeys():
    myObject = myFile.Get(keyName.GetName())
    for key in myObject.GetListOfKeys():
        if "TH1" in key.GetClassName() and 'BoardParam_run_1' in key.GetName():
            mySubObject = myObject.Get(key.GetName())
            axis_x = mySubObject.GetXaxis()

            nb_xbins = axis_x.GetNbins()
            for i in range(1, nb_xbins+1):
                print(f"{axis_x.GetBinLabel(i)}: {mySubObject.GetBinContent(i)}")

myFile.Close()
