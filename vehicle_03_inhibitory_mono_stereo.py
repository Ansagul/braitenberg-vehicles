import pygame
import math
import random

# Initialize Pygame and font system
pygame.init()
pygame.font.init()
font = pygame.font.SysFont("Arial", 20)

# Setting up the screen dimensions and window title
WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Vehicle 3A & 3B")

# Setting the frame rate
clock = pygame.time.Clock()
fps = 120

# Defining the colors for later use
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)

# Activation functions for sensor processing
def inverse_distance(d):
    return 1 / d if d != 0 else 1

def threshold(d):
    return inverse_distance(d) if d > 150 else 0

def sinoside(d):
    return math.sin(d / 100)  # scaled down for more realistic values

# Defining a Circle class to draw the sun
class Circle:
    def __init__(self, position, radius=50, color=YELLOW):
        self.position = pygame.math.Vector2(position)
        self.radius = radius
        self.color = color

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, self.position, self.radius)

# Creating a Vehicle class with mono/stereo, crossed wiring, and inhibition
class Vehicle:
    def __init__(self, position, direction, color, mono=True, cross=False, inhibitory=True):
        self.position = pygame.math.Vector2(position)
        self.direction = direction  # angle in degrees
        self.color = color
        self.radius = 30

        # Sensor configuration
        self.sensor_offset = self.radius + 10
        self.sensor_radius = 8

        # Behavior toggles
        self.mono = mono
        self.cross = cross
        self.inhibitory = inhibitory
        self.noise = True  

        # Movement behavior tuning
        self.speed_scaling = 2
        self.rotation_scaling = 3
        self.friction = 0.98 

        self.update_sensors()

    # Calculate the world position of the sensors based on vehicle direction
    def update_sensors(self):
        forward = pygame.math.Vector2(0, -self.sensor_offset)
        self.sensor_left = self.position + forward.rotate(self.direction - 30)
        self.sensor_right = self.position + forward.rotate(self.direction + 30)

    # Draw the vehicle body and sensors
    def draw(self, surface):
        pygame.draw.circle(surface, self.color, self.position, self.radius)
        pygame.draw.circle(surface, GREEN, self.sensor_left, self.sensor_radius)
        if not self.mono:
            pygame.draw.circle(surface, GREEN, self.sensor_right, self.sensor_radius)

    # Move function controlling vehicle behavior
    def move(self, sun_position):
        if self.mono:
            # In mono, only one sensor is active
            d = self.sensor_left.distance_to(sun_position)
            act = sinoside(d) 
            #inverse_distance and threshold can also be used but it shows different behaviors 
            #one reason can be different scaling is required for each function. Normalizing can help solve this issue
            speed = 1 - act if self.inhibitory else act
            left_speed = right_speed = speed
        else:
            # Stereo behavior: each sensor controls a motor
            d_left = self.sensor_left.distance_to(sun_position)
            d_right = self.sensor_right.distance_to(sun_position)

            # If crossed, inputs are swapped
            left_act = sinoside(d_right)
            right_act = sinoside(d_left)

            if self.inhibitory:
                left_speed = 1 - left_act
                right_speed = 1 - right_act
            else:
                left_speed = left_act
                right_speed = right_act

        # Add noise to simulate imperfect motor control
        if self.noise:
            left_speed += random.uniform(-0.05, 0.05)
            right_speed += random.uniform(-0.05, 0.05)

        # Clamp speeds to [0, 1] range
        left_speed = max(0, min(1, left_speed))
        right_speed = max(0, min(1, right_speed))

        # Compute rotation based on difference in motor speeds
        rotation = (right_speed - left_speed) * self.rotation_scaling
        if self.cross:
            rotation *= -1  # Reverses turn direction if wiring is crossed

        # Add directional noise/jitter if enabled
        if self.noise:
            self.direction += rotation + random.uniform(-0.5, 0.5)
        else:
            self.direction += rotation

        # Compute final movement vector
        avg_speed = (left_speed + right_speed) / 2
        avg_speed *= self.speed_scaling
        avg_speed *= self.friction  # slow down based on friction

        move_vec = pygame.math.Vector2(0, -1).rotate(self.direction)
        self.position += move_vec * avg_speed
        self.position.x %= WIDTH
        self.position.y %= HEIGHT

        # Update sensor positions after movement
        self.update_sensors()

# Creating the sun 
sun = Circle((WIDTH // 2, HEIGHT // 2), radius=30, color=YELLOW)

# Creating the two vehicles with different configurations
# Vehicle 3A: Mono sensor, inhibitory behavior
vehicle_3a = Vehicle((100, 500), 55, RED, mono=True, cross=False, inhibitory=True)

# Vehicle 3B: Stereo, inhibitory, crossed wiring
vehicle_3b = Vehicle((500, 500), 55, BLUE, mono=False, cross=True, inhibitory=True)

# Main simulation loop
running = True
while running:
    screen.fill((0, 0, 0))  # background
    sun.draw(screen)

    # Event handling for quit and keyboard toggles
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            # Toggle mono/stereo mode for both vehicles
            if event.key == pygame.K_m:
                vehicle_3a.mono = not vehicle_3a.mono
                vehicle_3b.mono = not vehicle_3b.mono

            # Toggle noise for both vehicles
            if event.key == pygame.K_n:
                vehicle_3a.noise = not vehicle_3a.noise
                vehicle_3b.noise = not vehicle_3b.noise
                print(f"Noise toggled: {vehicle_3a.noise}")

    # Update and draw both vehicles
    vehicle_3a.move(sun.position)
    vehicle_3b.move(sun.position)
    vehicle_3a.draw(screen)
    vehicle_3b.draw(screen)

    # Display configuration info
    label_3a = font.render("3A - Mono, Inhibitory", True, WHITE)
    label_3b = font.render("3B - Stereo, Inhibitory, Crossed", True, WHITE)
    noise_label = font.render(f"Noise: {'ON' if vehicle_3a.noise else 'OFF'} (press N)", True, WHITE)

    screen.blit(label_3a, (10, HEIGHT - 60))
    screen.blit(label_3b, (10, HEIGHT - 35))
    screen.blit(noise_label, (10, HEIGHT - 20))

    pygame.display.flip()
    clock.tick(fps)

pygame.quit()
