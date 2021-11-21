from pydantic import BaseModel, validator


class Vote(BaseModel):
    post_id: int
    direction: int

    @validator("direction")
    def validate_direction(cls, direction):
        if direction not in (1, 0):
            raise ValueError("direction must be either 1 or 0")
        return direction


