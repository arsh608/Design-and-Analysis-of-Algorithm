from typing import List, Dict, Tuple


def karatsuba(
    multiplicand: int, multiplier: int, threshold: int = 64, want_trace: bool = False
):
    """
    Multiply two large integers using Karatsuba's divide-and-conquer algorithm.

    The algorithm splits each number into high and low parts:
    a = a_high * 10^m + a_low
    b = b_high * 10^m + b_low

    Then computes: z2 = a_high * b_high
                   z0 = a_low * b_low
                   z1 = (a_high + a_low) * (b_high + b_low) - z2 - z0

    Final result: z2 * 10^(2m) + z1 * 10^m + z0

    Args:
        multiplicand: First integer to multiply
        multiplier: Second integer to multiply
        threshold: Minimum digit count to use Karatsuba (below this, use direct multiplication)
        want_trace: Whether to generate execution trace

    Returns:
        Tuple of (product, trace_list)
    """
    execution_trace: List[Dict] = []

    def recursive_multiply(
        first_number: int, second_number: int, recursion_depth: int
    ) -> int:
        """
        Recursively multiply two numbers using Karatsuba's method.
        """
        if first_number == 0 or second_number == 0:
            if want_trace:
                execution_trace.append(
                    {
                        "depth": recursion_depth,
                        "case": "base_zero",
                        "a": first_number,
                        "b": second_number,
                        "prod": 0,
                    }
                )
            return 0

        max_digit_count = max(len(str(abs(first_number))), len(str(abs(second_number))))

        if max_digit_count <= threshold:
            direct_product = first_number * second_number
            if want_trace:
                execution_trace.append(
                    {
                        "depth": recursion_depth,
                        "case": "base_mul",
                        "a": first_number,
                        "b": second_number,
                        "prod": direct_product,
                    }
                )
            return direct_product

        split_position = max_digit_count // 2
        base_power = 10**split_position

        first_high, first_low = divmod(first_number, base_power)
        second_high, second_low = divmod(second_number, base_power)

        high_product = recursive_multiply(first_high, second_high, recursion_depth + 1)
        low_product = recursive_multiply(first_low, second_low, recursion_depth + 1)
        cross_product = recursive_multiply(
            first_high + first_low, second_high + second_low, recursion_depth + 1
        )
        middle_term = cross_product - high_product - low_product

        final_product = (
            high_product * (base_power**2) + middle_term * base_power + low_product
        )

        if want_trace:
            execution_trace.append(
                {
                    "depth": recursion_depth,
                    "case": "karatsuba",
                    "n": max_digit_count,
                    "m": split_position,
                    "a_high": first_high,
                    "a_low": first_low,
                    "b_high": second_high,
                    "b_low": second_low,
                    "z2": high_product,
                    "z1": middle_term,
                    "z0": low_product,
                    "prod": final_product,
                }
            )

        return final_product

    result = recursive_multiply(multiplicand, multiplier, recursion_depth=0)
    return result, execution_trace


def parse_ints_file(file_path: str):
    """
    Parse a file containing two large integers for multiplication.

    File format: Two lines, each containing one integer.

    Args:
        file_path: Path to the input file

    Returns:
        Tuple of (first_integer, second_integer)

    Raises:
        ValueError: If file doesn't contain exactly two integers
    """
    with open(file_path, "r") as input_file:
        non_empty_lines = [line.strip() for line in input_file if line.strip()]

    if len(non_empty_lines) < 2:
        raise ValueError(
            "Integer dataset file must contain two lines (one integer per line)."
        )

    first_integer = int(non_empty_lines[0])
    second_integer = int(non_empty_lines[1])

    return first_integer, second_integer


def pretty_trace(trace, max_rows: int = 200):
    """
    Format the execution trace into a human-readable string representation.

    Args:
        trace: List of trace dictionaries from algorithm execution
        max_rows: Maximum number of trace rows to display

    Returns:
        Formatted multi-line string showing the trace
    """
    formatted_output = []
    for step_index, trace_step in enumerate(trace[:max_rows]):
        step_case = trace_step["case"]

        if step_case == "base_zero":
            formatted_output.append(
                f"[{step_index:03d}] depth={trace_step['depth']} BASE_ZERO "
                f"a={trace_step['a']} b={trace_step['b']} -> 0"
            )
        elif step_case == "base_mul":
            a_digits = len(str(trace_step["a"]))
            b_digits = len(str(trace_step["b"]))
            prod_digits = len(str(trace_step["prod"]))
            formatted_output.append(
                f"[{step_index:03d}] depth={trace_step['depth']} BASE_MUL "
                f"a={a_digits}d * b={b_digits}d -> {prod_digits}d"
            )
        else:
            z2_size = len(str(abs(trace_step["z2"])))
            z1_size = len(str(abs(trace_step["z1"])))
            z0_size = len(str(abs(trace_step["z0"])))
            formatted_output.append(
                f"[{step_index:03d}] depth={trace_step['depth']} KARATSUBA "
                f"n={trace_step['n']} m={trace_step['m']} "
                f"a=({trace_step['a_high']},{trace_step['a_low']}) "
                f"b=({trace_step['b_high']},{trace_step['b_low']}) -> "
                f"z2,z1,z0 sizes=({z2_size}d,{z1_size}d,{z0_size}d)"
            )

    if len(trace) > max_rows:
        formatted_output.append(f"... ({len(trace) - max_rows} more steps)")

    return "\n".join(formatted_output)
