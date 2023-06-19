from cs50 import get_int


def main():
    while True:
        n = get_int("Height: ")
        if n < 9 and n > 0:
            break

    draw(n)


def draw(n):
    for i in range(1, n + 1):
        print(" " * (n - i) + "#" * i + "  " + "#" * i)


if __name__ == "__main__":
    main()