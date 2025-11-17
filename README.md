# Standard Schema JSON

Repository for JSON schemas and validators for Rotterdam pilot ship-to-shore operational data exchange, based on the IMO Compendium (FAL.5/Circ. 55).

## Overview

This project provides:
- **JSON Schemas** - Standardized schemas for maritime data exchange
- **Validators** - TypeScript/Node.js and Python validators (Python in TBD)
- **Examples** - Sample payloads and implementation examples

## Repository Structure

```
standard-schema-json/
├── schemas/              # JSON Schema definitions
├── validators/
│   ├── node/            # TypeScript/Node.js validator
│   └── python/          # Python validator (coming soon)
└── examples/            # Example payloads and usage
```

## JSON Schemas

Located in the [`schemas/`](schemas/) directory:

- **`pilot_schema_imo_only.json`** - Core IMO Compendium fields only
- **`pilot_schema_imo_plus_additional.json`** - IMO fields plus additional custom properties

See the [schemas README](schemas/README.md) for detailed descriptions.

## Quick Start

### Node.js Validator

```bash
cd validators/node
npm install
npm run build

# Run example server
npm run example
```

See the [Node.js validator README](validators/node/README.md) for detailed usage.

### Python Validator

Coming soon.

## Example Payloads

Example payloads are available in [`examples/payloads/`](examples/payloads/):

- `imo.json` - Complete payload with all IMO fields
- `with-additional.json` - Payload including additional custom properties

## Usage Example

```typescript
import { RotterdamPilotSchema } from '@standard-schema/validator-node';

const data = {
  imoCompendium: {
    imoNumber: "9876543",
    shipName: "MV Rotterdam Star"
  }
};

const validated = RotterdamPilotSchema.parse(data);
```

## Contributing

Contributions are welcome. Please feel free to submit issues or pull requests.

## License

MIT
