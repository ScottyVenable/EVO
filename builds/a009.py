import pygame
import random
from OpenGL.GL import *

# Define constants
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
FPS = 30

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.OPENGL | pygame.DOUBLEBUF)
pygame.display.set_caption("Evolution Simulation")

# OpenGL initialization
glMatrixMode(GL_PROJECTION)
glLoadIdentity()
glOrtho(0, WIDTH, HEIGHT, 0, -1, 1)
glMatrixMode(GL_MODELVIEW)

# Define parameters
population_size = 5
food_scarcity = 0.01
lifespan = 75
mutation_rate = 0.02
reproduction_chance = 0.03  # Chance of reproducing in each frame

# Define classes
class Organism:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.age = 0
        self.alive = True
        self.mutation = random.uniform(-mutation_rate, mutation_rate)
        self.velocity = [random.uniform(-1, 1), random.uniform(-1, 1)]  # Random initial velocity

    def update(self):
        if self.alive:
            self.age += 1
            if self.age > lifespan:
                self.alive = False

            # Update position based on velocity
            self.x += self.velocity[0]
            self.y += self.velocity[1]

            # Wrap around the screen edges (optional)
            if self.x > WIDTH:
                self.x = 0
            elif self.x < 0:
                self.x = WIDTH
            if self.y > HEIGHT:
                self.y = 0
            elif self.y < 0:
                self.y = HEIGHT

    def draw(self):
        # Draw the organism using OpenGL
        w, h = 10, 10  # Size of the organism
        glColor3f(0, 1, 0)  # Set color (green)
        glBegin(GL_QUADS)
        glVertex2f(self.x - w / 2, self.y - h / 2)
        glVertex2f(self.x + w / 2, self.y - h / 2)
        glVertex2f(self.x + w / 2, self.y + h / 2)
        glVertex2f(self.x - w / 2, self.y + h / 2)
        glEnd()

# Define the reproduction function
def reproduce(organism):
    if organism.alive and random.random() < reproduction_chance:
        offspring = Organism(
            organism.x + random.randint(-10, 10),
            organism.y + random.randint(-10, 10)
        )
        offspring.age = 0
        organisms.append(offspring)

class Food:
    def __init__(self):
        # Changed the size of food to 3x3
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(0, HEIGHT)

    def draw(self):
        # Draw the food using OpenGL
        w, h = 3, 3  # Size of the food
        glColor3f(1, 0, 0)  # Set color (red)
        glBegin(GL_QUADS)
        glVertex2f(self.x - w / 2, self.y - h / 2)
        glVertex2f(self.x + w / 2, self.y - h / 2)
        glVertex2f(self.x + w / 2, self.y + h / 2)
        glVertex2f(self.x - w / 2, self.y + h / 2)
        glEnd()

# Create lists for organisms and food
organisms = [Organism(random.randint(0, WIDTH), random.randint(0, HEIGHT)) for _ in range(population_size)]
foods = [Food() for _ in range(int(WIDTH * HEIGHT * food_scarcity))]

# Game loop
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    glClear(GL_COLOR_BUFFER_BIT)
    
    # Draw organisms and food using OpenGL
    for organism in organisms:
        organism.update()
        organism.draw()

    for food in foods:
        food.draw()
    
    # Check for collisions
    hits = []  # Store indices of organisms that collided with food
    for i, organism in enumerate(organisms):
        for j, food in enumerate(foods):
            if abs(organism.x - food.x) < 5 and abs(organism.y - food.y) < 5:
                hits.append(i)
                break

    # Remove collided organisms and spawn offspring
    for i in reversed(hits):
        reproduce(organisms[i])
        del organisms[i]

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
