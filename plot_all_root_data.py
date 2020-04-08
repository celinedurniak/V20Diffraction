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

import ROOT
import numpy as np
import matplotlib.pyplot as plt

path_to_file = '/Users/celinedurniak/Documents/test_root/Diffraction/TBL_Data_DreamTeam_Feb2018/DREAMTeam_Feb2018/DENEX/'

# Create dictionary to generate plots
# Each entry corresponds to the spectrum number, the associated root file
# and the folder to get the data from
# Spectrum09 is dealt with separately at the end of the script

dict_root_files = {'Spectrum03': ("Spectrum03_DENEX006_1_18-02-05_0000.root", "Meas_3"),
                   'Spectrum08': ("Spectrum08_DENEX006_1_18-02-07_0002.root", "Meas_2"),
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
    myFile = ROOT.TFile.Open(path_to_file + ROOTfile, "read")

    for keyName in myFile.GetListOfKeys():
        myObject = myFile.Get(keyName.GetName())

        if dir_with_data in str(myObject):
            for key in myObject.GetListOfKeys():
                # 1D line plot
                if "TH1I" in key.GetClassName():
                    mySubObject = myObject.Get(key.GetName())

                    # extract data
                    axis_x = mySubObject.GetXaxis()

                    ar_object = np.zeros(axis_x.GetNbins() - 1)
                    for i in range(1, axis_x.GetNbins()):
                        ar_object[i - 1] = mySubObject.GetBinContent(i)

                    # plot
                    fig, ax = plt.subplots()
                    ax.plot(ar_object)
                    ax.set_title(key_spec + " " + key.GetName())

                    # save plot
                    plt.savefig(ROOTfile[:10] + key.GetName().replace(',', '_') + '.png')
                    # to display the plot uncomment the line below
                    # plt.show()
                    plt.close(fig)

                # 2D contourplot
                elif "TH2" in key.GetClassName():

                    mySubObject = myObject.Get(key.GetName())

                    # extract data
                    axis_x = mySubObject.GetXaxis()
                    axis_y = mySubObject.GetYaxis()

                    # create x- and y-axis
                    xaxis = axis_x.GetXmin() \
                            + (axis_x.GetXmax() - axis_x.GetXmin()) / (
                                        axis_x.GetNbins() - 2) * np.arange(axis_x.GetNbins() - 1)
                    yaxis = axis_y.GetXmin() \
                            + (axis_y.GetXmax() - axis_y.GetXmin()) / (
                                        axis_y.GetNbins() - 2) * np.arange(axis_y.GetNbins() - 1)

                    # fill 2d matrice
                    ar_object = np.zeros((axis_x.GetNbins() - 1, axis_y.GetNbins() - 1))

                    # invert y axis
                    if tag_invert_y:
                        for i in range(1, axis_x.GetNbins()):
                            for j in range(1, axis_y.GetNbins()):
                                ar_object[i - 1, axis_y.GetNbins() - j - 1] = \
                                    mySubObject.GetBinContent(i, j)
                    # keep original orientation of y-axis
                    else:
                        for i in range(1, axis_x.GetNbins()):
                            for j in range(1, axis_y.GetNbins()):
                                ar_object[i - 1, j - 1] = mySubObject.GetBinContent(i, j)

                    # plot
                    fig, ax = plt.subplots()
                    CS = ax.contourf(xaxis, yaxis, ar_object.transpose(),
                                     cmap=plt.cm.get_cmap('gist_earth'))
                    ax.set_title(key_spec + " " + key.GetName())
                    cbar = fig.colorbar(CS)

                    # save plot
                    plt.savefig(ROOTfile[:10] + key.GetName().replace(',', '_') + '.png')
                    # to display the plot uncomment the line below
                    # plt.show()
                    plt.close(fig)

    myFile.Close()


# Specific handling of Spectrum09: issue with one dataset
ROOTfile = "Spectrum09_DENEX006_1_18-02-08_0001.root"
dir_with_data = "Meas_1"

print("Spectrum09")
myFile = ROOT.TFile.Open(path_to_file + ROOTfile, "read")

for keyName in myFile.GetListOfKeys():
    myObject = myFile.Get(keyName.GetName())

    if dir_with_data in str(myObject):

        for key in myObject.GetListOfKeys():

            # 1D line plot - discard plotting buggy data
            if "TH1I" in key.GetClassName() and not '1D3' in key.GetName():
                mySubObject = myObject.Get(key.GetName())

                # extract data
                axis_x = mySubObject.GetXaxis()

                ar_object = np.zeros(axis_x.GetNbins()-1)
                for i in range(1, axis_x.GetNbins()):
                    ar_object[i-1]=mySubObject.GetBinContent(i)

                # plot
                fig, ax = plt.subplots()
                ax.plot(ar_object)
                ax.set_title("Spectrum09" + " " + key.GetName())

                # save plot
                plt.savefig(ROOTfile[:10] + key.GetName().replace(',', '_') + '.png')
                # to display the plot uncomment the line below
                # plt.show()
                plt.close()

            # 2D contourplot
            elif "TH2" in key.GetClassName():

                mySubObject = myObject.Get(key.GetName())

                # extract data
                axis_x = mySubObject.GetXaxis()
                axis_y = mySubObject.GetYaxis()

                # create x- and y-axis
                xaxis = axis_x.GetXmin() \
                    + (axis_x.GetXmax() - axis_x.GetXmin()) \
                    / (axis_x.GetNbins()-2)*np.arange(axis_x.GetNbins() - 1)
                yaxis = axis_y.GetXmin() \
                    + (axis_y.GetXmax() - axis_y.GetXmin()) \
                    / (axis_y.GetNbins() - 2) * np.arange(axis_y.GetNbins()-1)

                # fill 2d matrice
                ar_object = np.zeros((axis_x.GetNbins()-1, axis_y.GetNbins()-1))

                # invert y axis
                if tag_invert_y:
                    for i in range(1, axis_x.GetNbins()):
                        for j in range(1, axis_y.GetNbins()):
                            ar_object[i - 1, axis_y.GetNbins() - j - 1] = \
                                mySubObject.GetBinContent(i, j)
                # keep original orientation of y-axis
                else:
                    for i in range(1, axis_x.GetNbins()):
                        for j in range(1, axis_y.GetNbins()):
                            ar_object[i - 1, j - 1] = mySubObject.GetBinContent(i, j)

                # plot
                fig, ax = plt.subplots()
                CS = ax.contourf(xaxis,
                                 yaxis,
                                 ar_object.transpose(),
                                 cmap=plt.cm.get_cmap('gist_earth'))

                ax.set_title("Spectrum09" + " " + key.GetName())
                cbar = fig.colorbar(CS)

                # save plot
                plt.savefig(ROOTfile[:10] + key.GetName().replace(',', '_') + '.png')
                # to display the plot uncomment the line below
                # plt.show()
                plt.close()

myFile.Close()
