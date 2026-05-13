import csv
import time


# =========================================================
# Load dataset text from a CSV file
# This function reads sentences from the dataset and joins
# them into one long text string for string searching.
# =========================================================
def load_text_from_csv(file_path, text_column=None, max_rows=None):
    sentences = []

    with open(file_path, "r", encoding="utf-8", errors="ignore") as file:
        reader = csv.DictReader(file)

        # If no column name is given, use the first column in the CSV file
        if text_column is None:
            text_column = reader.fieldnames[0]

        for i, row in enumerate(reader):
            # Stop reading if max_rows limit is reached
            if max_rows is not None and i >= max_rows:
                break

            sentence = row.get(text_column, "")

            # Add only non-empty sentences
            if sentence:
                sentences.append(sentence.strip())

    # Merge all sentences into one large text
    return " ".join(sentences)


# =========================================================
# Algorithm 1: Naive String Matching
# Design family: Brute Force
#
# This algorithm compares the pattern with every possible
# position in the text, character by character.
#
# Returns:
#   count      -> number of occurrences
#   positions  -> list of starting indices
# =========================================================
def naive_string_search(text, pattern):
    n = len(text)
    m = len(pattern)

    count = 0
    positions = []

    # Invalid cases: empty pattern or pattern longer than text
    if m == 0 or m > n:
        return count, positions

    # Try every possible starting position
    for i in range(n - m + 1):
        match = True

        # Compare pattern characters one by one
        for j in range(m):
            if text[i + j] != pattern[j]:
                match = False
                break

        # If all characters matched, record the occurrence
        if match:
            count += 1
            positions.append(i)

    return count, positions


# =========================================================
# Algorithm 2: Rabin-Karp String Matching
# Design family: Space-Time Tradeoff / Hashing
#
# This algorithm compares hash values first, and only checks
# characters when the hash values match.
#
# Returns:
#   count      -> number of occurrences
#   positions  -> list of starting indices
# =========================================================
def rabin_karp_search(text, pattern, base=256, prime=101):
    n = len(text)
    m = len(pattern)

    count = 0
    positions = []

    # Invalid cases: empty pattern or pattern longer than text
    if m == 0 or m > n:
        return count, positions

    pattern_hash = 0
    window_hash = 0
    h = 1

    # Compute the value of h = pow(base, m-1) % prime
    # This is used when removing the leading character
    for _ in range(m - 1):
        h = (h * base) % prime

    # Compute initial hash for the pattern and the first text window
    for i in range(m):
        pattern_hash = (base * pattern_hash + ord(pattern[i])) % prime
        window_hash = (base * window_hash + ord(text[i])) % prime

    # Slide the pattern across the text
    for i in range(n - m + 1):
        # If the hash values match, verify character by character
        if pattern_hash == window_hash:
            match = True

            for j in range(m):
                if text[i + j] != pattern[j]:
                    match = False
                    break

            if match:
                count += 1
                positions.append(i)

        # Compute the hash of the next text window
        if i < n - m:
            window_hash = (
                base * (window_hash - ord(text[i]) * h) + ord(text[i + m])
            ) % prime

            # Convert negative hash to positive
            if window_hash < 0:
                window_hash += prime

    return count, positions


# =========================================================
# Measure execution time of an algorithm
#
# This function runs the same algorithm multiple times
# and returns the average execution time.
#
# Returns:
#   average_time  -> average running time
#   result        -> final search result (count, positions)
# =========================================================
def measure_execution_time(search_function, text, pattern, repeat=5):
    times = []
    result = None

    for _ in range(repeat):
        start = time.perf_counter()
        result = search_function(text, pattern)
        end = time.perf_counter()

        times.append(end - start)

    average_time = sum(times) / repeat
    return average_time, result


# =========================================================
# Run one comparison experiment for both algorithms
#
# This function:
# 1) runs Naive String Matching
# 2) runs Rabin-Karp
# 3) checks that both produce the same result
# 4) prints the results in a clean format
# =========================================================
def run_comparison(text, pattern, case_name, text_size_label, repeat=5):
    print("=" * 80)
    print(f"CASE TYPE        : {case_name}")
    print(f"TEXT SIZE LABEL  : {text_size_label}")
    print(f"TEXT LENGTH      : {len(text)}")
    print(f"PATTERN          : '{pattern}'")
    print(f"PATTERN LENGTH   : {len(pattern)}")
    print("-" * 80)

    naive_time, (naive_count, naive_positions) = measure_execution_time(
        naive_string_search, text, pattern, repeat
    )

    rk_time, (rk_count, rk_positions) = measure_execution_time(
        rabin_karp_search, text, pattern, repeat
    )

    # Ensure both algorithms return identical results
    assert naive_count == rk_count, "Mismatch in occurrence counts!"
    assert naive_positions == rk_positions, "Mismatch in occurrence positions!"

    print("Naive String Matching Results")
    print(f"Occurrences found           : {naive_count}")
    print(f"First 10 starting positions : {naive_positions[:10]}")
    print(f"Average time over {repeat} runs : {naive_time:.6f} seconds")
    print()

    print("Rabin-Karp Results")
    print(f"Occurrences found           : {rk_count}")
    print(f"First 10 starting positions : {rk_positions[:10]}")
    print(f"Average time over {repeat} runs : {rk_time:.6f} seconds")
    print()

    # Display the faster algorithm in this experiment
    if naive_time < rk_time:
        print("Faster algorithm in this experiment: Naive String Matching")
    elif rk_time < naive_time:
        print("Faster algorithm in this experiment: Rabin-Karp")
    else:
        print("Both algorithms took تقريبًا the same time")

    print("=" * 80)
    print()


# =========================================================
# Create text for Best Case
#
# Best case here means the first character of the pattern
# mismatches quickly in most positions, reducing comparisons.
# =========================================================
def create_best_case_text(base_text):
    return base_text


# =========================================================
# Create text for Average Case
#
# Average case uses normal text from the dataset with a
# reasonably common word as the pattern.
# =========================================================
def create_average_case_text(base_text):
    return base_text


# =========================================================
# Create text for Worst Case
#
# Worst case is artificially created to make the Naive
# algorithm perform many repeated comparisons.
# Example:
#   text    = "aaaaaa....aaaaa"
#   pattern = "aaaab"
# =========================================================
def create_worst_case_text(length):
    return "a" * length


# =========================================================
# Main program
# =========================================================
def main():
    # -----------------------------------------------------
    # Update this path to match your CSV file name
    # -----------------------------------------------------
    file_path = "wikipedia_sentences.csv"

    # -----------------------------------------------------
    # Load a large text from the dataset
    # You can increase max_rows if your computer can handle it
    # -----------------------------------------------------
    full_text = load_text_from_csv(file_path, text_column=None, max_rows=50000)

    # -----------------------------------------------------
    # Prepare different input sizes for experiments
    # These are useful for screenshots in section d
    # -----------------------------------------------------
    small_text = full_text[:10000]
    medium_text = full_text[:50000]
    large_text = full_text[:100000]

    # -----------------------------------------------------
    # BEST CASE experiments
    # Pattern starts with a character likely to mismatch fast
    # -----------------------------------------------------
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

    # -----------------------------------------------------
    # AVERAGE CASE experiments
    # Use a normal pattern that may naturally appear in text
    # -----------------------------------------------------
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

    # -----------------------------------------------------
    # WORST CASE experiments
    # Artificial text is used because worst-case behavior is
    # easier to demonstrate with highly repetitive characters
    # -----------------------------------------------------
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
# Program entry point
# =========================================================
if __name__ == "__main__":
    main()