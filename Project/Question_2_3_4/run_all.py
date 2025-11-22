import os
import time
import pandas as pd
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from algorithms.closest_pair import parse_points_file, closest_pair
from algorithms.karatsuba import parse_ints_file, karatsuba


def process_all_closest_pair_datasets(
    dataset_directory="datasets/closest_pair", output_plot_directory="outputs/plots"
):
    """
    Process all closest pair datasets and generate results with visualizations.

    Args:
        dataset_directory: Path to directory containing point dataset files
        output_plot_directory: Path where visualization plots will be saved

    Returns:
        List of dictionaries containing performance metrics for each dataset
    """
    result_records = []
    dataset_files = sorted(
        [
            filename
            for filename in os.listdir(dataset_directory)
            if filename.endswith(".txt")
        ]
    )

    for dataset_filename in dataset_files:
        full_path = os.path.join(dataset_directory, dataset_filename)
        point_collection = parse_points_file(full_path)

        start_timestamp = time.time()
        minimum_distance, closest_pair_result, _ = closest_pair(
            point_collection, want_trace=False
        )
        execution_duration = (time.time() - start_timestamp) * 1000

        result_records.append(
            {
                "problem": "closest_pair",
                "file": dataset_filename,
                "n_points": len(point_collection),
                "distance": minimum_distance,
                "time_ms": execution_duration,
            }
        )

        plot_figure, plot_axes = plt.subplots(figsize=(8, 6))
        x_values = [point[0] for point in point_collection]
        y_values = [point[1] for point in point_collection]
        plot_axes.scatter(x_values, y_values, s=8, alpha=0.6)

        if closest_pair_result:
            pair_x_coords = [closest_pair_result[0][0], closest_pair_result[1][0]]
            pair_y_coords = [closest_pair_result[0][1], closest_pair_result[1][1]]
            plot_axes.plot(pair_x_coords, pair_y_coords, linewidth=2, color="red")
            plot_axes.scatter(
                [closest_pair_result[0][0], closest_pair_result[1][0]],
                [closest_pair_result[0][1], closest_pair_result[1][1]],
                s=30,
                color="red",
            )

        plot_axes.set_title(
            f"{dataset_filename} — Minimum Distance: {minimum_distance:.6f}"
        )
        plot_axes.set_xlabel("X coordinate")
        plot_axes.set_ylabel("Y coordinate")

        output_filename = dataset_filename.replace(".txt", "") + ".png"
        output_filepath = os.path.join(output_plot_directory, output_filename)
        plot_figure.savefig(output_filepath, bbox_inches="tight", dpi=150)
        plt.close(plot_figure)

    return result_records


def process_all_karatsuba_datasets(dataset_directory="datasets/integer_multiplication"):
    """
    Process all Karatsuba multiplication datasets and generate performance metrics.

    Args:
        dataset_directory: Path to directory containing integer dataset files

    Returns:
        List of dictionaries containing performance metrics for each dataset
    """
    result_records = []
    dataset_files = sorted(
        [
            filename
            for filename in os.listdir(dataset_directory)
            if filename.endswith(".txt")
        ]
    )

    for dataset_filename in dataset_files:
        full_path = os.path.join(dataset_directory, dataset_filename)
        first_number, second_number = parse_ints_file(full_path)
        first_digit_length = len(str(abs(first_number)))
        second_digit_length = len(str(abs(second_number)))

        start_timestamp = time.time()
        multiplication_product, _ = karatsuba(
            first_number, second_number, threshold=64, want_trace=False
        )
        execution_duration = (time.time() - start_timestamp) * 1000

        is_correct = multiplication_product == first_number * second_number

        result_records.append(
            {
                "problem": "karatsuba",
                "file": dataset_filename,
                "digits_a": first_digit_length,
                "digits_b": second_digit_length,
                "prod_digits": (
                    len(str(abs(multiplication_product)))
                    if multiplication_product != 0
                    else 1
                ),
                "time_ms": execution_duration,
                "verified": is_correct,
            }
        )

    return result_records


def main():
    """
    Main execution function that processes all datasets and generates output files.
    """
    os.makedirs("outputs/plots", exist_ok=True)

    all_results = []
    all_results.extend(process_all_closest_pair_datasets())
    all_results.extend(process_all_karatsuba_datasets())

    results_dataframe = pd.DataFrame(all_results)
    results_dataframe.to_csv("outputs/results.csv", index=False)

    print("\n=== Batch Processing Complete ===")
    print(results_dataframe)
    print(f"\nTotal datasets processed: {len(all_results)}")
    print("Results saved to: outputs/results.csv")


if __name__ == "__main__":
    main()
