def pyramid_pattern(n):
    for i in range(n):
        print(' ' * (n - i - 1) + '*' * (2 * i + 1))


def main():
    print("Hello, World!")
    number = int(input("Enter a number: "))
    pyramid_pattern(number)
    print("Goodbye!")

if __name__ == "__main__":
    main()
