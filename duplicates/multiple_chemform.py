import re
from sys import argv


def parse_formula(formula):
    """Parse a chemical formula into its constituent elements and their counts."""
    elements = re.findall(r"([A-Z][a-z]*)(\d*)", formula)
    return {element: int(count) if count else 1 for element, count in elements}


def find_multiples_of_formula(formula, formulas):
    """Find multiples of a given chemical formula within a list of formulas."""
    parsed_formula = parse_formula(formula)
    multiples = []

    for other_formula in formulas:
        if formula == other_formula:
            continue  # Skip the same formula

        parsed_other_formula = parse_formula(other_formula)

        # Check if both formulas contain the same elements
        if set(parsed_formula.keys()) != set(parsed_other_formula.keys()):
            continue  # Skip if the sets of elements are different

        # Check if all elements in the other formula are multiples of the elements in the original formula
        is_multiple = True
        for element, count in parsed_other_formula.items():
            if count % parsed_formula[element] != 0:
                is_multiple = False
                break  # Not a multiple if ratio is not integer
            if (
                count // parsed_formula[element]
                != parsed_other_formula[list(parsed_other_formula.keys())[0]]
                // parsed_formula[list(parsed_formula.keys())[0]]
            ):
                is_multiple = False
                break  # Not a multiple if ratios between corresponding elements differ

        if is_multiple:
            multiples.append(other_formula)

    return multiples


# Read chemical formulas from a file
def read_chemical_formulas_from_file(filename):
    with open(filename, "r") as file:
        chemical_formulas = [line.strip() for line in file if line.strip()]
    return chemical_formulas


# run
# input file should be tmp.txt from group_by_chemel.sh
filename = argv[1]
chemical_formulas = read_chemical_formulas_from_file(filename)
for formula_to_check in chemical_formulas:
    multiples = find_multiples_of_formula(formula_to_check, chemical_formulas)
    if multiples:
        print(f"Multiples of {formula_to_check}: {multiples}")
