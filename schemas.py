from pydantic import BaseModel, Field
from typing import Literal


class CatchRequest(BaseModel):
    """
    Raw information about a fielding chance.

    These values describe the conditions at the moment
    the fielder attempts the catch.
    """

    distance_m: float = Field(
        ...,
        ge=0,
        le=50,
        description="Approximate distance the ball travels toward the fielder after the chance is created, in metres."
    )

    ball_speed_mps: float = Field(
        ...,
        ge=1,
        le=50,
        description="Estimated speed of the ball at the time of the fielding chance, in metres per second."
    )

    lateral_angle_deg: float = Field(
        ...,
        ge=0,
        le=90,
        description="Angle of the ball from the fielder's body line. 0 is directly in front and 90 is directly to the side."
    )

    reaction_time_s: float = Field(
        ...,
        ge=0.1,
        le=5,
        description="Estimated time available for the fielder to react, in seconds."
    )

    fielder_movement: Literal[
        "stationary",
        "forward",
        "sideways",
        "backward",
        "diving"
    ] = Field(
        ...,
        description="Type of movement required from the fielder."
    )

    catch_height: Literal[
        "low",
        "waist",
        "chest",
        "high",
        "overhead"
    ] = Field(
        ...,
        description="Approximate height of the ball when the catch opportunity occurs."
    )

    pressure_level: float = Field(
        ...,
        ge=0,
        le=10,
        description="Contextual pressure level from 0 (low pressure) to 10 (very high pressure)."
    )


class CatchResponse(BaseModel):
    """
    Analytical output of the Catch Probability Model.
    """

    catch_probability: float = Field(
        ...,
        ge=0,
        le=1,
        description="Estimated probability of successfully completing the catch."
    )

    catch_probability_percent: float = Field(
        ...,
        ge=0,
        le=100,
        description="Catch probability expressed as a percentage."
    )

    difficulty_score: float = Field(
        ...,
        ge=0,
        le=1,
        description="Overall difficulty score. 0 is easiest and 1 is most difficult."
    )

    difficulty_rating: str = Field(
        ...,
        description="Human-readable difficulty classification."
    )

    interpretation: str = Field(
        ...,
        description="Plain-language explanation of the analytical result."
    )
