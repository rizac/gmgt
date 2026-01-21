# gmgt

*G*round *M*otion *G*round *T*ruth is a collection of datasets 
of Ground motion time hisotries and metadata specifically
created for Big data and machine learning applications.

In this README you will find how to acceess and work with the data in 
Python


## Getting started

Data has been created with a public Python prpoject hosted on 
[GitHub](https://github.com/rizac/gmgt-collect). 
Please refer to that project if you are supplying new source data 
to be harmonized and shipped as gmgt dataset. 


## Download the datasets

Data is hosted on a private server at GFZ (section 2.6). 
To access the data, you must use using SSH (Secure Shell Protocol), 
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
and send it to lemgo@gfz.de (rizac@gfz.de in CC)


### Download the data

In you terminal, `cd` to the directory you want to save the 
files from the GFZ server (recommended name `gmgt`` and type:

```bash
scp -P 54646 -r ethz@casco.gfz.de:/home/ethz/gmgt/datasets .
```

This will create a `datasets` directory with all files
The process will likely take several minutes.


## Data structure

The downloaded directory structure will be as follows:

```
ngawest2.hdf
esm.hdf
kiknet_knet.hdf
```

where each `hdf` file denotes a gmgt dataset, composed of 
time histories (accelerometers in m/sˆ2) and relative metadata.

## Usage

1. Clone the repository

   ```
   git clone https://git.gfz-potsdam.de/rizac/gmgt.git
   cd gmgt
   ```

2. If you already have your Python virtual environment and setup,
   you can copy the file `gmgt.py` in your Python module, or even its 
   [content](https://git.gfz-potsdam.de/rizac/gmgt/-/blob/main/gmgt.py?ref_type=heads) 
   directly in your code. This is a very "quick and dirty" approach: 
   it's fast, but you need to be sure that all requirements are already
   installed.

2. Otherwise, you can create a new fresh virtual env (it can be done
   inside the `gmgt` cloned directory for instance):
   ```
   python3 -m venv .env       # create a venv. Please use Ptyhon 3.11+
   source .env/bin/activate   # Linux/macOS
   # .\env\Scripts\activate  # Windows PowerShell
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
[Python notebook](https://git.gfz-potsdam.de/rizac/gmgt/-/blob/main/gmgt.py?ref_type=heads)
