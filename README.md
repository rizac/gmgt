# GMGT

**G**round **M**otion **G**round **T**ruth is a software for the generation and deployement
datasets of Ground motion time histories and metadata specifically
created for Big data and machine learning applications.

In this README you will find how to access and work with the data in 
Python. Other references (also mentioned throughout the README) include:

- [Metadata fields (columns) description](metadata_fields.yml)
- [Python module](gmgt.py)
- [Python notebook](gmgt.ipynb)

For any question / problem / enhancement please open a new Issue
(see "Issues" on top of this web page). 


If you want to create your datasets, please contact us for the source data, and then have a look at 
[GMGT (collect)](README-collect.md)

If you want to use the already generated data (interal private useage only), please refer
to [GMGT (download)](README-download.md)

## Getting started

We assume in the following that you have generated or downloaded the GMGT datasets into a `datasests` directory. 

## Datasets directory structure

The `datasets` directory - if all the script of the `collect` directory are executed,
will contain the following files:

| Dataset      |  #waveforms |
|:-------------|------------:|
| ngawest2.hdf |      2,012  |
| esm.hdf      |     45,586  |
| kik2.hdf     |     899,875 | 
| knet2.hdf    |     499,196 | 
|              |  1,466,699  |


where each `hdf` file denotes a gmgt dataset, composed of 
time histories (accelerometers in m/sˆ2) and relative 
[metadata](https://github.com/rizac/gmgt-collect/blob/main/metadata_fields.yml)
all in a single hdf file.

## Usage

> Hint: For processing large datasets, we recommend 
> executing Python modules as scripts instead of Jupyter notebooks, 
> which are better suited for illustrative examples and exploratory 
> analysis; running heavy computations in a script is 
> more efficient

1. Clone the repository

   ```
   git clone https://github.com/rizac/gmgt.git
   cd gmgt
   ```

2. If you already have your Python virtual environment and setup,
   you can copy the file `gmgt.py` in your Python module, or even its 
   [content](gmgt.py) 
   directly in your code. This is a very "quick and dirty" approach: 
   it's fast, but you need to be sure that all requirements are already
   installed.

3. Otherwise, you can create a new fresh virtual env (it can be done
   inside the `gmgt` cloned directory for instance):
   ```
   python3 -m venv .env       # create a venv. Please use Ptyhon 3.11+
   source .env/bin/activate   # Linux/macOS
   # .\env\Scripts\activate   # Windows PowerShell (not tested)
   ```
   
   and then install this package (from within the gmgt directory):
   ```
   pip install .
   ```

   Then you can start coding (Jupyter, Python module) 
   after activating the virtual environment each time
   (type `deactivate` to deactivate the ven). In your code,
   you just have to import:

   ```python
   from gmgt import get_records
   ```

For illustrative purposes (or if you really want to stick to 
Notebooks to process the data) we provided also a
[Python notebook](gmgt.ipynb)
