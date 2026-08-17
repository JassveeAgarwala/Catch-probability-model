from fastapi import FastAPI, HTTPException
from schemas import CatchRequest, CatchResponse
from services import calculate_catch_probability
from pydantic import ValidationError

app = FastAPI(
    title="Catch Probability Model API",
    description="API for estimating the probability of converting a fielding chance into a successful catch.",
    version="1.0.0"
)


@app.get("/")
def root():
    return {
        "api_name": "Catch Probability Model",
        "status": "running",
        "version": "1.0.0"
    }


@app.post("/api/v1/catch-probability", response_model=CatchResponse)
def catch_probability(request: CatchRequest):

    try:
        result = calculate_catch_probability(request)
        return result

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc)
        )
