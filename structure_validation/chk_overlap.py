#!/usr/bin/env python3
import argparse

from pymatgen.io.cif import CifParser

# Covalent radii revisited -- DOI:10.1039/B801115J
COVALENT_RADII = {
    "H": 0.31,
    "He": 0.28,
    "Li": 1.28,
    "Be": 0.96,
    "B": 0.84,
    "C": 0.76,  # for sp3; sp2 = 0.73; sp = 0.69
    "C_1": 0.69,
    "C_2": 0.73,
    "C_R": 0.73,
    "C_3": 0.76,
    "N": 0.71,
    "O": 0.66,
    "F": 0.57,
    "Ne": 0.58,
    "Na": 1.66,
    "Mg": 1.41,
    "Al": 1.21,
    "Si": 1.11,
    "P": 1.07,
    "S": 1.05,
    "Cl": 1.02,
    "Ar": 1.06,
    "K": 2.03,
    "Ca": 1.76,
    "Sc": 1.7,
    "Ti": 1.6,
    "V": 1.53,
    "Cr": 1.39,
    "Mn": 1.61,  # low spin = 1.39
    "Fe": 1.52,  # low spin = 1.32
    "Co": 1.5,  # low spin = 1.26
    "Ni": 1.24,
    "Cu": 1.32,
    "Zn": 1.22,
    "Ga": 1.22,
    "Ge": 1.2,
    "As": 1.19,
    "Se": 1.2,
    "Br": 1.2,
    "Kr": 1.16,
    "Rb": 2.2,
    "Sr": 1.95,
    "Y": 1.9,
    "Zr": 1.75,
    "Nb": 1.64,
    "Mo": 1.54,
    "Tc": 1.47,
    "Ru": 1.46,
    "Rh": 1.42,
    "Pd": 1.39,
    "Ag": 1.45,
    "Cd": 1.44,
    "In": 1.42,
    "Sn": 1.39,
    "Sb": 1.39,
    "Te": 1.38,
    "I": 1.39,
    "Xe": 1.4,
    "Cs": 2.44,
    "Ba": 2.15,
    "La": 2.07,
    "Ce": 2.04,
    "Pr": 2.03,
    "Nd": 2.01,
    "Pm": 1.99,
    "Sm": 1.98,
    "Eu": 1.98,
    "Gd": 1.96,
    "Tb": 1.94,
    "Dy": 1.92,
    "Ho": 1.92,
    "Er": 1.89,
    "Tm": 1.9,
    "Yb": 1.87,
    "Lu": 1.87,
    "Hf": 1.75,
    "Ta": 1.7,
    "W": 1.62,
    "Re": 1.51,
    "Os": 1.44,
    "Ir": 1.41,
    "Pt": 1.36,
    "Au": 1.36,
    "Hg": 1.32,
    "Tl": 1.45,
    "Pb": 1.46,
    "Bi": 1.48,
    "Po": 1.4,
    "At": 1.5,
    "Rn": 1.5,
    "Fr": 2.6,
    "Ra": 2.21,
    "Ac": 2.15,
    "Th": 2.06,
    "Pa": 2,
    "U": 1.96,
    "Np": 1.9,
    "Pu": 1.87,
    "Am": 1.8,
    "Cm": 1.69,
}


if __name__ == "__main__":
    code_desc = (
        "Check structure for overlapping atomic sites using Cordero Covalent radii."
    )
    parser = argparse.ArgumentParser(description=code_desc)
    parser.add_argument(
        "filename",
        type=str,
        required=True,
        help="path to structure file (cif)",
    )
    args = parser.parse_args()

    try:
        filename = args.filename
        parser = CifParser(filename)
        structure = parser.get_structures(primitive=False)[0]

        num_atoms = len(structure.frac_coords)

        criteria = 0.7
        num_problem = 0
        for i in range(num_atoms - 1):
            for j in range(i + 1, num_atoms):

                distance = structure.get_distance(i, j)
                if distance > 3.65:
                    continue
                else:
                    sum_radii = (
                        COVALENT_RADII[str(structure.species[i])]
                        + COVALENT_RADII[str(structure.species[j])]
                    )
                    if distance < criteria * sum_radii:
                        num_problem += 1
    except:
        print("CTEST   %s    Error  %i" % (filename, num_atoms))
        exit(1)
    if num_problem == 0:
        print("CTEST   %s   Good  %i" % (filename, num_atoms))
    elif num_problem > 0:
        print("CTEST   %s   Bad   %i   %i" % (filename, num_atoms, num_problem))
