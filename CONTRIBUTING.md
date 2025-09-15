Contributing to codon-recoder
=============================

Thanks for your interest in contributing! This guide covers how to get set up, make changes, and submit them.

Getting started
- Fork and clone the repository.
- Create a virtual environment (recommended) and install in editable mode:
  - `python -m venv .venv && source .venv/bin/activate`
  - `pip install -e .`
- Run tests to verify your environment:
  - `pytest -q`
  - In restricted environments (no tmp/cache writes):
    `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src pytest -q --capture=no -p no:cacheprovider`

Making changes
- Keep changes focused; avoid unrelated refactors in the same PR.
- Add tests for any new behavior or bug fixes.
- Maintain API stability or clearly document breaking changes in the PR.
- Follow existing code style: type annotations, small functions, clear names.

Feature ideas & bugs
- Open an issue before large changes to align on scope and design.
- When reporting bugs, include minimal reproducible examples (DNA, AA, command used).

Coding tips
- Put shared constants in `src/codon_recode/tables.py`.
- Core logic lives in `src/codon_recode/recoder.py`.
- The CLI is in `src/codon_recode/cli.py`.
- Add tests under `tests/` and keep them fast and deterministic.

Commit and PR
- Use clear commit messages (imperative mood): "Add wobble tie-break option".
- Open a PR with a description of the change, rationale, and any caveats.
- Link to related issues and include before/after examples if relevant.

License
- By contributing, you agree that your contributions are licensed under the MIT License.

