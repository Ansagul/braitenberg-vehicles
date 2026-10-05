import pygame
import math

pygame.init()

# Setting up the screen dimensions and window title
WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Braitenberg Vehicle 2")

# Initializing font for displaying debug text
pygame.font.init()
font = pygame.font.SysFont("Arial", 20)

# Setting the frame rate
clock = pygame.time.Clock()
fps = 60

# Defining the colors for later use
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Defining a Circle class to draw the sun and vehicle body
class Circle:
    def __init__(self, position, radius=50, color=RED):
        self.position = pygame.math.Vector2(position)
        self.radius = radius
        self.color = color

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, self.position, self.radius)

# Creating a Vehicle class with sensor-controlled movement based on light (sun) location
class Vehicle:
    def __init__(self, position, direction, radius=30, color=RED):
        self.position = pygame.math.Vector2(position)
        self.direction = direction  # angle in degrees
        self.radius = radius
        self.color = color

        self.speed_scaling = 1500  # used to control movement speed based on sensor distance
        self.sensor_radius = 10
        self.sensor_offset = self.radius + self.sensor_radius  # how far forward the sensors are placed
        self.sensor_spacing = 40  # distance between the left and right sensors
        self.sensor_color = GREEN

    # Drawing the vehicle body and its sensors
    def draw(self, surface):
        pygame.draw.circle(surface, self.color, self.position, self.radius)
        pygame.draw.circle(surface, self.sensor_color, self.left_sensor_position, self.sensor_radius)
        pygame.draw.circle(surface, self.sensor_color, self.right_sensor_position, self.sensor_radius)

    # Updating the positions of left and right sensors based on vehicle direction
    def update_sensors(self):
        forward = pygame.math.Vector2(0, -1).rotate(self.direction)
        right = forward.rotate(-90)

        self.left_sensor_position = self.position + forward * self.sensor_offset - right * (self.sensor_spacing / 2)
        self.right_sensor_position = self.position + forward * self.sensor_offset + right * (self.sensor_spacing / 2)
         # Counterfactual: sensors placed *behind* the vehicle
        #base = self.position - forward * self.sensor_offset
        #self.left_sensor_position = base - right * (self.sensor_spacing / 2)
        #self.right_sensor_position = base + right * (self.sensor_spacing / 2)
    # Controlling vehicle movement based on sensor readings
    def move(self, sun_position):
        # Update the sensor positions first
        self.update_sensors()

        # Measure distances from each sensor to the sun
        left_distance = self.left_sensor_position.distance_to(sun_position)
        right_distance = self.right_sensor_position.distance_to(sun_position)

        # Inverse of distance gives light intensity (closer = brighter)
        left_speed = self.speed_scaling / (left_distance + 1)
        right_speed = self.speed_scaling / (right_distance + 1)
        #FOR CROSSED WIRING:left sensor to right motor, right sensor to left motor
        #left_motor_speed =  self.speed_scaling / (right_distance + 1)
        #right_motor_speed = self.speed_scaling / (left_distance + 1)

        # Vehicle 2 behavior: each sensor controls motor on the same side
        speed = (left_speed + right_speed) 
        rotation = (right_speed - left_speed) * 0.5  # turn rate based on difference

        # Update direction and position of the vehicle
        self.direction += rotation
        direction_vector = pygame.math.Vector2(0, -1).rotate(self.direction)
        self.position += direction_vector * speed * (0.1)

        # Keep the vehicle within screen bounds
        self.position.x %= WIDTH
        self.position.y %= HEIGHT

        # Render debug information
        text = f"Left Dist: {left_distance:.2f} | Right Dist: {right_distance:.2f}\nSpeed: {speed:.2f}"
        lines = text.split('\n')
        for i, line in enumerate(lines):
            text_surface = font.render(line, True, WHITE)
            screen.blit(text_surface, (10, 10 + i * 20))

# Creating a sun and a vehicle
sun = Circle((WIDTH // 2, HEIGHT // 2), radius=30, color=YELLOW)
vehicle = Vehicle((300, 500), 0)

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update screen and objects
    screen.fill((0, 0, 0))  # black background
    sun.draw(screen)
    vehicle.move(sun.position)
    vehicle.draw(screen)

    pygame.display.flip()
    clock.tick(fps)

pygame.quit()
