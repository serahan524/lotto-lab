# Development rules

- Keep modules focused on a single responsibility.
- Use type hints for functions.
- Do not hardcode credentials or API keys.
- Use logging instead of print for operational messages.
- Include error handling for external data collection.
- Write pytest tests for core business logic.
- Do not add dependencies unless necessary.
- Do not implement features without explicit instructions.

## Python Environment

- Use the project's `.venv` virtual environment.
- Do not install Python packages globally.
- Keep project dependencies in `pyproject.toml`.
- Do not commit `.venv` to Git.