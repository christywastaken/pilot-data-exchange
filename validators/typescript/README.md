### === NOTE: This is all very much WIP ===
# TypeScript Validator

TypeScript/Node.js validator for Standard Schema JSON using [Zod](https://zod.dev/) v4.


## Features

- ✅ **Type-safe validation** with full TypeScript support
- ✅ **Generic validation functions** - works with any Zod schema
- ✅ **Standardized errors** - consistent `ValidationError` format
- ✅ **Safe validation** - non-throwing option with `validateSafe()`
- ✅ **Express.js integration** example included

## Installation

```bash
npm install
```

## Usage

See the complete example in [`examples/express-server.ts`](examples/express-server.ts).

```typescript
import { ShipToShoreSchema } from '../src/validators/index.js'
import { validate, ValidationError } from '../src/index.js'
import express from 'express'

const app = express()
const port = 3000

app.use(express.json())

app.post('/rotterdam-pilot', (req, res) => {
  try {
    const validatedData = validate(ShipToShoreSchema, req.body)
    return res.status(200).json({
      success: true,
      message: 'validation passed',
      data: validatedData
    })
  } catch (err) {
    if (err instanceof ValidationError) {
      return res.status(400).json(err)
    }
    return res.status(500).json({ message: 'Internal server error' })
  }
})

app.listen(port, () => {
  console.log(`Server is running at http://localhost:${port}`)
})
```

## Scripts

- `npm run build` - Compile TypeScript to JavaScript
- `npm run dev` - Run Express example in watch mode (with auto-reload)
- `npm run example` - Run compiled Express example server
- `npm run typecheck` - Type check without building
- `npm run clean` - Remove build artifacts
- `npm run prepublishOnly` - Clean and build (runs automatically before publish)

## Development

### Running the Example Server

```bash
# Development mode with auto-reload
npm run dev

# Or build and run
npm run build
npm run example
```

The server will start at `http://localhost:3000`.

### Testing with Example Payloads

Use the example payloads from [`../../examples/payloads/`](../../examples/payloads/):

```bash
# Test with minimal payload
curl -X POST http://localhost:3000/rotterdam-pilot \
  -H "Content-Type: application/json" \
  -d @../../examples/payloads/minimal.json

# Test with full payload
curl -X POST http://localhost:3000/rotterdam-pilot \
  -H "Content-Type: application/json" \
  -d @../../examples/payloads/full.json
```

## Requirements

- Node.js >= 22.0.0
- TypeScript >= 5.6.0
- Zod >= 4.1.0

## Schema Support

Currently supports:
- ✅ `v0.0.2.json` (as `RotterdamPilotSchema`)
- ✅ Generic `validate()` and `validateSafe()` work with any Zod schema

## Error Format

All validation errors follow a consistent format:

```json
{
  "message": "Validation Error",
  "errors": [
    {
      "field": "imoCompendium.arrivalPortCode",
      "message": "Invalid UN/LOCODE format",
      "code": "invalid_format"
    }
  ]
}
```

This format is designed to be consistent across language implementations (Python validator coming soon).

## License

MIT
