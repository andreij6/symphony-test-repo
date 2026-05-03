# Symphony Test Repo

This is a minimal project for testing Symphony + Claude Code orchestration.

## Project structure

```
src/         Python source code
tests/       pytest test suite
```

## Commands

```bash
# Run tests
pytest tests/ -v

# Run the app
python src/main.py

# Install deps
pip install -r requirements.txt
```

## Conventions

- Python 3.11+
- Use `pytest` for all tests
- Keep functions small and focused
- Each module should have a matching test file under `tests/`

## Agent notes

- This repo is used for end-to-end testing of the Symphony orchestration pipeline.
- Complete each Linear issue fully before moving to Human Review.
- Always run `pytest tests/ -v` and confirm it passes before submitting a PR.
- Use `gh` CLI for all GitHub operations.
