# A7.py
# CS 1400
# Assignment 7: Search and Optimization
# Written by Shaan Luthra

import random
import time

#Returns list with highest score being increased 100 and the other scores are increased by the same amount
def curve_scores(scores):
    if len(scores) == 0:
        return []

    max_score = scores[0]
    for score in scores:
        if score > max_score:
            max_score = score

    curve_amount = 100 - max_score

    curved = []
    for score in scores:
        curved.append(score + curve_amount)

    return curved

#Returns true if duplicates
def contains_duplicate(words):
    for i in range(len(words)):
        current_word = words[i]
        # Look at the remaining words after the current one
        for j in range(i + 1, len(words)):
            if words[j] == current_word:
                return True
    return False

#Returns a list containing what was in the string
def list_to_string(numbers):
    result = "["
    for i in range(len(numbers)):
        result += str(numbers[i])
        # Add comma and space except for the last number
        if i != len(numbers) - 1:
            result += ", "
    result += "]"
    return result

#loops through a for loop that finds the smallest multiple of 3 in the list
def find_smallest_positive_multiple_of_three(numbers):
    smallest = None
    for num in numbers:
        if num > 0 and num % 3 == 0:
            if smallest is None or num < smallest:
                smallest = num
    return smallest

#goes through every point to find a target number and returns true if found
def sequential_search(target, numbers):
    for num in numbers:
        if num == target:
            return True
    return False

#goes through the list to find number using binary search and returns true if found
def binary_search(target, numbers):
    low = 0
    high = len(numbers) - 1
    while low <= high:
        mid = (low + high) // 2
        if numbers[mid] == target:
            return True
        elif numbers[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return False

#mesures average time to perform num_searches using sequential or binary on shuffled or unshuffled with different list sizes, and rounds to the 6th decimal
def measure_search_times(list_size, strategy, shuffled, num_searches):
    numbers = list(range(list_size))

    if shuffled:
        random.shuffle(numbers)

    if strategy == "binary" and shuffled:
        start_time = time.time()
        numbers.sort()
    else:
        start_time = time.time()

    for _ in range(num_searches):
        target = random.choice(numbers)
        if strategy == "sequential":
            sequential_search(target, numbers)
        elif strategy == "binary":
            binary_search(target, numbers)

    total_time = time.time() - start_time
    average_time = total_time / num_searches
    return round(average_time, 6)


def main():
    #Tests curve scores
    print("Testing curve_scores:")
    print("Input: [45, 85, 90], expecting [55, 95, 100], returning ", curve_scores([45, 85, 90]))
    print("Input: [], expecting [], returning", curve_scores([]))

    #tests contains duplicates
    print("\nTesting contains_duplicate:")
    print("Input: ['hi', 'bye'], expecting false, returning ", contains_duplicate(["hi", "bye"]))
    print("Input: ['the', 'boy', 'the'], expecting true, returning ", contains_duplicate(["the", "boy", "the"]))
    print("Input: [], expecting false, returning ", contains_duplicate([]))

    #test list to string
    print("\nTesting list_to_string:")
    print("Input: [1, 2, 3], expecting [1, 2, 3], returning ", list_to_string([1, 2, 3]))
    print("Input: [], expecting [], returning ", list_to_string([]))

    # --- Test find_smallest_positive_multiple_of_three ---
    print("\nTesting find_smallest_positive_multiple_of_three:")
    print("Input: [-3, 0, 2, 3, 1, 6] expecting 3, returning ", find_smallest_positive_multiple_of_three([-3, 0, 2, 3, 1, 6]))  # expect 3
    print("Input: [1, 2, 5] expecting none, returning ", find_smallest_positive_multiple_of_three([1, 2, 5]))                      # expect None

    # --- Test sequential_search & binary_search ---
    print("\nTesting searches:")
    nums = [2, 5, 10, 20]
    print("Sequential search for 10, expecting true, returns ", sequential_search(10, nums))
    print("Binary search for 15, expecting false, returns", binary_search(15, nums))

if __name__ == "__main__":
    main()
