# IBEX
<a href="https://github.com/johnzech/bento-box"><img src="ibex-logo.svg" alt="ibex" width="50%" /></a>

Project Ibex: RNA sequence matching to save the world (we hope)

<a href="https://www.buymeacoffee.com/humanitydriven"><img src="https://img.shields.io/badge/buymeacoffee- -brightgreen" alt="code-size"/></a><img src="https://img.shields.io/github/languages/code-size/johnzech/ibex" alt="code-size"/><a href="LICENSE"><img src="https://img.shields.io/github/license/johnzech/ibex.svg" alt="license" /></a>

## Table of Contents

* [Prerequisites](#prerequisites)
* [Getting Started](#getting-started)
* [Install Methods](#intall-methods)
   * [Installing w/ Vagrant](#installing-w/-vagrant)
   * [Installing on other vm/hardware](#installing-on-other-vm/hardware)
* [Usage](#usage)
   * [Build the sequence db](#build-the-sequence-db)
   * [Analyze Matches](#analyze-matches)
   * [Getting Result Sets](#getting-result-sets)
* [Architecture](#architecture)
* [License](#license)

## Prerequisites
* make sure you have a GB or two to spare on your drive
* get your hands on a file called all_sequences.txt and place it in data/source_data/human/
  * use this: curl -O https://rna-sequences.s3-us-west-1.amazonaws.com/all_sequences.txt
  * fyi, all_sequences.txt was generated using this data set: https://www.ncbi.nlm.nih.gov/nuccore/?term=(srcdb_refseq[prop]+AND+biomol_rna[prop])+AND+%22Homo+sapiens%22[Primary+Organism]

## Getting Started
These are the high level instructions for getting started. Refer to the more detailed steps below to actually get started.
1. Choose your install target.
   * Vagrant box (useful for local test environments)
   * Any other VM, bare metal hardward, etc
2. Install/configure machine
3. Build the sequence database
4. Analyze matches
5. Produce result set

## Install Methods
Choose one of these based on your use case.

### Installing w/ Vagrant
Note: these instructions assume that you've set up Vagrant and a virtualization solution (i.e. Virtualbox) on your computer. For more on this, check here: https://www.vagrantup.com/docs/installation
1. Review the Vagrantfile located in ./dev_env/
    * Update as needed (especially port forwarding if you've got various other vms running)
2. Navigate to `./dev_env/` in a terminal
3. run: 
```sh
vagrant up
```

### Installing on other vm/hardware
1. Set up a computer/vm with CentOS 8 (minimal install)
2. Place project files in `/var/ibex/` (or clone the repo there)
3. Navigate to `/var/ibex/dev_env/` and run the following:
```sh
   ./packages.sh
   ./dev_env.sh
   ./postgres.sh
   ./schema.sh
```
## Usage
Processing data with Ibex is done in 3 stages:
1. loading sequences into the db
2. analyzing sequence matches
3. generating result sets based on those matches

Note: all commands listed below should be run from the ibex root dir (`/var/ibex`)

### Build the sequence db
This process will insert all sequences found in the text file. The end result should be a row for each sequence in the `ibex.sequence` table. 

Building the sequence table usually takes 1-2 hours.
Important: double check that the `all_sequences.txt` file is in `/var/ibex/data/source_data/human/` (from prereqs above)
```sh
python3 build_sequence_db.py
```


### Analyze Matches
For each sequence saved in the db, determine which substrings match with substrings of the viral genome. 

This stage will insert rows into the `ibex.matches` table.

This is by far the most time consuming stage. With most hardware profiles, it will take several days to complete the analyze stage for all sequences.

Running this as a background proc with a nohup is recommended. The second command below can be started and left to run on the machine (as long as it's not powered down). Output will be saved to `analyze.out`.

To run directly on command line:
```sh
python3 analyze.py
```
To run in background (with nohup):
```sh
nohup python3 analyze.py > analyze.out &
```


### Getting Result Sets
A result set is a set of viral genome substrings that had no overlapping/matching human substrings, thus making them potentially viable attack surfaces. 

Pass a sequence size into the result set script to limit to result strings that are at least x in length. HINT: if you've analyzed all of the matches, this will likely need to be 14 or greater to yeild any results.

This command should complete relatively quickly.

```sh
python3 get_result_set.py 14
```



## Architecture

The following bash output is the directory structure and organization of ibex:

```sh
tree
```

```sh
.
├── analyze.py
├── build_sequence_db.py
├── data
│   ├── db
│   │   └── placeholder.txt
│   └── source_data
│       ├── human
│       │   ├── big_ones.txt
│       │   ├── format_example.txt
│       │   └── headers.txt
│       └── sars_cov2
│           └── MN988668.1
├── dev_env
│   ├── create_database.sql
│   ├── dev_env.sh
│   ├── generate_putty_key.bat
│   ├── ibex_schema.sql
│   ├── packages.sh
│   ├── postgres.sh
│   ├── schema.sh
│   └── Vagrantfile
├── get_result_set.py
├── ibex-logo.svg
├── __init__.py
├── LICENSE
├── paths.py
├── README.md
├── result_set.py
├── scraper
│   └── rna_scraper.py
├── sequence_db
│   ├── init_db.py
│   ├── sequence_db_postgres.py
│   └── sequence_db.py
├── sequence_parser
│   ├── __init__.py
│   └── parser.py
├── substring
│   ├── __init__.py
│   └── substring_toolkit.py
└── validate.py

10 directories, 31 files
```


## License
[LGPLv2.1](LICENSE) © John Zechlin
