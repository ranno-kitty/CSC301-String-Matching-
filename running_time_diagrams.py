import matplotlib.pyplot as plt

# These are the same input sizes used in the experiment.
# Each value means the number of characters in the tested text segment.
input_sizes = ["Small\n10,000", "Medium\n50,000", "Large\n100,000"]

# These values are taken from the Actual Running Time table in Section III, point 3.
# The times are already reported in milliseconds.
results = {
    "Best Case": {
        "Naive String Matching": [1.700, 7.440, 14.844],
        "Rabin-Karp": [1.359, 7.670, 18.180]
    },
    "Average Case": {
        "Naive String Matching": [1.880, 8.741, 16.381],
        "Rabin-Karp": [2.245, 10.635, 19.005]
    },
    "Worst Case": {
        "Naive String Matching": [4.436, 19.616, 37.405],
        "Rabin-Karp": [2.626, 7.706, 17.015]
    }
}

# These labels connect the practical diagram with the theoretical order of growth.
# This is required because the rubric asks for running time and order of growth.
order_labels = {
    "Best Case": {
        "Naive String Matching": "Naive String Matching - Best Θ(n)",
        "Rabin-Karp": "Rabin-Karp - Θ(n + k)"
    },
    "Average Case": {
        "Naive String Matching": "Naive String Matching - Avg Θ(nk)",
        "Rabin-Karp": "Rabin-Karp - Avg Θ(n + k)"
    },
    "Worst Case": {
        "Naive String Matching": "Naive String Matching - Worst Θ(nk)",
        "Rabin-Karp": "Rabin-Karp - Practical Θ(n + k)"
    }
}

# Draw one diagram for each case.
for case_name, algorithms in results.items():
    plt.figure(figsize=(8, 5))

    # Plot both algorithms on the same diagram to make the comparison clear.
    for algorithm_name, times in algorithms.items():
        plt.plot(
            input_sizes,
            times,
            marker="o",
            label=order_labels[case_name][algorithm_name]
        )

    plt.title(case_name + " Running Time")
    plt.xlabel("Dataset Size (characters)")
    plt.ylabel("Average Running Time (ms)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    # Save the diagram with a clear file name.
    file_name = case_name.replace(" ", "_") + "_Running_Time.png"
    plt.savefig(file_name, dpi=300, bbox_inches="tight")
    plt.show()