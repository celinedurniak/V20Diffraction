# Plot graphs of output datafiles generated by a McStas simulation
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
from mcstasscript.interface import instr
from mcstasscript.interface import plotter
from mcstasscript.interface import functions
from mcstasscript.interface import reader

import numpy as np
import matplotlib.pyplot as plt


# path to load McStas simulation data
path_to_model = "/Users/celinedurniak/V20DiffractionData"

assert os.path.exists(path_to_model), 'The path does not exist.'

# Folder containing output of McStas simulation
result_folder = 'V20_config6'

assert os.path.isdir(os.path.join(path_to_model, result_folder)), \
    'The folder which should contain the outputs of McStas simulation does not exist'

# read instrument file
model_to_open = os.path.join(path_to_model, result_folder, "V20_config6.instr")

assert os.path.isfile(model_to_open), 'There is an issue with the McStas .instr file to be opened.'

InstrReader = reader.McStas_file(model_to_open)

# check McStas instrument file for the type of sample
McStasInstrument = instr.McStas_instr("McStasInstrument")
InstrReader.add_to_instr(McStasInstrument)
McStasInstrument.print_components()

McStasInstrument.print_component('NAK')

# access data stored after McStas simulations
data_to_plot = functions.load_data(os.path.join(path_to_model, result_folder))

# Create a dictionary containing filenames, shape of output data, x, y labels and
# position of component
dict_mcstas_files = {}

for item in data_to_plot:
    file_key = item.metadata.info['filename'].rstrip()
    xlabel = item.metadata.info['xlabel'].rstrip()
    ylabel = item.metadata.info['ylabel'].rstrip()
    position = [float(item) for item in item.metadata.info['position'].split()]
    type_array = item.metadata.info['type']
    start = type_array.find('(') + 1
    end = type_array.find(')', start)

    if ',' in type_array[start:end]:
        nx_value, ny_value = type_array[start:end].split(',')

        dict_mcstas_files[file_key] = ((int(nx_value),
                                        int(ny_value)),
                                       xlabel,
                                       ylabel,
                                       position)
    else:
        dict_mcstas_files[file_key] = (int(type_array[start:end]),
                                       xlabel,
                                       ylabel,
                                       position)

# plot all datafiles on a single page
# plotter.make_sub_plot(data_to_plot)
for item in data_to_plot:
    plotter.make_sub_plot(item)

# plot selected datafiles with matplotlib

# plot 1D data generated by McStas simulation and plot using matplotlib
selected_filename = 'monitor_Hetube6.dat'

datafile1D_to_open = os.path.join(path_to_model, result_folder,  selected_filename)

assert os.path.isfile(datafile1D_to_open), 'There is an issue with the 1D datafile to be opened.'

# quick check that we have 1D or 2D data
print(dict_mcstas_files[selected_filename])

fig, ax = plt.subplots()
x, y = np.genfromtxt(datafile1D_to_open, usecols=(0, 1), unpack=True)
ax.plot(x, y, label=selected_filename)
ax.set_xlabel(dict_mcstas_files[selected_filename][1])
ax.set_ylabel(dict_mcstas_files[selected_filename][2])
ax.legend()
plt.show()

# plot 2D
selected_filename = 'monitor_tx_DENEX.dat'

datafile2D_to_open = os.path.join(path_to_model, result_folder, selected_filename)

assert os.path.isfile(datafile2D_to_open), 'There is an issue with the 2D datafile to be opened.'

print(dict_mcstas_files[selected_filename])

data2d = np.genfromtxt(datafile2D_to_open, max_rows=dict_mcstas_files[selected_filename][0][0])

if float(dict_mcstas_files[selected_filename][-1][0]) < 0:
    data2d = np.flip(data2d, 0)

fig, ax = plt.subplots()
contf = ax.imshow(np.flip(data2d, 0), aspect='auto')
ax.set_xlabel(dict_mcstas_files[selected_filename][1])
ax.set_ylabel(dict_mcstas_files[selected_filename][2])
ax.set_title(selected_filename)
cbar = fig.colorbar(contf)
plt.show()
