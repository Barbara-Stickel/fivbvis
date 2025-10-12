# Tests for fivbvis

This directory contains unit tests and integration tests for the fivbvis package.

## Quick Start - Verify API

The easiest way to verify your API calls are working:

```bash
python verify_api.py
```

This script will test:
- ✓ Beach team list (tournament 8244, expecting 80+ teams)
- ✓ Beach tournament list and single tournament
- ✓ Player list and single player (ID 143192)

## Running Unit Tests

Install test dependencies:
```bash
pip install -r requirements-dev.txt
```

Run all unit tests (mocked, no API calls):
```bash
pytest tests/test_references.py
```

Run tests with coverage:
```bash
pytest tests/test_references.py --cov=fivbvis
```

Run specific test class:
```bash
pytest tests/test_references.py::TestBeach
```

Run specific test:
```bash
pytest tests/test_references.py::TestBeach::test_getBeachMatch
```

## Running Integration Tests

Integration tests make actual API calls to verify everything works:

```bash
# Run all integration tests
pytest tests/test_integration.py -v -s

# Run specific integration test
pytest tests/test_integration.py::TestBeachIntegration::test_getBeachTeamList_with_tournament -v -s
```

**Note:** Integration tests require internet connection and will take longer to run.

## Test Structure

### Unit Tests (`test_references.py`)
- **TestArticle**: Tests for article retrieval methods
- **TestBeach**: Tests for beach volleyball methods (matches, tournaments, teams)
- **TestPlayer**: Tests for player information methods
- **TestVolleyball**: Tests for volleyball match methods
- **TestFivbVisCore**: Tests for core functionality (parameter conversion, field cleanup)

Uses `unittest.mock` to mock HTTP requests - no actual API calls.

### Integration Tests (`test_integration.py`)
- **TestBeachIntegration**: Real API calls for Beach methods
  - Tournament 8244 team list (expecting 80+ teams)
  - Tournament list and single tournament retrieval
- **TestPlayerIntegration**: Real API calls for Player methods
  - Player list retrieval
  - Single player retrieval (ID 143192)

### Verification Script (`../verify_api.py`)
Standalone script to quickly verify API functionality with formatted output.

