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

import os
import uproot
import numpy as np
import matplotlib.pyplot as plt

# to save tiff files
from PIL import Image

path_to_file = '/Users/celinedurniak/V20DiffractionData/DENEX'

assert os.path.exists(path_to_file), 'The path does not exist.'

# Create dictionary to generate plots
# Each entry corresponds to the spectrum number, the associated root file
# and the folder to get the data from

dict_root_files = {'Spectrum03': ('Spectrum03_DENEX006_1_18-02-05_0000.root', 'Meas_3'),
                   'Spectrum08': ('Spectrum08_DENEX006_1_18-02-07_0002.root', 'Meas_2'),
                   'Spectrum09': ('Spectrum09_DENEX006_1_18-02-08_0001.root', 'Meas_1'),
                   'Spectrum11': ('Spectrum11_DENEX006_1_18-02-09_0001.root', 'Meas_1'),
                   'Spectrum12': ('Spectrum12_DENEX006_1_18-02-10_0000.root', 'Meas_1')}

# Ask user if y-axis should be inverted for 2D data
reply_invert_y = ''
while reply_invert_y not in ['y', 'n', 'yes', 'no']:
    reply_invert_y = str(input('Invert y axis of 2D plots (y/n)? ')).lower().strip()
tag_invert_y = reply_invert_y.startswith('y')

reply_save_1d_dat = ''
while reply_save_1d_dat not in ['y', 'n', 'yes', 'no']:
    reply_save_1d_dat = str(input('Save 1D data to ascii files (y/n)? ')).lower().strip()
tag_save_1d_dat = reply_save_1d_dat.startswith('y')

reply_save_1d_png = ''
while reply_save_1d_png not in ['y', 'n', 'yes', 'no']:
    reply_save_1d_png = str(input('Save 1D data to png files (y/n)? ')).lower().strip()
tag_save_1d_png = reply_save_1d_png.startswith('y')

reply_save_2d_dat = ''
while reply_save_2d_dat not in ['y', 'n', 'yes', 'no']:
    reply_save_2d_dat = str(input('Save 2D data to ascii files (y/n)? ')).lower().strip()
tag_save_2d_dat = reply_save_2d_dat.startswith('y')

reply_save_2d_png = ''
while reply_save_2d_png not in ['y', 'n', 'yes', 'no']:
    reply_save_2d_png = str(input('Save 2D data to png files (y/n)? ')).lower().strip()
tag_save_2d_png = reply_save_2d_png.startswith('y')

reply_save_2d_tif = ''
while reply_save_2d_tif not in ['y', 'n', 'yes', 'no']:
    reply_save_2d_tif = str(input('Save 2D data to tiff files (y/n)? ')).lower().strip()
tag_save_2d_tif = reply_save_2d_tif.startswith('y')

# Loop over datafiles
for key_spectrum in dict_root_files.keys():
    print(key_spectrum)

    ROOTfile = dict_root_files[key_spectrum][0]
    dir_with_data = dict_root_files[key_spectrum][1]

    # open root file
    file_to_open = os.path.join(path_to_file, ROOTfile)
    with uproot.open(file_to_open)[dir_with_data] as myFile:
        for key in myFile.keys():

            if key_spectrum == 'Spectrum09' and ('1D3' in str(key) or 'FINISHED' in str(key)):
                continue

            # 1D line plot
            if 'TH1I' in str(myFile[key]):
                # do not consider problematic dataset in Spectrum09

                key_name = myFile[key].name.decode('utf-8')
                arr_object = myFile[key].values

                # naming of outputs - the extension will be added once the format
                # is chosen (.png or .dat for 1D data)
                name_output_file = ROOTfile[:10] + key_name.replace(',', '_')

                # plot
                fig, ax = plt.subplots()
                ax.plot(arr_object)
                ax.set_title(key_name)
                # plt.show()

                # save plot
                if tag_save_1d_png:
                    fig.savefig(name_output_file + '.png')
                    plt.close()

                if tag_save_1d_dat:
                    np.savetxt(name_output_file + '.dat', arr_object, fmt="%d")

            # 2D contourplot
            elif 'TH2' in str(myFile[key]):
                key_name = myFile[key].name.decode('utf-8')

                # extract info about x, y axis (min, max and number of bins)
                x_min = myFile[key].xlow
                x_max = myFile[key].xhigh
                bins_x = myFile[key].xnumbins
                y_min = myFile[key].ylow
                y_max = myFile[key].yhigh
                bins_y = myFile[key].ynumbins

                # create x- and y-axis
                xaxis = x_min + (x_max - x_min) / (bins_x - 1) * np.arange(bins_x)
                yaxis = y_min + (y_max - y_min) / (bins_y - 1) * np.arange(bins_y)

                # invert y axis
                if tag_invert_y:
                    arr_object = np.flip(myFile[key].values, 1)
                    # add info about inverted y axis to name of outputs - the extension will be
                    # added later
                    name_output_file = ROOTfile[:10] + '_' + key_name.replace(',', '_') + '_inv_y'
                # keep original orientation
                else:
                    arr_object = myFile[key].values
                    # name of outputs - the extension will be added later
                    name_output_file = ROOTfile[:10] + "_" + key_name.replace(',', '_')

                # plot
                fig, ax = plt.subplots()
                CS = ax.contourf(xaxis,
                                 yaxis,
                                 arr_object.transpose(),
                                 cmap=plt.cm.get_cmap('gist_earth'))
                ax.set_title(key_name)
                cbar = fig.colorbar(CS)
                # plt.show()

                if tag_save_2d_dat:
                    np.savetxt(name_output_file + '.dat', arr_object, fmt="%d")

                if tag_save_2d_png:
                    fig.savefig(name_output_file + '.png')

                plt.close()

                if tag_save_2d_tif:
                    im_from_png = np.array(Image.open(name_output_file + '.png'))
                    Image.fromarray(im_from_png).save(name_output_file + ".tiff", "TIFF")
