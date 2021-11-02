from collections import defaultdict
from itertools import permutations
from pprint import pprint
from random import choice, shuffle
from string import ascii_uppercase
from typing import Dict, List, NamedTuple, Optional, Tuple

from csp import CSP, Constraint


def display_grid(grid: Grid) -> None:
    for row in grid:
        print(" ".join([str(r) for r in row]))


class SudokuConstraint(Constraint[int, List[int]]):
    def __init__(self, rows: List[int]) -> None:
        super().__init__(rows)
        self.rows: List[int] = rows

    def satisfied(self, assigned: Dict[int, Tuple[int, ...]]):
        columns: Dict[int, List[int]] = defaultdict(list)
        blocks: Dict[int, List[int]] = defaultdict(list)
        for i in range(len(assigned)):
            for j in range(9):
                columns[j].append(assigned[i][j])
                blocks[j // 3 + i // 3 * 3].append(assigned[i][j])

        for digits in columns.values():
            if len(set(digits)) != len(digits):
                return False

        for digits in blocks.values():
            if len(set(digits)) != len(digits):
                return False

        return True


if __name__ == "__main__":
    rows: List[int] = list(range(9))
    possible_digits: Dict[int, List[permutations]] = {}
    for row in rows:
        digits = list(range(1, 10))
        shuffle(digits)
        possible_digits[row] = permutations(digits)

    csp: CSP[int, Tuple[int, ...]] = CSP(rows, possible_digits)
    csp.add_constraint(SudokuConstraint(rows))
    solution: Optional[Dict[int, Tuple[int, ...]]] = csp.backtracking_search()
    if solution is None:
        print("No solution found!")
    else:
        pprint(solution)
