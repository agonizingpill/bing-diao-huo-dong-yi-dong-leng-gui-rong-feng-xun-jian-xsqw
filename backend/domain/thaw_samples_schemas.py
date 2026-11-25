from typing import Annotated

from pydantic import BaseModel, ConfigDict, FiniteFloat, StringConstraints

class ObserveSeam(BaseModel):
    model_config = ConfigDict(extra="forbid")
    code: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=160)]
    cell: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=160)]
    mass_kg: FiniteFloat
    melt: FiniteFloat
    drift: FiniteFloat
    empty_test: bool
    piece: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=160)]
