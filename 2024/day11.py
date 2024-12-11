filepath = "day11.txt"

def blink(stones):
    new_stones = {}
    for stone, counter in stones.items():
        result = blink_single_stone(stone)
        if isinstance(result, int):
            new_stones[result] = new_stones.get(result, 0) + counter
        else:
            for x in result:
                new_stones[x] = new_stones.get(x, 0)  + counter

    return new_stones

def blink_single_stone(stone):
    if stone == 0:
        return 1
    elif len(str(stone)) % 2 == 0:
        l = int(len(str(stone)) / 2)
        return int(str(stone)[:l]), int(str(stone)[l:])
    else:
        return stone * 2024

def solve_part_i():
    with open(filepath) as file:
        line = file.readline().strip()

    stones = {}
    for i in map(int, line.split()):
        stones[i] = stones.setdefault(i, 0) + 1

    for i in range(75):
        print("Blink", i+1, ": ", end='')
        stones = blink(stones)
        #print(stones)

    stones_len = sum(v for k, v in stones.items())
    print(stones_len)


solve_part_i()