"# UnaryCrest

## 🎯 Interactive Turing Machine Simulator for Unary Addition

An elegant, interactive web-based visualization of a Turing Machine that performs unary arithmetic addition. Built with Next.js frontend and Python backend, featuring real-time animations and API integration.

## ✨ Features

- **Next.js Frontend** - Modern React-based UI with server-side rendering
- **Python Backend Integration** - Calls Python Turing Machine simulator via API routes
- **Real-time Tape Visualization** - Watch the Turing Machine head move across the tape
- **State Diagram** - Visual representation of all machine states
- **Step-by-Step Execution** - Detailed log of every transition
- **Adjustable Speed** - Control animation speed from 100ms to 2000ms
- **Docker Support** - Fully containerized development environment
- **JSON API** - RESTful API for programmatic access
- **Responsive Design** - Works on desktop, tablet, and mobile

## 🚀 Quick Start

### Option 1: Run Locally with Node.js

Prerequisites: Node.js 18+ and Python 3

```bash
# Clone the repository
git clone https://github.com/NiksheyYadav/UnaryCrest.git
cd UnaryCrest

# Install dependencies
npm install

# Run the development server
npm run dev
```

Then visit http://localhost:3000

### Option 2: Run with Docker Compose

Prerequisites: Docker and Docker Compose

```bash
# Clone the repository
git clone https://github.com/NiksheyYadav/UnaryCrest.git
cd UnaryCrest

# Build and start the container
docker-compose up

# Or run in detached mode
docker-compose up -d
```

Then visit http://localhost:3000

To stop the container:
```bash
docker-compose down
```

### Option 3: View the Static HTML

Simply open `index.html` in your web browser for a standalone JavaScript version:

```bash
# Open in your default browser (or double-click index.html)
open index.html  # macOS
xdg-open index.html  # Linux
start index.html  # Windows
```

### Run the Python Simulator (CLI)

Run the traditional test suite:

```bash
python3 turing-machine-addition.py
```

Run in JSON mode:

```bash
echo '{"a":"111","b":"11","speed_ms":200}' | python3 turing-machine-addition.py --json
```

## 📡 API Reference

### POST /api/simulate

Endpoint for running the Turing Machine simulator.

**Request:**
```json
{
  "a": "111",
  "b": "11",
  "speed_ms": 200
}
```

**Response:**
```json
{
  "initial_tape": "111_11",
  "transitions": [
    {
      "state": "q0",
      "head": 2,
      "read": "1",
      "write": "1",
      "direction": "R",
      "tape_snapshot": "111+11"
    },
    ...
  ],
  "final_tape": "11111",
  "steps": 8
}
```

**Error Response:**
```json
{
  "error": "Invalid unary number for \"a\". Must be a string of 1s (e.g., \"111\")"
}
```

**Example with curl:**
```bash
curl -X POST http://localhost:3000/api/simulate \
  -H "Content-Type: application/json" \
  -d '{"a":"111","b":"11","speed_ms":200}'
```

## 🏗️ Architecture

This project integrates Next.js and Python in a unique way:

1. **Frontend (Next.js/React)**: Provides the interactive UI at `pages/index.js`
2. **API Route (`pages/api/simulate.js`)**: Next.js API route that spawns Python as a child process
3. **Python Simulator (`simulator.py`)**: Efficient Turing Machine implementation with JSON I/O
4. **Python CLI (`turing-machine-addition.py`)**: Wrapper that supports both CLI and JSON modes

The Python process is spawned per-request by the Next.js API route, communicating via stdin/stdout with JSON.

## 🛠️ Development

### Project Structure

```
UnaryCrest/
├── pages/
│   ├── _app.js                 # Next.js app wrapper
│   ├── index.js                # Main UI page
│   └── api/
│       └── simulate.js         # API endpoint for Python integration
├── public/
│   └── styles.css              # Global styles
├── simulator.py                # Efficient Turing Machine module
├── turing-machine-addition.py  # Python CLI (supports --json mode)
├── index.html                  # Standalone HTML version
├── package.json                # Node.js dependencies
├── next.config.js              # Next.js configuration
├── Dockerfile                  # Docker image definition
├── docker-compose.yml          # Docker Compose configuration
└── README.md                   # This file
```

### Building for Production

```bash
npm run build
npm run start
```

### Docker Production Build

Update the Dockerfile CMD to:
```dockerfile
CMD ["npm", "run", "build && npm", "run", "start"]
```

## 📖 Documentation

- **[Quick Start Guide](quick-start-guide.md)** - Detailed usage instructions
- **[Project Report](tm-project-report.md)** - Complete design and implementation details

## 🎓 About

This project demonstrates the implementation of a Turing Machine simulator for performing addition on unary numbers (e.g., 3 + 2 = 5 represented as "111 + 11" → "11111").

**Course:** Automata Theory - B.Tech 5th Semester CSE  
**Purpose:** Educational demonstration of computational theory concepts

The project showcases:
- Turing Machine simulation and visualization
- Integration of Python backend with Next.js frontend
- Efficient tape representation using lists instead of string concatenation
- JSON-based API communication between processes
- Containerization with Docker

## 🤝 Contributing

Feel free to explore, learn, and contribute to this educational project!

## 📄 License

Created for educational purposes as part of the Automata Theory coursework." 
