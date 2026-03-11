#!/usr/bin/env python3
"""
Convert an Inform interactive fiction transcript to a styled HTML page.
Usage: python transcript_to_html.py input.txt output.html
       (or pipe: python transcript_to_html.py < input.txt > output.html)
"""

import sys
import re
import html


# Canonical room names. A line is a room header if its base text (before any
# parenthesised suffix) exactly matches one of these.
ROOM_NAMES = {
    "Passage (North End)", "Passage (South End)", "West Porch", "Nave",
    "Tower Stairs", "Bell Tower", "Quire", "High Altar Area", "Crypt Stairs",
    "Sacristy", "FitzAlan Chantry", "Lady Chapel", "St Jude Chapel",
    "Cloister Northwest", "Cloister North", "Cloister Northeast",
    "Cloister West", "Cloister East", "Cloister Southwest", "Cloister South",
    "Cloister Southeast", "Garth", "Prior's Solar", "Locutory", "Lavatorium",
    "Chapter House", "Scriptorium", "Library", "Slype", "Infirmary",
    "Infirmary Chapel", "Herbarium", "Garden", "Restricted Garden",
    "Refectory", "Kitchen", "Undercroft", "FitzAlan Crypt", "Main Crypt",
    "Crypt Vestry", "Day Stairs", "Dorter", "Dorm", "Night Stairs",
    "Necessarium", "Lay Brothers' Cells",
}

# Pre-build a set of base names (the part before any parenthesised suffix)
# so we can match "Dorm (on your cot)" -> base "Dorm"
_ROOM_BASE = {re.sub(r'\s*\(.*', '', name).strip() for name in ROOM_NAMES}


def is_room_header(text):
    """Return True if text is a room name (possibly with a parenthesised suffix)."""
    base = re.sub(r'\s*\(.*', '', text).strip()
    return base in _ROOM_BASE


def classify_lines(lines):
    """
    Classify each line. Types: quote, command, room_header, story_break,
    pre, prose, blank.
    """
    result = []
    in_quote_block = False
    quote_buffer = []

    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        # Blank line
        if not stripped:
            if in_quote_block:
                next_nonblank = next(
                    (lines[j] for j in range(i+1, len(lines)) if lines[j].strip()),
                    ''
                )
                nb_indent = len(next_nonblank) - len(next_nonblank.lstrip(' '))
                if nb_indent >= 4 or next_nonblank.startswith('\t'):
                    quote_buffer.append('')
                    i += 1
                    continue
                result.append(('quote', '\n'.join(quote_buffer)))
                quote_buffer = []
                in_quote_block = False
            result.append(('blank', ''))
            i += 1
            continue

        # Command line
        if stripped.startswith('> '):
            if in_quote_block:
                result.append(('quote', '\n'.join(quote_buffer)))
                quote_buffer = []
                in_quote_block = False
            result.append(('command', stripped[2:]))
            i += 1
            continue

        # Story break
        if re.match(r'^\s*-+\s*&&\s*-+\s*$', stripped):
            if in_quote_block:
                result.append(('quote', '\n'.join(quote_buffer)))
                quote_buffer = []
                in_quote_block = False
            result.append(('story_break', ''))
            i += 1
            continue

        # Indented blocks
        indent = len(line) - len(line.lstrip(' '))
        if indent >= 4 or line.startswith('\t'):
            if in_quote_block:
                quote_buffer.append(stripped)
            else:
                in_quote_block = True
                quote_buffer = [stripped]
            i += 1
            continue
        elif indent >= 2:
            if in_quote_block:
                result.append(('quote', '\n'.join(quote_buffer)))
                quote_buffer = []
                in_quote_block = False
            result.append(('pre', line.rstrip()))
            i += 1
            continue

        # Close quote block if open
        if in_quote_block:
            result.append(('quote', '\n'.join(quote_buffer)))
            quote_buffer = []
            in_quote_block = False

        # Room header (exact match)
        if is_room_header(stripped):
            result.append(('room_header', stripped))
            i += 1
            continue

        result.append(('prose', stripped))
        i += 1

    if in_quote_block and quote_buffer:
        result.append(('quote', '\n'.join(quote_buffer)))

    return result


def group_paragraphs(classified):
    """
    Group prose lines into paragraphs. Consecutive prose lines separated only
    by other prose lines (no blank between them) are joined with <br>, since
    Inform sometimes emits multi-line responses that belong together visually.
    A blank line between prose lines starts a new paragraph.
    """
    result = []
    # para_buffer holds lines for the current paragraph; each entry is a string.
    # We use '\n' as a within-paragraph line-break marker.
    para_buffer = []
    pre_buffer = []

    def flush_para():
        if para_buffer:
            result.append(('paragraph', '\n'.join(para_buffer)))
            para_buffer.clear()

    def flush_pre():
        if pre_buffer:
            result.append(('pre_block', '\n'.join(pre_buffer)))
            pre_buffer.clear()

    for kind, text in classified:
        if kind == 'prose':
            flush_pre()
            para_buffer.append(text)
        elif kind == 'blank':
            # A blank line ends the current paragraph
            flush_pre()
            flush_para()
        elif kind == 'pre':
            flush_para()
            pre_buffer.append(text)
        else:
            flush_para()
            flush_pre()
            result.append((kind, text))

    flush_para()
    flush_pre()
    return result


def to_html(classified):
    """Convert classified blocks to HTML."""
    parts = []
    for kind, text in classified:
        text = text.replace('---', '\u2014')
        t = html.escape(text)
        if kind == 'command':
            parts.append(f'<div class="command"><span class="prompt">&gt;</span> {t}</div>')
        elif kind == 'quote':
            lines = t.split('\n')
            inner = '<br>'.join(lines)
            parts.append(f'<blockquote>{inner}</blockquote>')
        elif kind == 'room_header':
            parts.append(f'<h2 class="room-header">{t}</h2>')
        elif kind == 'paragraph':
            # Within a paragraph, newlines become <br>
            inner = t.replace('\n', '<br>\n')
            parts.append(f'<p>{inner}</p>')
        elif kind == 'pre_block':
            parts.append(f'<pre class="game-pre">{t}</pre>')
        elif kind == 'story_break':
            parts.append('<hr class="story-break">')
        else:
            parts.append(f'<p>{t}</p>')

    return '\n'.join(parts)


HTML_TEMPLATE = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Our Lady of Thorns — Transcript</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=IM+Fell+English:ital@0;1&family=Cinzel:wght@400;600&family=Courier+Prime:wght@400;700&display=swap" rel="stylesheet">
<style>
  :root {
    --parchment:    #f5eedc;
    --ink:          #2a1f0e;
    --faded-ink:    #5c4a2a;
    --command-bg:   #1e1a14;
    --command-text: #c8b87a;
    --prompt:       #7a6030;
    --rule-color:   #9c7c3a;
    --quote-border: #8b6914;
    --room-color:   #5a1a00;
    --shadow:       rgba(42,31,14,0.15);
  }

  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

  body {
    background-color: #2a1f0e;
    background-image:
      repeating-linear-gradient(
        0deg,
        transparent,
        transparent 28px,
        rgba(0,0,0,0.03) 28px,
        rgba(0,0,0,0.03) 29px
      );
    font-family: 'IM Fell English', Georgia, serif;
    color: var(--ink);
    min-height: 100vh;
    padding: 3rem 1rem;
  }

  .page {
    max-width: 680px;
    margin: 0 auto;
    background: var(--parchment);
    background-image:
      url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='400' height='400'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.65' numOctaves='3' stitchTiles='stitch'/%3E%3CfeColorMatrix type='saturate' values='0'/%3E%3C/filter%3E%3Crect width='400' height='400' filter='url(%23n)' opacity='0.04'/%3E%3C/svg%3E");
    padding: 4rem 4.5rem;
    box-shadow:
      0 0 0 1px rgba(156,124,58,0.3),
      0 4px 40px rgba(0,0,0,0.6),
      inset 0 0 80px rgba(180,140,60,0.08);
    position: relative;
  }

  /* Decorative corner rules */
  .page::before, .page::after {
    content: '';
    position: absolute;
    width: 40px; height: 40px;
    border-color: var(--rule-color);
    border-style: solid;
    opacity: 0.5;
  }
  .page::before { top: 20px; left: 20px; border-width: 1px 0 0 1px; }
  .page::after  { bottom: 20px; right: 20px; border-width: 0 1px 1px 0; }

  /* Header */
  .transcript-header {
    text-align: center;
    margin-bottom: 2.5rem;
    padding-bottom: 1.5rem;
    border-bottom: 1px solid var(--rule-color);
  }
  .transcript-header h1 {
    font-family: 'Cinzel', serif;
    font-weight: 600;
    font-size: 1.5rem;
    letter-spacing: 0.08em;
    color: var(--room-color);
    text-transform: uppercase;
  }
  .transcript-header p {
    font-family: 'IM Fell English', serif;
    font-style: italic;
    font-size: 0.85rem;
    color: var(--faded-ink);
    margin-top: 0.4rem;
  }

  /* Normal prose paragraphs */
  p {
    font-size: 1.05rem;
    line-height: 1.75;
    color: var(--ink);
    margin-bottom: 0.9rem;
    text-align: justify;
    hyphens: auto;
  }

  /* Room headers */
  h2.room-header {
    font-family: 'Cinzel', serif;
    font-weight: 400;
    font-size: 0.95rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--room-color);
    margin: 1.8rem 0 0.6rem;
    padding-bottom: 0.3rem;
    border-bottom: 1px solid rgba(156,124,58,0.35);
  }

  /* Commands */
  .command {
    font-family: 'Courier Prime', 'Courier New', monospace;
    font-weight: 700;
    font-size: 0.9rem;
    background: var(--command-bg);
    color: var(--command-text);
    padding: 0.55rem 1rem;
    margin: 1.4rem -1rem;
    border-left: 3px solid var(--prompt);
    letter-spacing: 0.05em;
    box-shadow: 0 2px 8px rgba(0,0,0,0.4);
  }
  .command .prompt {
    color: var(--prompt);
    margin-right: 0.4em;
    font-weight: 400;
  }

  /* Blockquotes (epigraphs, in-game quotes) */
  blockquote {
    font-family: 'IM Fell English', Georgia, serif;
    font-style: italic;
    font-size: 1rem;
    line-height: 1.8;
    color: var(--faded-ink);
    margin: 1.8rem 0 1.8rem 2rem;
    padding: 0.5rem 0 0.5rem 1.5rem;
    border-left: 2px solid var(--quote-border);
  }

  /* Preformatted in-game text (schedules, carvings, etc.) */
  pre.game-pre {
    font-family: 'Courier Prime', 'Courier New', monospace;
    font-size: 0.88rem;
    line-height: 1.6;
    color: var(--faded-ink);
    margin: 0.8rem 0 0.8rem 1.5rem;
    white-space: pre;
    background: none;
    border: none;
  }

  /* Story break rule */
  hr.story-break {
    border: none;
    margin: 2.5rem auto;
    width: 60%;
    position: relative;
    height: 1px;
    background: linear-gradient(to right, transparent, var(--rule-color), transparent);
  }
  hr.story-break::before {
    content: '✦';
    position: absolute;
    left: 50%;
    top: 50%;
    transform: translate(-50%, -50%);
    background: var(--parchment);
    color: var(--rule-color);
    padding: 0 0.6rem;
    font-size: 0.75rem;
  }

  /* Responsive */
  @media (max-width: 600px) {
    .page { padding: 2.5rem 1.8rem; }
    .command { margin: 1.2rem -0.5rem; }
  }
</style>
</head>
<body>
<article class="page">
  <header class="transcript-header">
    <h1>Our Lady of Thorns</h1>
    <p>An interactive monastic tragedy &mdash; transcript</p>
  </header>
  <main>
{CONTENT}
  </main>
</article>
</body>
</html>
'''


def convert(text):
    lines = text.splitlines()
    classified = classify_lines(lines)
    classified = group_paragraphs(classified)
    body = to_html(classified)
    return HTML_TEMPLATE.replace('{CONTENT}', body)


def main():
    if len(sys.argv) == 3:
        with open(sys.argv[1], 'r', encoding='utf-8') as f:
            text = f.read()
        result = convert(text)
        with open(sys.argv[2], 'w', encoding='utf-8') as f:
            f.write(result)
        print(f"Written to {sys.argv[2]}")
    elif len(sys.argv) == 2:
        with open(sys.argv[1], 'r', encoding='utf-8') as f:
            text = f.read()
        print(convert(text))
    else:
        text = sys.stdin.read()
        print(convert(text))


if __name__ == '__main__':
    main()
