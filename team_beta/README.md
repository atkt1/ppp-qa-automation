# Team Beta - Placeholder

This directory is reserved for Team Beta's test automation code.

## Setup Instructions

When ready to onboard Team Beta:

1. Copy the structure from `team_alpha` as a template
2. Create `pyproject.toml` with core dependency
3. Create package structure:
   ```
   team_beta/
   ├── __init__.py
   ├── conftest.py
   ├── pages/
   ├── api_clients/
   ├── data/
   └── tests/
       ├── web/
       ├── api/
       └── integration/
   ```
4. Update `.gitlab-ci.yml` to uncomment the team_beta job
5. Add team-specific markers to `pytest.ini` if needed

## Getting Started

```bash
cd src/teams/team_beta
poetry install
poetry run playwright install
poetry run pytest
```
