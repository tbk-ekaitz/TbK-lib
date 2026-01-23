#!/bin/bash
# TbK LaTeX Compilation Script
# Usage: ./compile.sh [file.tex]
# If no file specified, compiles example/asclepius-user-guide.tex

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Default file to compile
TEXFILE="${1:-example/asclepius-user-guide.tex}"

# Check if file exists
if [ ! -f "$TEXFILE" ]; then
    echo "Error: File '$TEXFILE' not found"
    exit 1
fi

echo "=== TbK LaTeX Compiler ==="
echo "Compiling: $TEXFILE"
echo ""

# Build Docker image if needed
if ! docker images | grep -q "tbk-latex"; then
    echo "Building Docker image..."
    docker-compose build latex
fi

# Compile using Docker
TEXFILE="$TEXFILE" docker-compose run --rm compile-file

echo ""
echo "=== Done ==="
