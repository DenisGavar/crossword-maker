class CrosswordError(Exception):
    def __init__(self, message: str = "Crossword maker error"):
        super().__init__(message)
        self.message = message

    def __str__(self):
        return f"{self.__class__.__name__}: {self.message}"


class APIError(CrosswordError):
    def __init__(
        self,
        message: str = "API request failed",
        status_code: int = None,
        endpoint: str = None,
    ):
        super().__init__(message)
        self.status_code = status_code
        self.endpoint = endpoint

    def __str__(self):
        details = []
        if self.status_code:
            details.append(f"status code: {self.status_code}")
        if self.endpoint:
            details.append(f"endpoint: {self.endpoint}")
        return (
            f"{super().__str__()} ({', '.join(details)})"
            if details
            else super().__str__()
        )


class WordNotFoundError(CrosswordError):
    def __init__(self, pattern: str = None, length: int = None):
        message = "Failed to find suitable word"
        if pattern or length:
            message += " for criteria:"
            if pattern:
                message += f" pattern='{pattern}'"
            if length:
                message += f" length={length}"
        super().__init__(message)


class GridGenerationError(CrosswordError):
    def __init__(self, size: int, attempts: int):
        super().__init__(
            f"Failed to generate grid of size {size}x{size} "
            f"after {attempts} attempts"
        )


class ValidationError(CrosswordError):
    def __init__(self, field: str, value: str):
        super().__init__(f"Invalid value '{value}' for field '{field}'")


class ConfigurationError(CrosswordError):
    def __init__(self, config_key: str):
        super().__init__(f"Missing or invalid configuration for: {config_key}")
