# Run McStas simulation using McStasScript
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
from mcstasscript.interface import reader
import dataconfig  # to get path to datafiles


# load McStas instrument file.

assert os.path.exists(dataconfig.data_mcstas), 'The path to McStas files does not exist.'

model_to_open = os.path.join(dataconfig.data_mcstas, 'V20_config6.instr')

assert os.path.isfile(model_to_open), 'There is an issue with the McStas .instr file to be opened.'

InstrReader = reader.McStas_file(model_to_open)

InstrReader.write_python_file('generated_mode.py', force=True)

demoV20 = instr.McStas_instr('V20diffraction')
InstrReader.add_to_instr(demoV20)

demoV20.print_components()

# Display parameters for a selected component
demoV20.get_component('source').show_parameters_simple()

demoV20.get_component('FOC_2_f').show_parameters_simple()

demoV20.print_component('FOC_2_f')

# Display all parameters for defined McStas model
demoV20.show_parameters()

# name of the folder where the output data from the simulation will be written
result_folder = 'testV20'

# With increment_folder_name enabled, a new folder with incremented number is created
data = demoV20.run_full_instrument(foldername=result_folder,
                                   mpi=2,
                                   ncount=2E4,
                                   increment_folder_name=True)

assert os.path.isdir(result_folder), \
    'The folder which should contain the outputs of McStas simulation does not exist'

# plot results
for item in data:
    plotter.make_sub_plot(item)
