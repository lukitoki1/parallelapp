def scale_indexes_to_range(x: int, y: int, multiplier: int) -> (int, int, int, int):
    def calculate_lower_bound(coord: int) -> int:
        return coord * multiplier

    def calculate_upper_bound(coord: int) -> int:
        return (coord + 1) * multiplier - 1

    return calculate_lower_bound(x), calculate_upper_bound(x), calculate_lower_bound(y), calculate_upper_bound(y)
