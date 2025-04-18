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
    print(f"Specified final demands: {final_demands}\n")
    
    result = cutting_stock(raw_length, final_demands)

    print("Result")
    print("------")
    print(f"Raws used: {sum(count for _,count in result)}\n")

    for pattern,count in result:
        # We don't show unused patterns
        if count == 0:
            continue
        
        pattern_without_zero_entries = {final: amount for final,amount in pattern.items() if amount>0}
        print(f"{count} times:\t{pattern_without_zero_entries}")
    
    waste = sum(map(lambda x: x[1] * (100 - sum(f*a for f,a in x[0].items())), result))
    print(f"\nTotal produced waste: {waste}\n")

    for final in final_demands:
        # We don't show finals that aren't overproduced
        produced = sum(count*pattern[final] for pattern,count in result)
        overproduced_amount = produced-final_demands[final]
        if overproduced_amount <= 0:
            continue
        
        print(f"Overproduction of finals of length {final}:\t{overproduced_amount}")
