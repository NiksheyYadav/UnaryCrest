# Turing Machine Addition Simulator - Quick Start Guide

## Installation & Setup

No installation needed! The simulator uses only Python's standard library.

```bash
python turing-machine-addition.py
```

---

## Quick Usage Examples

### Example 1: Simple Addition
```python
from turing-machine-addition import TuringMachine

# Create a machine instance
tm = TuringMachine()

# Run addition: 3 + 2
result = tm.run(3, 2)
print(f"Result: {result}")  # Output: Result: 5
```

### Example 2: Multiple Operations
```python
tm = TuringMachine()

# Test multiple additions
test_cases = [(3, 2), (5, 1), (2, 3), (1, 1)]

for num1, num2 in test_cases:
    result = tm.run(num1, num2)
    print(f"{num1} + {num2} = {result}")
```

### Example 3: Access Execution Log
```python
tm = TuringMachine()
result = tm.run(3, 2)

# Get step-by-step execution trace
log = tm.get_execution_log()

for entry in log:
    print(f"Step {entry['step']}: State {entry['state']}, "
          f"Head at {entry['position']}, Symbol: {entry['symbol']}")
```

### Example 4: View State Diagram
```python
tm = TuringMachine()
tm.print_state_diagram()
```

---

## Function Reference

### `TuringMachine()`
Initialize a new Turing Machine instance.

```python
tm = TuringMachine()
```

---

### `initialize_tape(num1, num2)`
Set up the tape with two numbers in unary format.

**Parameters:**
- `num1` (int): First number (≥ 0)
- `num2` (int): Second number (≥ 0)

**Example:**
```python
tm.initialize_tape(3, 2)  # Sets up "111+11" on tape
```

---

### `run(num1, num2, verbose=True)`
Execute the complete addition operation.

**Parameters:**
- `num1` (int): First operand
- `num2` (int): Second operand
- `verbose` (bool): Print step-by-step output (default: True)

**Returns:**
- (int): Result of addition

**Example:**
```python
result = tm.run(5, 3)  # Returns 8
result = tm.run(0, 7)  # Returns 7
```

---

### `step()`
Execute a single transition of the Turing Machine.

**Returns:**
- (bool): True if halted, False if can continue

**Example:**
```python
while not tm.step():
    print(f"Current state: {tm.current_state}")
```

---

### `get_execution_log()`
Retrieve the complete step-by-step execution history.

**Returns:**
- (list): List of dictionaries with step information

**Example:**
```python
log = tm.get_execution_log()
for entry in log:
    print(entry)
```

---

### `print_state_diagram()`
Print the state diagram and transition table.

**Example:**
```python
tm.print_state_diagram()
```

---

## Testing

### Run All Tests
```bash
python turing-machine-addition.py
```

### Run Specific Test
```python
from turing-machine-addition import TuringMachine

tm = TuringMachine()

# Test a specific operation
result = tm.run(5, 3)
assert result == 8, f"Expected 8, got {result}"
print("Test passed!")
```

---

## Understanding the Output

### Sample Run Output
```
======================================================================
Initialized tape for 3 + 2
======================================================================
Tape content: 111 + 11
Tape representation: _111+11_
Head position: 1
Initial state: q0

Step 0: δ(q0, '1') = (q0, '1', R) | Head: 2
Step 1: δ(q0, '1') = (q0, '1', R) | Head: 3
Step 2: δ(q0, '1') = (q0, '1', R) | Head: 4
Step 3: δ(q0, '+') = (q2, '+', R) | Head: 5
Step 4: δ(q2, '1') = (q3, '1', R) | Head: 6
Step 5: δ(q3, '1') = (q3, '1', R) | Head: 7
Step 6: δ(q3, '_') = (q4, '_', L) | Head: 6
Step 7: δ(q4, '1') = (q5, '1', S) | Head: 6

======================================================================
EXECUTION COMPLETE
======================================================================
Final tape: _111+11
Final state: q5
Result: 3 + 2 = 5
Total steps: 8
======================================================================
```

### Interpretation
- **δ(q, a) = (q', a', d)**: Transition from state q with symbol a
- **Head position**: Current tape head location
- **Total steps**: Number of transitions executed
- **Final state q5**: Machine reached halt state (success)

---

## Supported Operations

| Operation | Example | Result |
|-----------|---------|--------|
| Addition | 3 + 2 | 5 |
| Unequal lengths | 5 + 1 | 6 |
| Reversed order | 2 + 3 | 5 |
| Minimal input | 1 + 1 | 2 |
| Zero addition | 0 + 5 | 5 |
| Equal numbers | 4 + 4 | 8 |

---

## Error Handling

### Invalid Input
```python
try:
    tm.run(-1, 3)  # Negative number
except ValueError as e:
    print(f"Error: {e}")
```

### Out of Bounds
The tape automatically extends with blanks as needed.

---

## Performance Notes

- **Time Complexity**: O(n + m) where n and m are the operands
- **Space Complexity**: O(n + m) for tape storage
- **Typical Run**: 5-10 steps for single-digit numbers

---

## Debugging Tips

1. **Enable Verbose Output**: Default is enabled, shows each step
2. **Check Execution Log**: Use `get_execution_log()` for detailed trace
3. **Verify Tape State**: Print `tm.tape` after each step
4. **Monitor Head Position**: Watch `tm.head_position` changes
5. **Track Current State**: Print `tm.current_state` for debugging

---

## Troubleshooting

**Q: Why does my addition give unexpected results?**
A: Ensure you're using non-negative integers. Unary doesn't support negative numbers.

**Q: How do I visualize the tape?**
A: Use the step-by-step output or print the execution log.

**Q: Can I modify the transition table?**
A: Yes! Edit the `self.transitions` dictionary in the `__init__` method.

**Q: How do I add more states?**
A: Add entries to both `self.states` dictionary and update `self.transitions` accordingly.

---

## Advanced Customization

### Custom Transition Function
```python
tm = TuringMachine()
tm.transitions[('q0', 'X')] = ('q1', 'Y', 'R')
```

### Custom Tape Initialization
```python
tm.tape = ['_', '1', '1', '+', '1', '_']
tm.head_position = 1
tm.current_state = 'q0'
```

---

## Performance Optimization

For large numbers, the simulator processes O(n + m) transitions. To speed up:
- Reduce verbose output
- Use batch processing instead of single operations

---

## References

- Turing Machine Theory
- Automata Theory: B.Tech 5th Semester CSE
- Formal Languages and Computability

---

## License & Attribution

Project: Design and Implementation of a Turing Machine for Unary Arithmetic Operations
Course: Automata Theory (B.Tech 5th Semester CSE)
Professor: Susanta Kundu
Date: November 17, 2025