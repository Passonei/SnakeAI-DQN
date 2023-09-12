import pygame
import random
import numpy as np

class Snake:
    def __init__(self, width=640, height=480, BLOCK_SIZE=20, SPEED=20):
        self.w=width
        self.h=height
        self.BLOCK_SIZE=BLOCK_SIZE
        self.SPEED=SPEED
        self.font = pygame.font.SysFont('arial', 25)
        self.reset()
        self.directions = [(-self.BLOCK_SIZE, 0),(self.BLOCK_SIZE, 0),
                            (0, -self.BLOCK_SIZE),(0, self.BLOCK_SIZE)]

        self.display = pygame.display.set_mode((self.w, self.h))
    
    def reset(self):
        self.direction = 0
        self.head = (self.w/2, self.h/2)
        self.snake = [self.head,
                    (self.head[0]+self.BLOCK_SIZE, self.head[1])]
        self.score = 0
        self._place_food()
        self.clock = pygame.time.Clock()

    def _place_food(self):
        x = random.randint(0, (self.w-self.BLOCK_SIZE)//self.BLOCK_SIZE)*self.BLOCK_SIZE
        y = random.randint(0, (self.h-self.BLOCK_SIZE)//self.BLOCK_SIZE)*self.BLOCK_SIZE
        self.food = (x, y)
        if self.food in self.snake:
            self._place_food()

    def get_state(self):
        state = np.zeros((12))
        state[self.direction] = 1

        # left
        if self._is_collision((self.head[0]-self.BLOCK_SIZE,self.head[1])):# and self.direction!=1: 
            state[4] = 1
        # right
        if self._is_collision((self.head[0]+self.BLOCK_SIZE,self.head[1])):# and self.direction!=0:
            state[5] = 1
        # up
        if self._is_collision((self.head[0],self.head[1]-self.BLOCK_SIZE)):# and self.direction!=3:
            state[6] = 1
        # down
        if self._is_collision((self.head[0],self.head[1]+self.BLOCK_SIZE)):# and self.direction!=2:
            state[7] = 1
 
        if self.head[0] > self.food[0]:
             state[8] = 1
        if self.head[1] > self.food[1]:
             state[9] = 1
        if self.head[0] < self.food[0]:
             state[10] = 1
        if self.head[1] < self.food[1]:
             state[11] = 1
             
        return state
            
    def play_step(self, human=True, action=0):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN and human:
                if event.key == pygame.K_LEFT and self.direction != 1:
                    self.direction = 0
                elif event.key == pygame.K_RIGHT and self.direction != 0:
                    self.direction = 1
                elif event.key == pygame.K_UP and self.direction != 3:
                    self.direction = 2
                elif event.key == pygame.K_DOWN and self.direction != 2:
                    self.direction = 3
        
        if not human:
            if action == 0 and self.direction != 1:
                self.direction = 0
            elif action == 1 and self.direction != 0:
                self.direction = 1
            elif action == 2 and self.direction != 3:
                self.direction = 2
            elif action == 3 and self.direction != 2:
                self.direction = 3

        self.display.fill('black')
        
        pygame.draw.rect(self.display, 'red', (self.food[0]+4, self.food[1]+4, 
                                                self.BLOCK_SIZE-8, self.BLOCK_SIZE-8))

        self._move(self.directions[self.direction])
        self.snake.insert(0, self.head)

        [pygame.draw.rect(self.display, 'green', (segment[0]+0.5, segment[1]+0.5, 
                            self.BLOCK_SIZE-1, self.BLOCK_SIZE-1)) for segment in self.snake]
        pygame.draw.rect(self.display, 'blue', (self.head[0]+4, self.head[1]+4, 
                            self.BLOCK_SIZE-8, self.BLOCK_SIZE-8))
        reward = 0
        game_over = False

        if self.head == self.food:
            self.score += 1
            reward = 10
            self._place_food()
        else:
            self.snake.pop()
        if self._is_collision(self.head):
            game_over = True
            reward = -10
            return reward, game_over, self.score
        
        text = self.font.render("Score: " + str(self.score), True, (200, 200, 200))
        self.display.blit(text, [0, 0])
        pygame.display.flip()
        if human:
            self.clock.tick(self.SPEED)
        else:
            self.clock.tick(0)
            
        return reward, game_over, self.score

    def _is_collision(self, head):
        if head[0] > self.w-self.BLOCK_SIZE or head[0] < 0 or head[1] > self.h-self.BLOCK_SIZE or head[1] < 0:
            return True
        if head in self.snake[1:]:
            return True
        return False

    def _move(self,direction):
        x = self.head[0] + direction[0]
        y = self.head[1] + direction[1]
        self.head = (x, y) 