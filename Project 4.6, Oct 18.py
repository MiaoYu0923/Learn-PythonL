def display_title():
    print("Prime Number Checker")
    print()

def get_valid_int():
    while True:
        num = int(input("Please enter a number between 1 and 5000: "))
        if num <= 1 or num >= 50000:
            print("Invaild number. Pls try again.")
        else:
            return num

def get_factor_count(num):
    factor_count = 0
    #this loop includes 1 and num
    for i in range(1, num + 1):
        reminder = num % i
        if reminder == 0:
            factor_count += 1
    return factor_count

def main():
    display_title()
    again = "y"
    while again == "y":
        num = get_valid_int()
        factor_count = get_factor_count(num)
        if factor_count == 2:
            print(num, "is a prime number.")
        else:
            print(num, "is not a prime number.")
            print("It has", factor_count, "factors.")
        print()
        again = input("Try again? (y/n): ")
        print()
    print("Bye!")
#if it started as the main module, call the main function
if __name__ == "__main__":
    main()
