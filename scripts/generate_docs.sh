#!/bin/bash

# Generate markdown documentation for GitHub Wiki
# This script extracts docstrings from Python modules and creates wiki pages

set -e

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

echo "🚀 Generating documentation for AnswerRocket Python Client..."
echo ""

# Run the Python documentation generator
python3 "$SCRIPT_DIR/generate_docs.py"

echo ""
echo "✅ Documentation generation complete!"
echo ""
echo "Generated files:"
ls -lh "$PROJECT_ROOT/wiki/"
echo ""
echo "📝 Wiki pages ready for GitHub at: $PROJECT_ROOT/wiki/"
