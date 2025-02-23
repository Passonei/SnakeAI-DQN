from datetime import datetime
from src.utils.utils import open_json, save_json


class Ranking:
    """
    Class to manage the ranking of the game

    Args:
        ranking_path: path to the ranking file
        max_size: maximum number of scores to be stored

    Attributes:
        scores: list of scores
        max_size: maximum number of scores to be stored
    """

    def __init__(self, ranking_path: str, max_size: int):
        self.ranking_path = ranking_path
        self.scores = open_json(ranking_path)
        self.max_size = max_size

    def reset(self) -> None:
        """Reset the scores list"""
        self.scores = []

    def add_score(self, name: str, score: int) -> None:
        """Add a new score to the ranking list"""
        length = len(self.scores)
        lowest_score = self.scores[-1][1] if length == self.max_size else 0

        if score > lowest_score:
            if name == "":
                name = "unknown"

            date = str(datetime.now().strftime("%Y-%m-%d"))
            self.scores.append([name, score, date])

            self._sort()
            self._delete()
            self._save()

    def _sort(self) -> None:
        self.scores = sorted(self.scores, key=lambda x: x[1], reverse=True)

    def _delete(self) -> None:
        self.scores = self.scores[:self.max_size]

    def _save(self) -> None:
        save_json(self.ranking_path, self.scores)
