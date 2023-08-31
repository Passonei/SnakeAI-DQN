import pygame
import pygame_textinput
from pygame.locals import *
from snake_game import Snake

class Interface:
    def __init__(self, width, height):
        pygame.init()
        self.screen_width = width
        self.screen_height = height
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Snake Game")

        self.font = pygame.font.Font(None, 36)
        self.input_active = False
        self.input_text = ""
        self.clock = pygame.time.Clock()

    def menu(self):
        play_button = self.font.render("Play", True, (255, 255, 255))
        play_button_rect = play_button.get_rect(center=(self.screen_width // 2, self.screen_height // 2 - 50))

        ranking_button = self.font.render("Ranking", True, (255, 255, 255))
        ranking_button_rect = ranking_button.get_rect(center=(self.screen_width // 2, self.screen_height // 2))

        settings_button = self.font.render("Settings", True, (255, 255, 255))
        settings_button_rect = settings_button.get_rect(center=(self.screen_width // 2, self.screen_height // 2 + 50))

        exit_button = self.font.render("Exit", True, (255, 255, 255))
        exit_button_rect = exit_button.get_rect(center=(self.screen_width // 2, self.screen_height // 2 + 100))
        
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                elif event.type == MOUSEBUTTONDOWN:
                    if play_button_rect.collidepoint(event.pos):
                        return "play"
                    elif ranking_button_rect.collidepoint(event.pos):
                        return "ranking"
                    elif settings_button_rect.collidepoint(event.pos):
                        return "settings"
                    elif exit_button_rect.collidepoint(event.pos):
                        return "exit"

            self.screen.fill((0, 0, 0))
            
            self.screen.blit(play_button, play_button_rect)
            self.screen.blit(ranking_button, ranking_button_rect)
            self.screen.blit(settings_button, settings_button_rect)
            self.screen.blit(exit_button, exit_button_rect)
            
            pygame.display.flip()
            self.clock.tick(30)

        pygame.quit()
    
    def settings(self):
        easy_button = self.font.render("Easy", True, (0, 255, 0))
        easy_button_rect = easy_button.get_rect(center=(self.screen_width // 2-150, self.screen_height // 2 + 50))

        medium_button = self.font.render("Medium", True, (255, 255, 0))
        medium_button_rect = medium_button.get_rect(center=(self.screen_width // 2, self.screen_height // 2 + 50))

        hard_button = self.font.render("Hard", True, (255, 0, 0))
        hard_button_rect = hard_button.get_rect(center=(self.screen_width // 2+150, self.screen_height // 2 + 50))
        
        end_game_text = self.font.render("DIFFICULTY LEVEL", True, (255, 255, 255))
        end_game_rect = end_game_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2 - 50))

        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                elif event.type == MOUSEBUTTONDOWN:
                    if easy_button_rect.collidepoint(event.pos):
                        return "easy"
                    elif medium_button_rect.collidepoint(event.pos):
                        return "medium"
                    elif hard_button_rect.collidepoint(event.pos):
                        return "hard"

            self.screen.fill((0, 0, 0))
            
            self.screen.blit(easy_button, easy_button_rect)
            self.screen.blit(medium_button, medium_button_rect)
            self.screen.blit(hard_button, hard_button_rect)
            self.screen.blit(end_game_text, end_game_rect)
            
            pygame.display.flip()
            self.clock.tick(30)
    
    def ranking(self, ranking_list):
        ranking_text = self.font.render("RANKING", True, (255, 255, 255))
        ranking_rect = ranking_text.get_rect(center=(self.screen_width // 2, 50))

        back_button = self.font.render("Back", True, (255, 255, 255))
        back_button_rect = back_button.get_rect(center=(self.screen_width // 2 + 50, self.screen_height - 50))

        reset_button = self.font.render("Reset", True, (255, 255, 255))
        reset_button_rect = reset_button.get_rect(center=(self.screen_width // 2 - 100, self.screen_height - 50))
        empty = True
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                elif event.type == MOUSEBUTTONDOWN:
                    if back_button_rect.collidepoint(event.pos):
                        return 
                    elif reset_button_rect.collidepoint(event.pos):
                        return "reset"

            self.screen.fill((0, 0, 0))
            
            self.screen.blit(ranking_text, ranking_rect)
            self.screen.blit(back_button, back_button_rect)
            self.screen.blit(reset_button, reset_button_rect)

            y_position = 150
            for idx, entry in enumerate(ranking_list):
                score_text = self.font.render(f"{idx + 1}. {entry['name']} - Score: {entry['score']} - {entry['date']}", True, (255, 255, 255))
                score_rect = score_text.get_rect(center=(self.screen_width // 2, y_position))
                self.screen.blit(score_text, score_rect)
                y_position += 50
                pygame.display.flip()
                empty = False

            if empty:
                pygame.display.flip()
            self.clock.tick(30)
    
    def end_game(self, score):
        play_button = self.font.render("Play again", True, (255, 255, 255))
        play_button_rect = play_button.get_rect(center=(self.screen_width // 2, self.screen_height // 2+100))

        menu_button = self.font.render("Menu", True, (255, 255, 255))
        menu_button_rect = menu_button.get_rect(center=(self.screen_width//2, self.screen_height//2+150))

        end_game_text = self.font.render("END GAME", True, (255, 0, 0))
        end_game_rect = end_game_text.get_rect(center=(self.screen_width//2, self.screen_height//2-100))

        score_text = self.font.render(f"Your Score: {score}", True, (255, 0, 0))
        score_rect = score_text.get_rect(center=(self.screen_width//2, self.screen_height//2-50))

        name_text = self.font.render("Enter your name:", True, (255, 255, 255))
        name_rect = name_text.get_rect(center=(self.screen_width//2, self.screen_height//2))
        name_input_rect = pygame.Rect(self.screen_width//3, self.screen_height//2+20, self.screen_width//3, 40)
        input_font = pygame.font.Font(None, 32)

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                elif event.type == MOUSEBUTTONDOWN:
                    if play_button_rect.collidepoint(event.pos):
                        return "play", self.input_text
                    elif menu_button_rect.collidepoint(event.pos):
                        return "menu", self.input_text
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        entered_name = self.input_text
                        print(f"Entered Name: {entered_name}")
                    elif event.key == pygame.K_BACKSPACE:
                        self.input_text = self.input_text[:-1]
                    else:
                        self.input_text += event.unicode

            self.screen.fill((0, 0, 0))

            self.screen.blit(end_game_text, end_game_rect)
            self.screen.blit(score_text, score_rect)            
            self.screen.blit(play_button, play_button_rect)
            self.screen.blit(menu_button, menu_button_rect)
            self.screen.blit(name_text, name_rect)
            
            pygame.draw.rect(self.screen, (255, 255, 255), name_input_rect, 2)
            input_surface = input_font.render(self.input_text, True, (255, 255, 255))
            self.screen.blit(input_surface, (name_input_rect.x + 5, name_input_rect.y + 5))



            pygame.display.flip()
            self.clock.tick(30)

        pygame.quit()
