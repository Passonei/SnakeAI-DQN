import random
import numpy as np
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Dense,InputLayer
from tensorflow.keras.optimizers import Adam

class Q_agent:
    def __init__(self) -> None:
        self.learning_rate = 0.001
        self.epsilon = 0.9
        self.epsilon_decay = 0.997
        self.epsilon_min = 0.01
        self.discount_rate = 0.9
        self.input_shape = (12,)
        self.model = self.bulid_model()

    def bulid_model(self):
        model = Sequential()
        model.add(InputLayer(input_shape=self.input_shape))
        model.add(Dense(128, activation='relu'))
        model.add(Dense(64, activation='relu'))
        model.add(Dense(4, activation='softmax'))
        model.compile(loss='mse', optimizer=Adam(learning_rate=self.learning_rate))
        return model
    
    def decision(self, state):
        if np.random.rand() <= self.epsilon:
            return random.randint(0, 3)
        else:
            decision = self.model.predict(state[np.newaxis,...],verbose=0)
            return np.argmax(decision[0])

    def fit(self, state, action, reward, next_state, done):
        target = reward
        if not done:
            q_next = np.amax(self.model.predict(next_state[np.newaxis,...],verbose=0))
            target = reward + self.discount_rate * q_next
        target_f = self.model.predict(state[np.newaxis,...],verbose=0)
        target_f[0][action] = target

        self.model.fit(state[np.newaxis,...], [target_f], epochs=1, verbose=0)

        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    def save_model(self,path):
        self.model.save(path)

    def load_model(self,path):
        self.model = load_model(path)
