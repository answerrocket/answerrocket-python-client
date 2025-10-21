from dataclasses import dataclass

RESULT_EXCEPTION_CODE = 1000

@dataclass
class MaxResult:
    """
    Base result class for AnswerRocket API operations.

    Attributes
    ----------
    success : bool
        Whether the operation succeeded. Defaults to False.
    code : int | str | None
        Error code or status code from the operation.
    error : str | None
        Error message if the operation failed.
    """
    success: bool = False
    code: int | str | None = None
    error: str | None = None
