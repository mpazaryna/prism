# PRISM

**Private Research and Intelligence System for Markets**

A Python-based research automation tool for investigating companies using AI-powered data collection and analysis.

## Status

This is an experimental project with partial implementations. The core pipeline architecture and Perplexity API integration are functional; other components use placeholder data.

| Component | Status |
|-----------|--------|
| Pipeline orchestration | ✓ Working |
| Perplexity collector | ✓ Working |
| yfinance collector | ✓ Working (basic) |
| Base collector | Placeholder data |
| Analysis module | Placeholder insights |
| NewsAPI collector | Stub only |

## Requirements

- Python 3.10+
- Poetry for dependency management
- API keys for Perplexity (optional: NewsAPI)

## Installation

```bash
# Clone and install dependencies
poetry install

# Set up environment variables
cp .env.example .env  # Then add your API keys
```

## Project Structure

```
research_kit/
├── pipeline.py          # Orchestrates collect → analyze → report
├── company.py           # Company management (in-memory)
├── analysis.py          # Analysis functions (placeholder)
├── reporting.py         # Report generation
├── collector/
│   ├── collector.py             # Base collector (dummy data)
│   ├── collector_perplexity.py  # Perplexity API integration
│   ├── collector_yfinance.py    # Yahoo Finance wrapper
│   └── collector_newsapi.py     # NewsAPI (stub)
└── utils/
    ├── logging.py        # Dual-output logging
    └── error_handling.py # Custom exceptions & decorators
```

## Usage

```python
from research_kit.pipeline import run_pipeline

# Run research pipeline for companies
results = run_pipeline(["Apple", "Microsoft"])
```

For Perplexity-based research:

```python
from research_kit.collector.collector_perplexity import research_company

result = research_company("Tell me about Acme Corp")
```

## Development

This project uses Invoke for task automation:

| Command | Description |
|---------|-------------|
| `invoke test` | Run full test suite |
| `invoke unit-test` | Run unit tests only |
| `invoke integration-test` | Run integration tests |
| `invoke lint` | Run flake8 and mypy |
| `invoke format` | Format with black and isort |
| `invoke all` | Format, lint, and test |

## Notable Implementations

**Perplexity API Integration** (`collector_perplexity.py`)
- Retry logic with exponential backoff using `tenacity`
- Handles 524 timeout errors and other edge cases
- Configurable search domains and recency filters

**Error Handling** (`utils/error_handling.py`)
- Custom exception hierarchy: `PRISMError`, `DataCollectionError`, `AnalysisError`, `ReportingError`
- `@handle_errors` decorator for consistent error wrapping

**Logging** (`utils/logging.py`)
- Dual-output loggers (file + console)
- `@log_function_call` decorator for tracing

## Documentation

See `docs/dev/` for:
- `architecture.md` - Design decisions and functional approach
- `milestone-*.md` - Feature specifications in Gherkin format

## License

MIT
