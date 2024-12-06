import math

def calculate_circle_area(radius):
    if radius < 0:
        raise ValueError("Radius cannot be negative")
    return math.pi * (radius ** 2)

# Example usage:
radius = 5
area = calculate_circle_area(radius)
print("The area of the circle is:", area)