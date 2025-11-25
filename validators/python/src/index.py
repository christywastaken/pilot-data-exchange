"""Core validation utilities."""

from typing import Any, Dict, List, Type, TypeVar, Union
from pydantic import BaseModel, ValidationError as PydanticValidationError


class ValidationError(Exception):
    """Creates a standardized validation error."""

    def __init__(
        self,
        message: str,
        errors: List[Dict[str, str]]
    ) -> None:
        super().__init__(message)
        self.errors = errors
        self.name = "ValidationError"

    def to_json(self) -> Dict[str, Any]:
        """Convert error to JSON-serializable dictionary."""
        return {
            "message": str(self),
            "errors": self.errors
        }


T = TypeVar("T", bound=BaseModel)


def validate(model: Type[T], data: Any) -> T:
    """
    Validates data against a Pydantic model and throws a ValidationError if validation fails.

    Args:
        model: The Pydantic model class to validate against
        data: The data to validate (dict, JSON string, or any compatible type)

    Returns:
        The validated model instance

    Raises:
        ValidationError: If validation fails
    """
    try:
        # If data is a dict, use model_validate, otherwise let Pydantic handle it
        if isinstance(data, dict):
            return model.model_validate(data)
        else:
            return model.model_validate_json(data) if isinstance(data, (str, bytes)) else model.model_validate(data)
    except PydanticValidationError as error:
        raise _format_pydantic_error(error)


def _format_pydantic_error(error: PydanticValidationError) -> ValidationError:
    """
    Stitch together the issues in Pydantic to create a standardized error template.
    TODO: probably remake this when we implement the errors in TypeScript too, so both have the same errors.

    Args:
        error: The Pydantic validation error

    Returns:
        A standardized ValidationError
    """
    errors = []
    for err in error.errors():
        # Join the location path with dots
        field = ".".join(str(loc) for loc in err["loc"])
        errors.append({
            "field": field,
            "message": err["msg"],
            "code": err["type"]
        })
    return ValidationError("Validation Error", errors)
