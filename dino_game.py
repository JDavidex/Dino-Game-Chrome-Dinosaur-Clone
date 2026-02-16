import pygame # Pygame library for game development
import os # To handle file paths
import random # For random number generation

pygame.init()

# Constants
SCREEN_WIDTH = 1100
SCREEN_HEIGHT = 600
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Dino Game")

RUNNING = [pygame.image.load(os.path.join("Assets/Dino", "run1.png")), pygame.image.load(os.path.join("Assets/Dino", "run2.png"))]
JUMPING = pygame.image.load(os.path.join("Assets/Dino", "jump.png"))
DUCKING = [pygame.image.load(os.path.join("Assets/Dino", "duck1.png")), pygame.image.load(os.path.join("Assets/Dino", "duck2.png"))]

SMALL_CACTUS = [pygame.image.load(os.path.join("Assets/Cactus", "small1.png")), pygame.image.load(os.path.join("Assets/Cactus", "small2.png")), pygame.image.load(os.path.join("Assets/Cactus", "small3.png"))]
LARGE_CACTUS = [pygame.image.load(os.path.join("Assets/Cactus", "large1.png")), pygame.image.load(os.path.join("Assets/Cactus", "large2.png")), pygame.image.load(os.path.join("Assets/Cactus", "large3.png"))]
BIRD = [pygame.image.load(os.path.join("Assets/Bird", "bird1.png")), pygame.image.load(os.path.join("Assets/Bird", "bird2.png"))]

CLOUD = pygame.image.load(os.path.join("Assets/Scenery", "cloud.png"))
BG = pygame.image.load(os.path.join("Assets/Scenery", "track.png"))

DEAD = pygame.image.load(os.path.join("Assets/Dino", "dead1.png"))
RESET = pygame.image.load(os.path.join("Assets/Other", "reset.png"))
GAME_OVER = pygame.image.load(os.path.join("Assets/Other", "gameover.png"))

JUMP_SOUND = pygame.mixer.Sound(os.path.join("Assets/Audio", "jump.mp3"))
DIE_SOUND = pygame.mixer.Sound(os.path.join("Assets/Audio", "die.mp3"))

# Dinosaur class to manage the player's character
class Dinosaur:
    X_POS = 80
    Y_POS = 310
    JUMP_VEL = 8.5

    def __init__(self):
        self.duck_img = DUCKING
        self.run_img = RUNNING
        self.jump_img = JUMPING
        self.dead_img = DEAD

        self.dino_duck = False
        self.dino_run = True
        self.dino_jump = False
        self.dino_dead = False

        self.step_index = 0 # To track animation steps
        self.jump_vel = self.JUMP_VEL
        self.image = self.run_img[0]
        self.dino_rect = self.image.get_rect() # Get rectangle for hitbox
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS

    def update(self, userInput):
        if self.dino_duck:
            self.duck()
        if self.dino_run:
            self.run()
        if self.dino_jump:
            self.jump(userInput)

        if self.step_index >= 10: # Reset step index for animation loop
            self.step_index = 0

        # Handle user input for actions
        if userInput[pygame.K_UP] and not self.dino_jump and not self.dino_duck: # Jumping
            self.dino_duck = False
            self.dino_run = False
            self.dino_jump = True
            JUMP_SOUND.play() # Play jump sound
        elif userInput[pygame.K_DOWN] and not self.dino_jump: # Ducking
            self.dino_duck = True
            self.dino_run = False
            self.dino_jump = False
        elif not (self.dino_jump or userInput[pygame.K_DOWN]): # Running
            self.dino_duck = False
            self.dino_run = True
            self.dino_jump = False
        if userInput[pygame.K_DOWN] and self.dino_jump: # If ducking while jumping
            self.jump_vel = -self.JUMP_VEL

    def duck(self):
        self.image = self.duck_img[self.step_index // 5] # Change image based on step index
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS + 36  # Adjust y position for ducking
        self.dino_rect.width = self.image.get_width() # Update width for ducking
        self.dino_rect.height = self.image.get_height() # Update height for ducking
        self.step_index += 1

    def run(self):
        self.image = self.run_img[self.step_index // 5] # Change image based on step index
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS
        self.step_index += 1

    def jump(self, userInput):
        self.image = self.jump_img
        if self.dino_jump:
            self.dino_rect.y -= self.jump_vel * 4 # Move up based on jump velocity
            self.jump_vel -= 0.8 # Decrease jump velocity to simulate gravity
        if self.jump_vel < -self.JUMP_VEL: # Reset after jump is complete
            self.dino_jump = False
            self.jump_vel = self.JUMP_VEL
            self.dino_rect.y = self.Y_POS # Reset to ground position
            if userInput[pygame.K_DOWN]: # If down key is still pressed after landing
                self.dino_duck = True
                self.dino_run = False
    
    def set_dead(self):
        self.image = self.dead_img
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS
    
    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.dino_rect.x, self.dino_rect.y))

# Cloud class for background scenery
class Cloud:
    def __init__(self):
        self.x = SCREEN_WIDTH + random.randint(800, 1000)
        self.y = random.randint(50, 100)
        self.image = CLOUD
        self.width = self.image.get_width()

    def update(self):
        self.x -= game_speed # Move cloud to the left
        if self.x < -self.width: # Reset cloud position when off screen
            self.x = SCREEN_WIDTH + random.randint(2500, 3000)
            self.y = random.randint(50, 100)

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.x, self.y))

# Obstacle base class
class Obstacle:
    def __init__(self, image, type):
        self.image = image # List of images for the obstacle type
        self.type = type # Type index to select specific image
        self.rect = self.image[self.type].get_rect()
        self.rect.x = SCREEN_WIDTH

    def update(self):
        self.rect.x -= game_speed # Move obstacle to the left
        if self.rect.x < -self.rect.width:
            obstacles.pop() # Remove obstacle when off screen

    def draw(self, SCREEN): # Draw the obstacle on the screen
        SCREEN.blit(self.image[self.type], self.rect)

# SmallCactus class inheriting from Obstacle
class SmallCactus(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2) # Randomly select cactus type
        super().__init__(image, self.type) # Initialize parent class
        self.rect.y = 325

# LargeCactus class inheriting from Obstacle
class LargeCactus(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2) # Randomly select cactus type
        super().__init__(image, self.type) # Initialize parent class
        self.rect.y = 300

# Bird class inheriting from Obstacle
class Bird(Obstacle):
    def __init__(self, image):
        self.type = 0 # Bird has only one type
        super().__init__(image, self.type) # Initialize parent class
        self.rect.y = random.choice([240, 270, 300]) # Random height for bird
        self.index = 0 # To track animation steps

    def draw(self, SCREEN, game_over=False): # Draw the bird with animation
        if self.index >= 9: # Reset index for animation loop
            self.index = 0
        SCREEN.blit(self.image[self.index // 5], self.rect) # Animate bird wings

        if not game_over:
            self.index += 1

# Main loop function (Everything in pygame runs in a while loop)
def main():
    global game_speed, x_pos_bg, y_pos_bg, points, obstacles, high_score # To modify these variables inside the function
    clock = pygame.time.Clock() # To control the frame rate
    run = True # Game loop flag
    player = Dinosaur()
    cloud = Cloud() 
    game_speed = 16
    x_pos_bg = 0
    y_pos_bg = 380
    points = 0
    font = pygame.font.Font('Assets/Font/PressStart2P-Regular.ttf', 20)
    obstacles = [] # List to hold active obstacles
    game_over = False
    reset_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 25, SCREEN_HEIGHT // 2 - 60, 50, 50)

    # Score function to keep track of points
    def score():
        global points, game_speed, high_score

        if not game_over:
            points += 1
            if points % 100 == 0:
                game_speed += 1

        if points > high_score:
            high_score = points

        hi_text = font.render("HI", True, (83, 83, 83))
        SCREEN.blit(hi_text, (SCREEN_WIDTH - 380, 30))
        
        hi_score_text = font.render(str(high_score).zfill(5), True, (83, 83, 83))
        SCREEN.blit(hi_score_text, (SCREEN_WIDTH - 300, 30))

        score_text = font.render(str(points).zfill(5), True, (83, 83, 83))
        SCREEN.blit(score_text, (SCREEN_WIDTH - 150, 30))

    # Draw background function for scrolling effect
    def draw_background():
        global x_pos_bg, y_pos_bg
        image_width = BG.get_width()
        SCREEN.blit(BG, (x_pos_bg, y_pos_bg)) # Draw first image
        SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg)) # Draw second image for seamless scrolling
        if x_pos_bg <= -image_width: # Reset position when off screen
            SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg)) # Draw second image
            x_pos_bg = 0

        if not game_over:
            x_pos_bg -= game_speed # Move background to the left

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False # Exit game loop
            if event.type == pygame.MOUSEBUTTONDOWN and game_over:
                if reset_button_rect.collidepoint(event.pos):
                    main() # Restart the game
                    return
            if event.type == pygame.KEYDOWN and game_over:
                if event.key == pygame.K_UP:
                    main() # Restart the game
                    return

        SCREEN.fill((255, 255, 255))
        
        userInput = pygame.key.get_pressed()

        player.draw(SCREEN) # Draw the dinosaur

        if not game_over:
            player.update(userInput) # Update dinosaur state based on user input

        if len(obstacles) == 0 and not game_over:
            random_spawn = random.randint(0, 9) # Randomly decide which obstacle to spawn
            if random_spawn == 0: # 10% chance to spawn a bird
                obstacles.append(Bird(BIRD))
            else: # 90% chance to spawn a cactus
                if random.randint(0, 1) == 0:
                    obstacles.append(SmallCactus(SMALL_CACTUS))
                else:
                    obstacles.append(LargeCactus(LARGE_CACTUS))

        for obstacle in obstacles:
            if isinstance(obstacle, Bird): # Special draw method for birds
                obstacle.draw(SCREEN, game_over)
            else:
                obstacle.draw(SCREEN) # Draw each obstacle
            
            if not game_over:
                obstacle.update() # Update each obstacle
            if player.dino_rect.colliderect(obstacle.rect) and not game_over:
                game_over = True
                player.dino_dead = True
                player.dino_run = False
                player.dino_duck = False
                player.dino_jump = False
                player.set_dead() # Change dinosaur to dead sprite
                DIE_SOUND.play() # Play die sound

        if game_over:
            SCREEN.blit(GAME_OVER, (SCREEN_WIDTH // 2 - GAME_OVER.get_width() // 2, SCREEN_HEIGHT // 2 - 100))
            SCREEN.blit(RESET, (SCREEN_WIDTH // 2 - RESET.get_width() // 2, SCREEN_HEIGHT // 2 - 60))

        draw_background() # Draw scrolling background
        cloud.draw(SCREEN) # Draw cloud

        if not game_over:
            cloud.update() # Update cloud position

        score() # Update and display score

        pygame.display.update() # Refresh the screen
        clock.tick(30) # Set frame rate to 30 FPS

high_score = 0 # Global high score variable
main()