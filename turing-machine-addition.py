# ============================================================================
# TURING MACHINE SIMULATOR FOR UNARY ARITHMETIC OPERATIONS (ADDITION)
# ============================================================================
# Course: Automata Theory - B.Tech 5th Semester CSE
# Project: Design and Implementation of a Turing Machine for Unary Arithmetic
# Date: November 17, 2025
# 
# This module implements a complete Turing Machine simulator that performs
# addition on unary numbers (e.g., 3 + 2 = 5 represented as 111 + 11 → 11111)
# ============================================================================

class TuringMachine:
    """
    A Turing Machine simulator that performs unary addition.
    
    The machine uses the following approach:
    - Input format: "111+11" where numbers are represented in unary (1s)
      and are separated by a '+' symbol
    - Algorithm:
      1. Move right through the first number
      2. Replace the '+' symbol with '1'
      3. Move right through the second number
      4. Move back left and erase the last '1'
      5. Halt
    
    This effectively performs the operation: n1 + n2 = (n1 + 1 + n2 - 1) = n1 + n2
    """
    
    def __init__(self):
        """Initialize the Turing Machine with states and transition table."""
        
        # Define all states
        self.states = {
            'q0': 'Initial state - read first number',
            'q1': 'Move to end of first number',
            'q2': 'Replace + with 1',
            'q3': 'Move to end of second number',
            'q4': 'Move left and erase last 1',
            'q5': 'Halt state - accept'
        }
        
        # Transition table: (state, symbol) -> (new_state, new_symbol, direction)
        # Direction: 'R' (right), 'L' (left), 'S' (stay)
        self.transitions = {
            # State q0: Read and skip first number
            ('q0', '1'): ('q0', '1', 'R'),      # Stay in q0, move right
            ('q0', '+'): ('q2', '+', 'R'),      # Found separator, go to q2
            
            # State q2: Replace + with 1
            ('q2', '1'): ('q3', '1', 'R'),      # First '1' of second number, go to q3
            
            # State q3: Move through second number to find the end
            ('q3', '1'): ('q3', '1', 'R'),      # Continue moving right
            ('q3', '_'): ('q4', '_', 'L'),      # Found end (blank), go back left to q4
            
            # State q4: Erase the last 1 and halt
            ('q4', '1'): ('q5', '1', 'S'),      # Erase last 1 by transitioning to halt
        }
        
        # Machine state variables
        self.tape = []
        self.head_position = 0
        self.current_state = 'q0'
        self.step_count = 0
        self.execution_log = []
    
    def initialize_tape(self, num1, num2):
        """
        Initialize the Turing Machine tape with two unary numbers.
        
        Args:
            num1 (int): First number to add (must be >= 0)
            num2 (int): Second number to add (must be >= 0)
            
        Raises:
            ValueError: If either number is negative
        """
        if num1 < 0 or num2 < 0:
            raise ValueError("Numbers must be non-negative")
        
        # Convert to unary representation
        unary1 = '1' * num1
        unary2 = '1' * num2
        
        # Create tape: "111+11" with blank spaces on both ends
        tape_content = unary1 + '+' + unary2
        self.tape = ['_'] + list(tape_content) + ['_'] * 10  # Extra blanks for tape expansion
        self.head_position = 1  # Start at first position (after initial blank)
        self.current_state = 'q0'
        self.step_count = 0
        self.execution_log = []
        
        print(f"{'='*70}")
        print(f"Initialized tape for {num1} + {num2}")
        print(f"{'='*70}")
        print(f"Tape content: {unary1} + {unary2}")
        print(f"Tape representation: {''.join(self.tape[:len(tape_content)+2])}")
        print(f"Head position: {self.head_position}")
        print(f"Initial state: {self.current_state}\n")
    
    def log_step(self):
        """
        Log the current configuration of the Turing Machine.
        Useful for debugging and analysis.
        """
        tape_str = ''.join(self.tape[:max(self.head_position + 5, len(self.tape)-5)])
        log_entry = {
            'step': self.step_count,
            'state': self.current_state,
            'position': self.head_position,
            'symbol': self.tape[self.head_position],
            'tape': tape_str
        }
        self.execution_log.append(log_entry)
    
    def get_execution_log(self):
        """
        Retrieve the complete execution log.
        
        Returns:
            list: List of dictionaries containing step-by-step execution details
        """
        return self.execution_log
    
    def step(self):
        """
        Execute one step of the Turing Machine transition function.
        
        Returns:
            bool: True if machine halted, False if it can continue
        """
        # Check if already halted
        if self.current_state == 'q5':
            return True
        
        # Get current symbol under head
        symbol = self.tape[self.head_position]
        key = (self.current_state, symbol)
        
        # Log current step
        self.log_step()
        
        # Check if transition is defined
        if key not in self.transitions:
            print(f"Step {self.step_count}: Undefined transition ({self.current_state}, '{symbol}') - HALTING")
            self.current_state = 'q5'
            return True
        
        # Perform transition
        new_state, new_symbol, direction = self.transitions[key]
        
        # Write new symbol to tape
        self.tape[self.head_position] = new_symbol
        
        # Move head
        if direction == 'R':
            self.head_position += 1
        elif direction == 'L':
            self.head_position -= 1
        # 'S' means stay in place
        
        # Update state
        self.current_state = new_state
        self.step_count += 1
        
        # Display step information
        symbol_display = repr(symbol) if symbol == '_' else symbol
        new_symbol_display = repr(new_symbol) if new_symbol == '_' else new_symbol
        print(f"Step {self.step_count-1}: δ({self.current_state}, {symbol_display}) = "
              f"({new_state}, {new_symbol_display}, {direction}) | "
              f"Head: {self.head_position}")
        
        # Check if halted
        if self.current_state == 'q5':
            return True
        
        return False
    
    def run(self, num1, num2, verbose=True):
        """
        Execute the Turing Machine to perform addition.
        
        Args:
            num1 (int): First operand
            num2 (int): Second operand
            verbose (bool): If True, print step-by-step execution
            
        Returns:
            int: The result of num1 + num2
        """
        self.initialize_tape(num1, num2)
        
        # Run the machine with a maximum step limit
        max_steps = 1000
        while self.step_count < max_steps:
            if self.step():
                break
        
        # Extract and return result
        result_tape = ''.join(self.tape).strip('_').replace('+', '')
        result = len(result_tape)
        
        # Print final summary
        print(f"\n{'='*70}")
        print(f"EXECUTION COMPLETE")
        print(f"{'='*70}")
        print(f"Final tape: {''.join(self.tape[:self.head_position + 5]).rstrip('_')}")
        print(f"Final state: {self.current_state}")
        print(f"Result: {num1} + {num2} = {result}")
        print(f"Total steps: {self.step_count}")
        print(f"{'='*70}\n")
        
        return result
    
    def print_state_diagram(self):
        """Print a text representation of the state diagram."""
        print("\n" + "="*70)
        print("STATE DIAGRAM AND TRANSITION TABLE")
        print("="*70)
        print("\nStates:")
        for state, description in self.states.items():
            print(f"  {state}: {description}")
        
        print("\nTransition Function δ(q, a) = (q', a', d):")
        print(f"{'State':<8} {'Input':<8} {'Next State':<12} {'Output':<8} {'Move':<6}")
        print("-" * 50)
        for (state, symbol), (next_state, new_symbol, direction) in sorted(self.transitions.items()):
            symbol_display = "BLANK" if symbol == '_' else symbol
            new_symbol_display = "BLANK" if new_symbol == '_' else new_symbol
            print(f"{state:<8} {symbol_display:<8} {next_state:<12} {new_symbol_display:<8} {direction:<6}")
        print("="*70 + "\n")


# ============================================================================
# TEST SUITE
# ============================================================================

def run_tests():
    """Execute comprehensive test cases."""
    
    print("\n" + "="*70)
    print("TURING MACHINE SIMULATOR - TEST SUITE")
    print("="*70 + "\n")
    
    # Initialize machine
    tm = TuringMachine()
    tm.print_state_diagram()
    
    # Test cases: (num1, num2, expected_result)
    test_cases = [
        (3, 2, 5),          # Basic case: 111 + 11 = 11111
        (2, 3, 5),          # Reversed: 11 + 111 = 11111
        (5, 1, 6),          # Edge case: longer first number
        (1, 1, 2),          # Minimal case: 1 + 1 = 11
        (0, 5, 5),          # Zero addition: 0 + 11111 = 11111
        (4, 4, 8),          # Equal numbers: 1111 + 1111 = 11111111
    ]
    
    passed = 0
    failed = 0
    
    for num1, num2, expected in test_cases:
        try:
            result = tm.run(num1, num2)
            if result == expected:
                print(f"✓ PASSED: {num1} + {num2} = {result}\n")
                passed += 1
            else:
                print(f"✗ FAILED: {num1} + {num2} = {result}, expected {expected}\n")
                failed += 1
        except Exception as e:
            print(f"✗ ERROR in test {num1} + {num2}: {e}\n")
            failed += 1
    
    # Summary
    print("="*70)
    print(f"TEST SUMMARY: {passed} passed, {failed} failed")
    print("="*70 + "\n")
    
    return passed, failed


if __name__ == "__main__":
    import sys
    import json
    
    # Check for JSON mode
    if '--json' in sys.argv:
        # JSON mode: read from stdin, write to stdout
        try:
            # Read JSON input from stdin
            input_data = json.load(sys.stdin)
            a = input_data.get('a', '')
            b = input_data.get('b', '')
            speed_ms = input_data.get('speed_ms', 0)
            
            # Import and use the efficient simulator
            from simulator import simulate_unary_addition
            
            # Run simulation
            result = simulate_unary_addition(a, b, speed_ms)
            
            # Output JSON result to stdout
            json.dump(result, sys.stdout)
            sys.stdout.flush()
            exit(0)
        except Exception as e:
            # Output error as JSON
            error_result = {
                'error': str(e),
                'message': 'Simulation failed'
            }
            json.dump(error_result, sys.stdout)
            sys.stdout.flush()
            exit(1)
    else:
        # Original CLI mode
        # Run all tests
        passed, failed = run_tests()
        
        # Exit with appropriate code
        exit(0 if failed == 0 else 1)