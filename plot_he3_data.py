# Plot graphs of He3 datafiles (.asc files)
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

# Naming of these files:
# -  The `bn4` format is a raw data file (event mode) that can be rebinned.
# Christian Jacobsen (HZG) wrote us a small python script to generate asci files from it, which also generates the filename. So you are completely right: the number indicates the binning size used to histogram the data. I attach the python script as well.
#
# - `chX` corresponds to the channel # of the 4 tubes.
#     a. There are four tubes for diffraction, *i.e.* four channels. TsDau has a total of
#     eight channels. Two of them were used for beam monitors, two were empty.
#    b.  In our case (Feb 2018), `Ch3` was a beam monitor and `Ch5`, `Ch6`, `Ch7`, `Ch8` were
#    the four diffraction tubes.
#
# - `binX` indicates the number of bins used to histogram the data.
#
# Only data with 2500 bins were considered for Spectrum3 in order to be consistent for all spectra.

import numpy as np
import matplotlib.pyplot as plt

path_to_he3_files = "/Users/celinedurniak/Documents/test_root/Diffraction/TBL_Data_DreamTeam_Feb2018/DREAMTeam_Feb2018/TsDau/"

# Spectrum 3
he3sp3ch3 = np.genfromtxt(path_to_he3_files+"Spectrum03.bn4ch3_bin2500.asc")
he3sp3ch5 = np.genfromtxt(path_to_he3_files+"Spectrum03.bn4ch5_bin2500.asc")
he3sp3ch6 = np.genfromtxt(path_to_he3_files+"Spectrum03.bn4ch6_bin2500.asc")
he3sp3ch7 = np.genfromtxt(path_to_he3_files+"Spectrum03.bn4ch7_bin2500.asc")
he3sp3ch8 = np.genfromtxt(path_to_he3_files+"Spectrum03.bn4ch8_bin2500.asc")

fig, ax = plt.subplots(3, 2, sharex='col', figsize=(10, 10))
plt.suptitle('Data from He3 tubes')

plt.figtext(0.5, 0.9, 'Spectrum 3', ha='center', va='center')
ax[0, 0].plot(he3sp3ch3[:, 0], he3sp3ch3[:, 1], label='Ch3')
ax[0, 0].legend()
ax[0, 0].grid()

ax[0, 1].plot(he3sp3ch5[:, 0], he3sp3ch5[:, 1], label='Ch5')
ax[0, 1].plot(he3sp3ch6[:, 0], he3sp3ch6[:, 1], label='Ch6')
ax[0, 1].plot(he3sp3ch7[:, 0], he3sp3ch7[:, 1], label='Ch7')
ax[0, 1].plot(he3sp3ch8[:, 0], he3sp3ch8[:, 1], label='Ch8')
ax[0, 1].legend()
ax[0, 1].grid()

# Spectrum 11
he3sp11ch3 = np.genfromtxt(path_to_he3_files+"Spectrum11.bn4ch3_bin2500.asc")
he3sp11ch5 = np.genfromtxt(path_to_he3_files+"Spectrum11.bn4ch5_bin2500.asc")
he3sp11ch6 = np.genfromtxt(path_to_he3_files+"Spectrum11.bn4ch6_bin2500.asc")
he3sp11ch7 = np.genfromtxt(path_to_he3_files+"Spectrum11.bn4ch7_bin2500.asc")
he3sp11ch8 = np.genfromtxt(path_to_he3_files+"Spectrum11.bn4ch8_bin2500.asc")

#fig.suptitle('Spectrum 11 - data from He3 tubes')
plt.figtext(0.5, 0.62, 'Spectrum 11', ha='center', va='center')
ax[1, 0].plot(he3sp11ch3[:, 0], he3sp11ch3[:, 1], label='Ch3')
ax[1, 0].legend()
ax[1, 0].grid()

ax[1, 1].plot(he3sp11ch5[:, 0], he3sp11ch5[:, 1], label='Ch5')
ax[1, 1].plot(he3sp11ch6[:, 0], he3sp11ch6[:, 1], label='Ch6')
ax[1, 1].plot(he3sp11ch7[:, 0], he3sp11ch7[:, 1], label='Ch7')
ax[1, 1].plot(he3sp11ch8[:, 0], he3sp11ch8[:, 1], label='Ch8')
ax[1, 1].legend()
ax[1, 1].grid()

# Spectrum 12
he3sp12ch3 = np.genfromtxt(path_to_he3_files+"Spectrum12.bn4ch3_bin2500.asc")
he3sp12ch5 = np.genfromtxt(path_to_he3_files+"Spectrum12.bn4ch5_bin2500.asc")
he3sp12ch6 = np.genfromtxt(path_to_he3_files+"Spectrum12.bn4ch6_bin2500.asc")
he3sp12ch7 = np.genfromtxt(path_to_he3_files+"Spectrum12.bn4ch7_bin2500.asc")
he3sp12ch8 = np.genfromtxt(path_to_he3_files+"Spectrum12.bn4ch8_bin2500.asc")

#fig, (ax1, ax2) = plt.subplots(2, figsize=(8,10))
plt.figtext(0.5, 0.35, 'Spectrum 12', ha='center', va='center')
#fig.suptitle('Spectrum 12 - data from He3 tubes')

ax[2, 0].plot(he3sp12ch3[:, 0], he3sp12ch3[:, 1], label='Ch3')
ax[2, 0].legend()
ax[2, 0].grid()
ax[2, 0].set_xlabel('TOF (ms)')

ax[2, 1].plot(he3sp12ch5[:, 0], he3sp12ch5[:, 1], label='Ch5')
ax[2, 1].plot(he3sp12ch6[:, 0], he3sp12ch6[:, 1], label='Ch6')
ax[2, 1].plot(he3sp12ch7[:, 0], he3sp12ch7[:, 1], label='Ch7')
ax[2, 1].plot(he3sp12ch8[:, 0], he3sp12ch8[:, 1], label='Ch8')
ax[2, 1].legend()
ax[2, 1].grid()
ax[2, 1].set_xlabel('TOF (ms)')

plt.show()
