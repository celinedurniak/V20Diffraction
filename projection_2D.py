# Calculate projection of selected part of 2D graph stored in .root files recorded at V20
# in February 2018

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
from matplotlib.widgets import SpanSelector

path_to_root_file = '/Users/celinedurniak/Documents/test_root/Diffraction/TBL_Data_DreamTeam_Feb2018/DREAMTeam_Feb2018/DENEX/'

ROOTfile = "Spectrum03_DENEX006_1_18-02-05_0000.root"
dir_with_data = "Meas_3"

data_to_plot = 'H_TOF,X1-X2_User_2D2_dsp_after_run_3'

# read .root file
myFile = ROOT.TFile.Open(path_to_root_file + ROOTfile, "read")

for keyName in myFile.GetListOfKeys():
    myObject = myFile.Get(keyName.GetName())
    if dir_with_data in str(myObject):
        for key in myObject.GetListOfKeys():
            # 2D contourplot
            if "TH2" in key.GetClassName() and data_to_plot in key.GetName():

                mySubObject = myObject.Get(key.GetName())
                # extract data
                axis_x = mySubObject.GetXaxis()
                axis_y = mySubObject.GetYaxis()

                h1 = mySubObject.ProjectionX()

                # xmax, xmin, ymax, ymin defined from .root file
                # and used for the user input validator
                xmin = axis_x.GetXmin()
                xmax = axis_x.GetXmax()
                ymin = axis_y.GetXmin()
                ymax = axis_y.GetXmax()

                nb_xbins = axis_x.GetNbins()
                nb_ybins = axis_y.GetNbins()

                # create x- and y-axis
                deltax = (xmax - xmin)/(nb_xbins-2)
                xaxis = xmin + deltax * np.arange(nb_xbins-1)
                deltay = (ymax - ymin)/(nb_ybins - 2)
                yaxis = ymin + deltay * np.arange(nb_ybins-1)

                # fill 2d matrice
                arr = np.zeros((axis_x.GetNbins() - 1, axis_y.GetNbins() - 1))

                # invert y axis
                for i in range(1, axis_x.GetNbins()):
                    for j in range(1, axis_y.GetNbins()):
                        arr[i - 1, axis_y.GetNbins() - j - 1] = mySubObject.GetBinContent(i, j)
myFile.Close()


# upper boundary for range of vertical values selected for the projection - initial values = full
# vertical range
new_ymax = int(ymax)
new_ymin = int(ymin)

# Set up figure
fig = plt.figure(num=data_to_plot, figsize=(9, 9))

# 2D plot i.e. contourplot
ax1 = fig.add_axes([0.09, 0.595, 0.8, 0.395])
contf = ax1.imshow(arr.transpose(), extent=[xmin, xmax, ymin, ymax], origin='lower', aspect='auto')

# colorbar
ax3 = fig.add_axes([.9, 0.595, 0.03, 0.395])
cb = plt.colorbar(contf, ax=ax1, cax=ax3)

# 1D plot i.e. projection
projection_1d = np.sum(arr, axis=1)
ax2 = fig.add_axes([0.09, 0.135, 0.8, 0.395])
ax2.plot(projection_1d)
ax2.set_xlim([xmin, xmax])
ax2.grid()
ax2.annotate('Press left mouse button on 2D plot to select area to calculate 1D projection',
             xy=(0.5, 0), xycoords='axes fraction',
             xytext=(0, -150), textcoords='offset pixels',
             horizontalalignment='center',
             verticalalignment='bottom')


def onselect(ymin, ymax):
    index_max_projection = (np.abs(yaxis - ymax)).argmin()
    index_min_projection = (np.abs(yaxis - ymin)).argmin()
    tr_arr = arr[:, index_min_projection:index_max_projection]
    projection_1d = np.sum(tr_arr, axis=1)

    ax2.clear()
    ax2.grid()
    ax2.set_xlim([xmin, xmax])
    ax2.plot(projection_1d, color='red')

    ax2.annotate(f"ymin: {ymin:.2f}, ymax: {ymax:.2f}",
                 xy=(1, 0), xycoords='axes fraction',
                 xytext=(-20, -90), textcoords='offset pixels',
                 horizontalalignment='right',
                 verticalalignment='bottom')

    print(f"ymin: {ymin}, ymax: {ymax}")
    fig.canvas.draw_idle()

    # save 1d projection
    np.savetxt("projection1D.out", projection_1d, fmt='%.4f',
               header=f"root file: {ROOTfile}, dataset: {data_to_plot} ymin: {ymin}, ymax: {ymax}")

span = SpanSelector(ax1, onselect=onselect, direction='vertical',
                    useblit=True, span_stays=True, button=1,
                    rectprops=dict(facecolor='None', edgecolor='red'))

plt.show()
