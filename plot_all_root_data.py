# Save all graphs stored in .root files recorded at V20 in February 2018 as .png files
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

import uproot
import numpy as np
import matplotlib.pyplot as plt

path_to_file = '/Users/celinedurniak/Documents/test_root/Diffraction/TBL_Data_DreamTeam_Feb2018/DREAMTeam_Feb2018/DENEX/'

# Create dictionary to generate plots
# Each entry corresponds to the spectrum number, the associated root file
# and the folder to get the data from

dict_root_files = {'Spectrum03': ("Spectrum03_DENEX006_1_18-02-05_0000.root", "Meas_3"),
                   'Spectrum08': ("Spectrum08_DENEX006_1_18-02-07_0002.root", "Meas_2"),
                   'Spectrum09': ("Spectrum09_DENEX006_1_18-02-08_0001.root", "Meas_1"),
                   'Spectrum11': ("Spectrum11_DENEX006_1_18-02-09_0001.root", "Meas_1"),
                   'Spectrum12': ("Spectrum12_DENEX006_1_18-02-10_0000.root", "Meas_1")}

# Ask user if y-axis should be inverted for 2D data
reply = ''
while reply not in ['y', 'n', 'yes', 'no']:
    reply = str(input('Invert y axis of 2D plots (y/n)? ')).lower().strip()

tag_invert_y = reply.startswith('y')

# Loop over datafiles
for key_spec in dict_root_files.keys():
    print(key_spec)

    ROOTfile = dict_root_files[key_spec][0]
    dir_with_data = dict_root_files[key_spec][1]

    # open root file
    with uproot.open(path_to_file + ROOTfile)[dir_with_data] as myFile:
        for keyName in myFile.keys():

            if key_spec == "Spectrum09" and ('1D3' in str(keyName) or 'FINISHED' in str(keyName)):
                continue

            # 1D line plot
            if "TH1I" in str(myFile[keyName]):
                # do not consider problematic dataset in Spectrum09

                key_name = myFile[keyName].name.decode('utf-8')
                arr_object = myFile[keyName].values

                # naming of outputs - the extension will be added once the format
                # is chosen (.png or .dat for 1D data)
                name_output_file = ROOTfile[:10] + key_name.replace(',', '_')

                # plot
                fig, ax = plt.subplots()
                ax.plot(arr_object)
                ax.set_title(key_name)

                # save plot
                plt.savefig(name_output_file + '.png')
                # to display the plot uncomment the line below
                # plt.show()
                plt.close(fig)

                # 2D contourplot
            elif "TH2" in str(myFile[keyName]):
                key_name = myFile[keyName].name.decode('utf-8')

                # extract info about x, y axis (min, max and number of bins)
                x_min = myFile[keyName].xlow
                x_max = myFile[keyName].xhigh
                bins_x = myFile[keyName].xnumbins
                y_min = myFile[keyName].ylow
                y_max = myFile[keyName].yhigh
                bins_y = myFile[keyName].ynumbins

                # create x- and y-axis
                xaxis = x_min + (x_max - x_min) / (bins_x - 1) * np.arange(bins_x)
                yaxis = y_min + (y_max - y_min) / (bins_y - 1) * np.arange(bins_y)

                # invert y axis
                if tag_invert_y:
                    arr_object = np.flip(myFile[keyName].values, 1)
                    # add info about inverted y axis to name of outputs - the extension will be
                    # added later
                    name_output_file = ROOTfile[:10] + "_" + key_name.replace(',', '_') + "_inv_y"
                # keep original orientation
                else:
                    arr_object = myFile[keyName].values
                    # name of outputs - the extension will be added later
                    name_output_file = ROOTfile[:10] + "_" + key_name.replace(',', '_')
                # plot
                fig, ax = plt.subplots()
                CS = ax.contourf(xaxis, yaxis, arr_object.transpose(),
                                 cmap=plt.cm.get_cmap('gist_earth'))
                ax.set_title(key_name)
                cbar = fig.colorbar(CS)

                # save plot
                plt.savefig(name_output_file + '.png')
                # to display the plot uncomment the line below
                # plt.show()
                plt.close(fig)
