#  MOSAEC Database (v1.0.0-release)

[![Zenodo](https://flat.badgen.net/static/Zenodo/10.5281%2Fzenodo.14025238/red/)](https://doi.org/10.5281/zenodo.14025238)
[![Preprint](https://flat.badgen.net/static/Preprint/10.26434%2Fchemrxiv-2024-zmq13/nblue/)](https://doi.org/10.26434/chemrxiv-2024-zmq13)
[![Article](https://flat.badgen.net/static/Article/10.1039%2Fd4sc07438f/nblue/)](https://doi.org/10.1039/d4sc07438f)
![Python](https://flat.badgen.net/static/Python/3.9%20|%203.11/green/)
[![Formatter](https://flat.badgen.net/static/Code%20Format/black/black)](https://black.readthedocs.io/en/stable/)

<p align="center">
    <img src="./misc/logo.png" alt="mosaecdb" width="500">
</p>

MOSAEC-DB is a database of metal-organic framework (MOF) and coordination polymer crystallographic information files (.cif) processed for atomistic simulations. 

This repository collects the software applied during database construction, validation, and analysis.

Additionally, this repository will provide further information regarding the use of the database and changes to the database: 
- [Frequently Asked Questions](FAQ.md)
- [Updates](CHANGELOG.md)

# Download
The MOSAEC-DB files, including all publicly-available crystal structures, scripts, and supplemental data, can be downloaded from the [zenodo](https://doi.org/10.5281/zenodo.14025238) repository.

# Database Construction

## Structure Retrieval & Symmetry Conversion

Initial crystal structures may be retrieved directly from the Cambridge Structural Database (CSD) through the [ConQuest](https://www.ccdc.cam.ac.uk/solutions/software/conquest/) program or their provided [Python API](https://www.ccdc.cam.ac.uk/solutions/csd-core/components/csd-python-api/).

Retrieved CSD crystal structures were converted to `P1` symmetry using our [CSD-Cleaner](https://github.com/uowoolab/CSD-cleaner) code.

## Solvent Removal

The [SAMOSA](https://github.com/uowoolab/SAMOSA) solvent removal method was utilized in database construction.  A [publication](https://doi.org/10.1021/acs.jcim.4c01897) outlining the details of this method is available. All `*_full` MOSAEC-DB structures were generated with default settings, while `*_partial` structures were generated with the `--keep_bound` option.

## Structure Error Analysis

The results of the [MOSAEC](https://github.com/uowoolab/MOSAEC) error checking algorithm were used to determine whether to include a structure in MOSAEC-DB. A [preprint](https://doi.org/10.26434/chemrxiv-2024-ftsv3) article outlining the details of this method is available, and the GitHub repository will be available to the public shortly (following its publication). Only structures which passed the MOSAEC error flagging routine were included in the final database.

## Structure Validation

Additional tools to check for problematic structures which may not have been caught by the structure error analyses are provided in [structure_validation](structure_validation/). This includes codes to search for overlapping and hypervalent atom sites.

## Duplicate Structure Analysis

Criterion based on pointwise distance distribution (PDD) scores were applied to identify duplicated and/or highly similar crystal structures with shared empirical formulas. The codes used to complete this analysis are provided in [duplicates](duplicates/).

# Descriptor Calculation

## Global Structure Features

Descriptors characterizing the databases' geometric and chemical environments were generated using a number of standard libraries. 

The codes generating the atomic property-weighted radial distribution function ([AP-RDF](https://github.com/uowoolab/MOF-Descriptor-Codes/tree/main/AP-RDFs)) and revised autocorrelation function ([RAC](https://github.com/uowoolab/MOF-Descriptor-Codes/tree/main/RACs)) are identical to those used in the ARC-MOF database.

Geometric properties were generated using the [Zeo++](http://www.zeoplusplus.org/) v0.3.0 software with default settings.

Any code used to generate descriptors which were not previously made available are provided in [descriptors](descriptors/), including the atom-specific persistent homology descriptors included in the zenodo record.

## Partial Atomic Charges

Electrostatic potential-derived partial atomic charges were computed for as many MOSAEC-DB structures as possible using the previously reported [REPEAT](https://doi.org/10.1021/ct9003405) method. The most recent version of this code is available at the following [repository](https://github.com/uowoolab/REPEAT).

Additionally, a broader set of MOSAEC-DB were assigned ML-predicted partial atomic charges using the [MEPO-ML](https://github.com/uowoolab/MEPO-ML) models that we reported in a recent [publication](https://doi.org/10.1038/s41524-024-01413-4).

## Framework Dimensionality

Each crystal structure's dimensionality was calculated using a previously reported [algorithm](https://github.com/ccdc-opensource/science-paper-mofs-2020/tree/main).

## Topology

The [CrystalNets](https://github.com/coudertlab/CrystalNets.jl) package was applied to compute the net topology. A simple julia [script](descriptors/runcrystalnet.jl) was used to characterize MOSAEC-DB crystal structures.

# File Management Utilities

Additional utilities unrelated to the MOSAEC-DB database construction and characterization processes are also provided in the zenodo record to facilitate simple file manipulations. These tools are available in [zenodo](zenodo/) alongside descriptions of their functions below.

## Unchanged Crystal Structure Retrieval

Crystal structures that were unchanged by the database construction protocol due to their lack of solvent are outlined in corresponding text files (.gcd). Access to these structures is subject to the users' CSD license status, however the computation ready structure can be regenerated by applying the provided structure processing codes to the relevant CSD REFCODES. This script makes use of a [CSD-Cleaner](https://github.com/uowoolab/CSD-cleaner) code that depends on the CSD Python API and pymatgen packages.

```
python get_unchanged_mofs.py --remove_disorder
```

Additionally, **experimental** functionality to regenerate the structure files containing partial atomic charges (REPEAT/MEPO-ML) is provided in these scripts. Consistency of these functions is subject to change with various versions of pymatgen and the CSD Python API, thus we cannot guarantee accuracy to the original, computed partial atomic charges. Testing was performed using Python 3.9.x, csd-python-api 3.1.0, and pymatgen 2024.5.31.

```
python get_unchanged_mofs.py --remove_disorder --write_repeat --write_mepoml
```

## Subset Preparation

Subsets of MOSAEC-DB are arranged according to common conventions of porosity in prior databases, as well as a diverse sampling of several chemical and geometric descriptors. Sampling was achieved using [farthest point sampling](https://github.com/uowoolab/MOF-Diversity-Analysis/blob/main/farthest_point_sampling.py) of the desired descriptor vector.

```
python get_subset.py ../subsets/______.txt
```

## Updates
Information regarding future updates and additions to the database will be outlined in the [zenodo](https://doi.org/10.5281/zenodo.14025238) record.

## Licensing
The [CC BY 4.0 license](https://creativecommons.org/licenses/by/4.0/) applies to the utilization of the MOSAEC database. Follow the license guidelines regarding the use, sharing, adaptation, and attribution of this data.

## Citation
Details relating to the appropriate citation will be updated at the time of publication in the README and zenodo record. A [preprint](https://doi.org/10.26434/chemrxiv-2024-zmq13) version of the article is available on ChemRxiv. Please contact the authors listed in the Contact section if you are unsure how to refer to this work in any publication.

## Contact
Reach out to any of the following authors with any questions:

Marco Gibaldi: marco.gibaldi@uottawa.ca

Tom Woo: tom.woo@uottawa.ca

