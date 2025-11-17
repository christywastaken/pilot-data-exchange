
import { RotterdamPilotSchema } from '../src/index.js'
import express from 'express'

const app = express()
const port = 3000

app.use(express.json())

app.post('/rotterdam-pilot', (req, res) => {
  try {
    const validatedQuery = RotterdamPilotSchema.parse(req.body)
    console.log(validatedQuery)
    return res.status(200).json({message: 'validation passed'})
  } catch (err) {
    console.error(err)
    return res.status(403).json({ 'Validation error': err })
  }

})

app.listen(port, () => {
  console.log(`Server is running at http://localhost:${port}`)
})