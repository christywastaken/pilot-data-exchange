"""Schema validators for Ship to Shore data exchange."""

import re
from datetime import datetime
from typing import Annotated, Optional, Union
from pydantic import BaseModel, Field, ConfigDict, BeforeValidator


# Reusable validator for ISO 8601 date strings
def validate_date_string(v: Union[str, datetime]) -> datetime:
    """Validate and parse ISO 8601 datetime strings."""
    if not isinstance(v, str):
        raise ValueError("Date must be a string in ISO 8601 format")

    if isinstance(v, str):
        # Check for ISO 8601 format with Z timezone
        if not re.match(r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$', v):
            raise ValueError("Invalid date format, expected ISO 8601 format")
        return datetime.fromisoformat(v.replace('Z', '+00:00'))

    raise ValueError(
        "Date must be a string in ISO 8601 format or a datetime object")


# This is a reusable type for date strings with validation and coercion. So, you pass in a string, it validates
# it and converts to datetime. if invalid, raises ValueError.
DateString = Annotated[datetime, BeforeValidator(validate_date_string)]


# Reusable validator for IMO number validation
def validate_imo_number(v: Union[int, str]) -> int:
    """
    Validate IMO number using the check digit algorithm.
    IMO numbers are 7 digits long and follow a specific check digit algorithm.
    """
    # Coerce to int if string
    imo = int(v) if isinstance(v, str) else v
    imo_str = str(imo)

    if len(imo_str) != 7:
        raise ValueError("Invalid IMO number")

    digits = [int(d) for d in imo_str]
    check_digit = digits[6]

    # Calculate check digit: sum of first 6 digits multiplied by their position (7-index)
    calculated_check = sum(digit * (7 - index)
                           for index, digit in enumerate(digits[:6])) % 10

    if check_digit != calculated_check:
        raise ValueError("Invalid IMO number")

    return imo

# Reusable type for IMO numbers with validation and coercion
ImoNumber = Annotated[int, BeforeValidator(validate_imo_number)]


# Reusable validator for UN/LOCODE format
def validate_unlocode(v: str) -> str:
    """Validate UN/LOCODE format: 2 letters + 3 letters/digits."""
    if not re.match(r'^[A-Z]{2}[A-Z0-9]{3}$', v):
        raise ValueError("Invalid UN/LOCODE format")
    return v


# Reusable type for UN/LOCODE with validation
UnLocode = Annotated[str, BeforeValidator(validate_unlocode)]


class ImoCompendiumProperties(BaseModel):
    """Properties of the IMO Compendium as per FAL.5/Circ. 55."""
    model_config = ConfigDict(extra='forbid')

    imo_number: ImoNumber = Field(alias="imoNumber")
    ship_name: Optional[str] = Field(None, alias="shipName")
    # TODO: [ENH] - e.g. max 2 decimal places, positive, etc.
    draught_overall: Optional[float] = Field(None, alias="draughtOverall")
    # TODO: [ENH] - e.g. max 2 decimal places, positive, etc.
    draught_forward: Optional[float] = Field(None, alias="draughtForward")
    # TODO: [ENH] - e.g. max 2 decimal places, positive, etc.
    draught_aft: Optional[float] = Field(None, alias="draughtAft")
    # TODO: [ENH] - validate against actual UN/LOCODE list?
    arrival_port_code: Optional[UnLocode] = Field(
        None, alias="arrivalPortCode")
    # TODO: [ENH] - validate against actual UN/LOCODE list?
    departure_port_code: Optional[UnLocode] = Field(
        None, alias="departurePortCode")
    # NOTE: Should this be optional as we won't have actual arrival, until we arrive?
    arrival_actual: Optional[DateString] = Field(None, alias="arrivalActual")
    arrival_estimated: Optional[DateString] = Field(
        None, alias="arrivalEstimated")
    ship_true_heading: Optional[float] = Field(
        None, alias="shipTrueHeading", ge=0, le=360)


class AdditionalProperties(BaseModel):
    """Properties of the additional (non-IMO) fields."""
    model_config = ConfigDict(extra='forbid')

    arrival_estimated_berth: Optional[DateString] = Field(
        None, alias="arrivalEstimatedBerth")
    arrival_estimated_port: Optional[DateString] = Field(
        None, alias="arrivalEstimatedPort")
    arrival_estimated_pilot_boarding_place: Optional[DateString] = Field(
        None, alias="arrivalEstimatedPilotBoardingPlace")


class ShipToShore(BaseModel):
    """Schema for Rotterdam Pilot - Ship to Shore data exchange."""
    model_config = ConfigDict(extra='forbid')

    imo_compendium: ImoCompendiumProperties = Field(alias="imoCompendium")
    additional: Optional[AdditionalProperties] = None


# Type alias for convenience (equivalent to TypeScript's type inference)
ShipToShoreType = ShipToShore
