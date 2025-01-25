import logging
import sys
from pathlib import Path

# Create a folder for logs
LOG_DIR = Path(__file__).parent.parent / "logs"
LOG_DIR.mkdir(exist_ok=True)


class CustomLogger:
    def __init__(self):
        self._logger = logging.getLogger("crossword_maker")
        self._logger.setLevel(logging.DEBUG)

        # Formatter
        formatter = logging.Formatter(
            fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

        # File handler
        file_handler = logging.FileHandler(
            filename=LOG_DIR / "crossword.log", encoding="utf-8"
        )
        file_handler.setFormatter(formatter)
        file_handler.setLevel(logging.DEBUG)

        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        console_handler.setLevel(logging.INFO)

        # Add handlers
        self._logger.addHandler(file_handler)
        self._logger.addHandler(console_handler)

        # Exceptions
        sys.excepthook = self.handle_exception

    def handle_exception(self, exc_type, exc_value, exc_traceback):
        self._logger.error(
            "Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback)
        )

    @property
    def logger(self):
        return self._logger


# Init
logger = CustomLogger().logger

if __name__ == "__main__":
    # Examples
    logger.debug("Debug message (visible only in file)")
    logger.info("Info message")
    logger.warning("Warning message")
    logger.error("Error message")
    logger.critical("Critical message")
