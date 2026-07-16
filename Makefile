.DEFAULT_GOAL := help
.PHONY: help install run lint format fix check test clean

help:
	@echo "Available commands:"
	@echo "  make install  Install dependencies"
	@echo "  make run      Run the chat server"
	@echo ""
	@echo "  make lint     Check style with ruff"
	@echo "  make format   Format code with ruff"
	@echo "  make fix      Auto-fix and format"
	@echo "  make check    Check without modifying (used by CI)"
	@echo "  make test     Run tests with pytest"
	@echo "  make clean    Remove __pycache__ and .pyc files"

install:
	poetry install

run:
	poetry run meshchat

lint:
	ruff check chatserver/

format:
	ruff format chatserver/

fix:
	ruff check chatserver/ --fix
	ruff format chatserver/

check:
	ruff check chatserver/
	ruff format chatserver/ --check

test:
	poetry run pytest

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
