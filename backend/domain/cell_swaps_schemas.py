from typing import Annotated

from pydantic import BaseModel, ConfigDict, FiniteFloat, StringConstraints

class ReserveSwap(BaseModel):
    model_config = ConfigDict(extra="forbid")
    code: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=160)]
    seam: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=160)]
    target: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=160)]
    handover: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=160)]


class ConfirmSwap(BaseModel):
    model_config = ConfigDict(extra="forbid")
    swap: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=160)]
    stamp: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=160)]
