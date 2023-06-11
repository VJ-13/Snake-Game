# Import the libaries
import pygame
import sys
import random
from pygame.math import Vector2
import asyncio

class SNAKE:
    # Inatilazies Variables and Load the Graphics and Sound
    def __init__(self):
        # Snake Body
        self.body = [Vector2(5,10), Vector2(4,10), Vector2(3,10)]
        self.direction = Vector2(0,0)
        self.new_block = False

        # Snake Head Graphics
        self.head_up = pygame.image.load('Graphics/head_up.png').convert_alpha()
        self.head_down = pygame.image.load('Graphics/head_down.png').convert_alpha()
        self.head_right = pygame.image.load('Graphics/head_right.png').convert_alpha()
        self.head_left = pygame.image.load('Graphics/head_left.png').convert_alpha()

		# Snake Tail Graphics
        self.tail_up = pygame.image.load('Graphics/tail_up.png').convert_alpha()
        self.tail_down = pygame.image.load('Graphics/tail_down.png').convert_alpha()
        self.tail_right = pygame.image.load('Graphics/tail_right.png').convert_alpha()
        self.tail_left = pygame.image.load('Graphics/tail_left.png').convert_alpha()

        # Snake Body Graphics
        self.body_vertical = pygame.image.load('Graphics/body_vertical.png').convert_alpha()
        self.body_horizontal = pygame.image.load('Graphics/body_horizontal.png').convert_alpha()

        # Snake Body(corners) Graphics
        self.body_tr = pygame.image.load('Graphics/body_tr.png').convert_alpha()
        self.body_tl = pygame.image.load('Graphics/body_tl.png').convert_alpha()
        self.body_br = pygame.image.load('Graphics/body_br.png').convert_alpha()
        self.body_bl = pygame.image.load('Graphics/body_bl.png').convert_alpha()

        # Sound for eating an apple
        self.crunch_sound = pygame.mixer.Sound('Sound/crunch.wav')

    # Draws out the Snake
    def draw_snake(self):
        # Snake graphics
        self.update_head_graphics()
        self.update_tail_graphics()

        for index, block in enumerate(self.body):

            # rect for the positioning
            x_pos = int(block.x * cell_size)
            y_pos = int(block.y * cell_size)
            block_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)

            # direction of the snake head
            if index == 0:
                # prints the Snake head
                screen.blit(self.head,block_rect)  
            elif index == len(self.body) - 1:
                # Prints The Snake tail
                screen.blit(self.tail,block_rect)
            else:
                previous_block = self.body[index + 1] - block
                next_block =  self.body[index - 1] - block

                if previous_block.x == next_block.x:
                    # Prints The Verical Blocks
                    screen.blit(self.body_vertical, block_rect)
                elif previous_block.y == next_block.y:
                    # Prints The Horizontal Blocks
                    screen.blit(self.body_horizontal, block_rect)
                else:
                    # Prints The Top Left Corner
                    if previous_block.x == -1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == -1:
                        screen.blit(self.body_tl,block_rect)
                    
                    # Prints The Bottom Left Corner
                    elif previous_block.x == -1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == -1:
                        screen.blit(self.body_bl,block_rect)
                    
                    # Prints The Top Right Corner
                    elif previous_block.x == 1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == 1:
                        screen.blit(self.body_tr,block_rect)
                    
                    # Prints The Bottom Right Corner
                    elif previous_block.x == 1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == 1:
                        screen.blit(self.body_br,block_rect)

    # Prints the Snake Head           
    def update_head_graphics(self):
        # Direction of the head
        head_relation = self.body[1] - self.body[0]
        if head_relation == Vector2(1,0):
            # Head Left
            self.head = self.head_left
        elif head_relation == Vector2(-1,0):
            # Head Right
            self.head = self.head_right
        elif head_relation == Vector2(0,1):
            # Head Up
            self.head = self.head_up
        elif head_relation == Vector2(0,-1):
            # Head Down
            self.head = self.head_down

    # Prints the Snake Tail 
    def update_tail_graphics(self):
        # Direction of the tail
        tail_relation = self.body[-2] - self.body[-1]
        if tail_relation == Vector2(1,0):
            # Tail Left
            self.tail = self.tail_left
        elif tail_relation == Vector2(-1,0):
            # Tail Right
            self.tail = self.tail_right
        elif tail_relation == Vector2(0,1):
            # Tail Up
            self.tail = self.tail_up
        elif tail_relation == Vector2(0,-1):
            # Tail Down
            self.tail = self.tail_down

    # Moves the Snake
    def move_snake(self):
        # If the snake eats the apple and gets a new block
        if self.new_block == True:
            # Adds a block to the snake
            body_copy = self.body[:]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
            self.new_block = False
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
    
    # Adds the Block to Snake
    def add_block(self):
        self.new_block = True

    # Plays the Crunch Sound
    def play_crunch_sound(self):
        self.crunch_sound.play()

    # Reset the Snake after it dies
    def reset(self):
       self.body = [Vector2(5,10), Vector2(4,10), Vector2(3,10)] 
       self.direction = Vector2(0,0)

class FRUIT:
    # Inatliazes Variables
    def __init__(self):
        self.randomize()
    
    # Draws the Fruit
    def draw_fruit(self):
        # Rect for the fruit
        fruit_rect = pygame.Rect(int(self.pos.x * cell_size),int(self.pos.y * cell_size),cell_size,cell_size)
        # Prints out the fruit
        screen.blit(apple, fruit_rect)
    
    # Randomizes the Fruit
    def randomize(self):
        # Randomizes the x and y position making sure it doesnt get out of screen
        self.x = random.randint(0,cell_number - 1)
        self.y = random.randint(0,cell_number - 1)
        self.pos = pygame.math.Vector2(self.x,self.y)

class MAIN:
    # Inatilazes Variables
    def __init__(self):
        self.snake = SNAKE()
        self.fruit = FRUIT()

    # Runs the Functions
    def update(self):
        self.snake.move_snake()
        self.check_collision()
        self.check_fail()     

    # Draws all the Elements
    def draw_elements(self):
        self.draw_grass()
        self.fruit.draw_fruit()
        self.snake.draw_snake()
        self.draw_score()
    
    # Checks if the Snake's Head is at the same position as Fruit
    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]:
            # reposition the fruit
            self.fruit.randomize()

            # add another block to the snake
            self.snake.add_block()

            # play the crunch sound
            self.snake.play_crunch_sound()

            for block in self.snake.body[1:]:
                # checks to see if the apple is at same position as the snake when the game starts
                if block == self.fruit.pos:
                    self.fruit.randomize()
    
    # Checks if the Snake died
    def check_fail(self):
        # check if the snake is outside the screen
        if not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y < cell_number:
            self.game_over()
        
        # check if the snake hits itself
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()
    
    # Runs the reset function in Snake
    def game_over(self):
        self.snake.reset()
    
    # Draws the grass
    def draw_grass(self):
        grass_colour = (167, 209, 61)
        for row in range(cell_number):
            # Even Row
            if row % 2 == 0:
                for col in range(cell_number):
                    # Even Blocks
                    if col % 2 == 0:
                        grass_rect =pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
                        pygame.draw.rect(screen, grass_colour, grass_rect)
            else:
                for col in range(cell_number):
                    # Odd Blocks
                    if col % 2 != 0:
                        grass_rect =pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
                        pygame.draw.rect(screen, grass_colour, grass_rect)

    # Draws the score
    def draw_score(self):
        # Initalizes the score
        score_text = str(len(self.snake.body) - 3)

        # Renders the font 
        score_surface = game_font.render(score_text, True, (56, 74, 12))

        # Make rect for score, apple, background
        score_x = int(cell_size * cell_number - 60)
        score_y = int(cell_size * cell_number - 40)
        score_rect = score_surface.get_rect(center = (score_x, score_y))
        apple_rect = apple.get_rect(midright = (score_rect.left, score_rect.centery))
        bg_rect =  pygame.Rect(apple_rect.left, apple_rect.top, apple_rect.width + score_rect.width + 6, apple_rect.height)

        # Prints the all the rect
        pygame.draw.rect(screen, (167, 209, 61), bg_rect)
        pygame.draw.rect(screen, (56, 74, 12), bg_rect, 2)
        screen.blit(score_surface, score_rect)
        screen.blit(apple, apple_rect)
         
# Fixes the sound
pygame.mixer.pre_init(44100, -16, 2, 512)
 
# Inatilizes the Variables
pygame.init()
cell_size = 40
cell_number = 20
screen = pygame.display.set_mode((cell_number * cell_size,cell_number * cell_size))
clock = pygame.time.Clock()

# Loads the apple and font
apple = pygame.image.load('Graphics/apple.png').convert_alpha()
game_font = pygame.font.Font('Font/PoetsenOne-Regular.ttf', 25)

# Updates the screen and set the time
SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)

main_game = MAIN()

async def main(self):
    # Game Loop
    while True:
        for event in pygame.event.get():
            # If the user press close it quits
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            # Updates the screen
            if event.type == SCREEN_UPDATE:
                main_game.update()
            
            # Checks for Player Input
            if event.type == pygame.KEYDOWN:
                # Up Key
                if event.key == pygame.K_UP:
                    # Not pressing the opposite key 
                    if main_game.snake.direction.y != 1:
                        main_game.snake.direction = Vector2(0, -1)
                # Down Key
                if event.key == pygame.K_DOWN:
                    # Not pressing the opposite key
                    if main_game.snake.direction.y != -1:
                        main_game.snake.direction = Vector2(0, 1)
                # Left Key
                if event.key == pygame.K_LEFT:
                    # Not pressing the opposite key
                    if main_game.snake.direction.x != 1:
                        main_game.snake.direction = Vector2(-1, 0)
                # Right Key
                if event.key == pygame.K_RIGHT:
                    # Not pressing the opposite key
                    if main_game.snake.direction.x != -1:
                        main_game.snake.direction = Vector2(1, 0)
                
        # Prints the background
        screen.fill((175,215,70))

        # Draws all the elements
        main_game.draw_elements() 

        # Updates the display
        pygame.display.update()
        await asyncio.sleep(0)
        # 60 FPS
        clock.tick(60)

if __name__ == "__main__":
    asyncio.run(main(main_game))
