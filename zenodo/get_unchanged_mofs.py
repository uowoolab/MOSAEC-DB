#!/usr/bin/env python3
import os
import shutil
import argparse

from ccdc import io
from ccdc.io import EntryReader

from clean_csd_mofs import clean_structure
from write_pac_cif import assign_partial_atomic_charge

CODE_PATH = os.path.dirname(os.path.realpath(__file__))


# text editing to remove disordered/partially occupied sites
def filter_disorder(cif):
    filtered_lines = []
    if isinstance(cif, str):
        lines = cif.split("\n")
    else:
        with open(cif, "r") as rf:
            lines = rf.read().split("\n")

    for line in lines:
        try:
            spl = line.split()
            if (spl[0][-1] != "*") and (spl[0][-1] != "?"):
                filtered_lines.append(line)
        except IndexError as ie:
            filtered_lines.append(line)
            continue
        except Exception as e:
            print(cif, " | error removing disordered sites")
            print(e)
        else:
            continue
    return "\n".join(filtered_lines)


# get cifs from csd
def print_cifs(gcd_file, write_path, rm_disordered_sites):
    with open(gcd_file, "r") as rf:
        refcode_list = [_ for _ in rf.read().split("\n") if _ != ""]

    reader = EntryReader("CSD")
    for refcode in refcode_list:
        try:
            entry = reader.entry(refcode)
            mol = entry.disordered_molecule
            cif_str = mol.to_string("cif")
            if rm_disordered_sites:
                cif_str = filter_disorder(cif_str)
            cif_path = os.path.join(write_path, f"{entry.identifier}.cif")
            with open(cif_path, "w") as wf:
                wf.write(cif_str)
        except Exception as e:
            print(refcode, " | failed to print cif")
            continue
    return refcode_list


# convert cifs to P1 symmetry
def convert2P1(refs, out_dir, rename=None):
    for ref in refs:
        try:
            clean_structure(
                f"{out_dir}/{ref}_P1.cif",
                read_path=f"tmp_cifs/{ref}",
                input_is_cif=True,
            )
            if rename:
                p1_name = ref + "_P1.cif"
                mdb_name = p1_name.replace("_P1.cif", rename)
                shutil.move(f"{out_dir}/{p1_name} ", f"{out_dir}/{mdb_name}")
        except Exception as e:
            print(ref, " | failed to convert2P1 cif")
            print(e)
            continue
    return 0


if __name__ == "__main__":
    code_desc = "Retrieve MOSAEC-DB cifs for refcodes which were unchanged."
    parser = argparse.ArgumentParser(description=code_desc)
    # full > os.path.join(CODE_PATH, "../database/full/unchanged_refcodes_full.gcd")
    # partial > os.path.join(CODE_PATH, "../database/partial/unchanged_refcodes_partial.gcd")
    parser.add_argument(
        "--gcd_files",
        nargs="+",
        default=[
            os.path.join(CODE_PATH, "../database/full/unchanged_refcodes_full.gcd"),
            os.path.join(
                CODE_PATH, "../database/partial/unchanged_refcodes_partial.gcd"
            ),
        ],
        help="path(s) to .gcd file with desired refcodes.",
    )
    parser.add_argument(
        "--remove_disorder",
        action="store_true",
        help="whether to remove disordered atom sites via simple text editing",
    )
    parser.add_argument(
        "--write_repeat",
        action="store_true",
        help="whether to also write files containing REPEAT charges.",
    )
    parser.add_argument(
        "--write_mepoml",
        action="store_true",
        help="whether to also write files containing MEPOML charges.",
    )
    args = parser.parse_args()

    print("Writing MOSAEC-DB cifs ...\n")
    for gcd in args.gcd_files:
        # print tmp cifs
        cif_dir = "tmp_cifs"
        os.makedirs(cif_dir, exist_ok=True)
        refs = print_cifs(gcd, cif_dir, args.remove_disorder)

        # convert cifs to P1 & rename
        p1_dir = "MOSAEC-DB_unchanged"
        os.makedirs(p1_dir, exist_ok=True)
        os.makedirs("./tmp", exist_ok=True)
        f_end = "_full.cif" if "full" in gcd else "_partial.cif"
        convert2P1(refs, p1_dir, rename=f_end)

        shutil.rmtree(cif_dir)
        shutil.rmtree("./tmp")

    if args.write_repeat:
        print("\nWriting MOSAEC-DB REPEAT cifs ...\n")
        repeat_dir = "MOSAEC-DB_unchanged_REPEAT"
        os.makedirs(repeat_dir, exist_ok=True)
        rpt_json = os.path.join(CODE_PATH, "../database_REPEAT/unchanged_repeat.json")
        assign_partial_atomic_charge(p1_dir, rpt_json, repeat_dir, pac_type="REPEAT")

    if args.write_mepoml:
        print("\nWriting MOSAEC-DB MEPO-ML cifs ...\n")
        mepoml_dir = "MOSAEC-DB_unchanged_MEPOML"
        os.makedirs(mepoml_dir, exist_ok=True)
        mpml_json = os.path.join(CODE_PATH, "../database_MEPOML/unchanged_mepoml.json")
        assign_partial_atomic_charge(p1_dir, mpml_json, mepoml_dir, pac_type="MEPOML")
