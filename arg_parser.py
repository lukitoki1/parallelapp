import argparse
import json
from typing import List

arg_parser = argparse.ArgumentParser("Run parallel Langton Ant program.")
arg_parser.add_argument("--conf", metavar="CONF", type=str, nargs=1, required=False, default=["config.json"],
                        help="config file containing board data")
arg_parser.add_argument("--gen", metavar="N_GEN", type=int, nargs=1, required=False, default=[25],
                        help="number of generations to simulate")
arg_parser.add_argument("--proc", metavar="N_PROC", type=int, nargs=1, required=False, default=[8],
                        help="maximum number of processes to use")
arg_parser.add_argument("--magn", metavar="MAGN", type=int, nargs=1, required=False, default=[10],
                        help="magnification of the board")


class Parser:
    def __init__(self):
        self.config_file_name: str = None

        self.width: int = None
        self.height: int = None
        self.black_cells: List[List[int]] = None
        self.ants: List[dict] = None

        self.n_generations: int = None
        self.n_processors: int = None
        self.magnification: int = None

        self.read_args()

    def read_args(self):
        args = vars(arg_parser.parse_args())

        self.config_file_name = args["conf"][0]
        self.n_generations = args["gen"][0]
        self.n_processors = args["proc"][0]
        self.magnification = args["magn"][0]

        with open(self.config_file_name) as file:
            config = json.load(file)

            self.width = config["width"]
            self.height = config["height"]
            self.black_cells = config["black_cells"]
            self.ants = config["ants"]
