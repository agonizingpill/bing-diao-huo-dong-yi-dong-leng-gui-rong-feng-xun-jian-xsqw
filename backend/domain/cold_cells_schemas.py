from typing import Annotated

from pydantic import BaseModel, ConfigDict, FiniteFloat, StringConstraints

class SetCellState(BaseModel):
    model_config = ConfigDict(extra="forbid")
    cell: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=160)]
    closed: bool
