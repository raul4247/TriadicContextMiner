# Triadic Context Miner

### What is this project?
This is a research project for mining data from triadic contexts.

The code will read a triadic context input and then process its data in the following steps:

1) Read triadic context
2) Flat the context to a dyadic one
3) Mine concepts using data-peeler
4) Find links between concepts using iPred 
4) Compute feature generators 
4) Compute association rules 
4) Save a report of the execution

The project was developed by Raul F. Mansur, oriented by Pedro H. B. Ruas and Mark A. J. Song, all from Pontifícia Universidade Católica de Minas Gerais (PUC MG).

### Requirements:
* [Python 3.x](https://www.python.org/downloads/)
* PIP (Package Installer for Python)
* [Data-Peeler](https://homepages.dcc.ufmg.br/~lcerf/fr/prototypes.html)

### How to use:
1) Build Data-Peeler's code and put the executable file in the root of the project
2) Put input files and output dir on configs.json
3) Run: `pip install -r requirements.txt`
4) Run `python triadic_miner.py`

