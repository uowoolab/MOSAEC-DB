## Frequently Asked Questions

<details>
  <summary>Why don't the number of crystal structure files (CIF) match the counts reported in the MOSAEC-DB article?</summary>

Structures which were unchanged during the solvent removal step could not be included publicly due to concerns relating to the Cambridge Structural Database (CSD) licensing agreements.

**This amounted to an approximate total of 45k files being omitted from the public database provided on zenodo.** 

Scripts to regenerate those structures are available to individuals with an active CSD license.

</details>

<details>
  <summary>Why didn't the script to retrieve unchanged structures find all of the REFCODEs outlined in the .gcd files?</summary>

The release version of MOSAEC-DB was constructed using several CSD data updates up to the version 5.4.5 (March 2024).

The crystal structure REFCODEs can change during these CSD data updates, and as a result some REFCODEs reported in MOSAEC-DB may no longer exist in current or future CSD data updates.

**Mismatch of the CSD database versions is the most likely cause of any mismatch**, though future additions to MOSAEC-DB should capture any new or updated REFCODEs included in the CSD.

</details>



