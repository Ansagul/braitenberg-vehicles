import pygame

pygame.init()
# Defining the frame and it#s caption here 
WIDTH, HEIGHT = 1200, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Braitenberg Vehicle")
# Defining the colors that will be used later in the code. Yellow for Sun, Red for Vehicle, Green for Sensor 
# and white was used for background in class but I am keeping the background black. 
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)

#Deifing a circle with variables position, radius and color. It will be used to draw all elements 
class Circle:
    def __init__(self, position, radius=50, color=RED):
        self.position = pygame.math.Vector2(position)
        self.radius = radius
        self.color = color

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, self.position, self.radius)
#Defining a Vehicle with an additional variable of direction and attaching a sensor with radius=15 to it. 
class Vehicle:
    def __init__(self, position, direction, radius=50, color=RED):
        self.position = pygame.math.Vector2(position)
        self.radius = radius
        self.color = color
        self.direction = direction
        self.sensor_radius = 15
        self.sensor_offset = self.radius + self.sensor_radius
        self.sensor_color = GREEN
        self.sensor_position = self.position + pygame.math.Vector2(0, -self.sensor_offset).rotate(self.direction)
        
    #Drawing the circles for Vehicle and Sensor 
    def draw(self, surface):
        pygame.draw.circle(surface, self.color, self.position, self.radius)
        pygame.draw.circle(surface, self.sensor_color, self.sensor_position, self.sensor_radius)
    #Distance to sun can be measured by sun's position
    def calculate_distance_to_sun(self, sun_position):
        return self.sensor_position.distance_to(sun_position)
    #Defining how the vehicle will move according to the sun's position 
    def move(self, sun_position):
        #sensor positon will move with vehicle and turn where required along the radius of the vehicle 
        self.sensor_position = self.position + pygame.math.Vector2(0, -self.sensor_offset).rotate(self.direction)
        #creating a vector to follow in the direction of sun by finding the difference in position of vehicle and sun 
        offset = sun_position - self.position
        if offset.length() == 0:
            return
        move_to_sun = offset.normalize()
        #defining the motion in which the vehicle will move
        forward = pygame.math.Vector2(0, -1).rotate(self.direction)
        #aligining the angle to the sun using the diection found in move_to_sun
        angle_to_sun = forward.angle_to(move_to_sun)
        #defining an arbitrary turn rate 
        turn_rate = 2  
        #definig the turning in a way that it only turns 2 degrees per frame 
        # and doesn't turn more clockwise or anticlockwose (using -sing)
        self.direction += max(-turn_rate, min(turn_rate, angle_to_sun))
        #finding distance to the sun to control spee d of the vehicle
        distance = self.position.distance_to(sun_position)
        #defining arbitrary maximum and minimum speed and distance 
        max_distance = 500
        max_speed = 4
        #intensity is basically finiding to find how fast or slow the speed should 
        # be depending on the distance. 
        intensity = max(0, max_distance - distance) / max_distance
        speed = intensity * max_speed
        #defining the movements 
        direction_vector = pygame.math.Vector2(0, -1).rotate(self.direction)
        self.position += direction_vector * speed
        self.sensor_position = self.position + pygame.math.Vector2(0, -self.sensor_offset).rotate(self.direction)
        
#Giving parameters to already defined objects to run the program 
sun = Circle((600, 300), radius=30, color=YELLOW)
vehicle = Vehicle((300, 500), 45)

clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    #took help from chatgpt to use mouse cursor as the position of the sun 
    sun.position = pygame.math.Vector2(pygame.mouse.get_pos())
    vehicle.move(sun.position)
#displaying the results 
    screen.fill((0, 0, 0))
    sun.draw(screen)
    vehicle.draw(screen)
    pygame.display.flip()

    clock.tick(60)

pygame.quit()
