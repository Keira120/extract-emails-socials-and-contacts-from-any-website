set -euo pipefail

# Run the scraper locally using the example input and output paths by default.
# You can override them:
#   ./scripts/run_local.sh --input data/input.json --output data/output.json --format csv

python -m src.main "$@"