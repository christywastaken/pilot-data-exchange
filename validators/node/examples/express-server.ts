
import { ShipToShoreSchema } from '../src/index.js'
import express from 'express'
import { ZodError } from 'zod'

const app = express()
const port = 3000

app.use(express.json())

function formatZodError(error: ZodError) {
  return error.issues.map((issue) => ({
    field: issue.path.join('.'),
    message: issue.message,
    code: issue.code
  }))
}

app.post('/rotterdam-pilot', (req, res) => {
  try {
    const validatedData = ShipToShoreSchema.parse(req.body)
    console.log(validatedData)
    return res.status(200).json({ 
      success: true, 
      message: 'validation passed'
    })
  } catch (err) {
    console.error(err)
    
    if (err instanceof ZodError) {
      return res.status(400).json({ 
        success: false,
        error: 'Validation failed',
        details: formatZodError(err)
      })
    }
    
    return res.status(500).json({ 
      success: false,
      error: 'Internal server error'
    })
  }

})

app.listen(port, () => {
  console.log(`Server is running at http://localhost:${port}`)
})