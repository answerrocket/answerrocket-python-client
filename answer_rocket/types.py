from dataclasses import dataclass

RESULT_EXCEPTION_CODE = 1000

@dataclass
class MaxResult:
    success = False
    code = None
    error = None
