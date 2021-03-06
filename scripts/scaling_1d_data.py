# Affine rescaling of 1D plots from McStas, Root and He3 tubes data
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
import uproot
import matplotlib.pyplot as plt
from matplotlib.widgets import TextBox, Button, CheckButtons
import matplotlib.gridspec as gridspec
import numpy as np
import re
import dataconfig  # to get path to datafiles


colors_curves = ['#1f77b4', '#ff7f0e', '#2ca02c']


fig, ax = plt.subplots(figsize=(9, 9))
fig.suptitle('Enter the formula to modify the x- or y-axes of McStas, ROOT or He3 tubes data',
             fontsize=12)
ax.title.set_text(r'Only affine transformations are allowed. Index m, r , h refers to McStas, '
                  r'ROOT and He3, respectively ')

# Mcstas data
path_to_mcstas_file = os.path.join(dataconfig.data_mcstas, 'monitor_Hetube5.dat')

assert os.path.isfile(path_to_mcstas_file), \
    'There is an issue with the chosen McStas output datafile'

x_mcstas, y_mcstas = np.genfromtxt(path_to_mcstas_file, usecols=(0, 1), unpack=True)

line_mcstas, = ax.plot(x_mcstas, y_mcstas, label='mcstas', color=colors_curves[0])
# store initial values
xini_mcstas = line_mcstas.get_xdata()
yini_mcstas = line_mcstas.get_ydata()

# ROOT data H_TOF_dsp_after_run_3
path_to_root_file = os.path.join(dataconfig.data_root, 'Spectrum03_DENEX006_1_18-02-05_0000.root')

assert os.path.isfile(path_to_root_file), 'There is an issue with the chosen ROOT file'

data_to_load = 'H_TOF_dsp_after_run_3'

with uproot.open(path_to_root_file)['Meas_3'] as myFile:
    for key, value in myFile.iterclassnames():
        # 1D line plot
        if 'TH1I' in str(value) and data_to_load in str(key): 
            y_root = myFile[key].counts(False)

x_root = np.arange(len(y_root))
line_root, = ax.plot(x_root, y_root, label='root', color=colors_curves[1])
# store initial values
xini_root = line_root.get_xdata()
yini_root = line_root.get_ydata()

# He3 data
path_to_he3_file = os.path.join(dataconfig.data_he3, 'Spectrum03.bn4ch3_bin2500.asc')

assert os.path.isfile(path_to_he3_file), \
    'There is an issue with the chosen datafile from He3 tube'

x_he3, y_he3 = np.genfromtxt(path_to_he3_file, usecols=(0, 1), unpack=True)
line_he3, = ax.plot(x_he3, y_he3, label='he3', color=colors_curves[2])
# store initial values
xini_he3 = line_he3.get_xdata()
yini_he3 = line_he3.get_ydata()

ax.legend()
ax.grid()
ax.set_autoscale_on(True)
ax.autoscale_view(True, True, True)

######
# add textboxes for editing scaling settings
fig.subplots_adjust(bottom=0.3)

gs = gridspec.GridSpec(3, 2)
gs.update(left=0.2, right=0.8, bottom=0.05, top=0.2, hspace=0.1, wspace=0.8)

axes = [fig.add_subplot(gs[i, j]) for i, j in [[0, 0], [0, 1], [1, 0], [1, 1], [2, 0], [2, 1]]]

abx_mcstas = TextBox(axes[0], r'$\alpha_{x,m}.x + \beta_{x,m}$', initial='x', label_pad=0.05)
aby_mcstas = TextBox(axes[1], r'$\alpha_{y,m}.y + \beta_{y,m}$', initial='y', label_pad=0.05)
abx_mcstas.label.set_color(colors_curves[0])
aby_mcstas.label.set_color(colors_curves[0])

abx_root = TextBox(axes[2], r'$\alpha_{x,r}.x + \beta_{x,r}$', initial='x', label_pad=0.05)
aby_root = TextBox(axes[3], r'$\alpha_{y,r}.y + \beta_{y,r}$', initial='y', label_pad=0.05)
abx_root.label.set_color(colors_curves[1])
aby_root.label.set_color(colors_curves[1])

abx_he3 = TextBox(axes[4], r'$\alpha_{x,h}.x + \beta_{x,h}$', initial='x', label_pad=0.05)
aby_he3 = TextBox(axes[5], r'$\alpha_{y,h}.y + \beta_{y,h}$', initial='y', label_pad=0.05)
abx_he3.label.set_color(colors_curves[2])
aby_he3.label.set_color(colors_curves[2])

# add reset button
axbtn = plt.axes([0.825, 0.05, 0.15, 0.05])
btn = Button(axbtn, 'Reset', color='0.85', hovercolor='0.95')

#####
lines = [line_mcstas, line_root, line_he3]

rax = plt.axes([0.825, 0.105, 0.15, 0.095])
labels = [str(line.get_label()) for line in lines]
visibility = [line.get_visible() for line in lines]
check = CheckButtons(rax, labels, visibility)


def hide_curve(label):
    """
    Hide curve when box is checked
    """
    index = labels.index(label)
    lines[index].set_visible(not lines[index].get_visible())
    plt.draw()


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass


def validate_formula(formula):
    """
    Check validity of input formula
    Only affine transformation is allowed
    These types of expressions are accepted:
    ±x, ±a * x ± b, x / a ± b where a, b are numbers (scientific notation allowed)
    The above formulae also apply for 'y' instead of x
    """
    # check that x xor y in expression and split formula into term before and after 'x' or 'y'
    if ('x' in formula and not 'y' in formula) or ('y' in formula and not 'x' in formula):
        elements_formula = re.split("[yx]{1}", formula)

        # Result of splitting should give two elements at most (could be empty strings)
        if len(elements_formula) != 2:
            return False
        else:
            # check the first element (before 'x' or 'y'):
            # it could be +, - or nothing
            if elements_formula[0] in ['', '+', '-']:
                check_first_element = True
            # or +alpha* or -alpha* where alpha is a number
            else:
                if elements_formula[0][-1] == '*' \
                        and is_number(elements_formula[0][:-1]):
                    check_first_element = True
                else:
                    check_first_element = False

            # check second element:
            # it could be empty
            if elements_formula[1] == '':
                check_second_element = True
            # or ±b(±a), /a±b, *a±b where a,b are numbers
            else:
                if elements_formula[1][0] in ['+', '-', '/', '*']:
                    # check that the last term contains only addition or subtraction of numbers
                    split_2nd_element = re.split("[+-]{1}", elements_formula[1][1:])
                    all(is_number(item) for item in split_2nd_element)
                    check_second_element = True
                else:
                    check_second_element = False

        return check_first_element and check_second_element
    else:
        return False


def rescale_plot_range():
    """
    redraw plot with updated boundaries (after rescaling one of the plots)
    """
    ax.relim()
    ax.autoscale_view(True, True, True)
    fig.canvas.draw()
    fig.canvas.flush_events()


def submit_abx_mcstas(val):
    """
    modify x values of mcstas curve with scaling and offset factors
    """
    if validate_formula(val):
        x_output = [eval(val) for x in xini_mcstas]
        line_mcstas.set_xdata(x_output)
        rescale_plot_range()


def submit_aby_mcstas(val):
    """
    modify y values of mcstas curve with scaling and offset factors
    """
    if validate_formula(val):
        y_output = [eval(val) for y in yini_mcstas]

        line_mcstas.set_ydata(y_output)
        rescale_plot_range()


def submit_abx_root(val):
    """
    modify x values of root curve with scaling and offset factors
    """
    if validate_formula(val):
        x_output = [eval(val) for x in xini_root]
        line_root.set_xdata(x_output)
        rescale_plot_range()


def submit_aby_root(val):
    """
    modify y values of root curve with scaling and offset factors
    """
    if validate_formula(val):
        y_output = [eval(val) for y in yini_root]
        line_root.set_ydata(y_output)
        rescale_plot_range()


def submit_abx_he3(val):
    """
    modify x values of he3 tube curve with scaling and offset factors
    """
    if validate_formula(val):
        x_output = [eval(val) for x in xini_he3]
        line_he3.set_xdata(x_output)
        rescale_plot_range()


def submit_aby_he3(val):
    """
    modify y values of he3 tube curve with scaling and offset factors
    """
    if validate_formula(val):
        y_output = [eval(val) for y in yini_he3]
        line_he3.set_ydata(y_output)
        rescale_plot_range()


def submit_reset(event):
    """
    Reset all textboxes
    """
    abx_mcstas.set_val('x')
    aby_mcstas.set_val('y')

    abx_root.set_val('x')
    aby_root.set_val('y')

    abx_he3.set_val('x')
    aby_he3.set_val('y')


check.on_clicked(hide_curve)

btn.on_clicked(submit_reset)

abx_mcstas.on_submit(submit_abx_mcstas)
aby_mcstas.on_submit(submit_aby_mcstas)

abx_root.on_submit(submit_abx_root)
aby_root.on_submit(submit_aby_root)

abx_he3.on_submit(submit_abx_he3)
aby_he3.on_submit(submit_aby_he3)

plt.show()
