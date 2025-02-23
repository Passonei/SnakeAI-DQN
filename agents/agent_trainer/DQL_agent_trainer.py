import pygame
import numpy as np
from collections import deque

from snake_game import Snake
from agents.agent_DQL import DQL_agent
from utils import open_json, logger_setup


class Trainer:
    """
    Class to train the agent

    There are two training modes:
    - Basic training: the agent trains every step
    In this mode, the agent learns surroundings, goal and how to move 

    - Advanced training: the agent trains only when eating the apple or dying
    In this mode, the agent learns achieving higher scores

    Args:
        model_path: path to the model
        env_hyperparams: hyperparameters of the environment
        agent_hyperparams: hyperparameters of the agent

    Attributes:
        env_hyperparams (dict): hyperparameters of the environment
        agent (DQL_agent): agent to train
        game (Snake): game to play
        min_to_save (int): minimum score to save the model
        num_of_games (int): number of games played
        basic_training (bool): training mode
        logger (Logger): logger
    """

    def __init__(
        self,
        model_path: str,
        env_hyperparams: dict[str, int],
        agent_hyperparams: dict[str, int]
    ):
        self.env_hyperparams = env_hyperparams
        self.game = Snake()
        self.game.reset()
        self.min_to_save = env_hyperparams["min_to_save"]
        self.num_of_games = 0
        self.basic_training = True
        self.logger = logger_setup("INFO", "DQL_train")
        self.agent = DQL_agent(**agent_hyperparams)
        self.best_score = 0
        self.last_5 = deque(maxlen=5)
        if model_path:
            self.agent.load_model(model_path)

        self.logger.info(
            f"Starting training for the agent with DQL algorithm, "
            f"env_hyperparams: {env_hyperparams}, "
            f"agent_hyperparams: {agent_hyperparams}"
        )

    def train(self) -> None:
        """
        Method to train the agent
        """
        while self.num_of_games < self.env_hyperparams["max_games"]:
            old_state, move, reward, new_state, done = self._play()
            self._train_agent(old_state, move, reward, new_state, done)

            if done:
                self._reset_round()

    def _train_agent(
        self,
        old_state: np.array,
        move: int,
        reward: float,
        new_state: np.array,
        done: bool
    ) -> None:
        if self.basic_training:
            self.agent.fit(old_state, move, reward, new_state, done)
        elif reward != 0:
            self.agent.fit(old_state, move, reward, new_state, done)

    def _reset_round(self) -> None:
        if self.game.score > self.min_to_save:
            self._save_best_model()

        if self.game.score > self.env_hyperparams["training_bound"]:
            self.basic_training = False

        self.last_5.append(self.game.score)
        if self.game.score > self.best_score:
            self.best_score = self.game.score

        self.logger.info(
            f"Game: {self.num_of_games}, Score: {self.game.score}, "
            f"Best score: {self.best_score}, "
            f"Mean_last_5: {round(np.mean(self.last_5), 2)}, "
            f"Probability of random move: {round(self.agent.epsilon, 3)}"
        )

        self.game.reset()
        self.num_of_games += 1

    def _play(self) -> tuple[np.array, int, float, np.array, bool]:
        old_state = self.game.get_state()
        move = self.agent.decision(old_state)
        reward, done, _ = self.game.play_step(human=False, action=move)
        new_state = self.game.get_state()

        return old_state, move, reward, new_state, done

    def _save_best_model(self) -> None:
        self.min_to_save = self.game.score
        self.agent.save_model(f"models/score{self.game.score}.h5")

        self.logger.info(f"Model saved with score: {self.game.score}")

    def _draw_info(self) -> None:
        text = self.game.font.render(
            "Game: " + str(self.num_of_games), True, (200, 200, 200))
        self.game.display.blit(text, [150, 0])

        score_text = self.game.font.render(
            "Best: " + str(self.best_score), True, (200, 200, 200))
        self.game.display.blit(score_text, [300, 0])

        mean_text = self.game.font.render(
            "Mean (5): " + str(round(np.mean(self.last_5), 2)), True, (200, 200, 200))
        self.game.display.blit(mean_text, [400, 0])

        pygame.display.flip()


if __name__ == "__main__":
    config = open_json("agents/agent_trainer/train_config.json")
    pygame.init()
    trainer = Trainer(**config)
    trainer.train()
