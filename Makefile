.PHONY: lint lint-fix check-types check-style format-check import-check test test-cov install

# Colors for better output
GREEN = \033[0;32m
YELLOW = \033[1;33m
RED = \033[0;31m
NC = \033[0m

# Run all linting checks
lint: check-types check-style format-check import-check
	@echo "$(GREEN)✅ All linting checks passed!$(NC)"

# Auto-fix formatting and imports
lint-fix:
	@echo "$(YELLOW)🛠️  Running auto-fix...$(NC)"
	poetry run black src/ tests/
	poetry run isort src/ tests/
	@echo "$(GREEN)✅ Auto-fix completed!$(NC)"

# Type checking with mypy
check-types:
	@echo "$(YELLOW)🔍 Running type checking...$(NC)"
	poetry run mypy src/

# Code style checking with flake8
check-style:
	@echo "$(YELLOW)🔍 Running code style check...$(NC)"
	poetry run flake8 src/ tests/ --max-line-length=119

# Format checking with black
format-check:
	@echo "$(YELLOW)🔍 Running format check...$(NC)"
	poetry run black src/ tests/ --check

# Import sorting check with isort
import-check:
	@echo "$(YELLOW)🔍 Running import check...$(NC)"
	poetry run isort src/ tests/ --check-only

# Run tests
test:
	@echo "$(YELLOW)🧪 Running tests...$(NC)"
	poetry run pytest tests/ -v

# Run tests with coverage
test-cov:
	@echo "$(YELLOW)🧪 Running tests with coverage...$(NC)"
	poetry run pytest tests/ --cov=src/ --cov-report=html

# Install dependencies
install:
	@echo "$(YELLOW)📦 Installing dependencies...$(NC)"
	poetry install

# Show help
help:
	@echo "$(GREEN)Available commands:$(NC)"
	@echo "  make install      - Install dependencies"
	@echo "  make lint         - Run all linting checks"
	@echo "  make lint-fix     - Auto-fix formatting"
	@echo "  make check-types  - Run only type checking"
	@echo "  make check-style  - Run only style checking"
	@echo "  make format-check - Run only format checking"
	@echo "  make import-check - Run only import checking"
	@echo "  make test         - Run tests"
	@echo "  make test-cov     - Run tests with coverage"
	@echo "  make help         - Show this help"