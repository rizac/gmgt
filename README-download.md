# GMGT

If you do not want or cannot supply the source data to be harmonized 
and create a GMGT dataset (see scripts under the `collect` directory),
you can access the already generated datasets hosted at GFZ

> **Disclaimer:** 
> Most datasets are released under a restricted license and provided here solely for research use.
> Redistribution in any form is in most cases strictly prohibited.
> The authors accept no responsibility for any misuse of the data.

## Download the datasets

Data is hosted on a private server at GFZ (section 2.6). 
To access the data, you must use SSH (Secure Shell Protocol), 
i.e., you must generate a pair of private and public keys, 
and send to us **the public key only** via email.


### Generating a ssh key pair

Open the terminal and generate your ssh key (replace your email below)

```bash
ssh-keygen -t ed25519 -C "your_email@example.com"
```

and follow instructions (if you are asked about a passphrase, 
you can leave it empty and continue). If you now type 
`ls -l $HOME/.ssh` (usual directory with ssh keys, or wherever you 
decided to save the key into) you should see something like this:
```
ls -l $HOME/.ssh/
drwx------   6 user  staff  192 Jan 19 16:02 .
drwxr-x---+ 31 user  staff  992 Jan 20 17:44 ..
-rw-r--r--   1 user  staff   94 Jan 19 16:02 id_ed25519.pub
-rw-------   1 user  staff  399 Jan 19 16:02 id_ed25519
... (other files not shown) ...
```

Take the file with `.pub` extension (e.g., `id_ed25519.pub`. 
**do not share with anybody the same file without extension:
it's the PRIVATE key**) 
and send it to lemgo@[domain] (rizac@[domain] in CC)
asking for access to the casco server as ethz user

In the following, [domain] refers to `gfz.de` 
and [port] to 54646 (both redacted for basic security hygiene).

### Download the data

In you terminal, `cd` to the directory you want to save the 
files from the GFZ server (recommended name `gmgt/datasets`) and type:

```bash
scp -P [port] -r ethz@casco.[domain]:/home/ethz/gmgt/datasets/*.hdf .
```

This will create a `datasets` directory with all files. 
The process will take several minutes (in the order of tens of minutes, 
not hours).

If you want to copy a specific dataset only  
(it could be necessary in the validation phase, where we
will likely recreate the datasets from scratch), type:

```commandline
scp -P [port] ethz@casco.[domain]:/home/ethz/gmgt/datasets/esm.hdf .
scp -P [port] ethz@casco.[domain]:/home/ethz/gmgt/datasets/kik.hdf .
scp -P [port] ethz@casco.[domain]:/home/ethz/gmgt/datasets/knet.hdf .
scp -P [port] ethz@casco.[domain]:/home/ethz/gmgt/datasets/ngawest2.hdf .
```

## Datasets directory structure

The `datasets` directory will contain the following files:

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
   [content](gmgt.py?ref_type=heads) 
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
   pip install -e .
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
[Python notebook](gmgt.ipynb?ref_type=heads)
