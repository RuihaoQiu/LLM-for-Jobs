#!/usr/bin/env bash
set -euo pipefail

# Run salary evaluation using the sample gold dataset
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="${SCRIPT_DIR%/scripts}"

cd "$REPO_ROOT"
python Evaluation/cli.py --data data/gold/salary_gold.csv --task salary

