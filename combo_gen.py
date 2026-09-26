#!/usr/bin/env python3
"""
combo_gen.py - Number Combination Generator
Generates every possible combination of given digits at a specified length.
"""

import itertools
import argparse
import sys
import os


def generate_combinations(digits, length, allow_repeat=True, output_file=None):
    """
    Generate all combinations/permutations of `digits` at `length` positions.

    Args:
        digits      : list of digit characters to use
        length      : number of positions in each combo
        allow_repeat: if True, digits can repeat (product); else no repeats (permutations)
        output_file : path to write results to (optional)

    Returns:
        total count of combinations generated
    """
    if allow_repeat:
        combos = itertools.product(digits, repeat=length)
    else:
        if length > len(digits):
            print(f"[!] Error: Cannot generate {length}-digit combos without repetition "
                  f"from only {len(digits)} unique digit(s).")
            sys.exit(1)
        combos = itertools.permutations(digits, length)

    count = 0
    out = open(output_file, "w") if output_file else sys.stdout

    try:
        for combo in combos:
            line = "".join(combo)
            out.write(line + "\n")
            count += 1
    finally:
        if output_file and not out.closed:
            out.close()

    return count


def parse_digits(raw: str) -> list:
    """Parse the digit input string into a deduplicated list."""
    # Strip spaces/commas/separators, keep unique order
    cleaned = []
    seen = set()
    for ch in raw.replace(",", "").replace(" ", ""):
        if ch not in seen:
            seen.add(ch)
            cleaned.append(ch)
    return cleaned


def estimate_total(n_digits, length, allow_repeat):
    if allow_repeat:
        return n_digits ** length
    else:
        from math import perm
        return perm(n_digits, length)


def confirm_large_output(total):
    """Ask user to confirm if output will be very large."""
    if total > 1_000_000:
        print(f"\n[!] Warning: This will generate {total:,} combinations.")
        ans = input("    Continue? [y/N]: ").strip().lower()
        if ans != "y":
            print("Aborted.")
            sys.exit(0)


def interactive_mode():
    """Run the generator interactively (no CLI args)."""
    print("=" * 55)
    print("     NUMBER COMBINATION GENERATOR  |  combo_gen.py")
    print("=" * 55)

    raw = input("\n[+] Enter digits to use (e.g. 0123456789 or 1,2,3): ").strip()
    if not raw:
        print("[!] No digits provided. Exiting.")
        sys.exit(1)
    digits = parse_digits(raw)
    print(f"    Unique digits: {' '.join(digits)} ({len(digits)} total)")

    try:
        length = int(input("[+] Combination length (e.g. 4): ").strip())
        if length <= 0:
            raise ValueError
    except ValueError:
        print("[!] Invalid length. Must be a positive integer.")
        sys.exit(1)

    repeat_ans = input("[+] Allow digit repetition? [Y/n]: ").strip().lower()
    allow_repeat = repeat_ans != "n"

    total = estimate_total(len(digits), length, allow_repeat)
    print(f"\n    Estimated combinations: {total:,}")
    confirm_large_output(total)

    save_ans = input("[+] Save to file? Enter filename or press Enter to print: ").strip()
    output_file = save_ans if save_ans else None

    print("\n[*] Generating combinations...\n")
    if output_file:
        count = generate_combinations(digits, length, allow_repeat, output_file)
        print(f"\n[+] Done! {count:,} combinations written to '{output_file}'")
    else:
        print("-" * 30)
        count = generate_combinations(digits, length, allow_repeat)
        print("-" * 30)
        print(f"\n[+] Done! {count:,} combinations generated.")


def cli_mode():
    """Run via command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Generate every possible combination of given digits.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # All 4-digit PINs (0-9, with repetition)
  python combo_gen.py --digits 0123456789 --length 4

  # All 3-char combos from {1,2,3} without repeating
  python combo_gen.py --digits 123 --length 3 --no-repeat

  # Save to file
  python combo_gen.py --digits 0123456789 --length 4 -o pins.txt
        """
    )
    parser.add_argument("--digits",   required=True, help="Digits to use, e.g. 0123456789")
    parser.add_argument("--length",   required=True, type=int, help="Length of each combination")
    parser.add_argument("--no-repeat", action="store_true", help="Disallow digit repetition")
    parser.add_argument("-o", "--output", default=None, help="Output file path (default: stdout)")

    args = parser.parse_args()

    digits = parse_digits(args.digits)
    if not digits:
        print("[!] No valid digits provided.")
        sys.exit(1)

    allow_repeat = not args.no_repeat
    total = estimate_total(len(digits), args.length, allow_repeat)

    print(f"[*] Digits   : {' '.join(digits)}", file=sys.stderr)
    print(f"[*] Length   : {args.length}", file=sys.stderr)
    print(f"[*] Repeat   : {allow_repeat}", file=sys.stderr)
    print(f"[*] Total    : {total:,}", file=sys.stderr)

    if args.output:
        confirm_large_output(total)

    count = generate_combinations(digits, args.length, allow_repeat, args.output)

    if args.output:
        print(f"[+] {count:,} combinations saved to '{args.output}'", file=sys.stderr)


# ─────────────────────────────────────────────
if __name__ == "__main__":
    if len(sys.argv) > 1:
        cli_mode()
    else:
        interactive_mode()
