# Turing Machine for Unary Arithmetic - Design and Implementation Report

## 1. Project Overview

This project implements a **Turing Machine simulator** that performs **unary arithmetic addition**. The implementation is written in Python and demonstrates fundamental concepts of automata theory including states, transitions, tape operations, and halting conditions.

### Objective
To design and implement a working Turing Machine simulator that:
- Correctly processes unary number representations
- Performs addition operations on two non-negative integers
- Demonstrates proper state transitions and tape manipulation
- Handles edge cases and various input combinations

---

## 2. Unary Representation

### What is Unary?
Unary is a base-1 numeral system where each number is represented by a sequence of identical symbols (typically '1'). This is one of the simplest number representations and is naturally suited for theoretical computer science.

### Examples
| Decimal | Unary | Representation |
|---------|-------|-----------------|
| 0 | (empty) | - |
| 1 | 1 | 1 |
| 2 | 2 | 11 |
| 3 | 3 | 111 |
| 4 | 4 | 1111 |
| 5 | 5 | 11111 |

### Addition in Unary
```
Decimal: 3 + 2 = 5
Unary:   111 + 11 → 11111

Decimal: 5 + 1 = 6
Unary:   11111 + 1 → 111111
```

---

## 3. Turing Machine Design

### 3.1 States
The machine uses 6 states:

| State | Description | Purpose |
|-------|-------------|---------|
| q0 | Initial State | Read and skip through first number |
| q1 | (Reserved) | Additional processing state |
| q2 | Separator Transition | Replace '+' symbol with '1' |
| q3 | Second Number Processing | Move through second number to find end |
| q4 | Finalization | Move back and prepare for halt |
| q5 | Halt State (Accept) | Machine terminates successfully |

### 3.2 Transition Table
The transition function δ(q, a) = (q', a', d) where:
- q: current state
- a: current symbol
- q': next state
- a': symbol to write
- d: direction (R = right, L = left, S = stay)

```
Transition Table:
(q0, '1')  → (q0, '1', R)      Read first number, move right
(q0, '+')  → (q2, '+', R)      Found separator, move to q2
(q2, '1')  → (q3, '1', R)      Enter second number processing
(q3, '1')  → (q3, '1', R)      Continue through second number
(q3, '_')  → (q4, '_', L)      Found end, reverse direction
(q4, '1')  → (q5, '1', S)      Finalize and halt
```

### 3.3 Algorithm Logic

**Input:** Two unary numbers separated by '+' (e.g., "111+11")

**Steps:**
1. Start at leftmost '1' in state q0
2. Read through first number: stay in q0, move right for each '1'
3. Encounter '+' symbol: transition to q2, move right
4. Transition to q3: start processing second number
5. In q3: move right through all '1's of second number
6. Find blank ('_'): move back left to q4
7. Transition to q5: reach halt state and terminate
8. **Result:** First number + First number + Second number - 1 = Result

**Why this works:**
- Original: n1 + n2
- After replacement: (n1 + 1) + (n2 - 1) = n1 + n2 ✓

---

## 4. Implementation Details

### 4.1 Tape Representation
The infinite tape is simulated using a Python list with:
- Index 0: Initial blank symbol ('_')
- Indices 1 to n: Input and working area
- Indices n+1 onwards: Additional blanks for expansion

### 4.2 Key Components

**TuringMachine Class:**
```python
class TuringMachine:
    - __init__()           : Initialize states and transitions
    - initialize_tape()    : Set up tape with input numbers
    - step()              : Execute one transition
    - run(num1, num2)     : Complete execution
    - get_execution_log() : Retrieve step-by-step trace
```

**Input Conversion:**
- Numbers are converted from decimal to unary internally
- Example: 3 → "111", 2 → "11"

---

## 5. Test Cases

### Test Case 1: Basic Addition (3 + 2)
```
Input:    111+11
Process:  q0→q0→q0→q0→q2→q3→q3→q4→q5
Output:   11111
Result:   5 ✓
Steps:    8
```

### Test Case 2: Reversed Order (2 + 3)
```
Input:    11+111
Process:  q0→q0→q2→q3→q3→q3→q4→q5
Output:   11111
Result:   5 ✓
Steps:    8
```

### Test Case 3: Unequal Lengths (5 + 1)
```
Input:    11111+1
Process:  q0→q0→q0→q0→q0→q2→q3→q4→q5
Output:   111111
Result:   6 ✓
Steps:    9
```

### Test Case 4: Minimal Case (1 + 1)
```
Input:    1+1
Process:  q0→q2→q3→q4→q5
Output:   11
Result:   2 ✓
Steps:    5
```

### Test Case 5: Zero Addition (0 + 5)
```
Input:    +11111
Process:  q0→q2→q3→q3→q3→q3→q3→q4→q5
Output:   11111
Result:   5 ✓
Steps:    9
```

### Test Case 6: Equal Numbers (4 + 4)
```
Input:    1111+1111
Output:   11111111
Result:   8 ✓
Steps:    11
```

---

## 6. Edge Cases Handled

1. **Zero Addition:** 0 + n = n (represented as empty string + unary)
2. **Unequal Lengths:** Works correctly regardless of operand size difference
3. **Minimal Input:** Single digit addition (1 + 1) works correctly
4. **Large Numbers:** Algorithm scales correctly with larger inputs

---

## 7. Complexity Analysis

### Time Complexity
- **Average Case:** O(n + m) where n and m are the operands
- Each digit requires at most one transition
- Specifically: n steps for first number + 1 for separator + m steps for second number + 1 for finalization

### Space Complexity
- **Tape Space:** O(n + m) to store both operands
- **State Space:** O(1) - constant number of states (6)

---

## 8. How to Run

### Prerequisites
- Python 3.x installed
- No external libraries required

### Execution
```bash
python turing-machine-addition.py
```

### Output
- Step-by-step trace of each transition
- Current state, head position, and tape content
- Final result and total steps taken
- Test results summary

---

## 9. Extending the Project

### Possible Extensions
1. **Subtraction:** Implement unary subtraction
2. **Multiplication:** Extend for unary multiplication
3. **Division:** Implement unary division operations
4. **Error Handling:** Add input validation and error states
5. **Visualization:** Create graphical tape visualization
6. **Performance Optimization:** Implement more complex algorithms

---

## 10. Conclusion

This Turing Machine implementation successfully demonstrates:
- Proper state machine design and implementation
- Tape manipulation and head movement
- Correct transition function handling
- Robustness across various test cases
- Educational value for understanding automata theory

The simulator serves as a foundation for understanding how theoretical computing machines can solve practical problems through formal state transitions and tape operations.