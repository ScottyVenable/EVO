# Evolution Simulation - Version a013 STABLE -- added seeking for food
import math
import pygame
import random
import pygame.font

# Define constants
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
FPS = 30



# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Evolution Simulation")

# Define parameters
population_size = 5
max_population_size = 12
food_scarcity = 0.0005
lifespan = 20000
mutation_rate = 0.02
reproduction_chance = 0.03  # Chance of reproducing in each frame
speed_multiplier = 1.0  # Initial speed multiplier
min_speed_multiplier = 0.25
max_speed_multiplier = 10.0

# Create a font object for rendering text
display_font = pygame.font.Font(None, 16)  # You can adjust the font size and style as needed
text_color = (0, 0, 0)  # Text color

# Define classes
def consume_food(self):
    self.hunger = min(self.hunger + 1, self.max_hunger)
    
class Organism(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((5, 5))
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.age = 0
        self.alive = True
        self.mutation = random.uniform(-mutation_rate, mutation_rate)
        self.velocity = [random.uniform(-1, 1), random.uniform(-1, 1)]  # Random initial velocity
        self.hunger = 5
        self.max_hunger = 25  # Maximum hunger value
        self.speed = 1

    def find_nearest_food(self):
        nearest_food = None
        nearest_distance = float('inf')

        for food in foods:
            distance = math.sqrt((self.rect.x - food.rect.x) ** 2 + (self.rect.y - food.rect.y) ** 2)

            if distance < nearest_distance:
                nearest_food = food
                nearest_distance = distance

        return nearest_food

    def wander(self):
        # Add some random noise to the current velocity
        noise = pygame.math.Vector2(random.uniform(-0.3, 0.3), random.uniform(-0.3, 0.3))
        self.velocity += noise

        # Normalize the new velocity and adjust speed
        self.velocity = self.velocity.normalize() * self.speed

    def update(self):
        if self.alive:
            self.age += 1
            if self.age > lifespan:
                self.alive = False

            if len(foods) > 0:
                closest_food = min(foods, key=lambda food: pygame.math.Vector2(food.rect.center).distance_to(self.rect.center))
                food_direction = pygame.math.Vector2(closest_food.rect.center) - pygame.math.Vector2(self.rect.center)
                food_direction = food_direction.normalize()
                self.velocity = food_direction * self.speed
            else:
                # If no food is available, wander randomly
                self.wander()

            self.decrease_hunger()  # Decrease hunger over time

            # Find the nearest food source
            nearest_food = self.find_nearest_food()

            if nearest_food:
                # Calculate the direction to the nearest food
                dx = nearest_food.rect.x - self.rect.x
                dy = nearest_food.rect.y - self.rect.y
                distance = math.sqrt(dx ** 2 + dy ** 2)

                # Move towards the nearest food source
                if distance > 0:
                    self.velocity[0] = dx / distance
                    self.velocity[1] = dy / distance
                else:
                    self.velocity[0] = 0
                    self.velocity[1] = 0

                # If the organism is close enough to the food, consume it
                if distance < 5:
                    foods.remove(nearest_food)
                    consume_food

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

            # Check for collisions with other organisms and change direction if necessary
            for other_organism in organisms:
                if other_organism != self:  # Skip checking collision with itself
                    if self.rect.colliderect(other_organism.rect):
                        # Change direction by reversing velocity components
                        self.velocity[0] *= -1
                        self.velocity[1] *= -1

    def lose_food(self):
        self.hunger = max(self.hunger - 1, 0)
    
    def consume_food(self):
        self.hunger = min(self.hunger + 1, self.max_hunger)

    def decrease_hunger(self):
        self.hunger = max(self.hunger - 0.01, 0)  # Decrease hunger over time

def reproduce(organism):
    if organism.alive and random.random() < reproduction_chance and organism.hunger >= 6:
        # Calculate a random distance and angle within a 20-pixel radius
        distance = random.uniform(10, 20)
        angle = random.uniform(0, 2 * math.pi)

        # Calculate the new position based on distance and angle
        new_x = organism.rect.x + distance * math.cos(angle)
        new_y = organism.rect.y + distance * math.sin(angle)

        # Ensure the new position is within the screen boundaries
        new_x = max(0, min(WIDTH, new_x))
        new_y = max(0, min(HEIGHT, new_y))

        offspring = Organism(
            organism.rect.x + random.randint(-10, 10),
            organism.rect.y + random.randint(-10, 10)
        )
        offspring.image.fill((0, 255, 0))
        offspring.age = 0
        offspring.hunger = 5
        offspring.max_hunger = 20
        organisms.add(offspring)

class Food(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Changed the size of food to 3x3
        self.image = pygame.Surface((3, 3))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH)
        self.rect.y = random.randint(0, HEIGHT)

# Create sprite groups
organisms = pygame.sprite.Group()
foods = pygame.sprite.Group()

# Create initial organisms
for _ in range(population_size):
    organism = Organism(random.randint(0, WIDTH), random.randint(0, HEIGHT))
    organisms.add(organism)

# Create food
for _ in range(int(WIDTH * HEIGHT * food_scarcity)):
    food = Food()
    foods.add(food)

# Game loop
clock = pygame.time.Clock()
running = True
paused = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # Controls
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
            # Get the current mouse cursor position
                mouse_x, mouse_y = pygame.mouse.get_pos()

                # Create a new food object at the mouse cursor position
                food = Food()
                food.rect.center = (mouse_x, mouse_y)
                foods.add(food)
                
            if event.key == pygame.K_RIGHT:  # Increase speed
                speed_multiplier = min(speed_multiplier * 2, max_speed_multiplier)
            elif event.key == pygame.K_LEFT:  # Decrease speed
                speed_multiplier = max(speed_multiplier / 2, min_speed_multiplier)

            elif event.key == pygame.K_r:  # Reset the game when "R" is pressed
                organisms.empty()
                foods.empty()
                for _ in range(population_size):
                    organism = Organism(random.randint(0, WIDTH), random.randint(0, HEIGHT))
                    organisms.add(organism)
                for _ in range(int(WIDTH * HEIGHT * food_scarcity)):
                    food = Food()
                    foods.add(food)
            elif event.key == pygame.K_SPACE:  # Pause/unpause the game when "Space" is pressed
                paused = not paused
    


    if not paused:
        # Create new organisms only if the population size is below the maximum limit
        for organism in organisms.copy():
            organism.update()
            if not organism.alive:
                organisms.remove(organism)
            else:
                if len(organisms) < max_population_size:
                    reproduce(organism)

        # Check for collisions
        hits = pygame.sprite.groupcollide(organisms, foods, False, True)
        for organism, food_list in hits.items():
            for _ in food_list:
                reproduce(organism)

    # Draw everything
    screen.fill(WHITE)
    organisms.draw(screen)
    foods.draw(screen)

    # Calculate and display the total population count
    population_count = len(organisms)
    paused_display = paused

    pop_count_text = display_font.render(f"POP: {population_count}", True, text_color)
    screen.blit(pop_count_text, (10, 10))  # Adjust the position as needed

    pause_text = display_font.render(f"PAUSED: {paused_display}", True, text_color)
    screen.blit(pause_text, (10, 30))  # Adjust the position as needed

    speed_text = display_font.render(f"Speed: x{speed_multiplier:.2f}", True, (0, 0, 0))
    screen.blit(speed_text, (10, 50))  # Adjust the position as needed

    pygame.display.flip()
    clock.tick(FPS * speed_multiplier)

pygame.quit()
