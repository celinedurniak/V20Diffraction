# Open .dat, .png and .tiff files containing 1D and 2D datasets, originally stored in  ROOT files
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
# along with this program. If not, see <https://www.gnu.org/licenses/>.

import os
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import dataconfig  # to get path to datafiles


assert os.path.exists(dataconfig.data_extracted_from_root), 'The path does not exist.'

# 1D datasets
# ascii files
dat_file = os.path.join(dataconfig.data_extracted_from_root, 'Spectrum03H_TOF_dsp_after_run_3.dat')

assert os.path.isfile(dat_file), 'There is an issue with the .dat file for 1D data to be opened.'

d1D = np.genfromtxt(dat_file)
fig, ax = plt.subplots()
ax.set_title('1D png file')
ax.grid()
ax.plot(d1D)
plt.show()

# # png files
png_file = os.path.join(dataconfig.data_extracted_from_root, 'Spectrum03H_TOF_dsp_after_run_3.png')

assert os.path.isfile(png_file), 'There is an issue with the .png file for 1D data to be opened.'

im1D = Image.open(png_file)
im1D.show()

# 2D datasets
# ascii files
dat2d_file = os.path.join(dataconfig.data_extracted_from_root, 'Spectrum03_H_TOF_X1-X2_User_2D2_dsp_run_3_inv_y.dat')

assert os.path.isfile(dat2d_file), 'There is an issue with the .dat file for 2D data to be opened.'

d2D = np.genfromtxt(dat2d_file)
fig, ax = plt.subplots()
CS = ax.contourf(d2D.transpose(), cmap=plt.cm.get_cmap('gist_earth'))
cbar = fig.colorbar(CS)
plt.show()

# png files
png2d_file = os.path.join(dataconfig.data_extracted_from_root, 'Spectrum03_H_TOF_X1-X2_User_2D2_dsp_run_3_inv_y.png')

assert os.path.isfile(png2d_file), 'There is an issue with the .png file for 2D data to be opened.'

im2Dpng = Image.open(png2d_file)
im2Dpng.show()

# tif files
tif2d_file = os.path.join(dataconfig.data_extracted_from_root, 'Spectrum03_H_TOF_X1-X2_User_2D2_dsp_run_3_inv_y.tiff')

assert os.path.isfile(tif2d_file), 'There is an issue with the .tif file for 2D data to be opened.'

im2Dtif = Image.open(tif2d_file)
im2Dtif.show()
