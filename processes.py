import multiprocessing as mp
from typing import List

import numpy as np
from PIL import Image

from ant import Ant
from utils import scale_indexes_to_range


def create_ant(ant_args: dict, board_size: List[str]):
    return Ant(ant_args['x'], ant_args['y'], ant_args['direction'], board_size[0], board_size[1])


def create_generation(ant: Ant, board: np.ndarray):
    print("creating generation")

    coords = ant.get_coords()
    board_value = board[coords[1], coords[0]]
    cell_type = ant.evolve(board_value)

    return {"ant": ant, "new_value": cell_type, "coords": coords}


def create_image(queue: mp.Queue, magnification: int, n_generations: int, n_calculated: mp.Value):
    while True:
        data = queue.get()
        matrix: np.ndarray = data["board"]
        ants = data["ants"]
        n_gen = data["i"]

        print(f"creating {n_gen} image")

        image = np.zeros((matrix.shape[1] * magnification, matrix.shape[0] * magnification, 3))

        for y, x in np.ndindex(matrix.shape):
            color = [255, 255, 255]
            x_lower, x_upper, y_lower, y_upper = scale_indexes_to_range(x, y, magnification)
            if matrix[y, x]:
                color = [0, 0, 0]

            image[y_lower:y_upper, x_lower:x_upper, :] = color

        for ant in ants:
            color = [255, 0, 0]
            x_lower, x_upper, y_lower, y_upper = scale_indexes_to_range(ant[0], ant[1], magnification)
            image[y_lower:y_upper, x_lower:x_upper, :] = color

        im = Image.fromarray(image.astype('uint8'))
        im.save(f'results/gen{n_gen}.png', 'PNG')

        with n_calculated.get_lock():
            n_calculated.value += 1
