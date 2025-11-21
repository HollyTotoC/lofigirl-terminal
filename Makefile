.PHONY: help install install-dev test lint format type-check clean run pre-commit setup venv

# Default target
.DEFAULT_GOAL := help

# Python interpreter
PYTHON := python3
VENV := venv
BIN := $(VENV)/bin

help: ## Show this help message
	@echo "LofiGirl Terminal - Development Commands"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'
	@echo ""

venv: ## Create virtual environment
	@echo "Creating virtual environment..."
	$(PYTHON) -m venv $(VENV)
	@echo "Virtual environment created at ./$(VENV)"
	@echo "Activate it with: source $(VENV)/bin/activate (Linux/Mac) or $(VENV)\\Scripts\\activate (Windows)"

install: venv ## Install production dependencies
	@echo "Installing production dependencies..."
	$(BIN)/pip install --upgrade pip setuptools wheel
	$(BIN)/pip install -r requirements/base.txt
	@echo "Production dependencies installed!"

install-dev: venv ## Install development dependencies
	@echo "Installing development dependencies..."
	$(BIN)/pip install --upgrade pip setuptools wheel
	$(BIN)/pip install -r requirements/dev.txt
	$(BIN)/pip install -e .
	@echo "Development dependencies installed!"
	@echo ""
	@echo "Next steps:"
	@echo "  1. Run 'make pre-commit-install' to set up git hooks"
	@echo "  2. Run 'make test' to verify everything works"

setup: install-dev pre-commit-install ## Complete development environment setup
	@echo ""
	@echo "✨ Development environment setup complete!"
	@echo ""
	@echo "You're ready to start developing! Try these commands:"
	@echo "  make test      - Run tests"
	@echo "  make lint      - Check code quality"
	@echo "  make format    - Format code"
	@echo "  make run       - Run the application"

pre-commit-install: ## Install pre-commit hooks
	@echo "Installing pre-commit hooks..."
	$(BIN)/pre-commit install
	@echo "Pre-commit hooks installed!"

pre-commit: ## Run pre-commit hooks on all files
	@echo "Running pre-commit hooks..."
	$(BIN)/pre-commit run --all-files

test: ## Run tests
	@echo "Running tests..."
	$(BIN)/pytest tests/ -v --cov=lofigirl_terminal --cov-report=term-missing --cov-report=html
	@echo ""
	@echo "Coverage report generated in htmlcov/index.html"

test-fast: ## Run tests without coverage
	@echo "Running tests (fast mode)..."
	$(BIN)/pytest tests/ -v

test-watch: ## Run tests in watch mode
	@echo "Running tests in watch mode..."
	$(BIN)/pytest-watch tests/

lint: ## Run linting checks
	@echo "Running flake8..."
	$(BIN)/flake8 src/ tests/
	@echo "✓ Linting passed!"

format: ## Format code with black
	@echo "Formatting code with black..."
	$(BIN)/black src/ tests/
	@echo "Sorting imports with isort..."
	$(BIN)/isort src/ tests/
	@echo "✓ Code formatted!"

format-check: ## Check if code is formatted correctly
	@echo "Checking code format..."
	$(BIN)/black --check src/ tests/
	$(BIN)/isort --check-only src/ tests/

type-check: ## Run type checking with mypy
	@echo "Running type checks..."
	$(BIN)/mypy src/
	@echo "✓ Type checking passed!"

check-all: format-check lint type-check test ## Run all checks (format, lint, type-check, test)
	@echo ""
	@echo "✓ All checks passed!"

clean: ## Clean temporary files and caches
	@echo "Cleaning temporary files..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "htmlcov" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type f -name "*.pyo" -delete 2>/dev/null || true
	find . -type f -name ".coverage" -delete 2>/dev/null || true
	find . -type f -name "coverage.xml" -delete 2>/dev/null || true
	rm -rf build/ dist/ 2>/dev/null || true
	@echo "✓ Cleanup complete!"

clean-all: clean ## Clean everything including venv
	@echo "Removing virtual environment..."
	rm -rf $(VENV)
	@echo "✓ Full cleanup complete!"

run: ## Run the application
	@echo "Running LofiGirl Terminal..."
	$(BIN)/lofigirl --help

run-tui: ## Launch the interactive TUI (recommended)
	@echo "🎵 Launching LofiGirl TUI..."
	$(BIN)/lofigirl tui

run-play: ## Run and play default station
	@echo "Playing default station..."
	$(BIN)/lofigirl play

run-list: ## List all available stations
	@echo "Available stations:"
	$(BIN)/lofigirl list

run-info: ## Show application info
	$(BIN)/lofigirl info

# Aliases for convenience
tui: run-tui ## Alias for run-tui

build: ## Build distribution packages
	@echo "Building distribution packages..."
	$(BIN)/python -m build
	@echo "✓ Build complete! Check dist/ directory"

install-local: ## Install package locally in development mode
	@echo "Installing package in development mode..."
	$(BIN)/pip install -e .
	@echo "✓ Package installed!"

docs: ## Generate documentation (placeholder)
	@echo "Documentation generation not yet implemented"
	@echo "TODO: Set up Sphinx documentation"

upgrade-deps: ## Upgrade all dependencies
	@echo "Upgrading dependencies..."
	$(BIN)/pip install --upgrade pip setuptools wheel
	$(BIN)/pip install --upgrade -r requirements/dev.txt
	@echo "✓ Dependencies upgraded!"

check-security: ## Run security checks
	@echo "Running security checks..."
	$(BIN)/bandit -r src/
	@echo "✓ Security check complete!"

# Development workflow helpers
dev: install-dev ## Alias for install-dev

watch: test-watch ## Alias for test-watch

quality: format lint type-check ## Format, lint, and type-check code

# CI/CD helpers
ci: check-all ## Run all CI checks

.PHONY: all
all: setup check-all ## Setup and run all checks
