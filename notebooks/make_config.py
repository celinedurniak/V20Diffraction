#!/usr/bin/env python
# Create dataconfig.py to store path to ROOT files, McStas simulation output and He3 ASCII files
# related to experiment at V20 in February 2018
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


def clean_path(path):
    """ Remove simple and double quotes from beginning and end of path """
    if path != '':
        if path.startswith('"'):
            return path.strip('"')
        elif path.startswith("'"):
            return path.strip("'")
        else:
            return path
    else:
        # leave empty string unchanged
        return path


def check_path(path):
    """ Check that path is an existing directory """
    if path != '':
        # print(f"{path} in check_path")
        assert os.path.isdir(path), f"Issue with {path}"


if __name__ == '__main__':
    path_data_root = clean_path(input('Enter absolute path to ROOT files: ').strip() or '')
    # print(f"data_root: {path_data_root[0]}")
    path_data_mcstas = clean_path(input('Enter absolute path to McStas files: ').strip() or '')
    path_data_he3 = clean_path(input('Enter absolute path to He3 ASCII files: ').strip() or '')
    path_data_extracted_from_root = clean_path(
        input('Enter absolute path to tif, dat, png files extracted from ROOT files: ').strip()
        or
        ''
    )

    # check validity of inputs if not empty strings
    check_path(path_data_root)
    check_path(path_data_mcstas)
    check_path(path_data_he3)
    check_path(path_data_extracted_from_root)

    # make the config.py
    with open('dataconfig.py', 'w') as file_out:
        file_out.write(f'data_root="{path_data_root}"\n')
        file_out.write(f'data_mcstas="{path_data_mcstas}"\n')
        file_out.write(f'data_he3="{path_data_he3}"\n')
        file_out.write(f'data_extracted_from_root="{path_data_extracted_from_root}"\n')
    print('dataconfig.py written')
