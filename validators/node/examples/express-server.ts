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
