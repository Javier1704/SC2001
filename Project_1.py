import numpy as np
import matplotlib.pyplot as plt
import time

def hybrid_sort(arr, start, end, S):
    if (end - start) <= S:
        return insertion_sort(arr, start, end)

    mid = start + ((end - start) // 2)

    comparisons = 0

    comparisons += hybrid_sort(arr, start, mid, S)
    comparisons += hybrid_sort(arr, mid, end, S)

    comparisons += merge(arr, start, mid, end)

    return comparisons

def merge_sort(arr, start, end):
    if (end - start) <= 1:
        return 0

    mid = start + ((end - start) // 2)

    comparisons = 0

    comparisons += merge_sort(arr, start, mid)
    comparisons += merge_sort(arr, mid, end)

    comparisons += merge(arr, start, mid, end)

    return comparisons

def merge(arr, start, mid, end):
    i = 0
    k = start
    comparisons = 0

    Bl = arr[start: mid]
    Br = arr[mid: end]

    for j in range(0, len(Br)):
        while i < len(Bl):
            comparisons += 1

            if Bl[i] <= Br[j]:
                arr[k] = Bl[i]
                i += 1
                k += 1

            else:
                break

        arr[k] = Br[j]
        k += 1

    while i < len(Bl):
        arr[k] = Bl[i]
        i += 1
        k += 1

    return comparisons

def insertion_sort(arr, start, end):
    comparisons = 0

    for i in range(start + 1, end):
        j = i - 1

        while j >= start:
            comparisons += 1

            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                j -= 1

            else: 
                break

    return comparisons

def part_ci():
    S = 5 
    X = 100000

    sizes = [1000, 10000, 100000, 1000000, 10000000]

    comparison_results = []

    rng = np.random.default_rng()

    for n in sizes:
        arr = rng.integers(low = 1, high = X + 1, size = n).tolist()
        comparisons = hybrid_sort(arr, 0, len(arr), S)
        comparison_results.append(comparisons)
        print("n = ", n, "Comparisons = ", comparisons)

    plt.plot(sizes, comparison_results, linestyle= '--', marker='o')

    plt.title("Fixed S, Key Comparisons Against n")
    plt.xlabel("Size")
    plt.ylabel("Key Comparisons")
    plt.show()

def part_cii():
    n = 1000000
    X = 100000

    S = list(range(1, 101))

    comparison_results = []

    rng = np.random.default_rng()

    original_arr = rng.integers(low = 1, high = X + 1, size = n).tolist()

    for s in S:
        arr = original_arr.copy()
        comparisons = hybrid_sort(arr, 0, len(arr), s)
        comparison_results.append(comparisons)
        print("S = ", s, "Comparisons = ", comparisons)

    plt.plot(S, comparison_results, linestyle= '--', marker= 'o')

    plt.title("Fixed n, Key Comparisons against s")
    plt.xlabel("Threshold S")
    plt.ylabel("Key Comparisons")

    plt.show()

def part_ciii():
    X = 100000

    sizes = [1000, 10000, 100000, 1000000, 10000000]
    S = list(range(1, 101))

    rng = np.random.default_rng()

    for n in sizes:
        original_arr = rng.integers(low = 1, high = X + 1, size = n).tolist()
        comparison_results = []
        comparison_results_time = []

        for s in S:
            arr = original_arr.copy()
            start_time = time.process_time()
            comparisons = hybrid_sort(arr, 0, len(arr), s)
            end_time = time.process_time()
            run_time = end_time - start_time
            comparison_results.append(comparisons)
            comparison_results_time.append(run_time)
            print(f"Size = {n}, S = {s}, comparisons = {comparisons}, runtime = {run_time}")

        min_comparisons = min(comparison_results)
        min_runtime = min(comparison_results_time)
        best_index_key_comparison = comparison_results.index(min_comparisons)
        best_index_runtime = comparison_results_time.index(min_runtime)
        best_S_key_comparison = S[best_index_key_comparison]
        best_S_runtime = S[best_index_runtime]

        print(f"For n = {n}, best S by key comparison = {best_S_key_comparison}, with {min_comparisons} comparisons, best S by runtime = {best_S_runtime}, with {min_runtime}.")

        plt.figure()

        plt.plot(S, comparison_results, linestyle= '--', marker= 'o')

        plt.title(f"Size {n}: S against key comparisons")
        plt.xlabel("Threshold S")
        plt.ylabel("Key Comparisons")

        plt.show(block = False)

        plt.figure()

        plt.plot(S, comparison_results_time, linestyle= '--', marker= 'o')

        plt.title(f"size {n}: S against runtime")
        plt.xlabel("Threshold S")
        plt.ylabel("Runtime")

        plt.show(block = False)

    plt.show()

def part_d():
    X = 100000
    n = 10000000
    S = 1

    rng = np.random.default_rng()

    original_arr = rng.integers(low = 1, high = X + 1, size = n).tolist()

    arr1 = original_arr.copy()

    hybrid_start_time = time.process_time()
    hybrid_comparisons = hybrid_sort(arr1, 0, len(arr1), S)
    hybrid_end_time = time.process_time()

    hybrid_runtime = hybrid_end_time - hybrid_start_time

    print(f"Hybrid runtime: {hybrid_runtime}s, Hybrid comparisons: {hybrid_comparisons}")

    arr2 = original_arr.copy()

    merge_start_time = time.process_time()
    merge_comparisons = merge_sort(arr2, 0, len(arr2))
    merge_end_time = time.process_time()

    merge_runtime = merge_end_time - merge_start_time

    print(f"Merge runtime: {merge_runtime}s, Merge comparisons: {merge_comparisons}")

    categories = ['Hybrid Sort', 'Merge Sort']
    runtime_values = [hybrid_runtime, merge_runtime]
    comparison_values = [hybrid_comparisons, merge_comparisons]

    plt.figure()

    plt.bar(categories, runtime_values, color = 'skyblue', edgecolor = 'black')

    plt.xlabel('Sorting Algorithm')
    plt.ylabel('CPU Time (seconds)')
    plt.title('Sorting Algorithm Against Runtime')

    plt.show(block = False)

    plt.figure()

    plt.bar(categories, comparison_values, color = 'skyblue', edgecolor = 'black')

    plt.xlabel('Sorting Algorithm')
    plt.ylabel('Key Comparisons')
    plt.title('Sorting Algorithm Against Key Comparisons')

    plt.show(block = False)

    plt.show()

part_d()