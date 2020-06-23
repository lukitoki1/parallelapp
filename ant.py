from typing import List

import numpy as np


class Ant:
    def __init__(self, x, y, direction, width: int, height: int):
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.direction = direction

    def evolve(self, cell_type: bool) -> bool:
        self.change_direction(cell_type)
        self.move()
        return not cell_type

    def apply_coord_bounds(self, coord: int, bounds: List[int]) -> int:
        lower_bound, upper_bound = bounds
        if coord < lower_bound:
            coord = upper_bound
        elif coord > upper_bound:
            coord = lower_bound
        return coord

    def move(self):
        move = {
            "NORTH": [-1, 0],
            "EAST": [0, 1],
            "SOUTH": [1, 0],
            "WEST": [0, -1]
        }[self.direction]

        self.y = self.apply_coord_bounds(self.y + move[0], [0, self.height - 1])
        self.x = self.apply_coord_bounds(self.x + move[1], [0, self.width - 1])

    def change_direction(self, cell_type):
        if cell_type:
            self.direction = {
                "NORTH": "EAST",
                "EAST": "SOUTH",
                "SOUTH": "WEST",
                "WEST": "NORTH",
            }[self.direction]
        else:
            self.direction = {
                "NORTH": "WEST",
                "EAST": "NORTH",
                "SOUTH": "EAST",
                "WEST": "SOUTH",
            }[self.direction]

    def get_coords(self) -> np.array:
        return np.array([self.x, self.y])
