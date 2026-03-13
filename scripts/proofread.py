#!/usr/bin/env python3
"""
Proofread an Inform interactive fiction transcript using the Anthropic API.
Chunks the transcript and checks each section for spelling/grammar errors,
while ignoring intentional archaisms, Latin, and dialect.

Usage:
    python proofread_transcript.py transcript.txt
    python proofread_transcript.py transcript.txt --output errors.txt
    python proofread_transcript.py transcript.txt --chunk-size 4000
"""

import sys
import re
import time
import argparse
import anthropic

SYSTEM_PROMPT = """You are proofreading the transcript of an interactive fiction game called
"Our Lady of Thorns", a medieval murder mystery set in a 1346 Benedictine priory on the
English coast. The protagonist is a novice monk named Aldwin.

Your job is to find genuine spelling and grammar errors in the game's output text.

IGNORE the following — these are intentional:
- Latin words, phrases, and prayers (e.g. "Deus miseratur", "Salve Regina", "nocturn")
- Archaic or period-appropriate English vocabulary (e.g. "dorter", "herbarium", "psalter",
  "sennight", "mete", "hauberk")
- Deliberately broken or accented English from Remigio, a Tuscan lay brother
  (he speaks with Italian grammar errors and limited vocabulary — this is intentional)
- British English spellings (colour, favour, realise, centre, etc.)
- Canonical hours and monastic terminology (Matins, Lauds, Terce, Sext, None, Vespers,
  Compline, Nocturn)
- Room names and proper nouns specific to the game world
- Commands typed by the player (lines starting with "> ")
- "[Comment recorded]" lines
- Score/turn count lines

For each genuine error you find, report it in this format:

LINE: <the line containing the error>
ERROR: <brief description of the error>
FIX: <suggested correction>

If you find no errors in a section, respond with exactly: NO ERRORS FOUND

Be conservative — when in doubt about whether something is intentional, skip it.
Focus on clear typos, wrong words, missing words, and grammatical errors in the
game's prose output."""


def chunk_transcript(text, chunk_size=4000):
    """
    Split transcript into chunks at paragraph/blank-line boundaries,
    keeping chunks near chunk_size characters.
    """
    paragraphs = re.split(r'\n\n+', text)
    chunks = []
    current = []
    current_len = 0

    for para in paragraphs:
        para_len = len(para) + 2  # +2 for the \n\n
        if current_len + para_len > chunk_size and current:
            chunks.append('\n\n'.join(current))
            current = [para]
            current_len = para_len
        else:
            current.append(para)
            current_len += para_len

    if current:
        chunks.append('\n\n'.join(current))

    return chunks


def proofread_chunk(client, chunk, chunk_num, total_chunks):
    """Send a chunk to the API and return the response text."""
    print(f"  Checking chunk {chunk_num}/{total_chunks} "
          f"({len(chunk)} chars)...", end='', flush=True)

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1000,
        system=SYSTEM_PROMPT,
        messages=[
            {
                "role": "user",
                "content": f"Please proofread this section of the game transcript:\n\n{chunk}"
            }
        ]
    )

    result = response.content[0].text
    print(" done.")
    return result


def format_results(results, total_chunks):
    """Combine chunk results into a final report."""
    lines = [
        "PROOFREADING REPORT — Our Lady of Thorns",
        "=" * 50,
        f"Checked {total_chunks} chunks.\n",
    ]

    errors_found = False
    for i, (chunk_num, result) in enumerate(results):
        if result.strip() != "NO ERRORS FOUND":
            errors_found = True
            lines.append(f"--- Chunk {chunk_num} ---")
            lines.append(result)
            lines.append("")

    if not errors_found:
        lines.append("No errors found.")

    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Proofread an IF transcript using the Anthropic API."
    )
    parser.add_argument("transcript", help="Path to the transcript file")
    parser.add_argument("--output", "-o", help="Output file for results (default: stdout)")
    parser.add_argument("--chunk-size", "-c", type=int, default=4000,
                        help="Approximate characters per chunk (default: 4000)")
    parser.add_argument("--delay", "-d", type=float, default=0.5,
                        help="Seconds to wait between API calls (default: 0.5)")
    args = parser.parse_args()

    # Read transcript
    try:
        with open(args.transcript, 'r', encoding='utf-8') as f:
            text = f.read()
    except FileNotFoundError:
        print(f"Error: file not found: {args.transcript}", file=sys.stderr)
        sys.exit(1)

    print(f"Transcript: {len(text):,} characters")
    chunks = chunk_transcript(text, args.chunk_size)
    print(f"Split into {len(chunks)} chunks (~{args.chunk_size} chars each)")
    print("Proofreading...\n")

    client = anthropic.Anthropic()  # uses ANTHROPIC_API_KEY env var
    results = []

    for i, chunk in enumerate(chunks, 1):
        result = proofread_chunk(client, chunk, i, len(chunks))
        results.append((i, result))
        if args.delay and i < len(chunks):
            time.sleep(args.delay)

    report = format_results(results, len(chunks))

    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"\nReport written to {args.output}")
    else:
        print("\n" + report)


if __name__ == '__main__':
    main()