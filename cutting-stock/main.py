from scipy.optimize import linprog
from collections.abc import Iterator
from itertools import product

# Type alias for patterns. Each `(key,value)`-pair indicates how many finals are produced in this pattern. The `key`
# holds the different final lengths, and the `value` how many of those finals are produced.
Pattern = dict[int,int]

def generate_patterns(finals: list[int], raw_length: int) -> Iterator[Pattern]:
    smallest_final = min(finals)
    maximum_in_raw_per_final = [range(raw_length//final + 1) for final in finals]

    for pattern in product(*maximum_in_raw_per_final):
        zipped = dict(zip(finals, pattern)) # zip-objects are iterators, but we want to iterate it more than once, so we transform it into a dict here

        # The pattern must not exceed the raw_length, and no final must be cuttable from the waste
        if 0 <= waste_for_pattern(raw_length, zipped) < smallest_final:
            yield zipped

def waste_for_pattern(raw_length: int, pattern: Pattern) -> int:
    # The waste is whatever remains of the raw after removing all finals produced by the pattern
    return raw_length - sum(final * count for final,count in pattern.items())

def cutting_stock(raw_length: int, final_to_demands: dict[int,int]) -> list[tuple[Pattern,int]]:
    finals = list(final_to_demands.keys())
    patterns = list(generate_patterns(finals, raw_length))

    # Each entry in `finals` is a length of a final that needs to be produced
    # finals = [ 140, 320, 360, 450 ]

    # Each pair in `final_to_demands` indicates how many of each final needs to be produced
    # final_to_demands = {
    #   140: 211,
    #   320: 395,
    #   360: 610,
    #   450: 97,
    # }

    # Each entry of `patterns` is a dictionary that indicates how many of each final is produced by that pattern
    # patterns = [
    #   { 140: 0, 320: 0, 360: 0, 450: 2 },
    #   { 140: 0, 320: 2, 360: 1, 450: 0 },
    #   { 140: 0, 320: 3, 360: 0, 450: 0 },
    #   { 140: 1, 320: 0, 360: 1, 450: 1 },
    #     ... and 8 more ...
    # ]

    raise NotImplementedError

    # Each decision variable corresponds to a pattern, and indicates how many of that pattern is produced

    objective = [] # TODO:

    inequality_constraints_matrix = []
    inequality_constraints_vector = []
    for final,demand in final_to_demands.items():
       # Each `final` has a constraint: we must produce at least as many as the `demand` specifies
       inequality_constraints_matrix.append([]) # TODO: Build up the constraints matrix row by row for each final
       inequality_constraints_vector.append() # TODO: Build up the constraints vector row by row for each final

    # Optimize using `linprog`
    result = linprog(objective, A_ub = inequality_constraints_matrix, b_ub = inequality_constraints_vector, integrality = 1)

    return list(zip(patterns, map(int, result.x)))

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Cutting stock problem solver")
    parser.add_argument("--file", required=True, help="CSV input file")
    file_name = parser.parse_args().file

    raw_length = None
    final_to_demands = None
    with open(file_name, "r") as file:
        lines = file.readlines()
        raw_length = int(lines[0])
        final_to_demands = dict(map(lambda line: map(int, line.split(",")), lines[1:]))

    print(f"Specified raw length: {raw_length}")
    print(f"Specified final demands: {final_to_demands}\n")

    result = cutting_stock(raw_length, final_to_demands)

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

    for final in final_to_demands:
        # We don't show finals that aren't overproduced
        produced = sum(count * pattern[final] for pattern,count in result)
        overproduced_amount = produced-final_to_demands[final]
        if overproduced_amount <= 0:
            continue
        
        print(f"Overproduction of finals of length {final}:\t{overproduced_amount}")
