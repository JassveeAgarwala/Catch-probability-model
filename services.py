from schemas import CatchRequest
from utils import (
    clamp,
    normalize_direct,
    normalize_inverse,
    sigmoid,
    round_value
)


def calculate_catch_probability(request: CatchRequest) -> dict:
    """
    Main analytical service.

    The model follows five steps:

    1. Convert raw fielding variables into normalized difficulty factors.
    2. Combine the factors using weighted difficulty.
    3. Convert difficulty into a logistic probability.
    4. Classify the catch difficulty.
    5. Return an interpretable analytical result.
    """

    # ---------------------------------------------------------
    # STEP 1: DERIVE NORMALIZED DIFFICULTY VARIABLES
    # ---------------------------------------------------------

    # Greater distance generally increases difficulty.
    distance_difficulty = normalize_direct(
        request.distance_m,
        0,
        30
    )

    # Greater ball speed reduces available adjustment time.
    speed_difficulty = normalize_direct(
        request.ball_speed_mps,
        5,
        40
    )

    # Greater lateral angle means the ball is further away
    # from the fielder's natural body line.
    angle_difficulty = normalize_direct(
        request.lateral_angle_deg,
        0,
        90
    )

    # Less reaction time means greater difficulty.
    reaction_difficulty = normalize_inverse(
        request.reaction_time_s,
        0.2,
        3.0
    )

    # ---------------------------------------------------------
    # STEP 2: CATEGORICAL DIFFICULTY FACTORS
    # ---------------------------------------------------------

    movement_scores = {
        "stationary": 0.00,
        "forward": 0.20,
        "sideways": 0.45,
        "backward": 0.70,
        "diving": 0.90
    }

    height_scores = {
        "waist": 0.00,
        "chest": 0.05,
        "low": 0.25,
        "high": 0.55,
        "overhead": 0.80
    }

    movement_difficulty = movement_scores[
        request.fielder_movement
    ]

    height_difficulty = height_scores[
        request.catch_height
    ]

    # Pressure is already provided on a 0-10 scale.
    pressure_difficulty = normalize_direct(
        request.pressure_level,
        0,
        10
    )

    # ---------------------------------------------------------
    # STEP 3: COMBINE FACTORS
    # ---------------------------------------------------------

    # The weights represent the assumed relative importance
    # of each factor.
    #
    # Reaction time and ball speed receive high weight because
    # they directly affect the time available to respond.
    #
    # Distance and movement also strongly affect difficulty.
    #
    # Height, angle and pressure have smaller but meaningful
    # contextual effects.

    difficulty_score = (
        0.20 * distance_difficulty +
        0.20 * speed_difficulty +
        0.15 * angle_difficulty +
        0.20 * reaction_difficulty +
        0.15 * movement_difficulty +
        0.05 * height_difficulty +
        0.05 * pressure_difficulty
    )

    difficulty_score = clamp(difficulty_score)

    # ---------------------------------------------------------
    # STEP 4: CONVERT DIFFICULTY INTO PROBABILITY
    # ---------------------------------------------------------

    # Logistic transformation.
    #
    # Difficulty = 0 means the situation is easiest.
    # Difficulty = 1 means the situation is hardest.
    #
    # The negative coefficient means that as difficulty
    # increases, catch probability decreases.

    logistic_score = 3.0 - (6.0 * difficulty_score)

    probability = sigmoid(logistic_score)

    probability = clamp(probability)

    # ---------------------------------------------------------
    # STEP 5: INTERPRETATION
    # ---------------------------------------------------------

    if probability >= 0.80:
        difficulty_rating = "Easy"
        interpretation = (
            "The fielding chance has a high estimated probability "
            "of being converted into a successful catch."
        )

    elif probability >= 0.60:
        difficulty_rating = "Moderate"
        interpretation = (
            "The chance is reasonably catchable, but one or more "
            "difficulty factors meaningfully affect the outcome."
        )

    elif probability >= 0.40:
        difficulty_rating = "Difficult"
        interpretation = (
            "The chance has substantial difficulty and requires "
            "good reaction, movement and execution."
        )

    else:
        difficulty_rating = "Very Difficult"
        interpretation = (
            "The fielding chance is highly difficult and has a "
            "relatively low estimated probability of success."
        )

    return {
        "catch_probability": round_value(probability, 4),
        "catch_probability_percent": round_value(probability * 100, 2),
        "difficulty_score": round_value(difficulty_score, 4),
        "difficulty_rating": difficulty_rating,
        "interpretation": interpretation
    }
