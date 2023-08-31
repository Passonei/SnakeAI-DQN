import pygame
import random

class Snake:
    def __init__(self, width=640, height=480, BLOCK_SIZE=20, SPEED=20):
        self.w=width
        self.h=height
        self.BLOCK_SIZE=BLOCK_SIZE
        self.SPEED=SPEED
        self.font = pygame.font.SysFont('arial', 25)
        self.reset()

        self.display = pygame.display.set_mode((self.w, self.h))
    
    def reset(self):
        self.direction = (-self.BLOCK_SIZE, 0)
        self.head = (self.w/2, self.h/2, self.BLOCK_SIZE, self.BLOCK_SIZE)
        self.snake = [self.head,
                    (self.head[0]+self.BLOCK_SIZE, self.head[1],
                    self.BLOCK_SIZE, self.BLOCK_SIZE)]
        self.score = 0
        self._place_food()
        self.clock = pygame.time.Clock()

    def _place_food(self):
        x = random.randint(0, (self.w-self.BLOCK_SIZE)//self.BLOCK_SIZE)*self.BLOCK_SIZE
        y = random.randint(0, (self.h-self.BLOCK_SIZE)//self.BLOCK_SIZE)*self.BLOCK_SIZE
        self.food = (x, y, self.BLOCK_SIZE, self.BLOCK_SIZE)
        if self.food in self.snake:
            self._place_food()
    
    def play_step(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and self.direction != (self.BLOCK_SIZE, 0):
                    self.direction = (-self.BLOCK_SIZE, 0)
                elif event.key == pygame.K_RIGHT and self.direction != (-self.BLOCK_SIZE, 0):
                    self.direction = (self.BLOCK_SIZE, 0)
                elif event.key == pygame.K_UP and self.direction != (0, self.BLOCK_SIZE):
                    self.direction = (0, -self.BLOCK_SIZE)
                elif event.key == pygame.K_DOWN and self.direction != (0, -self.BLOCK_SIZE):
                    self.direction = (0, self.BLOCK_SIZE)

        self.display.fill('black')
        
        pygame.draw.rect(self.display, 'red', self.food)

        self._move(self.direction)
        self.snake.insert(0, self.head)

        [pygame.draw.rect(self.display, 'green', segment) for segment in self.snake]
        
        game_over = False
        if self._is_collision():
            game_over = True
            return game_over, self.score

        if self.head == self.food:
            self.score += 1
            self._place_food()
        else:
            self.snake.pop()
        
        text = self.font.render("Score: " + str(self.score), True, (200, 200, 200))
        self.display.blit(text, [0, 0])
        pygame.display.flip()
        self.clock.tick(self.SPEED)

        return game_over, self.score

    def _is_collision(self):
        if self.head[0] >= self.w or self.head[0] < 0 or self.head[1] >= self.h or self.head[1] < 0:
            return True
        if self.head in self.snake[1:]:
            return True
        return False

    def _move(self, direction):
        x = self.head[0] + direction[0]
        y = self.head[1] + direction[1]
        self.head = (x, y, self.BLOCK_SIZE, self.BLOCK_SIZE) 


