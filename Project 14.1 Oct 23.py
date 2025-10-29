

class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height
    def width(self):
        return self.width
    def height(self):
        return self.height
    def get_perimeter(self):
        return 2 * (self.width + self.height)
    def get_area(self):
        return self.width * self.height
    def string_representation(self):
        w = self.width
        h = self.height
        for i in range(h):
            if i == 0 or i == h-1:
                print("* " * w)
            else:
                print("* " + "  " * (w-2) + "*")



    def display(self):
        print("Rectangle Calculator")
        print()
        print("Height: " + str(self.height))
        print("Width: " + str(self.width))
        print("Perimeter: " + str(self.get_perimeter()))
        print("Area: "+ str(self.get_area()))
        print()
        print(self.string_representation())

def main():
    choice = True
    while choice:
        width = int(input("Width: "))
        height = int(input("Height: "))
        rectangle = Rectangle(width, height)
        rectangle.display()
        choice = input("Continue? (y/n): ")
        if choice == "n":
            print()
            print("Bye")
            break
        elif choice == "y":
            continue
        else:
            print("Invalid input")

if __name__ == "__main__":
    main()







