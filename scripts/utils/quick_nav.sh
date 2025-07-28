#!/bin/bash
# Quick Project Navigation Helper
# Usage: source quick_nav.sh

# Navigate to common directories
alias goto-core="cd src/core"
alias goto-nlp="cd src/nlp" 
alias goto-api="cd src/api"
alias goto-tests="cd tests"
alias goto-scripts="cd scripts"
alias goto-docs="cd docs"
alias goto-frontend="cd frontend"

# Quick commands
alias run-tests="python -m pytest tests/"
alias run-unit="python -m pytest tests/unit/"
alias run-integration="python -m pytest tests/integration/"
alias start-dev="bash scripts/deployment/start_development.sh"
alias start-prod="bash scripts/deployment/start_production.sh"

# Show project structure
alias show-structure="tree -I '__pycache__|*.pyc|.git|venv|.venv|chatbot_env'"

echo "🚀 Chatbot Diya Quick Navigation Loaded!"
echo ""
echo "Quick Commands:"
echo "  goto-core      - Go to core source code"
echo "  goto-nlp       - Go to NLP components"  
echo "  goto-api       - Go to API source"
echo "  goto-tests     - Go to tests directory"
echo "  goto-scripts   - Go to utility scripts"
echo "  goto-docs      - Go to documentation"
echo "  goto-frontend  - Go to web frontend"
echo ""
echo "  run-tests      - Run all tests"
echo "  run-unit       - Run unit tests only"
echo "  start-dev      - Start development server"
echo "  show-structure - Display project tree"
