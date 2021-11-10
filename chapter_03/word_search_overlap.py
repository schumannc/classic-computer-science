from typing import NamedTuple, List, Dict, Optional, Set, KeysView
from random import choice, shuffle
from string import ascii_uppercase
from csp import CSP, Constraint
from pprint import pprint

Grid = List[List[str]]


class GridLocation(NamedTuple):
    row: int
    column: int
    letter: str


def generate_grid(rows: int, columns: int) -> Grid:
    # initialize grid with random letters
    return [[choice(ascii_uppercase) for c in range(columns)] for r in range(rows)]


def display_grid(grid: Grid) -> None:
    for row in grid:
        print(" ".join(row))


def generate_domain(word: str, grid: Grid) -> List[List[GridLocation]]:
    domain: List[List[GridLocation]] = []
    height: int = len(grid)
    width: int = len(grid[0])
    length: int = len(word)
    rword: str = word[::-1]
    for row in range(height):
        for col in range(width):
            columns: range = range(col, col + length)
            rows: range = range(row, row + length)
            if col + length <= width:
                # left to right
                domain.append(
                    [GridLocation(row, c, word[i]) for i, c in enumerate(columns)]
                )
                # reversed left to right
                domain.append(
                    [GridLocation(row, c, rword[i]) for i, c in enumerate(columns)]
                )
                # diagonal towards bottom right
                if row + length <= height:
                    domain.append(
                        [
                            GridLocation(r, col + (r - row), word[i])
                            for i, r in enumerate(rows)
                        ]
                    )
                    domain.append(
                        [
                            GridLocation(r, col + (r - row), rword[i])
                            for i, r in enumerate(rows)
                        ]
                    )
            if row + length <= height:
                # top to bottom
                domain.append(
                    [GridLocation(r, col, word[i]) for i, r in enumerate(rows)]
                )
                # reversed top to bottom
                domain.append(
                    [GridLocation(r, col, rword[i]) for i, r in enumerate(rows)]
                )
                # diagonal towards bottom left
                if col - length >= 0:
                    domain.append(
                        [
                            GridLocation(r, col - (r - row), word[i])
                            for i, r in enumerate(rows)
                        ]
                    )
                    domain.append(
                        [
                            GridLocation(r, col - (r - row), rword[i])
                            for i, r in enumerate(rows)
                        ]
                    )
    shuffle(domain)
    return domain


class WordSearchConstraint(Constraint[str, List[GridLocation]]):
    def __init__(self, words: List[str]) -> None:
        super().__init__(words)
        self.words: List[str] = words

    def satisfied(self, assignment: Dict[str, List[GridLocation]]) -> bool:
        for word1, grid1 in assignment.items():
            location1: Set[Tuple(int, int)] = {(r.row, r.column) for r in grid1}
            for word2, grid2 in assignment.items():
                if word1 == word2:
                    continue
                location2: Set[Tuple(int, int)] = {(r.row, r.column) for r in grid2}
                overlap: Set[Tuple(int, int)] = location1.intersection(location2)
                if len(overlap) > 0:
                    letters1 = {g.letter for g in grid1 if (g.row, g.column) in overlap}
                    letters2 = {g.letter for g in grid2 if (g.row, g.column) in overlap}
                    if letters1 != letters2:
                        return False
        return True


if __name__ == "__main__":
    grid: Grid = generate_grid(9, 9)
    words: List[str] = ["MATTHEW", "JOE", "MARY", "SARAH", "SALLY", "JORGE", "MILLY"]
    locations: Dict[str, List[List[GridLocation]]] = {}
    for word in words:
        locations[word] = generate_domain(word, grid)
    csp: CSP[str, List[GridLocation]] = CSP(words, locations)
    csp.add_constraint(WordSearchConstraint(words))
    solution: Optional[Dict[str, List[GridLocation]]] = csp.backtracking_search()
    if solution is None:
        print("No solution found!")
    else:
        for grid_locations in solution.values():
            for loc in grid_locations:
                grid[loc.row][loc.column] = loc.letter
    pprint(solution)
    display_grid(grid)
