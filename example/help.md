# TbK Example - Compilation Guide

## Quick Start

```bash
cd example
pdflatex asclepius-user-guide.tex
```

Run twice for TOC/references:
```bash
pdflatex asclepius-user-guide.tex && pdflatex asclepius-user-guide.tex
```

## Files

| File | Description |
|------|-------------|
| `asclepius-user-guide.tex` | Main example (hardcoded strings) |
| `asclepius-user-guide-i18n.tex` | Internationalized version |
| `strings/en.json` | English strings (source) |
| `strings/strings-en.sty` | English strings (LaTeX) |

## Internationalization

To translate:
1. Copy `strings/en.json` to `strings/XX.json`
2. Translate strings in the JSON file
3. Generate LaTeX: `python generate-strings.py strings/XX.json strings/strings-XX.sty`
4. In `.tex` file, change `\usepackage{strings/strings-en}` to `\usepackage{strings/strings-XX}`

## Requirements

- LaTeX distribution (TeX Live, MiKTeX)
- Packages: `fontawesome5`, `tcolorbox`, `tikz`, `fancyhdr`, `hyperref`, `booktabs`, `xcolor`

## Troubleshooting

**Missing packages:** Install via `tlmgr install <package>` or MiKTeX console.

**Clean build:** Delete `.aux`, `.log`, `.toc` files and recompile.
