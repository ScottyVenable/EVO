import pygame
import random

# Define constants
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
FPS = 4

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Evolution Simulation")

# Define parameters
population_size = 50
food_scarcity = 0.006
lifespan = 300
mutation_rate = 0.02

# Define classes
class Organism(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((10, 10))
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
                self.rect.top = HEIGH


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

# Create organisms and food
for _ in range(population_size):
    organism = Organism(random.randint(0, WIDTH), random.randint(0, HEIGHT))
    organisms.add(organism)

for _ in range(int(WIDTH * HEIGHT * food_scarcity)):
    food = Food()
    foods.add(food)

# Game loop
clock = pygame.time.Clock()
running = False

while not running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = True

    # Update organisms
    for organism in organisms:
        organism.update()
        if not organism.alive:
            organisms.remove(organism)
            new_organism = organism.reproduce()
            if new_organism:
                organisms.add(new_organism)

    # Check for collisions
    hits = pygame.sprite.groupcollide(organisms, foods, False, True)
    for organism, food_list in hits.items():
        for _ in food_list:
            new_organism = organism.reproduce()
            if new_organism:
                organisms.add(new_organism)

    # Draw everything
    screen.fill(WHITE)
    organisms.draw(screen)
    foods.draw(screen)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
