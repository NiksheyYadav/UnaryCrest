"""
Efficient Turing Machine Simulator for Unary Addition
Provides structured JSON-compatible output for API integration
"""

from typing import Dict, List, Any
from collections import deque


def simulate_unary_addition(a: str, b: str, speed_ms: int = 0) -> Dict[str, Any]:
    """
    Simulate unary addition using a Turing Machine.
    
    Args:
        a: First operand as unary string (e.g., "111" for 3)
        b: Second operand as unary string (e.g., "11" for 2)
        speed_ms: Animation speed in milliseconds (not used in simulation, for client)
    
    Returns:
        Dictionary with keys:
        - initial_tape: Initial tape configuration as string
        - transitions: List of transition dictionaries
        - final_tape: Final tape configuration as string
        - steps: Total number of steps
    """
    
    # Validate inputs
    if not all(c == '1' for c in a) and a != "":
        raise ValueError(f"Invalid unary number 'a': {a}")
    if not all(c == '1' for c in b) and b != "":
        raise ValueError(f"Invalid unary number 'b': {b}")
    
    # Define transitions
    transitions_table = {
        ('q0', '1'): ('q0', '1', 'R'),
        ('q0', '+'): ('q2', '+', 'R'),
        ('q2', '1'): ('q3', '1', 'R'),
        ('q3', '1'): ('q3', '1', 'R'),
        ('q3', '_'): ('q4', '_', 'L'),
        ('q4', '1'): ('q5', '1', 'S'),
    }
    
    # Initialize tape as list for efficient modification
    tape_content = a + '_' + b
    initial_tape_str = tape_content
    
    # Use list for efficient indexing and modification
    tape = ['_'] + list(a + '+' + b) + ['_']
    head = 1  # Start at first symbol after initial blank
    state = 'q0'
    step_count = 0
    execution_log: List[Dict[str, Any]] = []
    
    # Run simulation
    max_steps = 10000  # Safety limit
    while step_count < max_steps and state != 'q5':
        # Get current symbol
        symbol = tape[head]
        key = (state, symbol)
        
        # Check if transition exists
        if key not in transitions_table:
            # Undefined transition, halt
            break
        
        # Get transition
        new_state, new_symbol, direction = transitions_table[key]
        
        # Log transition before making changes
        # Create tape snapshot efficiently
        tape_snapshot = ''.join(tape).strip('_')
        if not tape_snapshot:
            tape_snapshot = '_'
        
        transition_entry = {
            'state': state,
            'head': head,
            'read': symbol,
            'write': new_symbol,
            'direction': direction,
            'tape_snapshot': tape_snapshot
        }
        execution_log.append(transition_entry)
        
        # Apply transition
        tape[head] = new_symbol
        
        # Move head
        if direction == 'R':
            head += 1
            # Extend tape if needed
            if head >= len(tape):
                tape.append('_')
        elif direction == 'L':
            head -= 1
            # Extend tape on left if needed
            if head < 0:
                tape.insert(0, '_')
                head = 0
        # 'S' stays in place
        
        # Update state
        state = new_state
        step_count += 1
    
    # Get final tape
    final_tape = ''.join(tape).strip('_')
    if not final_tape:
        final_tape = '_'
    
    # Return structured result
    result = {
        'initial_tape': initial_tape_str,
        'transitions': execution_log,
        'final_tape': final_tape,
        'steps': step_count
    }
    
    return result


if __name__ == '__main__':
    # Simple test
    result = simulate_unary_addition('111', '11')
    print(f"Initial: {result['initial_tape']}")
    print(f"Final: {result['final_tape']}")
    print(f"Steps: {result['steps']}")
    print(f"Transitions: {len(result['transitions'])}")
