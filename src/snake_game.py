import pygame
import random
import numpy as np


class Snake:
    """
    Class for the snake game

    Args:
        width: width of the game
        height: height of the game
        BLOCK_SIZE: size of the block
        SPEED: speed of the game

    Attributes:
        w (int): width of the game
        h (int): height of the game
        BLOCK_SIZE (int): size of the block
        SPEED (int): speed of the game
        font (pygame.font.SysFont): font of the game
        reset (method): reset the game
        directions (list): list of directions
        display (pygame.display.set_mode): display of the game
    """

    def __init__(
            self,
            width: int = 640,
            height: int = 480,
            BLOCK_SIZE: int = 20,
            SPEED: int = 20
    ):
        self.w = width
        self.h = height
        self.BLOCK_SIZE = BLOCK_SIZE
        self.SPEED = SPEED
        self.font = pygame.font.SysFont('arial', 25)
        self.reset()
        self.directions = [
            (-self.BLOCK_SIZE, 0),
            (self.BLOCK_SIZE, 0),
            (0, -self.BLOCK_SIZE),
            (0, self.BLOCK_SIZE)
        ]

        self.display = pygame.display.set_mode((self.w, self.h))

    def reset(self) -> None:
        """Reset the game"""
        self.direction = 0
        self.head = (int(self.w/2), int(self.h/2))
        self.snake = [
            self.head,
            (self.head[0] + self.BLOCK_SIZE, self.head[1])
        ]
        self.score = 0
        self._place_food()
        self.clock = pygame.time.Clock()

    def _place_food(self) -> None:
        x = random.randint(0, (self.w - self.BLOCK_SIZE) //
                           self.BLOCK_SIZE) * self.BLOCK_SIZE
        y = random.randint(0, (self.h - self.BLOCK_SIZE) //
                           self.BLOCK_SIZE) * self.BLOCK_SIZE
        self.food = (x, y)
        if self.food in self.snake:
            self._place_food()

    def get_state(self) -> np.ndarray:
        """
        Get the state of the game

        State is represented by a numpy array with 12 elements:
        first 4 elements represent the direction of the snake
        next 4 elements represent if the snake will collide with the wall
        next 4 elements represent the direction of the food

        Returns:
            np.ndarray: state of the game
        """
        state = np.zeros(12, dtype=int)

        if 0 <= self.direction < 4:
            state[self.direction] = 1

        collisions = [
            (self.head[0] - self.BLOCK_SIZE, self.head[1]),  # Left
            (self.head[0] + self.BLOCK_SIZE, self.head[1]),  # Right
            (self.head[0], self.head[1] - self.BLOCK_SIZE),  # Up
            (self.head[0], self.head[1] + self.BLOCK_SIZE),  # Down
        ]
        state[4:8] = [int(self._is_collision(pos)) for pos in collisions]

        state[8:12] = [
            int(self.head[0] > self.food[0]),  # Food is left
            int(self.head[1] > self.food[1]),  # Food is up
            int(self.head[0] < self.food[0]),  # Food is right
            int(self.head[1] < self.food[1])   # Food is down
        ]

        return state

    def play_step(self, human: bool = True, action: int = 0) -> tuple[int, bool, int]:
        self._pick_direction(human, action)
        self._move(self.directions[self.direction])
        self.snake.insert(0, self.head)

        self._draw_elements()

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

    def _draw_elements(self) -> None:
        self.display.fill('black')
        pygame.draw.rect(self.display, 'red', (self.food[0]+4, self.food[1]+4,
                                               self.BLOCK_SIZE-8, self.BLOCK_SIZE-8))
        for segment in self.snake:
            pygame.draw.rect(self.display, 'green', (segment[0]+0.5, segment[1]+0.5,
                                                     self.BLOCK_SIZE-1, self.BLOCK_SIZE-1))

        pygame.draw.rect(self.display, 'blue', (self.head[0]+4, self.head[1]+4,
                                                self.BLOCK_SIZE-8, self.BLOCK_SIZE-8))

        text = self.font.render(
            "Score: " + str(self.score), True, (200, 200, 200))
        self.display.blit(text, [0, 0])
        pygame.display.flip()

    def _pick_direction(self, human: bool, action: int) -> None:
        if human:
            self._human_control()
            self.clock.tick(self.SPEED)
        else:
            self._agent_control(action)

    def _human_control(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and self.direction != 1:
                    self.direction = 0
                elif event.key == pygame.K_RIGHT and self.direction != 0:
                    self.direction = 1
                elif event.key == pygame.K_UP and self.direction != 3:
                    self.direction = 2
                elif event.key == pygame.K_DOWN and self.direction != 2:
                    self.direction = 3

    def _agent_control(self, action: int) -> None:
        if 0 <= action < 4:
            if action == 0 and self.direction != 1:
                self.direction = 0
            elif action == 1 and self.direction != 0:
                self.direction = 1
            elif action == 2 and self.direction != 3:
                self.direction = 2
            elif action == 3 and self.direction != 2:
                self.direction = 3

    def _is_collision(self, head: tuple[int, int]) -> bool:
        x, y = head
        if not (0 <= x < self.w and 0 <= y < self.h):
            return True
        return head in self.snake[1:]

    def _move(self, direction: tuple[int, int]) -> None:
        dx, dy = direction
        self.head = (self.head[0] + dx, self.head[1] + dy)
