#!/usr/bin/env python3
"""
Generate LaTeX strings file from JSON translation file.

Usage:
    python generate-strings.py strings/en.json strings/strings-en.sty

This script reads a JSON file with translatable strings and generates
a LaTeX .sty file that can be loaded with \\usepackage.
"""

import json
import sys
import os
from datetime import datetime

def flatten_dict(d, parent_key='', sep='.'):
    """Flatten nested dictionary with dot notation keys."""
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)

def escape_latex(text):
    """Escape special LaTeX characters in text."""
    if not isinstance(text, str):
        return str(text)

    # Note: We don't escape $ and \ as they may be intentional LaTeX commands
    # Only escape characters that would break in macro definitions
    replacements = {
        '#': '\\#',
        '%': '\\%',
        '&': '\\&',
        '_': '\\_',
    }

    for char, replacement in replacements.items():
        text = text.replace(char, replacement)

    return text

def generate_sty(json_path, output_path):
    """Generate a .sty file from JSON."""

    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Get language from meta or filename
    lang = data.get('meta', {}).get('language', 'en')
    description = data.get('meta', {}).get('description', f'{lang.upper()} strings')

    # Flatten the dictionary
    flat = flatten_dict(data)

    # Remove meta entries
    flat = {k: v for k, v in flat.items() if not k.startswith('meta.')}

    # Generate output
    lines = []
    lines.append(f'%% strings-{lang}.sty')
    lines.append(f'%% {description}')
    lines.append(f'%% Generated from {os.path.basename(json_path)} on {datetime.now().strftime("%Y-%m-%d %H:%M")}')
    lines.append('%% DO NOT EDIT DIRECTLY - edit the JSON file and regenerate')
    lines.append('%%')
    lines.append('')
    lines.append('\\NeedsTeXFormat{LaTeX2e}')
    lines.append(f'\\ProvidesPackage{{strings/strings-{lang}}}[{datetime.now().strftime("%Y/%m/%d")} v1.0 {lang.upper()} Strings]')
    lines.append('')
    lines.append('\\RequirePackage{xparse}')
    lines.append('')
    lines.append('%% String access command')
    lines.append('\\NewDocumentCommand{\\str}{m}{%')
    lines.append('  \\csname str@#1\\endcsname')
    lines.append('}')
    lines.append('')
    lines.append('%% String definitions')

    # Group by prefix
    current_section = ''
    for key, value in sorted(flat.items()):
        prefix = key.split('.')[0] if '.' in key else ''

        if prefix != current_section:
            current_section = prefix
            lines.append('')
            lines.append(f'%% {prefix.upper() if prefix else "MISC"}')

        # Escape the value for LaTeX
        escaped_value = escape_latex(value)

        # Use csname for keys with dots
        lines.append(f'\\expandafter\\newcommand\\csname str@{key}\\endcsname{{{escaped_value}}}')

    lines.append('')
    lines.append('\\endinput')

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

    print(f'Generated {output_path} with {len(flat)} strings')

def main():
    if len(sys.argv) < 3:
        print('Usage: python generate-strings.py <input.json> <output.sty>')
        print('Example: python generate-strings.py strings/en.json strings/strings-en.sty')
        sys.exit(1)

    json_path = sys.argv[1]
    output_path = sys.argv[2]

    if not os.path.exists(json_path):
        print(f'Error: {json_path} not found')
        sys.exit(1)

    generate_sty(json_path, output_path)

if __name__ == '__main__':
    main()
