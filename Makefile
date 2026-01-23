# TbK LaTeX Compilation Makefile
# Usage:
#   make build    - Build Docker image
#   make compile  - Compile example document
#   make shell    - Open shell in container
#   make clean    - Remove generated files

.PHONY: build compile shell clean help

# Default target
help:
	@echo "TbK LaTeX Compilation"
	@echo ""
	@echo "Usage:"
	@echo "  make build     - Build Docker image"
	@echo "  make compile   - Compile example document"
	@echo "  make shell     - Open interactive shell in container"
	@echo "  make clean     - Remove generated LaTeX files"
	@echo ""
	@echo "To compile a specific file:"
	@echo "  TEXFILE=path/to/file.tex make compile-file"

# Build Docker image
build:
	docker-compose build latex

# Compile the example document
compile: build
	docker-compose run --rm compile

# Compile a specific file (use TEXFILE env var)
compile-file: build
	docker-compose run --rm compile-file

# Open interactive shell
shell: build
	docker-compose run --rm latex bash

# Clean generated files
clean:
	find . -name "*.aux" -delete
	find . -name "*.log" -delete
	find . -name "*.out" -delete
	find . -name "*.toc" -delete
	find . -name "*.synctex.gz" -delete
	find . -name "*.fls" -delete
	find . -name "*.fdb_latexmk" -delete
	@echo "Cleaned LaTeX auxiliary files"

# Clean including PDFs
clean-all: clean
	find . -name "*.pdf" -delete
	@echo "Cleaned all generated files including PDFs"
