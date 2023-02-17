This folder contains Jupyter notebooks to plot and manipulate
data recorded at V20 in February 2018, when diffraction experiments were performed.

There are different ways to use ROOT. Installation instructions can be found 
[here](https://root.cern.ch/root/html534/guides/users-guide/InstallandBuild.html#installing-precompiled-binaries).  
But here, in order to be able to use Python3 as well, we will create a conda environment using
[`uproot`](https://github.com/scikit-hep/uproot#compressed-objects-in-root-files).  
These instructions can be used to install on MacOS, Linux and Windows. Windows' support is the
reason for using `uproot` (version 4 at least) instead of the ROOT conda package, 
which is not available on Windows.

Here are the steps to follow:

- install anaconda or miniconda (see
  [link](https://docs.conda.io/projects/conda/en/latest/user-guide/install/download.html))

- download or clone this repository from https://github.com/celinedurniak/V20Diffraction.

- unzip if you chose to download.

- in a terminal, move to where you put the folder

- create a conda environment using the `environment.yml` file, by typing the following line in a
  terminal:
    ```
    conda env create -f environment.yml
    ```

- activate your environment, called `v20_root_env` by typing in the terminal
    ```
    conda activate v20_root_env
    ```

The created environment also contains:
-
   - [`ess`](https://scipp.github.io/ess/), required for Wave-Frame Multiplication
    stitching

   - `Pillow` required to convert datasets stored in ROOT files to tiff images,

   - `McStasScript`required to run `McStas` simulations from Python script or Jupyter notebook. Note
    that you have to configure your installation by following the instructions at
    [link](https://github.com/PaNOSC-ViNYL/McStasScript).


You can now use the Jupyter notebooks. The next step is to specify the path
to the different datafiles by running `make_config.py` either in the `notebooks` folder. In the terminal where your conda environment is activated, type the following
commands, if you want to use the notebooks:

   ```
   cd notebooks
   python makeconfig.py
   ```
You will be asked to enter different absolute paths respectively to:
- the ROOT files
- the folder containing results of the McStas simulation you want to compare the ROOT files to
- the folder to the He3 tubes ASCII files related to the same experiment as the one, when the ROOT
  files have been recorded.
- the fourth path has to be entered if you already have converted some of the ROOT files to .tif,
  .dat or .png (using `plot_all_root_data.py` or `ROOTfile_metadata_and_plots.ipynb`).

Simply press `Enter` if you do not have such types of files. The output is written in a
`dataconfig.py`, which is imported in the notebooks to get access the datafiles' contents.

You can also directly create a `dataconfig.py` by hand. Its content is  

```python
data_root="Absolute path to ROOT data files to be specified"
data_mcstas="Absolute path to McStas output data files to be specified"
data_he3="Absolute path to He3 tubes ASCII data files to be specified"
data_extracted_from_root="Absolute path to output files from conversion of ROOT files to be specified"
```
If you do not have any particular type of datafiles, leave an empty quote `""`.

**Comments**:  

- help about Jupyter notebook: jupyter.org

- to deactivate your environment:
    ```
    conda deactivate
    ```
- to remove the environmwent:
    ```
    conda remove --name v20_root_env --all
    ```

- another way to use ROOT and Python is to write Python scripts importing `uproot` and running these
  scripts in the activated environment created above.

  To run the Python script, in a terminal:

      * activate your conda environment (if it is not already the case)
      * move to where your Python script is located
        (*i.e.*, typing `cd path_to_where_your_python_script_is`)
      * type `python name_of_python_script.py`

   Note that you will have to edit the script to specify the path where the data (ROOT file,
   McStas output files, data from He3 tubes)

- on Linux, I had to install something else:
    ```
    conda install -c conda-forge mpich
    conda install -c anaconda gxx_linux-64
    ```

- to test your installation, in the activated conda environment you can run the Python script
  `check_installation.py` located in the `tools` folder. It will check if `uproot`, `PIL`,
  `McStasScript` and `matplotlib` are installed.


**Content of the folder**:

For different aspects of the data treatment, Jupyter notebooks are provided:

| Actions performed                                   | Jupyter notebook                     |
|:----------------------------------------------------|:-------------------------------------|
| run McStas simulation                               | `Run_McStas_simulation.ipynb`+       |
| plot McStas output datafiles                        | `Plot_McStas_output.ipynb`+          |
| plot ascii files from He3 tubes                     | `Plot_He3_data.ipynb`                |
| plot all ROOT files                                 | `ROOTfile_metadata_and_plots.ipynb`* |
| display metadata stored in a selected ROOT file     | `ROOTfile_metadata_and_plots.ipynb`* |
| plot and compare data from He3, ROOT and McStas     | `Plot_ROOT_He3_McStas.ipynb`+        |
| calculate and display projection of 2D data         | `projection_2D.py`                   |
| generate tif, dat, png from ROOT files              | `ROOTfile_metadata_and_plots.ipynb`* |
| open and display tif, dat, png from ROOT files      | `Open_tiff_png_dat_from_ROOT.ipynb`* |
| compare 2D data from ROOT and McStas                | `Compare_2D_datasets.ipynb`          |
| perform WFM stitching on ROOT and Mcstas data       | `WFM_Stitching_2D.ipynb`             |
| compare 1D projections from 2D ROOT and Mcstas data | `Projection_2D.ipynb`                |


Legend of the table: * : requires PIL and + : requires McstasScript  

Here are short descriptions about these documents:

- `Compare_2D_datasets.ipynb`
   Notebook to compare 2D data from ROOT and McStas. The data are cropped, resampled to the coarser
   grid and rescaled in intensity.

- `Open_tiff_png_dat_from_ROOT.ipynb`
   Notebook to open and display `.dat`, `.png`, `.tiff` files of 1D and 2D datasets, originally
   stored in ROOT files

- `Plot_He3_data.ipynb`
   Notebook to plot ascii files from He3 tubes (after rebinning)

- `Plot_McStas_output.ipynb`
   Notebook to plot output data of McStas simulation. Two approaches are presented:
       - using `McStasScript`
       - using `matplotlib`

- `Plot_ROOT_He3_McStas.ipynb`
   Notebook to plot data from He3, ROOT files and McStas simulations.
   We focus on He3tube5 and Spectrum03

- `Projection_2D.ipynb`
   Notebook to compare 1D projections from 2D ROOT and McStas data. The range of y-values to
   generate the projections is set by the user

- `ROOTfile_metadata_and_plots.ipynb`
   Notebook to display metadata in a user-selected ROOT file and display and save all graphs stored
    in ROOT files

- `Run_McStas_simulation.ipynb`
   Notebook to run a McStas simulation using McStasScript functionalities

- `WFM_Stitching_2D.ipynb`
   Notebook to perform WFM stitching on ROOT and McStas data
