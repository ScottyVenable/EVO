# Evolution Simulation
import math
import pygame
import random
import pygame.font
import pygame_gui
import gamedata.organism
import utils.parameters
import utils.constants
import gamedata.environment
import gamedata.items
from gamedata.items import Foods
import datetime
import os
from utils.logging import Timestamping

Colors = utils.constants.Colors()
Parameters = utils.parameters
ItemDatabase = gamedata.items


# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((Parameters.WIDTH, Parameters.HEIGHT))
pygame.display.set_caption("Evolution")

class CreateLog:
    logs_directory = "logs"

    def __init__(self, log_filename):
        self.timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        self.log_file_path = os.path.join(self.logs_directory, f"{log_filename}_{self.timestamp}.txt")
        os.makedirs(self.logs_directory, exist_ok=True)

    # Create the 'logs' directory if it doesn't exist
    os.makedirs(logs_directory, exist_ok=True)

generation_log = CreateLog("generation")

# Populate the Data

food_list = [Foods.berry, Foods.hazelnut]

for food in food_list:
    # Format the output using string formatting
    print("FOODS LOADED:")
    print(f"\n--------\n   Name: {food.name}\n   Description: \"{food.description}\"\n   Weight: {food.weight}\n   Type: {food.item_type}\n   Nutrients: {food.nutrients}\n   Spawns Naturally: {'Yes' if food.spawns_naturally else 'No'}\n   Rarity: {'common' if food.spawn_probability >= 0.008 else 'uncommon' if food.spawn_probability >= 0.005 else 'rare' if food.spawn_probability >= 0.002 else 'very rare'}")

spawning_foods = [] # Create the list of foods that spawn naturally

spawning_foods_group = pygame.sprite.Group() # Create the group of sprites for the spawning foods.
for food in spawning_foods:
    spawning_foods_group.add(food)


for food in food_list: # Add the naturally occuring foods to the list of foods that will spawn when the game starts.
    if food.spawns_naturally:
        spawning_foods.append(food)

spawn_probabilities = [food.spawn_probability for food in spawning_foods]
def generate_natural_food():
    generated_food = random.choices(spawning_foods, weights=spawn_probabilities, k=1)[0]
    food_sprite = generated_food.sprite

    # Randomly generate coordinates for the food's position
    food_x = random.randint(0, Parameters.WIDTH - food_sprite.get_width())
    food_y = random.randint(0, Parameters.HEIGHT - food_sprite.get_height())

    # Set the position of the food sprite
    generated_food.rect.x = food_x
    generated_food.rect.y = food_y

    with open(generation_log.log_file_path, "a") as log_file:
        timestamp = Timestamping.log_timestamps()
        log_file.write(f"{timestamp}Generated food item: '{generated_food.name}'\n")

    # Add the food sprite to the spawning foods group

def generate_initial_foods():
    max_foods = 20
    with open(generation_log.log_file_path, "a") as log_file:
        timestamp = Timestamping.log_timestamps()
        log_file.write(f"{timestamp}Generating Foods...\n")
    for _ in range(max_foods):
        generate_natural_food()
        timestamp = Timestamping.log_timestamps()
        print(f"{timestamp}Finished generating foods!\n")

# Define parameters
population_size = 5
max_population_size = 15
food_scarcity = 0.0008
lifespan = 10000000
mutation_rate = 0.02
reproduction_chance = 0.03  # Chance of reproducing in each frame
speed_multiplier = 1.0  # Initial speed multiplier
min_speed_multiplier = 0.25
max_speed_multiplier = 10.0

# Run initial methods
generate_initial_foods()

# Create a font object for rendering text
display_font = pygame.font.Font(None, 16)  # You can adjust the font size and style as needed
text_color = (0, 0, 0)  # Text color

# Define classes
    
class Organism(pygame.sprite.Sprite):
    """This class represents an Organism in the simulation"""
    
    def __init__(self, x, y):
        """Initialize the Organism"""
        super().__init__()
        hunger_gained = 0  # Tracks the amount of hunger gained by the Organism
        self.image = pygame.Surface((8, 8))  # Create an image for the Organism
        self.image.fill(Colors.BLUE)  # Set the color of the Organism
        self.rect = self.image.get_rect()  # Get the rect associated with the image
        self.rect.center = (x, y)  # Set the position of the Organism
        self.age = 0  # Initial age of the Organism
        self.alive = True  # Flag to indicate if the Organism is alive
        self.mutation = random.uniform(-mutation_rate, mutation_rate)  # Mutation rate of the Organism
        self.velocity = [random.uniform(-1, 1), random.uniform(-1, 1)]  # Random initial velocity of the Organism
        self.hunger = 5  # Initial hunger value of the Organism
        self.max_hunger = 25  # Maximum hunger value of the Organism
        self.speed = 2  # Speed of the Organism

       


    def consume_food(self):
        self.hunger = min(self.hunger + 1, self.max_hunger)
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

        if len(spawning_foods_group) > 0:
            closest_food = min(spawning_foods_group, key=lambda food: pygame.math.Vector2(food.rect.center).distance_to(self.rect.center))
            food_direction = pygame.math.Vector2(closest_food.rect.center) - pygame.math.Vector2(self.rect.center)
            food_direction = food_direction.normalize()
            self.velocity = food_direction * self.speed
        else:
            # If no food is available, wander randomly
            self.wander()



            # Update position based on velocity
            self.rect.x += self.velocity[0]
            self.rect.y += self.velocity[1]

            # Wrap around the screen edges (optional)
            if self.rect.left > Parameters.WIDTH:
                self.rect.right = 0
            elif self.rect.right < 0:
                self.rect.left = Parameters.WIDTH
            if self.rect.top > Parameters.HEIGHT:
                self.rect.bottom = 0
            elif self.rect.bottom < 0:
                self.rect.top = Parameters.HEIGHT

            # Check for collisions with other organisms and change direction if necessary
            for other_organism in organisms:
                if other_organism != self:  # Skip checking collision with itself
                    if self.rect.colliderect(other_organism.rect):
                        # Change direction by reversing velocity components
                        self.velocity[0] *= -1
                        self.velocity[1] *= -1



def reproduce(organism):
    if organism.alive and random.random() < reproduction_chance and organism.hunger >= 6:
        # Calculate a random distance and angle within a 20-pixel radius
        distance = random.uniform(10, 20)
        angle = random.uniform(0, 2 * math.pi)

        # Calculate the new position based on distance and angle
        new_x = organism.rect.x + distance * math.cos(angle)
        new_y = organism.rect.y + distance * math.sin(angle)

        # Ensure the new position is within the screen boundaries
        new_x = max(0, min(Parameters.WIDTH, new_x))
        new_y = max(0, min(Parameters.HEIGHT, new_y))

        offspring = Organism(
            organism.rect.x + random.randint(-10, 10),
            organism.rect.y + random.randint(-10, 10)
        )
        offspring.image.fill((0, 255, 0))
        offspring.age = 0
        offspring.hunger = 5
        offspring.max_hunger = 20
        organisms.add(offspring)

    def __init__(self, food_type):
        super().__init__()
        self.food_type = food_type
        self.nutrients = 0
        self.weight = 0
        self.spawn_probability = 0

        if self.food_type == "berry":
            self.image = pygame.Surface((3, 3))
            self.image.fill(Colors.RED)
            self.nutrients = 2
            self.spawn_probability = 0.03
            self.weight = 0.5

        elif self.food_type == "seed":
            self.image = pygame.Surface((2, 4))
            self.image.fill(Colors.BROWN)
            self.nutrients = 8
            self.spawn_probability = 0.004
            self.weight = 0.3

        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, Parameters.WIDTH)
        self.rect.y = random.randint(0, Parameters.HEIGHT)

    def get_nutrition_value(self):
        return self.nutrients * self.weight

    

# Create sprite groups
organisms = pygame.sprite.Group()
rocks = pygame.sprite.Group()


# Create initial organisms
for _ in range(population_size):
    organism = Organism(random.randint(0, Parameters.WIDTH), random.randint(0, Parameters.HEIGHT))
    organisms.add(organism)

# In my main.py, how do I get this code to spawn the berrys and nuts in the game, calling from the items I populated from the items file?
for _ in range(int(Parameters.WIDTH * Parameters.HEIGHT * food_scarcity)):
    # Determine the type of food to spawn based on probabilities
    food_type = random.choices(["berry", "seed"], [food.spawn_probability for food in food_list])[0]



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
                for Food in food_list:
                    if Food.name == "Berry":    # Find the "Berry" item in the list of food.
                        berry = Food
                        break
                berry.rect.center = (mouse_x, mouse_y)
                spawned_food.add(berry)

            if event.key == pygame.K_e:
                # Get the current mouse cursor position
                mouse_x, mouse_y = pygame.mouse.get_pos()

                # Create a new organism object at the mouse cursor position
                organism = Organism(mouse_x, mouse_y)
                organisms.add(organism)

            if event.key == pygame.K_RIGHT:  # Increase speed
                speed_multiplier = min(speed_multiplier * 2, max_speed_multiplier)
            elif event.key == pygame.K_LEFT:  # Decrease speed
                speed_multiplier = max(speed_multiplier / 2, min_speed_multiplier)

            elif event.key == pygame.K_r:  # Reset the game when "R" is pressed
                organisms.empty()
                spawned_food.empty()
                for _ in range(population_size):
                    organism = Organism(random.randint(0, Parameters.WIDTH), random.randint(0, Parameters.HEIGHT))
                    organisms.add(organism)
                for _ in range(int(Parameters.WIDTH * Parameters.HEIGHT * food_scarcity)):
                    berry = Food("berry")
                    seed = Food("seed")
                    spawned_food.add(berry, seed)
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
        hits = pygame.sprite.groupcollide(organisms, spawning_foods_group, False, True)
        for organism, food_list in hits.items():

            for _ in food_list:
                reproduce(organism)


    # Draw everything
    screen.fill(Colors.WHITE)
    organisms.draw(screen)
    spawning_foods_group.draw(screen)

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
    clock.tick(Parameters.FPS * speed_multiplier)

pygame.quit()
