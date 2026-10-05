import pygame
import random
import math

pygame.init()

# Set up the window size and caption
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Braitenberg Vehicle 1 - Collision Simulation")

# Initialize font for displaying text
pygame.font.init()
font = pygame.font.SysFont("Arial", 16)

# Set up the clock for controlling the frame rate
clock = pygame.time.Clock()
fps = 60

# Define basic colors to be used in the simulation
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# Number of vehicles to be simulated
NUM_VEHICLES = 10


# Circle class is used for both the sun and vehicles (since they are circles)
class Circle:
    def __init__(self, position, radius=50, color=RED):
        self.position = pygame.math.Vector2(position)  # Position is a 2D vector
        self.radius = radius  # Radius of the circle
        self.color = color  # Color of the circle

    def draw(self, surface):
        # Draw the circle on the given surface
        pygame.draw.circle(surface, self.color, self.position, self.radius)


# Vehicle class defines each vehicle's behavior
class Vehicle:
    def __init__(self, position, direction, radius=15, color=RED):
        self.position = pygame.math.Vector2(position)  # Position as a 2D vector
        self.direction = direction  # Direction vehicle is facing in degrees
        self.radius = radius  # Vehicle's radius
        self.color = color  # Vehicle color

        # Scaling factors for speed and sensor behavior
        self.speed_scaling = 300
        self.sensor_radius = 5  # Sensor radius
        self.sensor_offset = self.radius + self.sensor_radius  # Distance of sensors from center
        self.sensor_spacing = 25  # Space between the left and right sensors
        self.sensor_color = GREEN  # Sensor color

    def update_sensors(self):
        # Calculate sensor positions based on vehicle's direction
        forward = pygame.math.Vector2(0, -1).rotate(self.direction)  # Direction vector
        right = forward.rotate(-90)  # Right vector for spacing sensors

        # Update the positions of left and right sensors based on the direction and offset
        self.left_sensor_position = self.position + forward * self.sensor_offset - right * (self.sensor_spacing / 2)
        self.right_sensor_position = self.position + forward * self.sensor_offset + right * (self.sensor_spacing / 2)

    def move(self, sun_position):
        # Update sensor positions
        self.update_sensors()

        # Calculate distances from sensors to the sun
        left_distance = self.left_sensor_position.distance_to(sun_position)
        right_distance = self.right_sensor_position.distance_to(sun_position)

        # Vehicle 1 logic: Left sensor affects right motor and vice versa
        left_speed = self.speed_scaling / (right_distance + 1)  # Inverse distance effect on speed
        right_speed = self.speed_scaling / (left_distance + 1)

        # Calculate the average speed and the difference in speed for rotation
        speed = (left_speed + right_speed) / 2
        rotation = (left_speed - right_speed) * 0.5

        # Update the vehicle's direction and position
        self.direction += rotation
        direction_vector = pygame.math.Vector2(0, -1).rotate(self.direction)
        self.position += direction_vector * speed  # Move the vehicle based on the direction and speed

        # Wrap the vehicle around the screen if it goes off the edges
        self.position.x %= WIDTH
        self.position.y %= HEIGHT

    def draw(self, surface):
        # Draw the vehicle (circle) and its sensors (smaller circles)
        pygame.draw.circle(surface, self.color, self.position, self.radius)
        pygame.draw.circle(surface, self.sensor_color, self.left_sensor_position, self.sensor_radius)
        pygame.draw.circle(surface, self.sensor_color, self.right_sensor_position, self.sensor_radius)

    def check_collision(self, other):
        # Avoid self-collision by checking if it's the same object
        if self == other:
            return False
        # Check if the distance between the two vehicles is less than the sum of their radii (i.e., collision)
        distance = self.position.distance_to(other.position)
        return distance < self.radius + other.radius

    def reflect(self):
        # When a collision is detected, make the vehicle reflect (bounce) in a random direction
        self.direction += 180 + random.uniform(-20, 20)  # Reflect and add some random jitter
        self.direction %= 360  # Keep the direction between 0 and 360 degrees


# Create the sun object (stationary at the center of the screen)
sun = Circle((WIDTH // 2, HEIGHT // 2), radius=40, color=YELLOW)

# Create a list of vehicles with random positions and directions
vehicles = []
for _ in range(20):
    pos = (random.randint(0, WIDTH), random.randint(0, HEIGHT))  # Random position
    dir = random.uniform(0, 360)  # Random direction (0-360 degrees)
    vehicles.append(Vehicle(pos, dir, color=RED))

# Main simulation loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Check if the quit event is triggered (e.g., closing the window)
            running = False

    # Clear the screen and draw the sun
    screen.fill(BLACK)
    sun.draw(screen)

    # Update and move each vehicle
    for v in vehicles:
        v.move(sun.position)

    # Check for collisions between vehicles and make them reflect (bounce)
    for i, v1 in enumerate(vehicles):
        for v2 in vehicles[i+1:]:  # Only check for pairwise collisions once
            if v1.check_collision(v2):
                v1.reflect()  # Reflect the first vehicle
                v2.reflect()  # Reflect the second vehicle

    # Draw each vehicle on the screen
    for v in vehicles:
        v.draw(screen)

    # Update the screen with the new frame
    pygame.display.flip()
    
    # Control the frame rate to ensure smooth simulation
    clock.tick(fps)

# Quit pygame when the simulation ends
pygame.quit()
