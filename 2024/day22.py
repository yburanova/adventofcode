filepath = "day22.txt"
import numpy as np

STOP_NUMBER = 2000

def read_file():
    return (int(line.strip()) for line in open(filepath))

def mix_secret(given, secret):
    return given ^ secret

def prune_secret(secret):
    return secret % 16777216

def simulate_secrets(secret, how_many):
    for i in range(how_many):
        secret = prune_secret(mix_secret(secret * 64, secret))
        secret = prune_secret(mix_secret(secret // 32, secret))
        secret = prune_secret(mix_secret(secret * 2048, secret))

    return secret

def simulate_diffs(secret, how_many):
    last_numbers = []

    for i in range(how_many):
        last_numbers.append(int(str(secret)[-1]))
        secret = prune_secret(mix_secret(secret * 64, secret))
        secret = prune_secret(mix_secret(secret // 32, secret))
        secret = prune_secret(mix_secret(secret * 2048, secret))
    diffs = np.diff(last_numbers)
    return last_numbers, diffs.tolist()

def generate_patterns(diffs):
    patterns = []
    for i in range(len(diffs) - 3):
        patterns.append(tuple(diffs[i:i + 4]))
    return patterns

# Find when a pattern first occurs for a buyer
def find_pattern_start(last_numbers, pattern):
    diffs = np.diff(last_numbers)
    for i in range(len(diffs) - 3):
        if tuple(diffs[i:i + 4]) == pattern:
            return i
    return -1


def solve_part_i():
    initials = read_file()
    result = 0
    for initial in initials:
        secret = simulate_secrets(initial, STOP_NUMBER)
        result += secret

    print("Part I:", result)

def solve_part_ii():
    initials = read_file()
    max_bananas = 0
    best_pattern = None
    all_patterns = set()
    all_last_numbers = []

    for initial in initials:
        last_numbers, diffs = simulate_diffs(initial, STOP_NUMBER)
        all_last_numbers.append(last_numbers)
        patterns = generate_patterns(diffs)
        all_patterns.update(patterns)

    print(f"{len(all_patterns)} patterns found")
    for pattern in all_patterns:
        total_bananas = 0
        for last_numbers in all_last_numbers:
            idx = find_pattern_start(last_numbers, pattern)
            if idx != -1:
                total_bananas += last_numbers[idx+4]

        # Track the best pattern
        if total_bananas > max_bananas:
            max_bananas = total_bananas
            best_pattern = pattern
            print("Best max bananas so far...", max_bananas)

    print("Best Patterns", best_pattern)
    print("Part I:", max_bananas)

#solve_part_i()
solve_part_ii()
