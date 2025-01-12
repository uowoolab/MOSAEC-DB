#!/usr/bin/env python3
import os
import shutil
import argparse

CODE_PATH = os.path.dirname(os.path.realpath(__file__))
print(CODE_PATH)
DB_PATH = CODE_PATH.replace("scripts", "")
print(DB_PATH)


def subset(txt_file, dest_dir):
    # define cif paths
    if "-neutral-" in dest_dir:
        fpath = os.path.join(DB_PATH, "database/full/neutral")
        ppath = os.path.join(DB_PATH, "database/partial/neutral")
    else:
        fpath = os.path.join(DB_PATH, "database/full/charged")
        ppath = os.path.join(DB_PATH, "database/partial/charged")

    with open(txt_file, "r") as rf:
        cifs = rf.read().split("\n")

    # separate cifs by origin directory
    fcifs = [os.path.join(fpath, x) for x in cifs if "_full" in x]
    pcifs = [os.path.join(ppath, x) for x in cifs if "_partial" in x]

    # move files
    print(f"Copying {len(fcifs + pcifs)} .cif files ... ")
    for cif in fcifs + pcifs:
        shutil.copy(cif, dest_dir)
    return 0


if __name__ == "__main__":
    code_desc = "Retrieve MOSAEC-DB cifs from a specific subset (.txt)."
    parser = argparse.ArgumentParser(description=code_desc)
    parser.add_argument(
        "subset",
        type=str,
        help="path to .txt file with MOSAEC-DB cif names.",
    )
    args = parser.parse_args()
    # create subset dir
    subset_dir = os.path.basename(args.subset)[:-4]
    print("Making subset directory ... ", subset_dir)
    os.makedirs(subset_dir, exist_ok=True)
    # find & move files
    subset(args.subset, subset_dir)
