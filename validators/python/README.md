# Python Validator

Python validator for Standard Schema JSON v0.0.1.

## Features

- Runtime validation using Pydantic
- Type hints for static analysis
- IMO number validation with check digit algorithm
- UN/LOCODE format validation
- ISO 8601 datetime parsing
- Standardized error formatting

## Installation

This project uses [uv](https://docs.astral.sh/uv/) for dependency management.

```bash
# Install dependencies and sync environment
uv sync
```

## Usage

### Basic Validation

```python
from src.validators.index import ShipToShore
from src.index import validate, ValidationError

data = {
    "imoCompendium": {
        "imoNumber": 9876543,
        "shipName": "MV Rotterdam Star",
        "arrivalPortCode": "NLRTM"
    }
}

try:
    validated = validate(ShipToShore, data)
    print(f"Valid data: {validated}")
except ValidationError as e:
    print(f"Validation failed: {e.to_json()}")
```

### Flask Example

See `examples/flask_server.py` for a complete Flask server example:

```bash
uv run examples/flask_server.py
```

Then test with:

```bash
curl -X POST http://localhost:3000/rotterdam-pilot \
  -H "Content-Type: application/json" \
  -d @../../examples/payloads/imo.json
```

## Schema

The validator implements the Ship to Shore Operational Data Exchange schema v0.0.2, including:

- **IMO Compendium** (FAL.5/Circ. 55): IMO number, ship details, draughts, port codes, arrival times, heading
- **Additional Fields**: Extended ETA fields for berth, port, and pilot boarding place



## License

MIT
