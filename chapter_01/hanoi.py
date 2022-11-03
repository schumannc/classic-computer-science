from typing import TypeVar, Generic, List


def hanoi(begin: list[int], end: list[int], temp: list[int], n: int) -> None:
    if n == 1:
        end.append(begin.pop())
    else:
        hanoi(begin, temp, end, n - 1)
        hanoi(begin, end, temp, 1)
        hanoi(temp, end, begin, n - 1)


if __name__ == "__main__":
    num_discs = 3
    tower_a = sorted([i for i in range(1, num_discs + 1)], reverse=True)
    tower_b, tower_c = [], []

    hanoi(tower_a, tower_c, tower_b, num_discs)
    print(tower_a)
    print(tower_b)
    print(tower_c)