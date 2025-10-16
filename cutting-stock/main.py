from scipy.optimize import linprog
from collections.abc import Iterator
from itertools import product

# Type alias for patterns. Each `(key,value)`-pair indicates how many finals are produced in this pattern. The `key`
# holds the different final lengths, and the `value` how many of those finals are produced.
Pattern = dict[int,int]

def patterns(finals: list[int], raw_length: int) -> Iterator[Pattern]: # TODO: Change to list, rename method
    smallest_final = min(finals)
    maximum_in_raw_per_final = [range(raw_length//final + 1) for final in finals]

    for pattern in product(*maximum_in_raw_per_final):
        zipped = list(zip(finals, pattern)) # zip-objects are iterators, but we want to iterate it twice, so we transform it into a list here
        pattern_length = sum(final * amount for final, amount in zipped)
        waste = raw_length - pattern_length

        # The pattern must not exceed the raw_length, and no final must be cuttable from the waste
        if 0 <= waste < smallest_final:
            yield dict(zipped)

def cutting_stock(raw_length: int, final_demands: dict[int,int]) -> list[tuple[Pattern,int]]:
    finals = list(final_demands.keys()) # TODO: rename + comments
    possible_patterns = list(patterns(finals, raw_length))

    raise NotImplementedError

    # finals = [ 140, 320, 360, 450 ]
    # final_demands = { # TODO: final_to_demands
    #   140: 211,
    #   ...
    # }

    # TODO: add comment about possible_patterns
    # possible_patterns = [
    #   { 140: 1, 320: 0, 360: 1, 450: 1 }, # <- First pattern
    #   { 140: ., 320: ., 360: ., 450: . }, # <- Second pattern
    #   ...
    # ]

    # TODO: Optimize using `linprog`

    # A_ub = []
    # b_ub = []
    # for final in finals:
    #   demand = final_demands[final]
    #   A_ub.append()
    #   b_ub.append()
    
    result = linprog(c, A_ub = A_ub, b_ub = b_ub, integrality = 1)

    return list(zip(possible_patterns, map(int, result.x)))

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

    waste = sum(count * (raw_length - sum(final*amount for final,amount in pattern.items())) for pattern,count in result)
    print(f"\nTotal produced waste: {waste}\n")

    for final in final_demands:
        # We don't show finals that aren't overproduced
        produced = sum(count * pattern[final] for pattern,count in result)
        overproduced_amount = produced-final_demands[final]
        if overproduced_amount <= 0:
            continue
        
        print(f"Overproduction of finals of length {final}:\t{overproduced_amount}")
