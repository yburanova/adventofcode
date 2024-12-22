filepath = "day22.txt"

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


def solve_part_i():
    initials = read_file()
    result = 0
    for initial in initials:
        secret = simulate_secrets(initial, STOP_NUMBER)
        print(secret)
        result += secret

    print("Part I:", result)

solve_part_i()