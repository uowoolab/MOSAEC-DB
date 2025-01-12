#!/usr/bin/env python3
import re
import argparse
import warnings


from pymatgen.core import Structure

from pymatgen.analysis.graphs import StructureGraph

# from pymatgen.analysis.graphs import MoleculeGraph
import pymatgen.analysis.local_env as env

from pymatgen.io.babel import BabelMolAdaptor

# from pymatgen.io.cif import CifWriter

import openbabel
from openbabel import pybel as pb


def read_cif(file_path):
    return Structure.from_file(file_path, sort=False)


def get_metal_indices(struct_):
    """This function returns metal site indices from a pymatgen Structure object"""
    metal_indices = []

    for i, site in enumerate(struct_.sites):
        if site.species.contains_element_type("metal"):
            metal_indices.append(i)

    return metal_indices


def get_graph(struct_):
    return StructureGraph.with_local_env_strategy(struct_, env.IsayevNN())


def get_smiles(mol):
    """This function returns a SMILES string from a pymatgen molecular graph"""
    babel_mol = BabelMolAdaptor(mol)
    pybel_mol = pb.Molecule(babel_mol.openbabel_mol)
    return pybel_mol.write("can").split()[0]


def get_subgraphs(graph_):
    smiles_list = []
    subgraphs = graph_.get_subgraphs_as_molecules(use_weights=False)
    for mol in subgraphs:
        if len(mol.sites) > 0:
            smiles = get_smiles(mol)
            smiles_list.append(smiles)

    return smiles_list


def check_atoms(graph_, struct_):
    graph_dict = graph_.as_dict()
    atom_dict = {}
    connection_dict = {}
    bad_atom_list = []
    counter = 0
    counter_2 = 2

    for atom in struct_:

        atom_id = "{}{}".format(atom.specie, 1)

        while atom_id in atom_dict.values():
            atom_id = "{}{}".format(atom.specie, counter_2)
            counter_2 += 1

        atom_dict["{}".format(counter)] = atom_id

        counter += 1
        counter_2 = 2

    for atom, connections in zip(
        graph_dict["graphs"]["nodes"], graph_dict["graphs"]["adjacency"]
    ):
        for connection in connections:
            atom1 = atom_dict["{}".format(atom["id"])]
            atom2 = atom_dict["{}".format(connection["id"])]
            bond_length = round(struct_.get_distance(atom["id"], connection["id"]), 4)
            if atom1 not in connection_dict.keys():
                connection_dict[atom1] = [atom2]
                if atom2 not in connection_dict.keys():
                    connection_dict[atom2] = [atom1]
                else:
                    connection_dict[atom2].append(atom1)
            else:
                connection_dict[atom1].append(atom2)
                if atom2 not in connection_dict.keys():
                    connection_dict[atom2] = [atom1]
                else:
                    connection_dict[atom2].append(atom1)
    for atom in connection_dict.keys():
        if re.sub(r"\d+", "", atom) == "H" and len(connection_dict[atom]) > 1:
            print("BAD ATOM: {}".format(atom))
            bad_atom_list.append(atom)
        elif re.sub(r"\d+", "", atom) == "C" and len(connection_dict[atom]) > 4:
            print("BAD ATOM: {}".format(atom))
            bad_atom_list.append(atom)
        elif re.sub(r"\d+", "", atom) == "O" and len(connection_dict[atom]) > 2:
            print("BAD ATOM: {}".format(atom))
            bad_atom_list.append(atom)
        elif (
            re.sub(r"\d+", "", atom) in ["F", "Cl", "Br", "I"]
            and len(connection_dict[atom]) > 1
        ):
            print("BAD ATOM: {}".format(atom))
            bad_atom_list.append(atom)
    return bad_atom_list


def main(filename):

    struct = read_cif(filename)
    # atom_dict = struct.as_dict()
    metals = get_metal_indices(struct)
    graph = get_graph(struct)
    graph.remove_nodes(indices=metals)

    bad_atoms = check_atoms(graph, struct)

    if len(bad_atoms) > 0:
        print(f" {filename} | BAD STRUCTURE")
    elif len(bad_atoms) == 0:
        print(f" {filename} | GOOD STRUCTURE")


if __name__ == "__main__":
    code_desc = "Checks structure for hypervalent H, C, O, and halogens atomic sites."
    parser = argparse.ArgumentParser(description=code_desc)
    parser.add_argument(
        "filename",
        type=str,
        required=True,
        help="path to structure file (cif)",
    )
    args = parser.parse_args()
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        input_cif = args.filename
        main(input_cif)
