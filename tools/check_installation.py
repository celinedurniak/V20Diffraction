# check if packages required by some of the scripts or notebooks are installed
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

import pkgutil

# check installation of uproot
if not pkgutil.find_loader("uproot"):
    message = '''
    uproot is not installed.
    It is required to use `display_metadata_root.py`, `plot_all_root_data.py`, `projection_2D.py`, 
    `scaling_1d_data.py`, `Plot_ROOT_He3_McStas.ipynb`, and `ROOTfile_metadata_and_plots.ipynb`.
    Please refer to the installation instructions for the exact command to use to install uproot.
    '''
    print(message)
else:
    print('''
    uproot is installed.
    ''')

# check installation of PIL
if not pkgutil.find_loader("PIL"):
    message = '''
    PIL is not installed. 
    It is required to use `open_tiff_png_dat_from_ROOT.py`, `plot_all_root_data.py`, 
    `Open_tiff_png_dat_from_ROOT.ipynb`, and  `ROOTfile_metadata_and_plots.ipynb`. 
    Please refer to the installation instructions for the exact command to use to install PIL.
    '''
    print(message)
else:
    print('''
    PIL is installed.
    ''')

# check installation of McStasScript
if not pkgutil.find_loader("mcstasscript"):
    message = '''
    McStasScript is not installed. 
    It is required to use `plot_mcstas_output.py`, `run_mcstas_sim.py`, `Plot_McStas_output.ipynb`, 
    and `Run_McStas_simulation.ipynb`. 
    Please refer to the installation instructions for the exact command to use to install 
    McStasScript.
    '''
    print(message)
else:
    print('''
    McStasScript is installed.
    ''')

# check installation of matplotlib
if not pkgutil.find_loader("matplotlib"):
    message = '''
    matplotlib is not installed. 
    It is required to use `open_tiff_png_dat_from_ROOT.py`, `plot_all_root_data.py`, 
    `plot_he3_data.py`, `plot_mcstas_output.py`, `projection_2D.py`, `scaling_1d_data.py`, 
    `Open_tiff_png_dat_from_ROOT.ipynb`, `Plot_He3_data.ipynb`,  `Plot_McStas_output.ipynb`, 
    `Plot_ROOT_He3_McStas.ipynb`, and `ROOTfile_metadata_and_plots.ipynb`. 
    Please refer to the installation instructions for the exact  command to use to install 
    matplotlib.
    '''
    print(message)
else:
    print('''
    matplotlib is installed.
    ''')
