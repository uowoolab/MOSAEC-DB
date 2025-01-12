# Structure Duplication Analysis using Pointwise Distance Distributions
Identification of duplicated crystal structure based on similarity of their pointwise distance distribution (PDD) scores.

# Workflow
Warning: Scripts contain relative paths that will require editing to work on each system.

1. Normalize the crystal structure file (cif) formats using your preferred method (e.g., pymatgen, critic23, etc.)
2. Run group_by_chemel.sh to create *.lst files by each empirical formula that contains the filenames possessing the same empirical formula.
3. Run pdd_matrix_elform.sh to run pairwise PDD comparisons for all *.lst files -- writes separate *_pdd.pyout & *_pdd.csv for each empirical formula.
4. Combine PDD results from *_pdd.pyout files e.g., `cat *_pdd.pyout | sed 's/ /.cif,/g' | awk '{print$1,$2,$3}' > pdd_scores.txt`
5. Use analyze_pdd_csv.py on the pdd_scores.txt to identify duplicate crystal structures based on a defined PDD score threshold (default:)

# Output
A summary of the duplicate structures is stored as a csv file (default: **duplicate_pdd.csv**).

Description of Columns:
| Column Header | Description |
| -------------- | -------------- |
| `cif` | structure filename |
| `unique` | whether the structure was identified as unique (True/False) |
| `no_duplicates` | number of structure duplicates identified within PDD threshold |
| `duplicate_ids` | structure filenames of those identified as duplicates |