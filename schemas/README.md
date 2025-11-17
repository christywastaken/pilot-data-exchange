# JSON Schemas

This directory contains JSON Schema definitions for ship-to-shore operational data exchange based on the IMO Compendium (FAL.5/Circ. 55).

## Available Schemas

### pilot_schema_imo_only.json

**Purpose:** Core IMO Compendium fields only  
**Version:** 2.0.0  
**IMO Compendium:** FAL.5/Circ. 55 (approved by FAL 49 in 2025)

This schema includes only the standard IMO Compendium fields:
- Ship identification (IMO number, ship name)
- Draught measurements (overall, forward, aft)
- Port information (arrival/departure codes)
- Timing information (actual/estimated arrival)
- Ship heading

**Use this schema when:** You need strict compliance with IMO standards and don't require custom extensions.

### pilot_schema_imo_plus_additional.json

**Purpose:** IMO Compendium fields plus additional custom properties  
**Version:** 2.0.0  
**IMO Compendium:** FAL.5/Circ. 55 (approved by FAL 49 in 2025)

This schema extends the core IMO fields with an `additional` section containing:
- Arrival estimate at berth
- Arrival estimate at port
- Arrival estimate at pilot boarding place

**Use this schema when:** You need IMO compliance plus additional timing and location data.

## Field Descriptions

#### NOTE: TBC which fields we want as required and optional

### Required Fields
- `imoNumber` (string) - IMO ship identification number from certificate
- `shipName` (string) - Ship name from IMO certificates

### Optional Fields
- `draughtOverall` (number, ≥0) - Maximum present static draught in meters
- `draughtForward` (number, ≥0) - Forward draught in meters
- `draughtAft` (number, ≥0) - Aft draught in meters
- `arrivalPortCode` (string) - Code for arrival port
- `departurePortCode` (string) - Code for departure port
- `arrivalActual` (datetime) - Actual time of arrival (ATA)
- `arrivalEstimated` (datetime) - Estimated time of arrival (ETA)
- `shipTrueHeading` (number, 0-360) - Ship heading in degrees from true north

## Example Payloads

See [`../examples/payloads/`](../examples/payloads/) for complete example payloads.

## Validation

Use the validators in [`../validators/`](../validators/) to validate data against these schemas:
- Node.js/TypeScript validator: [`validators/node/`](../validators/node/)
- Python validator: Coming soon
