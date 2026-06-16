# Contributing to Fake News Detection

First off, thank you for considering contributing to the Fake News Detection Platform! It is people like you who make open source such a great community.

## How Can I Contribute?

### Reporting Bugs
If you find a bug, please create an issue in the GitHub repository. Include:
* A clear description of the bug.
* Steps to reproduce the issue.
* Expected and actual behavior.
* Screenshots or log outputs if applicable.

### Suggesting Enhancements
If you have ideas for new features or improvements:
* Open an issue explaining the proposed enhancement.
* Detail why it would be useful and how it should work.

### Pull Requests
To submit changes:
1. **Fork the repository** and create your branch from `main`.
2. **Set up the environments**:
   * For the Python backend: Follow the instructions in the [backend README](backend/README.md) to set up dependencies and API keys.
   * For the Next.js frontend: Set up packages with `npm install` inside `frontend/verinews-ui`.
3. **Commit your changes**: Ensure your commit messages are clear and follow standard conventions.
4. **Test your code**: Ensure the existing test suite passes (e.g., `pytest` in the backend) and no new lint issues are introduced.
5. **Open a Pull Request (PR)** against the `main` branch. Provide a comprehensive description of the changes.

## Code Style & Standards
* **Python**: Follow PEP 8 standards. Use standard docstrings for modules and functions.
* **TypeScript / React**: Maintain clean component structures and use modern React patterns with Tailwind/Vanilla CSS.
* **Tests**: Write unit tests for new logic and helpers under the `tests/` directory.

## Licensing
By contributing, you agree that your contributions will be licensed under the MIT License.
