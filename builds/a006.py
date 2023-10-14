# Evolution Simulation - Version a006 (Multithreading)
import pygame
import random
import threading

# Define constants
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
FPS = 30

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Evolution Simulation")

# Define parameters
population_size = 5  # Changed to 5 organisms
food_scarcity = 0.01  # Changed to typical value of 0.01
lifespan = 300
mutation_rate = 0.02
reproduction_chance = 0.01  # Chance of reproducing in each frame

# Define classes
class Organism(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((5, 5))  # Changed the size to match food
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
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
            self.rect.x += self.velocity[0]
            self.rect.y += self.velocity[1]

            # Wrap around the screen edges (optional)
            if self.rect.left > WIDTH:
                self.rect.right = 0
            elif self.rect.right < 0:
                self.rect.left = WIDTH
            if self.rect.top > HEIGHT:
                self.rect.bottom = 0
            elif self.rect.bottom < 0:
                self.rect.top = HEIGHT

# Define the reproduction function
def reproduce(organism):
    if organism.alive and random.random() < reproduction_chance:
        offspring = Organism(
            organism.rect.x + random.randint(-10, 10),
            organism.rect.y + random.randint(-10, 10)
        )
        offspring.image.fill((0, 255, 0))
        offspring.age = 0
        organisms.add(offspring)

class Food(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((5, 5))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH)
        self.rect.y = random.randint(0, HEIGHT)

# Create sprite groups
organisms = pygame.sprite.Group()
foods = pygame.sprite.Group()

# Create 5 organisms initially
for _ in range(population_size):
    organism = Organism(random.randint(0, WIDTH), random.randint(0, HEIGHT))
    organisms.add(organism)

# Create food with typical scarcity
for _ in range(int(WIDTH * HEIGHT * food_scarcity)):
    food = Food()
    foods.add(food)

# Game loop variables
running = True

# Create a lock for synchronization
lock = threading.Lock()

# Define a function for the game logic thread
def game_logic():
    global running
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Update organisms
        with lock:
            for organism in organisms.copy():
                organism.update()
                if not organism.alive:
                    organisms.remove(organism)
                else:
                    reproduce(organism)

        # Check for collisions
        with lock:
            hits = pygame.sprite.groupcollide(organisms, foods, False, True)
            for organism, food_list in hits.items():
                for _ in food_list:
                    reproduce(organism)

        pygame.time.delay(10)  # Add a small delay to reduce CPU usage

# Define a function for the rendering thread
def rendering():
    global running
    while running:
        screen.fill(WHITE)
        with lock:
            organisms.draw(screen)
            foods.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)

# Create game logic and rendering threads
game_logic_thread = threading.Thread(target=game_logic)
rendering_thread = threading.Thread(target=rendering)

# Start both threads
game_logic_thread.start()
rendering_thread.start()

# Wait for both threads to finish
game_logic_thread.join()
rendering_thread.join()

pygame.quit()
