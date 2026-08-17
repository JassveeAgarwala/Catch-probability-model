import math


def clamp(value: float, minimum: float = 0.0, maximum: float = 1.0) -> float:
    """
    Restricts a value to a specified range.
    """
    return max(minimum, min(value, maximum))


def normalize_inverse(
    value: float,
    minimum: float,
    maximum: float
) -> float:
    """
    Converts a variable where a higher raw value means
    an easier situation into a difficulty score.

    Example:
    More reaction time = lower difficulty.
    """
    if maximum == minimum:
        return 0.0

    normalized = (value - minimum) / (maximum - minimum)

    return clamp(1.0 - normalized)


def normalize_direct(
    value: float,
    minimum: float,
    maximum: float
) -> float:
    """
    Converts a variable where a higher raw value means
    a more difficult situation into a 0-1 difficulty score.
    """
    if maximum == minimum:
        return 0.0

    normalized = (value - minimum) / (maximum - minimum)

    return clamp(normalized)


def sigmoid(value: float) -> float:
    """
    Logistic sigmoid function.

    Converts a continuous model score into a probability
    between 0 and 1.
    """
    return 1.0 / (1.0 + math.exp(-value))


def round_value(value: float, digits: int = 4) -> float:
    """
    Keeps API output readable.
    """
    return round(value, digits)
