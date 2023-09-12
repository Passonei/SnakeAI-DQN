from snake_game import Snake
from interface import Interface
from agent_DQL import Q_agent
from datetime import datetime
import pymongo
import json

def load_config():
    config = None
    try:
        file = open('config/config.json')
        config = json.load(file)
        file.close()
    except Exception as e:
        print(e)
    finally:
        return config

def save_score(name, score):
    if name == "":
        name = "unknown"
    score_data = {
        "name": name,
        "score": score,
        "date": datetime.now().strftime("%d/%m/%Y")
    }
    scores_collection.insert_one(score_data)

def human_play():
    game.reset()
    human = True
    game.play_step(human=human)
    game.clock.tick(1)
    while True:
        _, game_over, score = game.play_step(human=human)
        if game_over == True:
            button, name = interface.end_game(score, human)
            save_score(name, score)

            if button == 'play':
                human_play()
            elif button == 'menu':
                run_menu()

def agent_play():
    game.reset()

    agent = Q_agent()
    agent.load_model(config_agent['path'])
    agent.epsilon=config_agent['epsilon_play']
    human=False

    while True:
        state = game.get_state()
        move = agent.decision(state)
        reward, game_over, score = game.play_step(human=human, action=move)

        if game_over == True:
            button, name = interface.end_game(score,human)
            save_score(name, score)

            if button == 'play':
                agent_play()
            elif button == 'menu':
                run_menu()

def run_menu():
    button = interface.menu()
    if button == 'play':
        human_play()
    elif button == 'agent':
        agent_play()
    elif button == 'ranking':
        ranking_list = scores_collection.find().sort("score", pymongo.DESCENDING).limit(5)
        button = interface.ranking(ranking_list)
        if button == 'reset':
            scores_collection.delete_many({})
        run_menu()
    elif button == 'settings':
        button = interface.settings()
        game.SPEED = config_game['level'][button]
        run_menu()
    elif button == 'exit':
        exit()

if __name__ == '__main__':
    config = load_config()
    config_game = config['game']
    config_ranking = config['ranking']
    config_agent = config['agent']

    interface = Interface(width=config_game['screen_width'],
                        height=config_game['screen_height'])
                        
    game = Snake(width=config_game['screen_width'], 
                height=config_game['screen_height'],
                BLOCK_SIZE=config_game['BLOCK_SIZE'],
                SPEED=config_game['level']['medium'])

    client = pymongo.MongoClient(config_ranking['adress']) 
    database = client[config_ranking['database']]
    scores_collection = database[config_ranking['collection']]

    run_menu()