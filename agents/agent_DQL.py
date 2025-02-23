import random
import numpy as np
from abc import ABC, abstractmethod
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Dense, InputLayer
from tensorflow.keras.optimizers import Adam


class Agent(ABC):
    """
    Abstract class for agents
    """

    @abstractmethod
    def decision(self, state: np.ndarray) -> int:
        raise NotImplementedError

    @abstractmethod
    def _score_state(self, state: np.array) -> float:
        raise NotImplementedError


class DQL_agent(Agent):
    """
    Q-learning agent

    Args:
        learning_rate: learning rate of the model
        epsilon: probability of random move
        epsilon_decay: decay of epsilon
        epsilon_min: minimum value of epsilon
        discount_rate: discount rate of the model

    Attributes:
        learning_rate (float): learning rate of the model
        epsilon (float): probability of random move
        epsilon_decay (float): decay of epsilon
        epsilon_min (float): minimum value of epsilon
        discount_rate (float): discount rate of the model
        input_shape (tuple): shape of the input
        model (Sequential): model of the agent
    """

    def __init__(
        self,
        learning_rate: float,
        epsilon: float,
        epsilon_decay: float,
        epsilon_min: float,
        discount_rate: float
    ) -> None:

        self.learning_rate = learning_rate
        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay
        self.epsilon_min = epsilon_min
        self.discount_rate = discount_rate
        self.input_shape = (12,)
        self.model = self._bulid_model()

    def decision(self, state: np.ndarray) -> int:
        """
        Decision of the agent

        Args:
            state: state of the game

        Returns:
            int: action of the agent
        """
        if np.random.rand() <= self.epsilon:
            return random.randint(0, 3)
        else:
            return np.argmax(self._score_state(state))

    def fit(
        self,
        state: np.array,
        action: int,
        reward: float,
        next_state: np.array,
        done: bool
    ) -> None:
        """
        Fit the model

        Args:
            state: state of the game
            action: action of the agent
            reward: reward of the agent
            next_state: next state of the game
            done: if the game is over
        """
        target = reward
        if not done:
            q_val = np.amax(self._score_state(next_state))
            target = reward + self.discount_rate * q_val

        target_f = self._score_state(state)
        target_f[0][action] = target

        self.model.fit(state[np.newaxis, ...], [target_f], epochs=1, verbose=0)

        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    def save_model(self, path: str) -> None:
        """
        Save the model

        Args:
            path: path to save the model
        """
        self.model.save(path)

    def load_model(self, path: str) -> None:
        """
        Load the model

        Args:
            path: path to load the model
        """
        self.model = load_model(path)

    def _bulid_model(self) -> Sequential:
        model = Sequential()
        model.add(InputLayer(input_shape=self.input_shape))
        model.add(Dense(128, activation="relu"))
        model.add(Dense(64, activation="relu"))
        model.add(Dense(4, activation="softmax"))
        model.compile(
            loss="mse",
            optimizer=Adam(learning_rate=self.learning_rate)
        )
        return model

    def _score_state(self, state: np.array) -> float:
        return self.model.predict(state[np.newaxis, ...], verbose=0)
