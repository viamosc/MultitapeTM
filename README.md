# Multi-Tape Turing Machine — Binary Adder

A Python simulation of a 3-tape Turing Machine that adds two binary numbers given in the form `A+B=`.

## Files

- `MultitapeTM.py` — the simulator and machine definition

## How it works

- **Tape 1**: input tape, holds the expression (e.g. `101+001=`)
- **Tape 2**: scratch tape, stores the second operand digit-by-digit
- **Tape 3**: output tape, stores the resulting sum

### States

| State | Purpose |
|---|---|
| `q0` | Scans past the first number and the `+` |
| `q1` | Copies the second number onto Tape 2 |
| `q2` | Moves back to align both numbers at their rightmost digits |
| `[q3,0]` | Adds digits with no carry, moving right-to-left |
| `[q3,1]` | Adds digits with a carry of 1, moving right-to-left |
| `qf` | Final/accepting state |

Each transition is defined by `(read_symbols) -> (next_state, write_symbols, head_directions)` across all three tapes, using `L` (left), `R` (right), `S` (stay).

## Changing the input

The input expression is set in `MultitapeTM.__init__` via `initialTapes`:

```python
[self.blankSymbol] * 2 + list("101+001=") + [self.blankSymbol] * 2
```

Replace `"101+001="` with any other binary expression in the form `A+B=` to test different inputs.

## Running

```
python3 MultitapeTM.py
```

The program prints the state, symbols read, and full tape contents at every step, then prints the final tape contents once it halts.

## Output

- **"Halting in final state"** — the machine reached `qf`, meaning addition completed successfully. Tape 3 holds the sum.
- **"Invalid input"** — the machine halted somewhere other than `qf` (e.g. malformed input, or no matching transition).

## Example

Input: `101+001=` (5 + 1 in binary)
Expected result on Tape 3: `110` (6 in binary)
