import cv2
import numpy as np
import pygame
import sys

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


def get_limit_points(image_path, num_points):
    # Load the image and convert to grayscale
    image = cv2.imread(image_path)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Threshold the grayscale image to create a binary image for white lines
    _, binary_image = cv2.threshold(gray_image, 200, 255, cv2.THRESH_BINARY)

    # Find contours for white lines
    contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Approximate the contours and extract points with given density
    limit_points_list = []
    for contour in contours:
        epsilon = 0.02 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)

        if len(approx) >= num_points:
            indices = np.linspace(0, len(approx) - 1, num_points, dtype=int)
            limit_points_list.append([tuple(approx[i][0]) for i in indices])

    # Return the dictionary containing the list of points with the label "limit"
    return {"limit": limit_points_list}


def image_processing_output_test(track_image_path, points_list):
    # Initialize Pygame
    pygame.init()

    # Load the track_image and get its dimensions
    track_image = pygame.image.load(track_image_path)
    image_width, image_height = track_image.get_width(), track_image.get_height()

    # Set the dimensions of the display window
    screen_width = image_width
    screen_height = image_height
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Image Processing Output Test")

    # Set up colors
    white = (255, 255, 255)
    red = (255, 0, 0)

    # Create a Pygame surface for the contour
    contour_surface = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)

    # Main loop
    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Clear the contour surface
        contour_surface.fill((0, 0, 0, 0))

        # Draw the contour on the contour surface
        for points in points_list:
            pygame.draw.lines(contour_surface, red, False, points, 3)

        # Blit the track_image and the contour surface onto the screen
        screen.blit(track_image, (0, 0))
        screen.blit(contour_surface, (0, 0))

        # Update the display
        pygame.display.update()

        # Limit the frame rate
        clock.tick(60)

    pygame.quit()
    sys.exit()





if __name__ == "__main__":
    # Usage example:
    image_path = "track_boundary_image.png"
    num_points = 100  # Adjust the number of points as needed

    boundary_points_dict = get_boundary_points(image_path, num_points)
    print(boundary_points_dict)

    image_path = "track_limit_image.png"
    num_points = 100  # Adjust the number of points as needed

    limit_points_dict = get_limit_points(image_path, num_points)
    print(limit_points_dict)

    # Usage example:
    track_image_path = "track_image.png"
    points_list = [  # Replace this with the output from the previous functions
        # List of points for orange loop
        # List of points for blue loop
        # List of points for track limit
    ]

    image_processing_output_test(track_image_path, points_list)
