This folder contains Python scripts and Jupyter notebooks to plot and manipulate 
data recorded at V20 in February 2018, when diffraction experiments were performed.

There are different ways to use ROOT. Installation instructions can be found at 
https://root.cern.ch/root/html534/guides/users-guide/InstallandBuild.html#installing-precompiled-binaries. 
But here, in order to be able to use Python3 as well, we will create a conda environment. 
These instructions can be used to install on MacOS or Linux. Unfortunately there is no `root` conda 
package available for Windows.  
Here are the steps to follow:  

- install anaconda or miniconda (see [link](https://docs.conda.io/projects/conda/en/latest/user-guide/install/download.html))

- create an environment, typing the following 2 lines in a terminal:
    ```
    conda create -n cern_root_env -c conda-forge root matplotlib ipywidgets
    conda activate cern_root_env
    ```

- activate your environment, called `cern_root_env` in this example (but you can choose something 
  else)
  
- install `McStasScript` following the instructions at [link](https://github.com/PaNOSC-ViNYL/McStasScript).

That's it. ROOT provides Jupyter notebooks. To run such a document, type the following command in 
a terminal

   ```
   root --notebook 
   ```

and then either select an existing notebook or create a new one.

Once in the document, just `import ROOT` to use its functionalities.

**Comments**:  

- help about Jupyter notebook: jupyter.org

- to deactivate your environment:
    ```
    conda deactivate
    ```
- to remove the environmwent:
    ```
    conda remove -n cern_root_env --all
    ```
  
- another way to use ROOT and Python is to write Python scripts importing ROOT and running these 
  scripts in the activated environment created above.

- on Linux, I had to install something else:
    ```
    conda install -c conda-forge mpich
    ```

**Content of the folder**:

For different aspects of the data treatment, Python scripts and/or Jupyter notebooks are provided. 
Here are short descriptions about these documents:

- `plot_mcstas_output.py`
   Python script to plot output data of McStas simulation. Two approaches are presented:
       - using `McStasScript`
       - using `matplotlib`

- `plot_he3_data.py`
   Python script to plot ascii files from He3 tubes (after rebinning)
   
- `display_metadata_root.py`
   Python script to display metadata stored in a selected ROOT file

- `plot_all_root_data.py` 
   Python script to plot all graphs stored in a ROOT file
   
- `projection_2D.py`
   Python script to calculate 1D projection of selected portion of 2D contourplot.
   The user can select the range of values to use to calculate the projection
   The values of this projection are saved in an `.out` file, which also contains in its header
   metadata about the ROOT file, the dataset used and the minimum and maximum values of y-values for
   the projection
   
- `run_mcstas_sim.py`
   Python script to run a McStas simulation using McStasScript
   
- `Plot_He3_data.ipynb`
   Notebook to plot ascii files from He3 tubes (after rebinning)

- `Plot_McStas_output.ipynb`
   Notebook to plot output data of McStas simulation. Two approaches are presented:
       - using `McStasScript`
       - using `matplotlib`
   
- `ROOTfile_metadata_and_plots.ipynb`
   Notebook to display metadata in a user-selected ROOT file and display and save all graphs stored
    in ROOT files
   
- `Run_McStas_simulation.ipynb`
   Notebook to run a McStas simulation using McStasScript functionalities
   
- `Plot_ROOT_He3_McStas.ipynb`
   Notebook to plot data from He3, ROOT files and McStas simulations. 
   We focus on He3tube5 and Spectrum03.
