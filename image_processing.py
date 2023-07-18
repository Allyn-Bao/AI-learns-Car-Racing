import cv2
import numpy as np

def get_boundary_points(image_path, num_points):
    # Load the image and convert to grayscale
    image = cv2.imread(image_path)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Threshold the grayscale image to create binary images for orange and blue
    _, orange_binary = cv2.threshold(gray_image, 100, 255, cv2.THRESH_BINARY)
    _, blue_binary = cv2.threshold(gray_image, 50, 255, cv2.THRESH_BINARY_INV)

    # Find contours for orange and blue
    orange_contours, _ = cv2.findContours(orange_binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    blue_contours, _ = cv2.findContours(blue_binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Approximate the contours and extract points with given density
    orange_points_list = []
    for contour in orange_contours:
        epsilon = 0.02 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)

        if len(approx) >= num_points:
            indices = np.linspace(0, len(approx) - 1, num_points, dtype=int)
            orange_points_list.append([tuple(approx[i][0]) for i in indices])

    blue_points_list = []
    for contour in blue_contours:
        epsilon = 0.02 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)

        if len(approx) >= num_points:
            indices = np.linspace(0, len(approx) - 1, num_points, dtype=int)
            blue_points_list.append([tuple(approx[i][0]) for i in indices])

    # Return the dictionary containing the lists of points with labels
    return {"orange": orange_points_list, "blue": blue_points_list}

# Usage example:
image_path = "track_boundary_image.png"
num_points = 100  # Adjust the number of points as needed

boundary_points_dict = get_boundary_points(image_path, num_points)
print(boundary_points_dict)
