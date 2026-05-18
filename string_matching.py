import csv
import time
import random


# =========================================================
# Load dataset text from a CSV file
# =========================================================
def load_text_from_csv(file_path, text_column=None, max_rows=None):

    sentences = []

    with open(file_path, "r", encoding="utf-8", errors="ignore") as file:

        reader = csv.DictReader(file)

        # Use first column if no column is specified
        if text_column is None:
            text_column = reader.fieldnames[0]

        for i, row in enumerate(reader):

            # Stop if max rows reached
            if max_rows is not None and i >= max_rows:
                break

            sentence = row.get(text_column, "")

            if sentence:
                sentences.append(sentence.strip())

    return " ".join(sentences)


# =========================================================
# Algorithm 1: Naive String Matching
# =========================================================
def naive_string_search(text, pattern):

    n = len(text)
    m = len(pattern)

    count = 0
    positions = []

    if m == 0 or m > n:
        return count, positions

    for i in range(n - m + 1):

        match = True

        for j in range(m):

            if text[i + j] != pattern[j]:
                match = False
                break

        if match:
            count += 1
            positions.append(i)

    return count, positions


# =========================================================
# Algorithm 2: Rabin-Karp String Matching
# =========================================================
def rabin_karp_search(text, pattern, base=256, prime=101):

    n = len(text)
    m = len(pattern)

    count = 0
    positions = []

    if m == 0 or m > n:
        return count, positions

    pattern_hash = 0
    window_hash = 0
    h = 1

    for _ in range(m - 1):
        h = (h * base) % prime

    for i in range(m):

        pattern_hash = (
            base * pattern_hash + ord(pattern[i])
        ) % prime

        window_hash = (
            base * window_hash + ord(text[i])
        ) % prime

    for i in range(n - m + 1):

        if pattern_hash == window_hash:

            match = True

            for j in range(m):

                if text[i + j] != pattern[j]:
                    match = False
                    break

            if match:
                count += 1
                positions.append(i)

        if i < n - m:

            window_hash = (
                base * (window_hash - ord(text[i]) * h)
                + ord(text[i + m])
            ) % prime

            if window_hash < 0:
                window_hash += prime

    return count, positions


# =========================================================
# Measure execution time
# =========================================================
def measure_execution_time(search_function, text, pattern, repeat=5):

    times = []
    result = None

    for _ in range(repeat):

        start = time.perf_counter()

        result = search_function(text, pattern)

        end = time.perf_counter()

        times.append(end - start)

    # Convert seconds to milliseconds
    average_time = (sum(times) / repeat) * 1000

    return average_time, result


# =========================================================
# Run comparison experiment
# =========================================================
def run_comparison(text, pattern, case_name, text_size_label, repeat=5):

    print("=" * 80)

    print(f"CASE TYPE        : {case_name}")
    print(f"TEXT SIZE LABEL  : {text_size_label}")
    print(f"TEXT LENGTH      : {len(text)}")
    print(f"PATTERN          : '{pattern}'")
    print(f"PATTERN LENGTH   : {len(pattern)}")

    print("-" * 80)

    # Naive
    naive_time, (naive_count, naive_positions) = (
        measure_execution_time(
            naive_string_search,
            text,
            pattern,
            repeat
        )
    )

    # Rabin-Karp
    rk_time, (rk_count, rk_positions) = (
        measure_execution_time(
            rabin_karp_search,
            text,
            pattern,
            repeat
        )
    )

    # Ensure same results
    assert naive_count == rk_count
    assert naive_positions == rk_positions

    # Naive output
    print("Naive String Matching Results")

    print(f"Occurrences found           : {naive_count}")

    print(f"First 10 starting positions : {naive_positions[:10]}")

    print(
        f"Average time over {repeat} runs : "
        f"{naive_time:.6f} ms"
    )

    print()

    # Rabin-Karp output
    print("Rabin-Karp Results")

    print(f"Occurrences found           : {rk_count}")

    print(f"First 10 starting positions : {rk_positions[:10]}")

    print(
        f"Average time over {repeat} runs : "
        f"{rk_time:.6f} ms"
    )

    print()

    # Faster algorithm
    if naive_time < rk_time:

        print(
            "Faster algorithm in this experiment: "
            "Naive String Matching"
        )

    elif rk_time < naive_time:

        print(
            "Faster algorithm in this experiment: "
            "Rabin-Karp"
        )

    else:
        print("Both algorithms took similar time")

    print("=" * 80)
    print()


# =========================================================
# Create Best Case
# =========================================================
def create_best_case_text(base_text):
    return base_text


# =========================================================
# Create Average Case
# =========================================================
def create_average_case_text(base_text):
    return base_text


# =========================================================
# Create Worst Case
# =========================================================
def create_worst_case_text(length):
    return "a" * length


# =========================================================
# Main Program
# =========================================================
def main():

    # Dataset path
    file_path = "wikipedia_sentences.csv"

    # Load dataset
    full_text = load_text_from_csv(
        file_path,
        text_column=None,
        max_rows=50000
    )

    # =====================================================
    # Random input sequences
    # =====================================================

    small_start = random.randint(
        0,
        len(full_text) - 10000
    )

    medium_start = random.randint(
        0,
        len(full_text) - 50000
    )

    large_start = random.randint(
        0,
        len(full_text) - 100000
    )

    small_text = full_text[
        small_start:small_start + 10000
    ]

    medium_text = full_text[
        medium_start:medium_start + 50000
    ]

    large_text = full_text[
        large_start:large_start + 100000
    ]

    # =====================================================
    # BEST CASE
    # =====================================================

    best_pattern = "zqxj_not_found"

    run_comparison(
        create_best_case_text(small_text),
        best_pattern,
        case_name="Best Case",
        text_size_label="Small",
        repeat=5
    )

    run_comparison(
        create_best_case_text(medium_text),
        best_pattern,
        case_name="Best Case",
        text_size_label="Medium",
        repeat=5
    )

    run_comparison(
        create_best_case_text(large_text),
        best_pattern,
        case_name="Best Case",
        text_size_label="Large",
        repeat=5
    )

    # =====================================================
    # AVERAGE CASE
    # =====================================================

    average_pattern = "the"

    run_comparison(
        create_average_case_text(small_text),
        average_pattern,
        case_name="Average Case",
        text_size_label="Small",
        repeat=5
    )

    run_comparison(
        create_average_case_text(medium_text),
        average_pattern,
        case_name="Average Case",
        text_size_label="Medium",
        repeat=5
    )

    run_comparison(
        create_average_case_text(large_text),
        average_pattern,
        case_name="Average Case",
        text_size_label="Large",
        repeat=5
    )

    # =====================================================
    # WORST CASE
    # =====================================================

    worst_small_text = create_worst_case_text(10000)

    worst_medium_text = create_worst_case_text(50000)

    worst_large_text = create_worst_case_text(100000)

    worst_pattern = "aaaab"

    run_comparison(
        worst_small_text,
        worst_pattern,
        case_name="Worst Case",
        text_size_label="Small",
        repeat=5
    )

    run_comparison(
        worst_medium_text,
        worst_pattern,
        case_name="Worst Case",
        text_size_label="Medium",
        repeat=5
    )

    run_comparison(
        worst_large_text,
        worst_pattern,
        case_name="Worst Case",
        text_size_label="Large",
        repeat=5
    )


# =========================================================
# Program Entry Point
# =========================================================
if __name__ == "__main__":
    main()
