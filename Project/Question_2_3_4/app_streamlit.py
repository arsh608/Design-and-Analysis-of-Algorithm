import streamlit as st
import os
import time
import pandas as pd
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from algorithms.closest_pair import (
    parse_points_file,
    closest_pair,
    pretty_trace as format_closest_pair_trace,
)
from algorithms.karatsuba import (
    parse_ints_file,
    karatsuba,
    pretty_trace as format_karatsuba_trace,
)

st.set_page_config(page_title="Divide & Conquer Algorithm Explorer", layout="wide")

st.title("Divide & Conquer Algorithm Explorer")
st.markdown(
    "Explore **Closest Pair of Points** and **Karatsuba Integer Multiplication** algorithms interactively."
)

closest_pair_tab, karatsuba_tab = st.tabs(
    ["Closest Pair of Points", "Karatsuba Multiplication"]
)

with closest_pair_tab:
    st.header("Closest Pair of Points Algorithm")
    dataset_directory = "datasets/closest_pair"

    available_files = sorted(
        [
            filename
            for filename in os.listdir(dataset_directory)
            if filename.endswith(".txt")
        ]
    )

    selected_file = st.selectbox(
        "Select a points dataset:",
        available_files,
        index=0 if available_files else None,
    )
    display_trace = st.toggle("Display algorithm trace", value=False)

    if selected_file:
        file_path = os.path.join(dataset_directory, selected_file)
        point_list = parse_points_file(file_path)
        st.write(
            f"Successfully loaded **{len(point_list)}** points from `{selected_file}`."
        )

        start_time = time.time()
        min_distance, closest_points, execution_trace = closest_pair(
            point_list, want_trace=display_trace
        )
        elapsed_time = (time.time() - start_time) * 1000

        results_column, visualization_column = st.columns(2)

        with results_column:
            st.metric("Minimum distance", f"{min_distance:.6f}")
            st.write(f"Closest pair coordinates: `{closest_points}`")
            st.write(f"Execution time: **{elapsed_time:.2f} ms**")

        with visualization_column:
            
            figure, axes = plt.subplots()
            x_coordinates = [point[0] for point in point_list]
            y_coordinates = [point[1] for point in point_list]
            axes.scatter(x_coordinates, y_coordinates, s=8, alpha=0.6)

          
            if closest_points:
                closest_x = [closest_points[0][0], closest_points[1][0]]
                closest_y = [closest_points[0][1], closest_points[1][1]]
                axes.plot(
                    closest_x, closest_y, linewidth=2, color="red", linestyle="--"
                )
                axes.scatter(
                    [closest_points[0][0], closest_points[1][0]],
                    [closest_points[0][1], closest_points[1][1]],
                    s=30,
                    color="red",
                )
            axes.set_title(f"Point Distribution: {selected_file}")
            axes.set_xlabel("X coordinate")
            axes.set_ylabel("Y coordinate")
            st.pyplot(figure)

       
        if display_trace and execution_trace:
            st.subheader("Algorithm Execution Trace (first 250 steps)")
            st.code(format_closest_pair_trace(execution_trace, max_rows=250))

with karatsuba_tab:
    st.header("Karatsuba Integer Multiplication Algorithm")
    integer_dataset_dir = "datasets/integer_multiplication"


    integer_files = sorted(
        [f for f in os.listdir(integer_dataset_dir) if f.endswith(".txt")]
    )

    selected_integer_file = st.selectbox(
        "Select an integer dataset:",
        integer_files,
        index=0 if integer_files else None,
        key="integer_selector",
    )
    show_algorithm_trace = st.toggle(
        "Display algorithm trace", value=False, key="integer_trace_toggle"
    )

    if selected_integer_file:
        integer_file_path = os.path.join(integer_dataset_dir, selected_integer_file)
        first_integer, second_integer = parse_ints_file(integer_file_path)
        first_digit_count = len(str(abs(first_integer)))
        second_digit_count = len(str(abs(second_integer)))

    
        computation_start = time.time()
        multiplication_result, algorithm_trace = karatsuba(
            first_integer, second_integer, threshold=64, want_trace=show_algorithm_trace
        )
        computation_time = (time.time() - computation_start) * 1000

        st.write(
            f"Input digit counts: First number = {first_digit_count}, Second number = {second_digit_count}"
        )

        result_string = str(multiplication_result)
       
        if len(result_string) > 240:
            truncated_result = f"{result_string[:120]} ... {result_string[-120:]}"
        else:
            truncated_result = result_string

        st.write("Computed product (truncated if too long):")
        st.code(truncated_result)

        st.metric("Result digit count", f"{len(result_string)}")
        st.write(f"Computation time: **{computation_time:.2f} ms**")


        if show_algorithm_trace and algorithm_trace:
            st.subheader("Algorithm Execution Trace (first 250 steps)")
            st.code(format_karatsuba_trace(algorithm_trace, max_rows=250))
