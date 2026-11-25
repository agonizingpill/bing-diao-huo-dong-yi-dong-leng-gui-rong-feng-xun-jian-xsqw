from typing import Annotated

from pydantic import BaseModel, ConfigDict, FiniteFloat, StringConstraints

class ScoreSeam(BaseModel):
    model_config = ConfigDict(extra="forbid")
    sample: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=160)]


class RecordSeam(BaseModel):
    model_config = ConfigDict(extra="forbid")
    code: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=160)]
    token: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=160)]
