import os
import json
import logging


def open_json(file_path: str) -> dict:
    with open(file_path) as file:
        return json.load(file)


def save_json(file_path: str, data: dict) -> None:
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)


def logger_setup(level: str, app: str) -> logging.Logger:
    if not os.path.exists("logs"):
        os.makedirs("logs")

    level = getattr(logging, level)

    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[
            logging.FileHandler(f"logs/{app}.log"),
            logging.StreamHandler()
        ]
    )

    logger = logging.getLogger(app)
    return logger
