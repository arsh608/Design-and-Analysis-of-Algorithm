"""
Divide-and-conquer implementation for finding the closest pair of points.
Uses O(n log² n) approach with optimized merge step.
"""

import math
from typing import List, Tuple, Dict

Point = Tuple[float, float]


def calculate_euclidean_distance(point_a: Point, point_b: Point) -> float:
    """
    Compute the Euclidean distance between two points in 2D space.
    
    Args:
        point_a: First point as (x, y) tuple
        point_b: Second point as (x, y) tuple
        
    Returns:
        Euclidean distance between the two points
    """
    delta_x = point_a[0] - point_b[0]
    delta_y = point_a[1] - point_b[1]
    return math.sqrt(delta_x * delta_x + delta_y * delta_y)


def brute_force_closest_pair(point_list: List[Point]):
    """
    Find the closest pair using brute force method (O(n²)).
    Used as base case for small point sets.
    
    Args:
        point_list: List of points to search
        
    Returns:
        Tuple of (minimum_distance, closest_pair_tuple)
    """
    minimum_distance = float("inf")
    closest_pair_result = None
    point_count = len(point_list)
    
    for i in range(point_count):
        for j in range(i + 1, point_count):
            current_distance = calculate_euclidean_distance(
                point_list[i], 
                point_list[j]
            )
            if current_distance < minimum_distance:
                minimum_distance = current_distance
                closest_pair_result = (point_list[i], point_list[j])
    
    return minimum_distance, closest_pair_result


def closest_pair(point_list: List[Point], want_trace: bool = False):
    """
    Find the closest pair of points using divide-and-conquer approach.
    Time complexity: O(n log² n)
    
    Args:
        point_list: List of points as (x, y) tuples
        want_trace: Whether to generate execution trace
        
    Returns:
        Tuple of (minimum_distance, closest_pair_tuple, trace_list)
    """
    execution_trace: List[Dict] = []

    if len(point_list) < 2:
        return float("inf"), None, execution_trace

    points_sorted_by_x = sorted(point_list, key=lambda p: (p[0], p[1]))
    points_sorted_by_y = sorted(point_list, key=lambda p: (p[1], p[0]))

    def recursive_solve(
        x_sorted_points: List[Point], 
        y_sorted_points: List[Point], 
        recursion_depth: int = 0
    ):
        """
        Recursive function that divides the problem and combines results.
        """
        point_count = len(x_sorted_points)
        
        if point_count <= 3:
            distance, pair = brute_force_closest_pair(x_sorted_points)
            if want_trace:
                execution_trace.append({
                    "depth": recursion_depth,
                    "case": "bruteforce",
                    "n": point_count,
                    "best": distance,
                    "pair": pair
                })
            return distance, pair

        median_index = point_count // 2
        median_x_value = x_sorted_points[median_index][0]
        left_half_x = x_sorted_points[:median_index]
        right_half_x = x_sorted_points[median_index:]

        left_half_y = []
        right_half_y = []
        for point in y_sorted_points:
            if point[0] < median_x_value or (point[0] == median_x_value and point in left_half_x):
                left_half_y.append(point)
            else:
                right_half_y.append(point)

        left_distance, left_pair = recursive_solve(
            left_half_x, 
            left_half_y, 
            recursion_depth + 1
        )
        right_distance, right_pair = recursive_solve(
            right_half_x, 
            right_half_y, 
            recursion_depth + 1
        )

        # Determine the minimum distance from recursive calls
        current_min_distance = left_distance
        current_closest_pair = left_pair
        if right_distance < current_min_distance:
            current_min_distance = right_distance
            current_closest_pair = right_pair

        vertical_strip = [
            point for point in y_sorted_points 
            if abs(point[0] - median_x_value) < current_min_distance
        ]

        strip_size = len(vertical_strip)
        for i in range(strip_size):
            j = i + 1
            while j < strip_size and (vertical_strip[j][1] - vertical_strip[i][1]) < current_min_distance:
                strip_distance = calculate_euclidean_distance(
                    vertical_strip[i], 
                    vertical_strip[j]
                )
                if strip_distance < current_min_distance:
                    current_min_distance = strip_distance
                    current_closest_pair = (vertical_strip[i], vertical_strip[j])
                j += 1

        if want_trace:
            execution_trace.append({
                "depth": recursion_depth,
                "case": "merge",
                "n": point_count,
                "midx": median_x_value,
                "dl": left_distance,
                "dr": right_distance,
                "d": current_min_distance,
                "strip_size": len(vertical_strip),
                "best_pair": current_closest_pair
            })

        return current_min_distance, current_closest_pair

    minimum_distance, closest_pair_result = recursive_solve(
        points_sorted_by_x, 
        points_sorted_by_y, 
        recursion_depth=0
    )
    return minimum_distance, closest_pair_result, execution_trace


def parse_points_file(file_path: str):
    """
    Parse a file containing point coordinates.
    
    File format options:
    1. First line is count n, followed by n lines of "x y"
    2. All lines are "x y" coordinates
    
    Args:
        file_path: Path to the input file
        
    Returns:
        List of points as (x, y) tuples
    """
    parsed_points = []
    with open(file_path, "r") as input_file:
        first_line = input_file.readline().strip()
        try:
            point_count = int(first_line)
            # Format: first line is count
            for _ in range(point_count):
                line = input_file.readline()
                if not line:
                    break
                x_coord, y_coord = map(float, line.split())
                parsed_points.append((x_coord, y_coord))
        except ValueError:
            # Format: all lines are coordinates
            x_coord, y_coord = first_line.split()
            parsed_points.append((float(x_coord), float(y_coord)))
            for line in input_file:
                x_coord, y_coord = line.split()
                parsed_points.append((float(x_coord), float(y_coord)))
    
    return parsed_points


def pretty_trace(trace, max_rows=200):
    """
    Format the execution trace into a human-readable string.
    
    Args:
        trace: List of trace dictionaries
        max_rows: Maximum number of trace rows to display
        
    Returns:
        Formatted string representation of the trace
    """
    formatted_lines = []
    for step_index, trace_step in enumerate(trace[:max_rows]):
        if trace_step["case"] == "bruteforce":
            formatted_lines.append(
                f"[{step_index:03d}] depth={trace_step['depth']} BRUTE "
                f"n={trace_step['n']} -> best={trace_step['best']:.6f} "
                f"pair={trace_step['pair']}"
            )
        else:
            formatted_lines.append(
                f"[{step_index:03d}] depth={trace_step['depth']} MERGE "
                f"n={trace_step['n']} midx={trace_step['midx']:.3f} "
                f"dl={trace_step['dl']:.6f} dr={trace_step['dr']:.6f} "
                f"d={trace_step['d']:.6f} strip={trace_step['strip_size']} "
                f"best_pair={trace_step['best_pair']}"
            )
    
    if len(trace) > max_rows:
        formatted_lines.append(
            f"... ({len(trace) - max_rows} more steps)"
        )
    
    return "\n".join(formatted_lines)
