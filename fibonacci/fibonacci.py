from functools import lru_cache
from typing import Generator


@lru_cache(maxsize=None)
def fib(n: int) -> int:
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)


def fib_generator(n: int)-> Generator[int, None, None]:
    yield 0
    if n > 0: yield 1
    last: int = 0
    next: int = 1
    for _ in range(1, n):
        last, next = next, last + next
        yield next


if __name__ == '__main__':
    assert fib(8) == 21, "Fail"
    assert [i for i in fib_generator(8)] == [0, 1, 1, 2, 3, 5, 8, 13, 21]
    