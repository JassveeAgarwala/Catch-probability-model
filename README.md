# Catch Probability Model API

## API Name

Catch Probability Model

## API Number

API 11

## Sprint

Sprint 2 — Player Analytics Sprint — Phase 1

## Student

Student 4 — Fielding Analytics


# 1. Objective

The Catch Probability Model estimates the likelihood that a fielding chance will be converted into a successful catch.

The API does not treat every catch opportunity as equal. It considers factors such as distance, ball speed, reaction time, lateral angle, fielder movement, catch height and match pressure.

The raw inputs are converted into normalized difficulty variables. These variables are combined into a single difficulty score and then transformed into a probability using a logistic function.

The final response provides both a numerical catch probability and a human-readable difficulty interpretation.


# 2. Scientific Principle

The model uses a weighted difficulty model followed by a logistic sigmoid transformation.

The general structure is:

difficulty = weighted combination of normalized difficulty factors

probability = 1 / (1 + e^(-z))

where:

z = 3 - 6 × difficulty

The logistic function is useful because it converts a continuous model score into a value between 0 and 1, allowing the result to be interpreted as a probability.

A higher difficulty score therefore produces a lower catch probability.


# 3. Raw Inputs

The API accepts the following raw variables:

| Field | Type | Range | Meaning |
|---|---|---|---|
| distance_m | float | 0–50 | Approximate distance involved in the fielding chance |
| ball_speed_mps | float | 1–50 | Estimated ball speed in metres per second |
| lateral_angle_deg | float | 0–90 | Angle of the ball from the fielder's body line |
| reaction_time_s | float | 0.1–5 | Estimated time available for reaction |
| fielder_movement | string | fixed categories | Movement required by the fielder |
| catch_height | string | fixed categories | Approximate height of the ball |
| pressure_level | float | 0–10 | Contextual pressure level |


# 4. Derived Variables

The API creates the following intermediate variables.

## distance_difficulty

Normalizes distance into a 0–1 difficulty scale.

A larger distance produces greater difficulty.

## speed_difficulty

Normalizes ball speed into a 0–1 difficulty scale.

A faster ball produces greater difficulty.

## angle_difficulty

Measures how far the ball is from the fielder's natural body line.

A larger lateral angle produces greater difficulty.

## reaction_difficulty

Uses inverse normalization.

Less available reaction time produces greater difficulty.

## movement_difficulty

Converts movement categories into numerical difficulty values.

The scale is:

stationary = 0.00

forward = 0.20

sideways = 0.45

backward = 0.70

diving = 0.90

## height_difficulty

Converts catch height into numerical difficulty.

The scale is:

waist = 0.00

chest = 0.05

low = 0.25

high = 0.55

overhead = 0.80

## pressure_difficulty

Converts the 0–10 pressure input into a 0–1 difficulty value.


# 5. Difficulty Score

The derived variables are combined using the following weighted model:

difficulty_score =
    0.20 × distance_difficulty
  + 0.20 × speed_difficulty
  + 0.15 × angle_difficulty
  + 0.20 × reaction_difficulty
  + 0.15 × movement_difficulty
  + 0.05 × height_difficulty
  + 0.05 × pressure_difficulty

The result is constrained between 0 and 1.

0 represents a very easy opportunity.

1 represents an extremely difficult opportunity.


# 6. Final Catch Probability

The difficulty score is converted into a logistic model score:

z = 3 - 6 × difficulty_score

The final probability is:

P(catch) = 1 / (1 + e^(-z))

The result is between 0 and 1.

It is also returned as a percentage.


# 7. Difficulty Interpretation

The API uses the following interpretation:

Probability >= 0.80
    Easy

Probability >= 0.60 and < 0.80
    Moderate

Probability >= 0.40 and < 0.60
    Difficult

Probability < 0.40
    Very Difficult


# 8. Endpoint

POST

/api/v1/catch-probability


# 9. Example Request

```json
{
    "distance_m": 8.5,
    "ball_speed_mps": 24.0,
    "lateral_angle_deg": 35.0,
    "reaction_time_s": 1.4,
    "fielder_movement": "sideways",
    "catch_height": "chest",
    "pressure_level": 5
}
