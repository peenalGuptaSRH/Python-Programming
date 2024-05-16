import ast
def count_squares(coords):
    point_set = {(x, y) for x, y in coords}  # Converts list to set for quick lookups
    squares = 0

    for (x1, y1) in point_set:
        for (x2, y2) in point_set:
            if x1 != x2 and y1 != y2:  # Ensures that we are looking at potential diagonal points of a square
                # Checks for existence of the other two corners of the square
                if (x1, y2) in point_set and (x2, y1) in point_set:
                    # Verifies that the shape is indeed a square by comparing the lengths
                    if abs(x1 - x2) == abs(y1 - y2):
                        squares += 1  # Found a square

    return squares // 4  # Each square is counted 4 times, so divide by 4

def get_coords_from_user():
    coords = []
    try:
        # coordinates = [[0,0],[0,1],[1,1],[1,0],[2,1],[2,0],[3,1],[3,0]]
        user_input_coordinates  = input("Enter coordinates in the format [(x1, y1), (x2, y2), ...]: ")
        # Convert the string to a list of lists
        result_coordinates = ast.literal_eval(user_input_coordinates)
        coords = []  # Initialize an empty list to store the coordinates
        for coordinate in result_coordinates:
            x, y = coordinate
            coords.append((x,y))
    except ValueError:
        # Catch the ValueError and ask for the input again
        print("Invalid input. Please enter exactly two integers separated by a comma, e.g., 3, 4.")
    # return coords
    print(coords)
    return coords
# Get coordinates from the user
user_coords = get_coords_from_user()
# Calculate and print the number of squares
print(f"Number of squares formed: {count_squares(user_coords)}")




# Time Complexity Analysis #O(n) time is required to convert a list of coordinates into a set, where n is the number of coordinates.
# Because each coordinate is compared with every other coordinate, the nested loop iterates through every pair of coordinates, resulting in an O(n^2) time complexity for this section.
# Because a set is used for coordinate_set, the time it takes to check if the other two corners in the set exist is O(1).
# Because of the nested loop that compares every pair of coordinates to find possible squares, the overall worst-case time complexity is O(n^2).

# Why in this case O(n^2) is optimal
# The O(n^2) complexity is justified by the requirement to compare each coordinate with every other coordinate in order to identify pairs that might form a square's diagonal.