import { z, ZodSchema, ZodError } from 'zod'
/**
 * Creates a standardized validation error.
 */
export class ValidationError extends Error {
	public readonly errors: Array<{
		field: string
		message: string
		code: string
	}>

	constructor(message: string, errors: Array<{ field: string; message: string; code: string }>) {
		super(message)
		this.name = 'ValidationError'
		this.errors = errors
	}

	toJSON() {
		return {
			message: this.message,
			errors: this.errors
		}
	}
}

/**
 * Validates data against a Zod schema and throws a ValidationError if validation fails.
 */
export function validate<T extends ZodSchema>(schema: T, data: unknown): z.infer<T> {
	try {
		return schema.parse(data)
	} catch (error) {
		if (error instanceof ZodError) {
			throw formatZodError(error)
		}
		throw error
	}
}

/**
 * Safely validates against a Zod schema, without throwing if Zod fails to validate
 */
export function validateSafe<T extends ZodSchema>(
	schema: T,
	data: unknown
): { success: true; data: z.infer<T> } | { success: false; error: ValidationError } {
	try {
		const result = schema.parse(data)
		return { success: true, data: result }
	} catch (error) {
		if (error instanceof ZodError) {
			return { success: false, error: formatZodError(error) }
		}
		throw error
	}
}

/**
 * Stich together the issues in Zod to create a standardized error template.
 * TODO: probably remake this when we implement the errors in python too, so both have the same errors.
 */
function formatZodError(error: ZodError) {
	const errors = error.issues.map((issue) => ({
		field: issue.path.join('.'),
		message: issue.message,
		code: issue.code
	}))
	return new ValidationError('Validation Error', errors)
}
