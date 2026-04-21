def hanoi(n, source, target, auxiliary):
    """Solve Tower of Hanoi and print moves."""
    if n == 1:
        print(f"Move disk 1 from {source} to {target}")
        return
    hanoi(n - 1, source, auxiliary, target)
    print(f"Move disk {n} from {source} to {target}")
    hanoi(n - 1, auxiliary, target, source)


def main():
    print("Tower of Hanoi Solver")
    print("-" * 40)

    while True:
        try:
            levels = int(input("Enter the number of tower levels (1-10): "))
            if 1 <= levels <= 10:
                break
            print("Please enter a number between 1 and 10.")
        except ValueError:
            print("Invalid input. Please enter a number.")

    print(f"\nSolving Tower of Hanoi with {levels} levels...")
    print(f"Total moves required: {2**levels - 1}\n")

    hanoi(levels, "A", "C", "B")

    print("\nDone!")


if __name__ == "__main__":
    main()
