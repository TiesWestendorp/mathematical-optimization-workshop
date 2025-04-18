from scipy.optimize import linprog
import numpy as np
from collections.abc import Iterator
from itertools import product

def patterns(finals: list[int], raw_length: int) -> Iterator[dict[int,int]]:
    smallest_final = min(finals)
    maximum_in_raw_per_final = map(lambda final: range(raw_length//final + 1), finals)

    for pattern in product(*maximum_in_raw_per_final):
        zipped = list(zip(finals, pattern)) # zip-objects are iterators, but we want to iterate it twice, so we transform it into a list here
        pattern_length = sum(map(lambda x: x[0] * x[1], zipped))
        waste = raw_length - pattern_length

        # The pattern must not exceed the raw_length, and no final must be cuttable from the waste
        if waste >= 0 and waste <= smallest_final:
            yield dict(zipped)

def cutting_stock(raw_length: int, final_demands: dict[int,int]) -> list[tuple[dict[int,int],int]]:
    finals = final_demands.keys()
    possible_patterns = list(patterns(finals, raw_length))

    raise NotImplementedError # TODO: Optimize using `linprog`

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Cutting stock problem solver")
    parser.add_argument("--file", required=True, help="CSV input file")
    file_name = parser.parse_args().file
 
    raw_length = None
    final_demands = None
    with open(file_name, "r") as file:
        lines = file.readlines()
        raw_length = int(lines[0])
        final_demands = dict(map(lambda line: map(int, line.split(",")), lines[1:]))
    
    print(f"Specified raw length: {raw_length}")
    print(f"Specified final demands: {final_demands}")
    print(f"Result: {cutting_stock(raw_length, final_demands)}")