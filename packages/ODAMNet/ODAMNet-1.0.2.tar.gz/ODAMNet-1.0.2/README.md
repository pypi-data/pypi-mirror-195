# README

ODAMNet is a Python package to study molecular relationship between environmental factors (called chemicals here) and 
rare diseases. 

The [ODAMNet documentation][ODAMNet documentation] is available in ReadTheDocs.

This tool was created within the framework of the [EJRP-RD project][EJPRD].

## Installation 

### From PyPI

ODAMNet is available as [Python package][pypi]. You can easily install it using `pip`.

```console
$ python3 -m pip install odamnet
```

### From Conda - *It's ongoing*

It is available in [bioconda][bioconda] too.

```console
$ conda install odamnet
```

### From Github

1. Clone the repository from GitHub

```console
$ git clone https://github.com/MOohTus/ODAMNet.git
```

2. Then, install it

```console
$ python3 -m pip install -e ODAMNet/
```

*If it's not working, try to update pip using pip install pip --upgrade*

## Usage

Three different approaches are available: 

- Overlap analysis
- Active Modules Identification (AMI, using [DOMINO][DOMINO])
- Random Walk with Restart (RWR, using [multiXrank][multiXrank])

```console
$ odamnet [overlap|domino|multixrank|networkCreation] [ARGS]
```

## Examples

Three approaches are implemented to study relationships between genes targeted by chemicals (extracted automatically 
from [CTD database][CTD]) and rare diseases (extracted automatically from [WikiPathways][WikiPathways]).

### Overlap analysis

This method computes the overlap between target genes and rare disease pathways. It is looking for direct associations, 
i.e., target genes that are part of rare disease pathways.

Give your chemicals list into `--chemicalsFile` input. 

```console
$ odamnet overlap --chemicalsFile FILENAME
```

### Active Module Identification (AMI)

The Active Module Identification is performed using DOMINO tool. 

DOMINO defines target genes as *active genes* to search for active modules using a biological network 
(e.g. protein-protein interaction network, PPI). Then, an overlap analysis is performed between identified active 
modules and rare disease pathways. 

Give your chemicals list and your biological network into `--chemicalsFile` and `--networkFile` respectively. 

```console
$ odamnet domino --chemicalsFile FILENAME --networkFile FILENAME
```

### Random Walk with Restart (RWR)

The Random Walk with Restart is performed using multiXrank Python package.

#### Network and bipartite creation

MultiXrank need networks as input. You need to create a network with the rare disease pathways. This network will not 
have any connection between disease nodes (i.e. disconnected network). Disease nodes will be only connected with gene 
nodes that are involved in disease pathways using a bipartite.  

Give a path to save generated disease network and disease-gene bipartite using `--networksPath` and `--bipartitePath` 
respectively.

```console
$ odamnet networkCreation --networksPath PATH --bipartitePath PATH
```

*Rare disease pathways are extracted automatically from WikiPathways.*

#### multiXrank

Random Walk with Restart mesures the proximity of every node (e.g. genes and diseases) to the target genes within a 
multilayer network. The multilayer network is composed of molecular multiplex and rare disease pathway network (the one 
created previously). 

Give your chemicals list into `--chemicalsFile` input. 

MultiXrank needs a configuration file (`--configPath`), networks directory (`--networksPath`),
the target genes file (`--seedsFile`) and a name to write the result into network file (`--sifFileName`). 

```console
$ odamnet multixrank --chemicalsFile FILENAME --configPath PATH --networksPath PATH --seedsFile FILENAME --sifFileName FILENAME
```

*We provide a molecular multiplex into the useCases directory in the [GitHub page][git].*

*You can also have more details about the configuration file in the [documentation page][doc].*

[ODAMNet documentation]: https://odamnet.readthedocs.io/
[pypi]: https://pypi.org/project/ODAMNet/
[bioconda]: https://bioconda.github.io/index.html
[EJPRD]: https://www.ejprarediseases.org/
[DOMINO]: http://domino.cs.tau.ac.il
[multiXrank]: https://multixrank-doc.readthedocs.io/en/latest/index.html
[WikiPathways]: https://www.wikipathways.org/
[CTD]: https://ctdbase.org/
[doc]: https://odamnet.readthedocs.io/en/latest/pages/formats/Input.html#configuration-file
[git]: https://github.com/MOohTus/ODAMNet/tree/main/useCases/InputData
