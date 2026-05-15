import matplotlib.pyplot as plt

input_sizes = ["Small\n10,000", "Medium\n50,000", "Large\n100,000"]

results = {
    "Best Case": {
        "Naive String Matching - Θ(nk)": [0.823, 6.843, 15.664],
        "Rabin-Karp - Avg Θ(n+k)": [1.030, 10.963, 21.842]
    },
    "Average Case": {
        "Naive String Matching - Θ(nk)": [3.194, 11.439, 15.506],
        "Rabin-Karp - Avg Θ(n+k)": [2.337, 14.034, 22.392]
    },
    "Worst Case": {
        "Naive String Matching - Θ(nk)": [2.365, 12.106, 29.477],
        "Rabin-Karp - Worst Θ(nk)": [2.256, 5.308, 17.122]
    }
}

for case_name, algorithms in results.items():
    plt.figure(figsize=(8, 5))

    for algorithm_name, times in algorithms.items():
        plt.plot(input_sizes, times, marker="o", label=algorithm_name)

    plt.title(case_name + " Running Time")
    plt.xlabel("Dataset Size (characters)")
    plt.ylabel("Average Running Time (ms)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    file_name = case_name.replace(" ", "_") + "_Running_Time.png"
    plt.savefig(file_name, dpi=300)
    plt.show()