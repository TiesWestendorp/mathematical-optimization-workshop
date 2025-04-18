from scipy import optimizefrom collections.abc import Iterator
from itertools import product

if __name__ == "__main__":
    main()

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

# TODO: allow input arguments
def main() -> None:
    raw_length = # TODO: read from file
    final_demands = # TODO: read from file
    possible_patterns = list(patterns(finals, raw_length))
    # TODO: Optimize!