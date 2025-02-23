from snake_game import Snake
from interface import Interface
from agents.agent_DQL import DQL_agent
from ranking.ranking import Ranking
from utils import open_json


def human_play():
    game.reset()
    human = True
    game.play_step(human=human)
    game.clock.tick(1)
    while True:
        play_game(human, None)


def agent_play():
    game.reset()

    agent = DQL_agent(learning_rate=0.001,
                      epsilon=0.9,
                      epsilon_decay=0.997,
                      epsilon_min=0.01,
                      discount_rate=0.9
                      )
    agent.load_model(config_agent["path"])
    agent.epsilon = config_agent["epsilon_play"]
    human = False

    while True:
        state = game.get_state()
        move = agent.decision(state)
        play_game(human, move)


def play_game(human, move):
    _, game_over, score = game.play_step(human=human, action=move)
    if game_over:
        button, name = interface.end_game(score, human)

        ranking.add_score(name, score)

        if button == "play":
            agent_play()
        elif button == "menu":
            run_menu()


def run_menu():
    button = interface.menu()
    if button == "play":
        human_play()
    elif button == "agent":
        agent_play()
    elif button == "ranking":
        ranking_list = ranking.scores
        button = interface.ranking(ranking_list)
        if button == "reset":
            ranking.reset()
        run_menu()
    elif button == "settings":
        button = interface.settings()
        game.SPEED = config_game["level"][button]
        run_menu()
    elif button == "exit":
        exit()


if __name__ == "__main__":
    config = open_json("config/config.json")
    config_game = config["game"]
    config_ranking = config["ranking"]
    config_agent = config["agent"]

    ranking = Ranking(
        config_ranking["path"], config_ranking["max_size"]
    )

    interface = Interface(
        width=config_game["screen_width"],
        height=config_game["screen_height"]
    )

    game = Snake(
        width=config_game["screen_width"],
        height=config_game["screen_height"],
        BLOCK_SIZE=config_game["BLOCK_SIZE"],
        SPEED=config_game["level"]["medium"]
    )

    run_menu()
