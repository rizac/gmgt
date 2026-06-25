[&laquo; back to README](README.md)

The `collect` sub directory contains the scripts for assembling
harmonized ground truth datasets of processed ground motion data and 
metadata which can then feed Deep- and Machine-learning applications.

The source data for generating the harmonized GMGT datasets is not publicly available and
has strict requirements (e.g. usage only, no redistribution). 
Please contact the author for questions or getting access to them

# Installation

- Clone this package

- Install a Python virtual environment:
  ```
  python3 -m venv .env 
  ```

- Activate the environment **to be done every time you run Python code**
  ```
  source .env/bin/activate
  ```

- Install required packages (pytest is optional, i.e. in square brackets. Remove
  if you do not plan to test scripts):
  ```
  pip install ".[collect]"
  ```
  <!--  pip install --upgrade pip setuptools && pip install "pandas<3" h5py pyyaml tables tqdm [pytest] -->

# Dataset generation

A GMGT dataset needs two sources: a metadata file (usually CSV or HDF) where each record is associated
to its medatata, and a directory of time histories (in any format you want) that should be present in
the metadata.

Once you have these requisites in place:

<details>
<summary>If you need to generate a new GMGT dataset from new source data, click here</summary>
   Copy one of the already implemented scripts `create_<dataset_name>.py` and modify the editable 
   functions (see instructions therein)
</details>

1. Create a YAML file that will be used as argument, where you setup the source metadata
   and the source time histories, e.g. in a file `<dataset_name>.yml`:
   
   ```yaml
    source_metadata: "/home/dasegen/source-datasets/<dataset_name>/<soude_metadata>.csv"
    source_data: "/home/dasegen/source-datasets/<dataset_name>/Waveforms"
    destination: "/home/dasegen/datasets/<dataset_name>"
    ```

2. Execute `create_<dataset_name>.py <dataset_name>.yml`

# Upload to casco server

Follow instructions in gmgt **reversing source and destination**. 
The machine currently used to create the datasets (rs1) has already
the ssh public key set on the server, so no password is required
