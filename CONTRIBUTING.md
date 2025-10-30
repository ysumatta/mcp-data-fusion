# Contributing to MCP Data Fusion

Thank you for your interest in contributing!

## Development Setup

```bash
# Clone and setup
git clone https://github.com/ysumatta/mcp-data-fusion.git
cd mcp-data-fusion

# Create virtual environment
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows

# Install dev dependencies
pip install -e ".[dev]"

# Run tests
pytest
```

## Code Style

- Use Black for formatting: `black src/`
- Use Ruff for linting: `ruff check src/`
- Type hints required: `mypy src/`

## Pull Requests

1. Fork the repository
2. Create feature branch: `git checkout -b feature/my-feature`
3. Make changes with tests
4. Ensure tests pass: `pytest`
5. Format code: `black src/ && ruff check src/`
6. Commit: `git commit -m "feat: add my feature"`
7. Push: `git push origin feature/my-feature`
8. Create Pull Request

## Commit Convention

Use conventional commits:
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation
- `test:` Tests
- `refactor:` Code refactoring

## Areas for Contribution

- Additional geocoding APIs
- More fuzzy matching algorithms
- ML-based matching
- Performance optimizations
- Documentation improvements

## Questions?

Open an issue or discussion on GitHub.
