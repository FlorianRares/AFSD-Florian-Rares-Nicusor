import time
import random
import csv
from dataclasses import dataclass, asdict
from statistics import mean

SEED = 42
RUNS_PER_TEST = 3

SIZES = [100, 500, 1000, 2000, 5000]

BUBBLE_MAX_SIZE = 5000

INPUT_TYPES = [
    "aleator",
    "sortat_crescator",
    "sortat_descrescator",
    "multe_duplicate",
    "aproape_sortat",
]

CSV_FILENAME = "rezultate_sortari.csv"


@dataclass
class SortStats:
    comparisons: int = 0
    moves: int = 0
    recursive_calls: int = 0


@dataclass
class TestResult:
    algorithm: str
    size: int
    input_type: str
    run_count: int
    avg_time: float
    min_time: float
    max_time: float
    avg_comparisons: float
    avg_moves: float
    avg_recursive_calls: float
    valid: bool


def is_sorted_ascending(arr):
    for i in range(len(arr) - 1):
        if arr[i] > arr[i + 1]:
            return False
    return True


def generate_random_list(n, rng):
    return [rng.randint(0, 100000) for _ in range(n)]


def generate_sorted_list(n, rng):
    arr = generate_random_list(n, rng)
    arr.sort()
    return arr


def generate_reverse_sorted_list(n, rng):
    arr = generate_random_list(n, rng)
    arr.sort(reverse=True)
    return arr


def generate_many_duplicates_list(n, rng):
    return [rng.randint(0, 10) for _ in range(n)]


def generate_nearly_sorted_list(n, rng):
    arr = list(range(n))
    swap_count = max(1, n // 20)
    for _ in range(swap_count):
        i = rng.randint(0, n - 1)
        j = rng.randint(0, n - 1)
        arr[i], arr[j] = arr[j], arr[i]
    return arr


def generate_test_data(n, input_type, seed):
    rng = random.Random(seed)

    if input_type == "aleator":
        return generate_random_list(n, rng)
    if input_type == "sortat_crescator":
        return generate_sorted_list(n, rng)
    if input_type == "sortat_descrescator":
        return generate_reverse_sorted_list(n, rng)
    if input_type == "multe_duplicate":
        return generate_many_duplicates_list(n, rng)
    if input_type == "aproape_sortat":
        return generate_nearly_sorted_list(n, rng)

    raise ValueError(f"Tip de intrare necunoscut: {input_type}")


def bubble_sort(arr):
    stats = SortStats()
    n = len(arr)

    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            stats.comparisons += 1
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                stats.moves += 1
                swapped = True
        if not swapped:
            break

    return arr, stats


def quick_sort(arr):

    stats = SortStats()

    def _quick_sort(lst):
        stats.recursive_calls += 1

        if len(lst) <= 1:
            return lst[:]

        pivot = lst[len(lst) // 2]

        less = []
        equal = []
        greater = []

        for x in lst:
            stats.comparisons += 1
            if x < pivot:
                less.append(x)
                stats.moves += 1
            else:
                stats.comparisons += 1
                if x > pivot:
                    greater.append(x)
                    stats.moves += 1
                else:
                    equal.append(x)
                    stats.moves += 1

        left_sorted = _quick_sort(less)
        right_sorted = _quick_sort(greater)

        stats.moves += len(left_sorted) + len(equal) + len(right_sorted)
        return left_sorted + equal + right_sorted

    sorted_arr = _quick_sort(arr)
    return sorted_arr, stats


def merge_sort(arr):
    stats = SortStats()

    def _merge_sort(lst):
        stats.recursive_calls += 1

        if len(lst) <= 1:
            return lst[:]

        mid = len(lst) // 2
        left = _merge_sort(lst[:mid])
        right = _merge_sort(lst[mid:])

        return merge(left, right)

    def merge(left, right):
        merged = []
        i = 0
        j = 0

        while i < len(left) and j < len(right):
            stats.comparisons += 1
            if left[i] <= right[j]:
                merged.append(left[i])
                stats.moves += 1
                i += 1
            else:
                merged.append(right[j])
                stats.moves += 1
                j += 1

        while i < len(left):
            merged.append(left[i])
            stats.moves += 1
            i += 1

        while j < len(right):
            merged.append(right[j])
            stats.moves += 1
            j += 1

        return merged

    sorted_arr = _merge_sort(arr)
    return sorted_arr, stats

def run_single_measurement(sort_name, sort_function, original_data):
    test_data = original_data.copy()

    start = time.perf_counter()
    sorted_result, stats = sort_function(test_data)
    end = time.perf_counter()

    elapsed = end - start

    return sorted_result, stats, elapsed


def validate_results(reference_sorted, result_sorted):
    return reference_sorted == result_sorted and is_sorted_ascending(result_sorted)


def run_experiments():
    random.seed(SEED)

    algorithms = [
        ("Bubble Sort", bubble_sort),
        ("Quick Sort", quick_sort),
        ("Merge Sort", merge_sort),
    ]

    results = []

    for size in SIZES:
        for input_type in INPUT_TYPES:
            base_seed = hash((SEED, size, input_type)) & 0xFFFFFFFF
            original_data = generate_test_data(size, input_type, base_seed)


            expected_sorted = sorted(original_data)

            for algorithm_name, algorithm_func in algorithms:
                if algorithm_name == "Bubble Sort" and size > BUBBLE_MAX_SIZE:
                    print(f"[SKIP] {algorithm_name} | n={size} | {input_type} (prea lent)")
                    continue

                times = []
                comparisons_list = []
                moves_list = []
                recursive_calls_list = []
                all_valid = True

                for run_index in range(RUNS_PER_TEST):
                    result_sorted, stats, elapsed = run_single_measurement(
                        algorithm_name,
                        algorithm_func,
                        original_data
                    )

                    valid = validate_results(expected_sorted, result_sorted)
                    if not valid:
                        all_valid = False

                    times.append(elapsed)
                    comparisons_list.append(stats.comparisons)
                    moves_list.append(stats.moves)
                    recursive_calls_list.append(stats.recursive_calls)

                results.append(
                    TestResult(
                        algorithm=algorithm_name,
                        size=size,
                        input_type=input_type,
                        run_count=RUNS_PER_TEST,
                        avg_time=mean(times),
                        min_time=min(times),
                        max_time=max(times),
                        avg_comparisons=mean(comparisons_list),
                        avg_moves=mean(moves_list),
                        avg_recursive_calls=mean(recursive_calls_list),
                        valid=all_valid,
                    )
                )

    return results

def print_results_table(results):
    header = (
        f"{'Algoritm':<15}"
        f"{'Dimensiune':<12}"
        f"{'Intrare':<22}"
        f"{'Timp mediu (s)':<18}"
        f"{'Comparatii':<15}"
        f"{'Mutari':<12}"
        f"{'Apeluri rec.':<15}"
        f"{'Valid':<8}"
    )

    print("\n" + "=" * len(header))
    print(header)
    print("=" * len(header))

    for r in results:
        print(
            f"{r.algorithm:<15}"
            f"{r.size:<12}"
            f"{r.input_type:<22}"
            f"{r.avg_time:<18.6f}"
            f"{int(r.avg_comparisons):<15}"
            f"{int(r.avg_moves):<12}"
            f"{int(r.avg_recursive_calls):<15}"
            f"{str(r.valid):<8}"
        )

    print("=" * len(header))


def save_results_to_csv(results, filename):
    with open(filename, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "algorithm",
            "size",
            "input_type",
            "run_count",
            "avg_time",
            "min_time",
            "max_time",
            "avg_comparisons",
            "avg_moves",
            "avg_recursive_calls",
            "valid",
        ])
        writer.writeheader()
        for r in results:
            writer.writerow(asdict(r))


def print_summary(results):
    print("\nREZUMAT:")
    invalid_tests = [r for r in results if not r.valid]

    if invalid_tests:
        print("Au existat teste invalide!")
        for r in invalid_tests:
            print(f" - {r.algorithm}, n={r.size}, intrare={r.input_type}")
    else:
        print("Toate testele au fost validate cu succes.")

    print(f"Rezultatele au fost salvate în fișierul: {CSV_FILENAME}")

def main():
    results = run_experiments()
    print_results_table(results)
    save_results_to_csv(results, CSV_FILENAME)
    print_summary(results)


if __name__ == "__main__":
    main()