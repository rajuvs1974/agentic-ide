#!/usr/bin/env bash

set -euo pipefail

echo "========================================"
echo " Agentic IDE Verification"
echo "========================================"

cd "$(dirname "$0")/../backend"

echo ""
echo "▶ Running tests..."
uv run pytest

echo ""
echo "▶ Running Ruff..."
uv run ruff check .

echo ""
echo "▶ Running Mypy..."
uv run mypy .

echo ""
echo "========================================"
echo " ✓ All verification checks passed"
echo "========================================"
