from sys import argv
import amd
import pandas as pd

structure_list = argv[1]
struc_base = structure_list.split(".cif")[0]

pdd_df = amd.compare(structure_list, by="PDD", k=100)

col_list = []
for col in pdd_df.columns:
    col_list.append(col)
    for idx in pdd_df.index:
        if col != idx and idx not in col_list:
            print(col, idx, pdd_df.loc[idx, col])


pdd_df.to_csv(f"{struc_base}.csv")
