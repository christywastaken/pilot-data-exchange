import z from "zod";

// Reusable schema for ISO 8601 date strings
const DateStringSchema = z
  .string()
  .refine((value) => /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$/.test(value), {
    message: "Invalid date format, expected ISO 8601 format",
  })
  .transform((value) => new Date(value));

// Reusable schema for IMO number validation
const ImoNumberSchema = z.coerce.number().refine(
    (val) => {
      // IMO numbers are 7 digits long and follow a specific check digit algorithm
      const str = val.toString();
      if (str.length !== 7) return false;
      const digits = str.split("").map(Number);
      const checkDigit = digits[6];
      const calculatedCheck = digits.slice(0, 6).reduce((sum, digit, index) => sum + digit * (7 - index), 0) % 10;
      return checkDigit === calculatedCheck;
    },
    { message: "Invalid IMO number" }
  )

// Properties of the IMO Compendium as per FAL.5/Circ. 55
const ImoCompendiumPropertiesSchema = z.strictObject({
  imoNumber: ImoNumberSchema,
  shipName: z.string(),
  draughtOverall: z.coerce.number(), // TODO: [ENH] - e.g. max 2 decimal places, positive, etc.
  draughtForward: z.coerce.number(), // TODO: [ENH] - e.g. max 2 decimal places, positive, etc.
  draughtAft: z.coerce.number(), // TODO: [ENH] - e.g. max 2 decimal places, positive, etc.
  arrivalPortCode: z.string().regex(/^[A-Z]{2}[A-Z0-9]{3}$/, "Invalid UN/LOCODE format"), // TODO: [ENH] - validate against actual UN/LOCODE list?
  departurePortCode: z.string().regex(/^[A-Z]{2}[A-Z0-9]{3}$/, "Invalid UN/LOCODE format"), // TODO: [ENH] - validate against actual UN/LOCODE list?
  arrivalActual: DateStringSchema.optional(), // NOTE: Should this be optional as we won't have actual arrival, until we arrive?
  arrivalEstimated: DateStringSchema,
  shipTrueHeading: z.coerce.number().min(0).max(360),
});

export const RotterdamPilotSchema = z.strictObject({
  imoCompendium: ImoCompendiumPropertiesSchema,
});
