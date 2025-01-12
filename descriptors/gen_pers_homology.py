#!/usr/bin/env python3
import os
import glob
import time
import argparse

import numpy as np
import pandas as pd

from multiprocessing import Pool
from subprocess import PIPE, Popen
from pymatgen.core import Structure
from mofdscribe.featurizers.topology import AtomCenteredPH


def run_bash(cmd):
    p = Popen([cmd], shell=True, stdout=PIPE, stderr=PIPE)
    out, err = p.communicate()
    return out.decode("utf-8").strip().split()


dest_path = f"{args.search_path}/homology_vectors"
run_bash(f"mkdir -p {dest_path}")


def gen_descriptors(file):
    stime = time.time()
    try:
        # read into pymatgen.Structure
        struct = Structure.from_file(file)
        # select mofdscribe featurizers
        new_types = (
            "H",
            "C",
            "N-P",
            "O-S-Se",
            "F-Cl-Br-I",
            "Li-Be-Na-Mg-K-Ca-Rb-Sr-Cs-Ba-Fr-Ra",
            "Al-Si-Ga-Ge-As-In-Sn-Sb-Te-Tl-Pb-Bi-Po-At",
            "Sc-Ti-V-Cr-Mn-Fe-Co-Ni-Cu-Zn-Y-Zr-Nb-Mo-Tc-Ru-Rh-"
            "Pd-Ag-Cd-Hf-Ta-W-Re-Os-Ir-Pt-Au-Hg",
            "La-Ce-Pr-Nd-Pm-Sm-Eu-Gd-Tb-Dy-Ho-Er-Tm-Yb-Lu-Ac-"
            "Th-Pa-U-Np-Pu-Am-Cm-Bk-Cf-Es-Fm-Md-No-Lr",
        )
        new_dimens = (0, 1, 2)
        featurizer = AtomCenteredPH(atom_types=new_types, dimensions=new_dimens)
        # calculate features
        feats = featurizer.featurize(struct)
        labels = featurizer.feature_labels()
        # output features
        bname = os.path.basename(file).replace(".cif", "")
        np.save(f"{dest_path}/{bname}.npy", feats)
        elapsedtime = time.time() - stime
        print(file, elapsedtime, "s")
    except Exception as e:
        print(f"{file} >> FEATURE CALCULATION Failed {e}\n")
        return None
    else:
        row = {"cif": [bname]}
        row.update({f"{label}": feats[i] for i, label in enumerate(labels)})
        return pd.DataFrame(row)


if __name__ == "__main__":
    code_desc = "Calculate Atom-specific Persistent Homology features as implemented in mofdscribe."
    parser = argparse.ArgumentParser(description=code_desc)
    parser.add_argument(
        "search_path", help="path where the structure files (cif) are located."
    )
    parser.add_argument("num_cpus", help="no. cpus available for multiprocessing.")
    args = parser.parse_args()
    #
    files = glob.glob(f"{args.search_path}/*.cif", recursive=False)
    pool = Pool(processes=int(args.num_cpus))
    df_path = f"{dest_path}/homology.csv"
    for results in pool.imap_unordered(gen_descriptors, files):
        if results is not None:
            if os.path.exists(df_path):
                results.to_csv(df_path, mode="a", header=False, index=False)
            else:
                results.to_csv(df_path, index=False)
