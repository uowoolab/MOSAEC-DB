#!/usr/bin/env python3
import os
import glob
import argparse

import pandas as pd


code_desc = "Analyze csv containing all PDD scores calculated for a given database."
parser = argparse.ArgumentParser(description=code_desc)
parser.add_argument(
    "pdd_csv",
    type=str,
    help="path to csv containing all structure pairs' precomputed pdd scores.",
)
parser.add_argument(
    "cif_path",
    type=str,
    help="path to directory containing all the structures to be considered.",
)
parser.add_argument(
    "-output_csv",
    type=str,
    default="duplicate_pdd.csv",
    help="path to csv containing all structure pairs' precomputed pdd scores.",
)
parser.add_argument(
    "-pdd_threshold",
    type=float,
    default=0.15,
    help="path to csv containing all structure pairs' precomputed pdd scores.",
)
args = parser.parse_args()

pdd_threshold = args.pdd_threshold

cpath = args.cif_path
cifs = glob.glob(f"{cpath}/*.cif", recursive=False)
cifs = [os.path.basename(x) for x in cifs if x[-8:] != "_pdd.cif"]
print(f"Total cifs from db to compare ... {len(cifs)}")
duplicates = {x: [] for x in cifs}

# read scores
ignore_lines = ["", "s1,s2,pdd_score"]
with open(args.pdd_csv, "r") as rf:
    dlines = [x for x in rf.read().split("\n") if x not in ignore_lines]

# go over files from duplicate analysis
# s1, s2, pdd_score
print("Total no. PDD scores to compare ... ", len(dlines) - 1)
for line in dlines:
    spl = line.split(",")
    cif1 = spl[0]
    cif2 = spl[1]
    pdd = float(spl[2])
    if pdd < pdd_threshold:
        duplicates[cif1].append(cif2)
        duplicates[cif2].append(cif1)
    else:
        continue


# get duplicate dictionary
unique = []
dupl = []
rows = []
for cif, dupes in duplicates.items():
    dupes = sorted(list(set(dupes)))
    if len(dupes) != 0:
        intersect = list(set(dupes) & set(unique))
        if len(intersect) == 0:
            unique.append(cif)
        else:
            dupl.append(cif)
    else:
        unique.append(cif)

    rows.append(
        {
            "cif": cif,
            "unique": True if cif in unique else False,
            "no_duplicates": len(dupes),
            "duplicate_ids": "/".join(dupes),
        }
    )


print(f"Total unique MOFs ... {len(unique)}")
print(f"Total duplicate MOFs ... {len(dupl)}")

df = pd.DataFrame(rows)
df.to_csv(args.output_csv, index=False)
