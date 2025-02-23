import pygame
from pygame.locals import *

LEVELS = {"easy": (0, 255, 0), "medium": (255, 255, 0), "hard": (255, 0, 0)}
MENU = ["play", "agent", "ranking", "settings", "exit"]


class Interface:
    """
    Class to manage the interface of the game

    Args:
        width: width of the screen
        height: height of the screen

    Attributes:
        screen (pygame.Surface): screen of the game
        font (pygame.font.Font): font of the text
        clock (pygame.time.Clock): clock of the game
    """

    def __init__(self, width: int, height: int):
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Snake Game")
        self.font = pygame.font.Font(None, 36)
        self.clock = pygame.time.Clock()
        self.center = (width // 2, height // 2)

    def menu(self) -> str:
        """Display the menu of the game"""
        buttons = {
            name: self._create_button(
                name.capitalize(), (self.center[0], 120 + i * 50)
            ) for i, name in enumerate(MENU)
        }
        while True:
            action = self._handle_events(buttons)
            if action:
                return action
            self._draw_buttons(buttons)

    def settings(self) -> str:
        """Display the settings of the game"""
        buttons = {
            lvl: self._create_button(
                lvl.capitalize(),
                (self.center[0] - 150 + i * 150, self.center[1] + 50),
                color
            ) for i, (lvl, color) in enumerate(LEVELS.items())
        }
        buttons["title"] = self._create_button(
            "DIFFICULTY LEVEL", (self.center[0], self.center[1] - 50)
        )
        while True:
            action = self._handle_events(buttons)
            if action in LEVELS.keys():
                return action
            self._draw_buttons(buttons)

    def ranking(self, ranking_list: list) -> str:
        """Display the ranking of the game"""
        buttons = {
            "back": self._create_button("Back", (self.center[0] + 100, self.center[1] * 2 - 50)),
            "reset": self._create_button("Reset", (self.center[0] - 100, self.center[1] * 2 - 50)),
            "RANKING": self._create_button("RANKING", (self.center[0], 50))
        }

        for i, entry in enumerate(ranking_list):
            buttons[f"entry_{i}"] = self._create_button(
                f"{i+1}. {entry[0]} - {entry[1]} - {entry[2]}", (self.center[0], 150 + i * 50))

        while True:
            action = self._handle_events(buttons)
            if action in ["back", "reset"]:
                return action
            self._draw_buttons(buttons)

    def end_game(self, score: int, human: bool) -> tuple:
        """Display the end game screen"""
        buttons = {"play": self._create_button("Play again", (self.center[0], self.center[1] + 100)),
                   "menu": self._create_button("Menu", (self.center[0], self.center[1] + 150))}
        self.name = "Agent Deep Q-learning" if not human else ""

        buttons["score"] = self._create_button(
            f"{'Your' if human else 'Agent'} Score: {score}",
            (self.center[0], self.center[1] - 150)
        )

        if human:
            buttons["input"] = self._create_button(
                "Enter your name", (self.center[0], self.center[1] - 100))

        while True:
            action = self._handle_events(buttons, human)
            if action:
                return action, self.name

            if human:
                buttons["name"] = self._create_button(
                    self.name, (self.center[0], self.center[1] - 50))

            self._draw_buttons(buttons)

    def _create_button(
            self,
            text: str,
            position: tuple[int, int],
            color: tuple[int, int, int] = (255, 255, 255)
    ) -> tuple[pygame.Surface, pygame.Rect]:
        button = self.font.render(text, True, color)
        return button, button.get_rect(center=position)

    def _draw_buttons(self, buttons: dict) -> None:
        self.screen.fill((0, 0, 0))
        for text, rect in buttons.values():
            self.screen.blit(text, rect)
        pygame.display.flip()

    def _handle_events(self, buttons: dict, human: bool = False) -> str:
        for event in pygame.event.get():
            if event.type == QUIT:
                return "exit"

            elif event.type == MOUSEBUTTONDOWN:
                for action, (_, rect) in buttons.items():
                    if rect.collidepoint(event.pos):
                        return action

            elif event.type == pygame.KEYDOWN and human:
                if event.key == pygame.K_BACKSPACE:
                    self.name = self.name[:-1]
                else:
                    self.name += event.unicode
