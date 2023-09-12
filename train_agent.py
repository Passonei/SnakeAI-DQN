from snake_game import Snake
from agent_DQL import Q_agent
import pygame

def train():    
    agent = Q_agent()
    game = Snake()
    game.reset()
    num_of_games = 0
    record=9

    while True:
        old_state = game.get_state()

        move = agent.decision(old_state)

        reward, done, score = game.play_step(human=False, action=move)

        new_state = game.get_state()

        if record<20:
            agent.fit(old_state, move, reward, new_state, done)
        elif reward!=0:
            agent.fit(old_state, move, reward, new_state, done)
        if done:

            if game.score>record:
                record = game.score
                print(game.score)
                agent.save_model(f"models/score{game.score}.h5")
            game.reset()
            num_of_games += 1
            print("Game: ",num_of_games)
            print("Probability of random move: ", round(agent.epsilon,3))

        if num_of_games == 200:
            break

if __name__ == "__main__":
    pygame.init()
    train()