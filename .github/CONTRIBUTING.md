# Contributing to GeneAnalyzer2

Thank you for your interest in contributing!
Improvements, bug fixes, and new features are welcome, but we ask that all changes follow the guidelines below to ensure consistency and maintainablity of the program.

## Table of Contents

1. [Getting Started](#getting-started)
2. [Development Workflow](#development-workflow)
3. [Coding Standards](#coding-standards)
4. [Testing](#testing)
5. [Pull Request Guidelines](#pull-request-guidelines)
6. [Reporting Issues](#reporting-issues)

---

## Getting Started

1. **Fork the Repository**
    Create your own fork of the project to work on.
2. **Clone your fork**

```sh
git clone https://github.com/<your-username>/GeneAnalyzer2
cd GeneAnalyzer2
```

3. ***Install Poetry*** 
```sh
pip install poetry
```

4. ***Install dependencies***
```sh
poetry install
poetry run setup-dev
```

5. ***Activate the poetry virtual environment***
```sh
poetry shell
```

## Development Workflow

1. ***Create a new branch for each feature or fix***
```sh
git checkout -b feature/your-new-feature
```
2. ***Keep your branch up to date with the master branch***
```sh
git pull origin main
```
3. ***Commit often and write clear commit messages***
```sh
git commit -am "Your clear message goes here"
``` 

## Coding Standards
This project follows the PEP8 guidelines. This is enforced with some minor configurations using flake8 for linting and formatting checks. 

Before you commit, run the following:
```sh
poetry run flake8 src tests
```

Please do the following, it will make your code easier to read:
- Use descriptive variable and function names
- Keep functions focused and avoid doing too much in one method/function
- Document all of your public methods and classes with docstrings
- If the method is not clear, add a docstring, even for private methods
- Always use type hints in your method signatures. This makes it easier to follow what your code is doing

### Commit style enforcement:
All commit messages are checked before a commit can be made. They must follow the following format:
```sh
<type>(<scope>): <short summary>
```

#### Types:
- feat     – a new feature
- fix      – a bug fix
- docs     – documentation only changes
- style    – formatting changes (no code logic)
- refactor – code restructuring without behavior change
- perf     – performance improvement
- test     – adding/updating tests
- chore    – maintenance, build, tooling
- build    – changes to build system/dependencies
- ci       – CI/CD config changes

#### Example: 
```sh
 git commit -am "feat(api): added CSV export endpoint"
``` 

Summary should be in lowercase, <=72 chars, and in past tense.

#### Body (optional):
   Explain the "what" and "why", not the "how".
   Wrap at 72 characters per line.

#### Footer (optional):
   Reference issues/tickets. Example: closes #123

## Testing
All new code must have test, both positive and negative for all public meethods. 
Note:
- Tests should go in the tests/ directory with folders mirroring the /src package structure.
- Any datasets required for tests should go in the tests/test_datasets/ folder.
- Do not commit large datasets or generated result files from your tests!

## pull Request Guidelines
1. Run linting and tests locally before pushing:
```sh
poetry run flake8 src tests
poetry run pytest
```
2. PRs will be checked by GitHub Actions CI automatically, so be sure it passes on your system before initiating a pull request. 
- Flake8 linting must pass.
- All tests must pass.
- No build artifacts or generated files should be in any of the commits. 
    - you can remove them from git tracking by doing the following:
```sh
git rm --cached <file>
```
3. You should provide a descriptive title and explain what your change does in the PR description.
4. Link any related issues to your PR if applicable

## Reporting Issues
When filing an issue:
- Provide a clear and descriptive title 
- Include as much detail as possible (error messages, environment info, reproduction steps, ect.).
- If relevant to the issue, include example inputs and outputs. 


Thank you for helping improve the GeneAnalyzer2 command-line tool! If you have any questions, feel free to reach out through walla42.businessmail@gmail.com.