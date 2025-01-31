## Frequently Asked Questions
- [Crystal structure (CIF) count doesn't match the publication?](#crystal-structure-cif-count-doesnt-match-the-publication)
- [Failed to find REFCODEs when retrieving unchanged structure?](#failed-to-find-refcodes-when-retrieving-unchanged-structures)
- [Structure XX missing descriptors?](#structure-xx-missing-descriptors)
- [Found a suspected erroneous crystal structure?](#found-a-suspected-erroneous-crystal-structure)

## Crystal structure (CIF) count doesn't match the publication?

Structures which were unchanged during the solvent removal step could not be included publicly due to concerns relating to the Cambridge Structural Database (CSD) licensing agreements.

**This amounted to an approximate total of 45k files being omitted from the public database provided on zenodo.** 

Scripts to regenerate those structures are available to individuals with an active CSD license.

## Failed to find REFCODEs when retrieving unchanged structures?

The release version of MOSAEC-DB was constructed using several CSD data updates up to the version 5.4.5 (March 2024).

The crystal structure REFCODEs can change during these CSD data updates, and as a result some REFCODEs reported in MOSAEC-DB may no longer exist in current or future CSD data updates.

**Mismatch of the CSD database versions is the most likely cause of any mismatch**, though future additions to MOSAEC-DB should capture any new or updated REFCODEs included in the CSD.

## Structure XX missing descriptors?

Any structures missing from the provided descriptors (e.g. RAC, RDF, etc.) csv files **failed during the calculation process**. The same principle applies to any of the data in the primary csv file (i.e. topology, dimensionality, etc.), and the partial atomic charge (REPEAT) structure files.

Future MOSAEC-DB updates may address these missing values with newer version of the descriptor calculation codes/packages. 

## Found a suspected erroneous crystal structure?

Though the MOSAEC-DB construction protocol eliminated a majority of the structure errors, we expect that erroneous structures will remain due to practical limitations in the employed structure validation approach. The MOSAEC algorithm was estimated to be **ca. 95% accurate in flagging erroneous structures and ca. 85% accurate in flagging error-free structures** during manual validation.

Feel free to contact the [authors](README.md#contact) with any structure error inquiries so that we may address them in future database versions. 

##

