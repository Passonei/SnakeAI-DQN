from snake_game import Snake
from interface import Interface
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

    while True:
        game_over, score = game.play_step()
        if game_over == True:
            button, name = interface.end_game(score)
            save_score(name, score)

            if button == 'play':
                human_play()
            elif button == 'menu':
                run_menu()

def run_menu():
    button = interface.menu()
    if button == 'play':
        human_play()
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

# jesli agent to automatycznie czyta nazwe i po grze zapisuje do bazy danych