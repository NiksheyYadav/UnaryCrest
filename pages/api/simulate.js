import { spawn } from 'child_process'
import path from 'path'

export default async function handler(req, res) {
  // Only allow POST requests
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed. Use POST.' })
  }

  try {
    const { a, b, speed_ms } = req.body

    // Validate input
    if (typeof a !== 'string' || typeof b !== 'string') {
      return res.status(400).json({ 
        error: 'Invalid input. Expected { a: string, b: string, speed_ms?: number }' 
      })
    }

    // Validate unary format (only '1's or empty string)
    if (a && !/^1+$/.test(a)) {
      return res.status(400).json({ 
        error: 'Invalid unary number for "a". Must be a string of 1s (e.g., "111")' 
      })
    }
    if (b && !/^1+$/.test(b)) {
      return res.status(400).json({ 
        error: 'Invalid unary number for "b". Must be a string of 1s (e.g., "11")' 
      })
    }

    // Prepare input JSON for Python
    const inputData = JSON.stringify({
      a: a || '',
      b: b || '',
      speed_ms: speed_ms || 0
    })

    // Get the path to the Python script
    const scriptPath = path.join(process.cwd(), 'turing-machine-addition.py')

    // Spawn Python process
    const python = spawn('python3', [scriptPath, '--json'])

    let stdout = ''
    let stderr = ''

    // Collect stdout
    python.stdout.on('data', (data) => {
      stdout += data.toString()
    })

    // Collect stderr
    python.stderr.on('data', (data) => {
      stderr += data.toString()
    })

    // Write input to stdin
    python.stdin.write(inputData)
    python.stdin.end()

    // Wait for process to complete
    await new Promise((resolve, reject) => {
      python.on('close', (code) => {
        if (code === 0) {
          resolve()
        } else {
          reject(new Error(`Python process exited with code ${code}`))
        }
      })

      python.on('error', (err) => {
        reject(err)
      })
    })

    // Parse the JSON output
    try {
      const result = JSON.parse(stdout)
      
      // Check if result contains an error
      if (result.error) {
        return res.status(500).json({
          error: result.error,
          message: result.message || 'Simulation error'
        })
      }

      // Return successful result
      return res.status(200).json(result)
      
    } catch (parseError) {
      console.error('Failed to parse Python output:', stdout)
      console.error('Stderr:', stderr)
      return res.status(500).json({
        error: 'Failed to parse simulator output',
        details: parseError.message,
        stdout: stdout.substring(0, 200),
        stderr: stderr.substring(0, 200)
      })
    }

  } catch (error) {
    console.error('Simulation error:', error)
    return res.status(500).json({
      error: 'Internal server error',
      message: error.message
    })
  }
}
