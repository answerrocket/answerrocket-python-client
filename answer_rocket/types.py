from dataclasses import dataclass

RESULT_EXCEPTION_CODE = 1000

@dataclass
class MaxResult:
    success: bool = False
    code: int | str | None = None
    error: str | None = None
