import sys

try:
    x = int(input("x: "))
    y = int(input("y: "))
except ValueError:
    print("Error: Invalid input.")
    sys.exit(1)

try: ## used to handle ZeroDivisionError exception so program doesn't crash.
    result = x / y
except ZeroDivisionError:
    print("Error: Cannon divide by 0.")
    sys.exit(1)


print(f"{x} / {y} = {result}")