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
ll $HOME/.ssh/
total 32
drwxr-x---+ 31 user  staff  992 Jan 20 17:44 ..
-rw-r--r--   1 user  staff   94 Jan 19 16:02 id_ed25519.pub
drwx------   6 user  staff  192 Jan 19 16:02 .
-rw-------   1 user  staff  399 Jan 19 16:02 id_ed25519
-rw-------   1 user  staff  730 Jan 19 15:59 known_hosts
-rw-r--r--   1 user  staff   85 Jan  8 13:57 known_hosts.old
```

Take the file ``d_ed25519.pub` 
(**important**: the file with **.pub** extension, **do not share with anybody the same file without extension**) 
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

- ngawest2.hdf
- esm.hdf
- kiknet_knet.hdf

where each `hdf` file denotes a gmgt dataset, composed of 
time histories (acceleromenters in m/sˆ2) and relatvie metadata.

<!-- Within each hdf file, time histories are stored as array of floats, 
whereas metadata in tabular structures. -->


## Accessing the fils in your code

A Python Notebook is available in this repository to 
illustrate how to access the time histories and the matadata

The notebook is given for illustrative purposes
Please refer to the Notebook. Remember that for 

