# Contributing to LofiGirl Terminal

First off, thank you for considering contributing to LofiGirl Terminal! 🎉

This document provides guidelines for contributing to the project. Following these guidelines helps maintain a high-quality codebase and makes the review process smoother for everyone.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Process](#development-process)
- [Coding Standards](#coding-standards)
- [Submitting Changes](#submitting-changes)
- [Reporting Bugs](#reporting-bugs)
- [Suggesting Features](#suggesting-features)
- [Questions](#questions)

## Code of Conduct

This project follows a simple code of conduct:

- Be respectful and inclusive
- Be patient with beginners
- Accept constructive criticism
- Focus on what is best for the community
- Show empathy towards others

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Git
- Basic understanding of Python and terminal applications

### Setting Up Your Development Environment

1. **Fork the Repository**

   Click the "Fork" button on GitHub to create your own copy.

2. **Clone Your Fork**

   ```bash
   git clone https://github.com/YOUR_USERNAME/lofigirl-terminal.git
   cd lofigirl-terminal
   ```

3. **Set Up Development Environment**

   ```bash
   # Complete setup (recommended)
   make setup

   # This will:
   # - Create a virtual environment
   # - Install all dependencies
   # - Set up pre-commit hooks
   ```

4. **Create a Branch**

   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/your-bug-fix
   ```

## Development Process

### 1. Making Changes

- Write clear, concise code
- Follow the coding standards (see below)
- Add tests for new features
- Update documentation as needed
- Keep commits focused and atomic

### 2. Running Tests

Before submitting changes, make sure all tests pass:

```bash
# Run all tests
make test

# Run specific tests
pytest tests/test_stations.py -v

# Run tests with coverage report
pytest tests/ --cov=lofigirl_terminal --cov-report=html
```

### 3. Code Quality Checks

Run all quality checks before committing:

```bash
# Format code
make format

# Run linter
make lint

# Run type checker
make type-check

# Run all checks
make check-all
```

### 4. Pre-commit Hooks

Pre-commit hooks run automatically when you commit. If they fail:

```bash
# Fix issues automatically where possible
make format

# Run hooks manually
make pre-commit
```

## Coding Standards

### Python Style

- **Formatting**: Use Black with 88 character line length
- **Import Sorting**: Use isort with Black profile
- **Linting**: Code must pass flake8 checks
- **Type Hints**: All functions must have type annotations

### Code Style Example

```python
"""Module docstring with Google-style format."""

from typing import Optional

from lofigirl_terminal.config import Config
from lofigirl_terminal.logger import get_logger

logger = get_logger(__name__)


def example_function(param: str, optional_param: Optional[int] = None) -> bool:
    """
    Brief description of function.

    Longer description if needed.

    Args:
        param: Description of param
        optional_param: Description of optional parameter

    Returns:
        Description of return value

    Raises:
        ValueError: When param is invalid

    Example:
        >>> result = example_function("test")
        >>> print(result)
        True
    """
    if not param:
        raise ValueError("param cannot be empty")

    logger.info(f"Processing: {param}")
    return True
```

### Docstring Style

Use Google-style docstrings for all public functions, classes, and modules:

```python
def function_name(arg1: str, arg2: int) -> bool:
    """
    Short description.

    Longer description if needed, explaining the purpose and behavior.

    Args:
        arg1: Description of arg1
        arg2: Description of arg2

    Returns:
        Description of return value

    Raises:
        ValueError: When something is wrong
        TypeError: When types don't match

    Example:
        >>> result = function_name("test", 42)
        >>> print(result)
        True
    """
    pass
```

### Testing Standards

- Write tests for all new features
- Maintain minimum 80% code coverage
- Use descriptive test names
- Follow AAA pattern (Arrange, Act, Assert)

```python
def test_station_creation() -> None:
    """Test creating a station instance."""
    # Arrange
    station_data = {
        "id": "test",
        "name": "Test Station",
        "url": "https://example.com",
        "description": "Test",
    }

    # Act
    station = Station(**station_data)

    # Assert
    assert station.id == "test"
    assert station.name == "Test Station"
```

### Commit Messages

Use conventional commits format:

```
type(scope): brief description

Longer description if needed.

- Bullet points for details
- Multiple changes explained

Fixes #123
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

**Examples:**
```
feat(player): add volume control functionality

Implemented volume control with validation and error handling.

- Added set_volume() method
- Added get_volume() method
- Added validation for volume range (0-100)
- Added tests for volume control

Fixes #42
```

```
fix(stations): handle empty station URLs

Station URLs are now validated to prevent empty values.

Fixes #56
```

## Submitting Changes

### Pull Request Process

1. **Update Your Branch**

   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

2. **Push to Your Fork**

   ```bash
   git push origin feature/your-feature-name
   ```

3. **Create Pull Request**

   - Go to GitHub and create a Pull Request
   - Fill out the PR template completely
   - Link related issues
   - Add screenshots/demos if applicable

4. **PR Checklist**

   - [ ] Tests pass (`make test`)
   - [ ] Code is formatted (`make format`)
   - [ ] Linter passes (`make lint`)
   - [ ] Type checks pass (`make type-check`)
   - [ ] Documentation updated
   - [ ] CHANGELOG.md updated (if applicable)
   - [ ] Commit messages follow convention

5. **Review Process**

   - Wait for maintainer review
   - Address feedback promptly
   - Update PR as needed
   - Once approved, maintainers will merge

### PR Template

When creating a PR, include:

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Code refactoring

## Related Issues
Fixes #123

## Testing
- [ ] All tests pass
- [ ] New tests added
- [ ] Manual testing performed

## Screenshots (if applicable)
Add screenshots or demos

## Checklist
- [ ] Code follows style guidelines
- [ ] Documentation updated
- [ ] Tests added/updated
- [ ] No breaking changes (or documented)
```

## Reporting Bugs

### Before Submitting a Bug Report

- Check existing issues to avoid duplicates
- Verify the bug in the latest version
- Collect relevant information

### Bug Report Template

```markdown
**Describe the Bug**
Clear description of the bug

**To Reproduce**
Steps to reproduce:
1. Run command '...'
2. Do action '...'
3. See error

**Expected Behavior**
What you expected to happen

**Actual Behavior**
What actually happened

**Environment**
- OS: [e.g., Ubuntu 22.04]
- Python version: [e.g., 3.11.2]
- Package version: [e.g., 0.1.0]

**Additional Context**
Any other relevant information

**Logs**
```
Paste relevant logs here
```
```

## Suggesting Features

### Feature Request Template

```markdown
**Is your feature request related to a problem?**
Clear description of the problem

**Describe the solution you'd like**
What you want to happen

**Describe alternatives you've considered**
Other solutions you've thought about

**Additional context**
Any other context, mockups, or examples

**Would you like to implement this?**
Are you willing to work on this feature?
```

## Questions

### Where to Ask

- **GitHub Discussions**: For general questions and ideas
- **GitHub Issues**: For bug reports and feature requests
- **Pull Requests**: For code-specific questions

### Good Question Guidelines

- Search existing discussions first
- Be specific and clear
- Provide context and examples
- Be patient and respectful

## Recognition

Contributors are recognized in:

- GitHub contributors page
- Release notes for significant contributions
- Special mentions for major features

## Additional Resources

### Useful Links

- [Project README](README.md)
- [Project Roadmap](CLAUDE.md)
- [Python Style Guide (PEP 8)](https://pep8.org/)
- [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)
- [Conventional Commits](https://www.conventionalcommits.org/)

### Development Tips

1. **Start Small**: Begin with small contributions to familiarize yourself
2. **Ask Questions**: Don't hesitate to ask if something is unclear
3. **Read Code**: Read existing code to understand patterns
4. **Check Issues**: Look for "good first issue" labels
5. **Stay Updated**: Keep your fork synchronized with upstream

## Thank You!

Your contributions make this project better for everyone. We appreciate your time and effort! 🎵

---

**Happy Contributing!** If you have questions about contributing, feel free to ask in GitHub Discussions.
