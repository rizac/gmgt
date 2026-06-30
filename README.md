# GMGT

**G**round **M**otion **G**round **T**ruth is a software for the generation 
and deployment of datasets of Ground motion time histories and metadata,
specifically created for Big data and machine learning applications.

<!-- In this README you will find how to access and work with the data in 
Python. Other references (also mentioned throughout the README) include:


- [Python module](gmgt.py)
- [Python notebook](gmgt.ipynb)
-->

For any question / problem / enhancement please open a new Issue
(see "Issues" on top of this web page). 

## Creating a new dataset

If you want to create your harmonized dataset form your source, 
please contact us for the source data, and then have a look at 
[GMGT (collect)](README-collect.md)

## Downloaded already created datasets (needs authorization)

If you want to skip the dataset generation, the GFZ section 2.6 hosts 
(for private usage only) already created datasets. 
Please refer to [GMGT (download)](README-download.md)

## Getting started

We assume in the following that you have generated or downloaded the GMGT datasets into a `datasests` directory. 

### Datasets directory structure

The `datasets` directory - if all the script of the `collect` directory are executed,
will contain the following files:

| Dataset      |    #waveforms |
|:-------------|--------------:|
| ngawest2.hdf |         2,012 |
| esm.hdf      |        45,586 |
| kik2.hdf     |       899,875 | 
| knet2.hdf    |       499,196 | 
| **Total:**   | **1,466,699** |


where each `hdf` file denotes a GMGT dataset, composed of 
time histories (accelerometers in m/sˆ2) and relative 
[metadata](https://github.com/rizac/gmgt-collect/blob/main/metadata_fields.yml) all in a single hdf file.

Each time history is a numpy container of 1 to 3 numeric arrays (denoting
each recording component) and a `dt` (denoting the sampling interval), whereas
the metadata is a tabular structure with the following fields:

- [Metadata fields (columns) description](metadata_fields.yml)

Users are supposed to select the time histories based on the metadata, and
work with the data, as explained in the associated python module and notebook
(see below for details)

### Usage

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
