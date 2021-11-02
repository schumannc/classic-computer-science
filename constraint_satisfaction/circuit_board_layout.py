from typing import NamedTuple, List, Dict, Optional, Tuple
from random import choice
from string import ascii_uppercase
from csp import CSP, Constraint


Grid = List[List[int]]  # type alias for grids

class GridLocation(NamedTuple):
    row: int
    column: int


class Shape(NamedTuple):
    idx: int
    width: int
    height: int


def generate_grid(rows: int, columns: int) -> Grid:
    # initialize grid with zeros
    return [[0 for c in range(columns)] for r in range(rows)]


def display_grid(grid: Grid) -> None:
    for row in grid:
        print(" ".join([str(r) for r in row]))


def generate_domain(shape: Shape, grid: Grid) -> List[List[GridLocation]]:
    domain: List[List[GridLocation]] = []
    height: int = len(grid)
    width: int = len(grid[0])
    for row in range(height):
        for col in range(width):
            columns: range = range(col, col + shape.width)
            rows: range = range(row, row + shape.height)
            if col + shape.width <= width and row + shape.height <= height:
                domain.append(
                    [GridLocation(r, c) for r in rows for c in columns]
                )
    return domain


class CircuitBoardConstraint(Constraint[str, List[GridLocation]]):
    def __init__(self, shapes: List[Shape]):
        super().__init__(shapes)
        self.shapes: List[Shape] = shapes

    def satisfied(self, assigned: Dict[Shape, List[GridLocation]]):
        # if there are any duplicates grid locations, then there is an overlap
        all_locations = [loc for value in assigned.values() for loc in value]
        return len(set(all_locations)) == len(all_locations)


if __name__ == '__main__':
    grid: Grid = generate_grid(9, 9)
    shapes: List[Shape] = [
        Shape(1, 1, 6),
        Shape(2, 4, 4),
        Shape(3, 3, 3),
        Shape(4, 2, 2),
        Shape(5, 5, 2),
        Shape(6, 3, 3),
    ]
    locations: Dict[Shape, List[List[GridLocation]]] = {}
    for shape in shapes:
        locations[shape] = generate_domain(shape, grid)
    csp: CSP[Shape, List[GridLocation]] = CSP(shapes, locations)
    csp.add_constraint(CircuitBoardConstraint(shapes))
    solution: Optional[Dict[Shape, List[GridLocation]]] = csp.backtracking_search()
    if solution is None:
        print("No solution found!")
    else:
        for shape, grid_locations in solution.items():
            for location in grid_locations:
                grid[location.row][location.column] = shape.idx
    
    display_grid(grid)