import { useState, useEffect } from 'react'
import Head from 'next/head'

export default function Home() {
  const [num1, setNum1] = useState(3)
  const [num2, setNum2] = useState(2)
  const [speed, setSpeed] = useState(800)
  const [isRunning, setIsRunning] = useState(false)
  const [currentState, setCurrentState] = useState('q0')
  const [stepCount, setStepCount] = useState(0)
  const [tape, setTape] = useState(['_'])
  const [headPosition, setHeadPosition] = useState(0)
  const [executionLog, setExecutionLog] = useState([])
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)

  const initializeTape = (a, b) => {
    const newTape = ['_']
    for (let i = 0; i < a; i++) newTape.push('1')
    newTape.push('+')
    for (let i = 0; i < b; i++) newTape.push('1')
    newTape.push('_')
    return newTape
  }

  const resetMachine = () => {
    setCurrentState('q0')
    setStepCount(0)
    setTape(initializeTape(num1, num2))
    setHeadPosition(1)
    setExecutionLog([])
    setResult(null)
    setError(null)
    setIsRunning(false)
  }

  const runSimulation = async () => {
    if (isRunning) return
    
    if (num1 < 0 || num2 < 0 || num1 > 20 || num2 > 20) {
      setError('Please enter numbers between 0 and 20')
      return
    }

    setIsRunning(true)
    setError(null)
    setResult(null)

    try {
      const response = await fetch('/api/simulate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          a: '1'.repeat(num1),
          b: '1'.repeat(num2),
          speed_ms: speed
        })
      })

      const data = await response.json()

      if (!response.ok) {
        throw new Error(data.error || 'Simulation failed')
      }

      // Animate through transitions
      setExecutionLog([])
      setTape(initializeTape(num1, num2))
      setHeadPosition(1)
      setCurrentState('q0')
      setStepCount(0)

      // Animate each transition
      for (let i = 0; i < data.transitions.length; i++) {
        await new Promise(resolve => setTimeout(resolve, speed))
        
        const transition = data.transitions[i]
        setCurrentState(transition.state)
        setHeadPosition(transition.head)
        setStepCount(i + 1)
        setExecutionLog(prev => [...prev, transition])

        // Update tape display based on snapshot
        const tapeArray = ['_', ...transition.tape_snapshot.split(''), '_']
        setTape(tapeArray)
      }

      // Show result
      const finalOnes = data.final_tape.replace(/[^1]/g, '').length
      setResult({
        num1,
        num2,
        result: finalOnes,
        finalTape: data.final_tape
      })
      setCurrentState('q5')
      
    } catch (err) {
      setError(err.message)
    } finally {
      setIsRunning(false)
    }
  }

  useEffect(() => {
    resetMachine()
  }, [])

  return (
    <>
      <Head>
        <title>UnaryCrest - Interactive Turing Machine Simulator</title>
        <meta name="description" content="Interactive Turing Machine Simulator for Unary Addition" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
      </Head>

      <div className="container">
        <header>
          <h1>🎯 UnaryCrest</h1>
          <p className="subtitle">Interactive Turing Machine Simulator for Unary Addition</p>
          <p className="description">
            Experience the beauty of computational theory through an interactive visualization of a Turing Machine 
            performing unary arithmetic. Watch as the machine processes numbers represented as sequences of 1&apos;s 
            and performs addition through elegant state transitions.
          </p>
        </header>

        <div className="controls-section">
          <h2>✨ Control Panel</h2>
          <div className="input-group">
            <div className="input-field">
              <label htmlFor="num1">First Number</label>
              <input 
                type="number" 
                id="num1" 
                value={num1} 
                onChange={(e) => setNum1(parseInt(e.target.value) || 0)}
                min="0" 
                max="20"
                disabled={isRunning}
              />
            </div>
            <div style={{fontSize: '2em', fontWeight: 'bold', color: '#667eea'}}>+</div>
            <div className="input-field">
              <label htmlFor="num2">Second Number</label>
              <input 
                type="number" 
                id="num2" 
                value={num2}
                onChange={(e) => setNum2(parseInt(e.target.value) || 0)}
                min="0" 
                max="20"
                disabled={isRunning}
              />
            </div>
          </div>
          <div className="input-group">
            <button 
              className="btn btn-primary" 
              onClick={runSimulation}
              disabled={isRunning}
            >
              {isRunning ? '⏳ Running...' : '▶ Run Simulation'}
            </button>
            <button 
              className="btn btn-secondary" 
              onClick={resetMachine}
              disabled={isRunning}
            >
              🔄 Reset
            </button>
          </div>
          <div className="speed-control">
            <label htmlFor="speed">Animation Speed:</label>
            <input 
              type="range" 
              id="speed" 
              min="100" 
              max="2000" 
              value={speed}
              step="100"
              onChange={(e) => setSpeed(parseInt(e.target.value))}
              disabled={isRunning}
            />
            <span id="speedLabel">{speed}ms</span>
          </div>
        </div>

        {error && (
          <div className="error-display">
            ❌ Error: {error}
          </div>
        )}

        <div className="visualization-section">
          <h2>📼 Tape Visualization</h2>
          <div className="state-display">
            Current State: <span className="state-current">{currentState}</span>
            <span style={{marginLeft: '30px'}}>Step: <span className="state-current">{stepCount}</span></span>
          </div>
          <div className="tape-container">
            {tape.map((symbol, index) => (
              <div 
                key={index}
                className={`tape-cell ${index === headPosition ? 'head' : ''} ${symbol === '_' ? 'blank' : ''}`}
              >
                {symbol === '_' ? '□' : symbol}
              </div>
            ))}
          </div>
          {result && (
            <div className="result-display show">
              <div>✅ Computation Complete!</div>
              <div style={{marginTop: '10px', fontSize: '1.2em'}}>
                {result.num1} + {result.num2} = {result.result}
              </div>
              <div style={{marginTop: '10px', fontSize: '0.8em', color: '#666'}}>
                &quot;{'1'.repeat(result.num1)} + {'1'.repeat(result.num2)}&quot; → &quot;{result.finalTape}&quot;
              </div>
            </div>
          )}
        </div>

        <div className="visualization-section">
          <h2>🔄 State Diagram</h2>
          <div className="state-diagram">
            {['q0', 'q1', 'q2', 'q3', 'q4', 'q5'].map(state => (
              <div 
                key={state}
                className={`state-node ${state === 'q5' ? 'halt' : ''} ${state === currentState ? 'active' : ''}`}
              >
                {state}
              </div>
            ))}
          </div>
        </div>

        <div className="visualization-section">
          <h2>📝 Execution Log</h2>
          <div className="execution-log">
            {executionLog.length === 0 ? (
              <p style={{textAlign: 'center', color: '#999'}}>Run a simulation to see the execution log...</p>
            ) : (
              executionLog.map((entry, index) => (
                <div 
                  key={index}
                  className={`log-entry ${index === executionLog.length - 1 ? 'highlight' : ''}`}
                >
                  Step {index}: δ({entry.state}, &apos;{entry.read}&apos;) = ({entry.state}, &apos;{entry.write}&apos;, {entry.direction}) | Head: {entry.head}
                </div>
              ))
            )}
          </div>
        </div>

        <div className="info-panel">
          <h2>📚 About Unary Addition</h2>
          <div className="info-grid">
            <div className="info-card">
              <h3>🔢 What is Unary?</h3>
              <p>Unary is a base-1 numeral system where numbers are represented by sequences of 1&apos;s. For example, 3 is &quot;111&quot; and 5 is &quot;11111&quot;.</p>
            </div>
            <div className="info-card">
              <h3>⚙️ How It Works</h3>
              <p>The Turing Machine reads through the first number, processes the &apos;+&apos; separator, moves through the second number, and produces the result through state transitions.</p>
            </div>
            <div className="info-card">
              <h3>🎯 States Explained</h3>
              <p>q0: Initial state, q1: Reserved, q2: Replace separator, q3: Process second number, q4: Finalize, q5: Halt (accept)</p>
            </div>
            <div className="info-card">
              <h3>💡 Algorithm</h3>
              <p>The machine performs addition by moving through both operands and utilizing clever state transitions. Time complexity: O(n+m)</p>
            </div>
          </div>
        </div>

        <footer>
          <p><strong>UnaryCrest - Turing Machine Addition Simulator</strong></p>
          <p>Automata Theory Project - B.Tech 5th Semester CSE</p>
          <p>Created with ❤️ for computational theory education</p>
        </footer>
      </div>
    </>
  )
}
