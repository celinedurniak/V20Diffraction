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

import os
import uproot
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import SpanSelector
import dataconfig  # to get path to datafiles

assert os.path.exists(dataconfig.data_root), 'The path to ROOT files does not exist.'

ROOTfile = 'Spectrum03_DENEX006_1_18-02-05_0000.root'

dir_with_data = 'Meas_3'

data_to_plot = 'H_TOF,X1-X2_User_2D2_dsp_after_run_3'

file_to_open = os.path.join(dataconfig.data_root, ROOTfile)

assert os.path.isfile(file_to_open), 'There is an issue with the file to be opened.'

with uproot.open(file_to_open)[dir_with_data] as myFile:
    for key in myFile.keys():
        # 2D contourplot
        if data_to_plot in str(key):
            # create x- and y-axis
            xaxis = myFile[key].axis(axis=0).edges()[:-1]
            yaxis = myFile[key].axis(axis=1).edges()[:-1]

            x_min = min(xaxis)
            x_max = max(xaxis)
            y_min = min(yaxis)
            y_max = max(yaxis)
        
            # fill 2d matrice with inverted y-axis
            arr_object = np.flip(myFile[key].counts(False), 1)

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
