# Node.js Validator

TypeScript/Node.js validator for Standard Schema JSON using [Zod](https://zod.dev/).

## Features

- Type-safe validation with TypeScript
- Runtime validation using Zod v4
- Express.js integration example

## Installation

```bash
npm install
```

## Usage

### As a Library

```typescript
import { RotterdamPilotSchema } from '@standard-schema/validator-node';

// Validate data
try {
  const validated = RotterdamPilotSchema.parse({
    imoCompendium: {
      imoNumber: "9876543",
      shipName: "MV Rotterdam Star"
    }
  });
  console.log('Valid!', validated);
} catch (error) {
  console.error('Validation failed:', error);
}
```

### With Express.js

See the complete Express.js example in [`examples/express-server.ts`](examples/express-server.ts).

```typescript
import { RotterdamPilotSchema } from './src/index.js';
import express from 'express';

const app = express();
app.use(express.json());

app.post('/validate', (req, res) => {
  try {
    const validated = RotterdamPilotSchema.parse(req.body);
    res.json({ success: true, data: validated });
  } catch (err) {
    res.status(400).json({ error: 'Validation failed', details: err });
  }
});

app.listen(3000);
```

## Scripts

- `npm run build` - Compile TypeScript to JavaScript
- `npm run dev` - Run Express example in watch mode
- `npm run example` - Run compiled Express example server
- `npm run typecheck` - Type check without building
- `npm run clean` - Remove build artifacts

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
# Test with full payload
curl -X POST http://localhost:3000/rotterdam-pilot \
  -H "Content-Type: application/json" \
  -d @../../examples/payloads/full.json
```

## Requirements

- Node.js >= 22.0.0
- TypeScript >= 5.6.0

## Schema Support

Currently supports:
-  `pilot_schema_imo_only.json` (as `RotterdamPilotSchema`)
-  `pilot_schema_imo_plus_additional.json` (coming soon)

## License

MIT
