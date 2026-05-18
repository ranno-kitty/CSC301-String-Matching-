import matplotlib.pyplot as plt

# Input sizes used in the experiment.
input_sizes = ["Small\n10,000", "Medium\n50,000", "Large\n100,000"]

# Running time results from Section III, Point 3.
# All times are in milliseconds (ms).
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

# Labels show the theoretical order of growth for each case.
order_labels = {
    "Best Case": {
        "Naive String Matching": "Naive String Matching - Best Θ(n)",
        "Rabin-Karp": "Rabin-Karp - Best Θ(n + k)"
    },
    "Average Case": {
        "Naive String Matching": "Naive String Matching - Average Θ(nk)",
        "Rabin-Karp": "Rabin-Karp - Average Θ(n + k)"
    },
    "Worst Case": {
        "Naive String Matching": "Naive String Matching - Worst Θ(nk)",
        "Rabin-Karp": "Rabin-Karp - Worst Θ(nk)"
    }
}

# Draw one graph for each case.
for case_name, algorithms in results.items():
    plt.figure(figsize=(8, 5))

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

    file_name = case_name.replace(" ", "_") + "_Running_Time.png"
    plt.savefig(file_name, dpi=300, bbox_inches="tight")
    plt.show()