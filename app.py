import ctypes
import multiprocessing as mp
from datetime import datetime
from itertools import repeat
from typing import List

import numpy as np

from ant import Ant
from arg_parser import Parser
from processes import create_ant, create_generation, create_image


class ParallelApp:
    def __init__(self):
        self.args = Parser()

        self.board: np.ndarray = None
        self.ants: List[Ant] = []

        self.generations = mp.Queue()
        self.images_pool: mp.Pool = None
        self.images_pool_control: mp.Value = None

        self.init_parallel()

    def run_parallel(self):
        self.init_image_creation()
        self.create_generations_parallel()
        self.close_image_creation()

    def init_parallel(self):
        def init_board():
            self.board = np.full((self.args.height, self.args.width), False, dtype=object)
            for cell in self.args.black_cells:
                self.board[cell[1], cell[0]] = True

        def init_ants_parallel():
            with mp.Pool(processes=self.args.n_processors) as pool:
                self.ants = pool.starmap(create_ant, zip(self.args.ants, repeat([self.args.width, self.args.height])))

        init_board()
        init_ants_parallel()

    def init_image_creation(self):
        if not self.images_pool_control:
            self.images_pool_control = mp.Value(ctypes.c_int)
            self.images_pool_control.value = 0

        self.images_pool = mp.Pool(self.args.n_processors, create_image,
                                   (self.generations, self.args.magnification, self.args.n_generations,
                                    self.images_pool_control))

    def create_generations_parallel(self):
        def init_generations():
            self.generations.put(
                {"board": self.board.copy(), "ants": list(map(lambda ant: ant.get_coords(), self.ants)), "i": 0})

        def create_generations():
            with mp.Pool(processes=self.args.n_processors) as pool:
                for i in range(1, self.args.n_generations):
                    data = pool.starmap(create_generation, zip(self.ants, repeat(self.board)))
                    updated_ants = []
                    ant_coords = []

                    for ant_gen in data:
                        coords = ant_gen["coords"]
                        self.board[coords[1], coords[0]] = ant_gen["new_value"]
                        updated_ants.append(ant_gen["ant"])
                        ant_coords.append(ant_gen["ant"].get_coords())

                    self.generations.put({"board": self.board.copy(), "ants": ant_coords, "i": i})
                    self.ants = updated_ants

        init_generations()
        create_generations()

    def close_image_creation(self):
        while True:
            with self.images_pool_control.get_lock():
                n_cal = self.images_pool_control.value

            if n_cal >= self.args.n_generations:
                self.images_pool.terminate()
                return


if __name__ == "__main__":
    begin = datetime.now()
    app = ParallelApp()
    app.run_parallel()
    print(f"Duration: {datetime.now() - begin}")
