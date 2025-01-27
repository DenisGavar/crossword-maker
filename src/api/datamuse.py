from typing import Optional
import requests
import random

from src.utils.logger import logger
from src.utils import exceptions
from src.config.config import Config


class DatamuseAPI:
    def __init__(self):
        self.base_url = "https://api.datamuse.com/words"

    def get_words(self, pattern: str = None) -> Optional[str]:
        params = {
            "sp": pattern,
            "max": 100,
            "md": "dpf",
        }

        try:
            response = requests.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()
            return self._filter_words(response.json())
        except requests.exceptions.RequestException as e:
            logger.error(f"Datamuse API error: {str(e)}")
            raise exceptions.APIError("Failed to fetch word from Datamuse API")

    def _filter_words(self, data: list) -> Optional[str]:
        if not data:
            return None

        filtered = []
        for item in data:
            word = item.get("word", "")
            tags = item.get("tags", [])

            # The word must contain only letters
            if not word.isalpha():
                continue

            # We need only nouns
            if not "n" in tags:
                continue

            # We need words with a certain frequency
            freq = 0
            for tag in tags:
                if tag.startswith("f:"):
                    try:
                        freq = float(tag.split(":")[1])
                        break
                    except ValueError as e:
                        logger.error(f"Datamuse API error: {str(e)}")
                        raise exceptions.APIError("Failed to get a word frequency")

            if freq > Config.MIN_WORD_FREQUENCY:
                filtered.append((word, freq))

        # return random.choice(filtered) if filtered else None

        return [
            pair[0] for pair in sorted(filtered, key=lambda pair: pair[1], reverse=True)
        ]
