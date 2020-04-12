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

import uproot
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import SpanSelector

path_to_root_file = '/Users/celinedurniak/Documents/test_root/Diffraction/TBL_Data_DreamTeam_Feb2018/DREAMTeam_Feb2018/DENEX/'

ROOTfile = 'Spectrum03_DENEX006_1_18-02-05_0000.root'
dir_with_data = 'Meas_3'

data_to_plot = 'H_TOF,X1-X2_User_2D2_dsp_after_run_3'

with uproot.open(path_to_root_file + ROOTfile)[dir_with_data] as myFile:
    for key in myFile.keys():
        # 2D contourplot
        if 'TH2' in str(myFile[key]) and data_to_plot in str(myFile[key]):
                # x_max, x_min, y_max, y_min defined from .root file
                x_min = myFile[key].xlow
                x_max = myFile[key].xhigh
                bins_x = myFile[key].xnumbins
                y_min = myFile[key].ylow
                y_max = myFile[key].yhigh
                bins_y = myFile[key].ynumbins

                # create x- and y-axis
                deltax = (x_max - x_min)/(bins_x - 1)
                xaxis = x_min + deltax * np.arange(bins_x)
                deltay = (y_max - y_min)/(bins_y - 1)
                yaxis = y_min + deltay * np.arange(bins_y)

                # fill 2d matrice with inverted y-axis
                arr_object = np.flip(myFile[key].values, 1)

# upper boundary for range of vertical values selected for the projection - initial values = full
# vertical range
new_ymax = int(y_max)
new_ymin = int(y_min)

# Set up figure
fig = plt.figure(num=data_to_plot, figsize=(9, 9))

# 2D plot i.e. contourplot
ax1 = fig.add_axes([0.09, 0.595, 0.8, 0.395])
contf = ax1.imshow(arr_object.transpose(),
                   extent=[x_min, x_max, y_min, y_max],
                   origin='lower',
                   aspect='auto')

# colorbar
ax3 = fig.add_axes([.9, 0.595, 0.03, 0.395])
cb = plt.colorbar(contf, ax=ax1, cax=ax3)

# 1D plot i.e. projection
projection_1d = np.sum(arr_object, axis=1)
ax2 = fig.add_axes([0.09, 0.135, 0.8, 0.395])
ax2.plot(projection_1d)
ax2.set_xlim([x_min, x_max])
ax2.grid()
ax2.annotate('Press left mouse button on 2D plot to select area to calculate 1D projection',
             xy=(0.5, 0), xycoords='axes fraction',
             xytext=(0, -150), textcoords='offset pixels',
             horizontalalignment='center',
             verticalalignment='bottom')


def onselect(y_min, y_max):
    index_max_projection = (np.abs(yaxis - y_max)).argmin()
    index_min_projection = (np.abs(yaxis - y_min)).argmin()
    tr_arr = arr_object[:, index_min_projection:index_max_projection]
    projection_1d = np.sum(tr_arr, axis=1)

    ax2.clear()
    ax2.grid()
    ax2.set_xlim([x_min, x_max])
    ax2.plot(projection_1d, color='red')

    ax2.annotate(f"ymin: {y_min:.2f}, ymax: {y_max:.2f}",
                 xy=(1, 0), xycoords='axes fraction',
                 xytext=(-20, -90), textcoords='offset pixels',
                 horizontalalignment='right',
                 verticalalignment='bottom')

    print(f"ymin: {y_min}, ymax: {y_max}")
    fig.canvas.draw_idle()

    # save 1d projection
    np.savetxt("projection1D.out", projection_1d, fmt='%.4f',
               header=f"root file: {ROOTfile}, dataset: {data_to_plot} ymin: {y_min}, ymax: {y_max}")


span = SpanSelector(ax1, onselect=onselect, direction='vertical',
                    useblit=True, span_stays=True, button=1,
                    rectprops=dict(facecolor='None', edgecolor='red'))

plt.show()
