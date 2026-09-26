# Combo Gen

A number combination generator — produces every possible combination (or permutation) of a given set of digits at a specified length. Built for generating PIN/passcode candidate lists for authorized security testing.

## Features

- **Two input modes**: interactive prompts, or CLI flags for scripting
- **Repeat or no-repeat**: choose between combinations with repetition (`itertools.product`) or without (`itertools.permutations`)
- **Large-output safeguard**: warns and asks for confirmation before generating over 1,000,000 combinations
- **Flexible output**: print to stdout or save directly to a file

## Requirements

Python 3.6+ — no external dependencies (standard library only).

## Usage

**Interactive mode:**
```bash
python3 combo_gen.py
```

**CLI mode:**
```bash
# All 4-digit PINs (0-9, with repetition)
python3 combo_gen.py --digits 0123456789 --length 4

# All 3-character combos from {1,2,3} without repeating digits
python3 combo_gen.py --digits 123 --length 3 --no-repeat

# Save output to a file
python3 combo_gen.py --digits 0123456789 --length 4 -o pins.txt
```

### Flags

| Flag | Description |
|---|---|
| `--digits` | Digits to use, e.g. `0123456789` (required) |
| `--length` | Length of each combination (required) |
| `--no-repeat` | Disallow digit repetition |
| `-o`, `--output` | Output file path (default: stdout) |

## Disclaimer

This tool generates candidate PIN/passcode lists. Use it only against systems and accounts you own or have explicit written authorization to test.

## Author

**Odejide Femisola Francis (Cyphem)**
Junior Penetration Tester — Web & API Security, Bug Bounty Hunter

- GitHub: [@CYPHEM18](https://github.com/CYPHEM18)
- LinkedIn: [femisola-odejide](https://www.linkedin.com/in/femisola-odejide-a3ab1135b)

## License

MIT — free to use, modify, and distribute.
