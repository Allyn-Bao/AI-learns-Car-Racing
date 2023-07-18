import pygame
import os
import sys

# Initialize Pygame
pygame.init()

# Set the dimensions of the display window
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Car Racing Game")

"""
Assets
"""
# Path to assets
track_image_path = os.path.join("assets", "Circuit.jpg")
track_boundary_image_path = os.path.join("assets", "track-boundary.jpg")
track_limit_image_path = os.path.join("assets", "track-limit.jpg")
# Load the background image and track boundary contour image
background_image = pygame.image.load(track_image_path).convert()
boundary_image = pygame.image.load(track_boundary_image_path).convert_alpha()
limit_image = pygame.image.load(track_limit_image_path).convert()

# Set the car's position and dimensions
car_width = 50
car_height = 80
car_x = (screen_width - car_width) // 2
car_y = screen_height - car_height - 20

# Set the car's movement speed
car_speed = 5

def draw_track_boundary(x_offset):
    screen.blit(boundary_image, (x_offset, 0))

def main():
    # Set the initial x_offset for moving the track background
    x_offset = 0

    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Move the track background and track boundary with the car
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            car_x -= car_speed
            x_offset += car_speed
        if keys[pygame.K_RIGHT]:
            car_x += car_speed
            x_offset -= car_speed

        # Draw the background image
        screen.blit(background_image, (x_offset, 0))

        # Draw the track boundary with offset
        draw_track_boundary(x_offset)

        # Draw the car
        pygame.draw.rect(screen, (255, 0, 0), (car_x, car_y, car_width, car_height))

        # Update the display
        pygame.display.update()

        # Limit the frame rate
        clock.tick(60)

if __name__ == "__main__":
    main()
