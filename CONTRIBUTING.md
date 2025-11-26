# Contributing to HedgeAI

Thank you for your interest in contributing to HedgeAI! This document provides guidelines and instructions for contributing.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Making Changes](#making-changes)
- [Code Style](#code-style)
- [Testing](#testing)
- [Submitting Changes](#submitting-changes)

## Code of Conduct

By participating in this project, you agree to maintain a respectful and inclusive environment.

## Getting Started

1. **Fork the repository**
   ```bash
   # Click "Fork" on GitHub
   ```

2. **Clone your fork**
   ```bash
   git clone https://github.com/YOUR_USERNAME/HedgeAI.git
   cd HedgeAI
   ```

3. **Add upstream remote**
   ```bash
   git remote add upstream https://github.com/ORIGINAL_OWNER/HedgeAI.git
   ```

## Development Setup

### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY
```

### Frontend Setup

```bash
cd frontend
npm install
cp .env.local.example .env.local
# Edit .env.local if needed
```

### Install Pre-commit Hooks

```bash
pip install pre-commit
pre-commit install
```

## Making Changes

1. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Write clean, readable code
   - Add tests for new functionality
   - Update documentation as needed

3. **Test your changes**
   ```bash
   # Backend
   cd backend
   pytest tests/ -v

   # Frontend
   cd frontend
   npm run lint
   npm run build
   ```

## Code Style

### Python (Backend)

- Follow PEP 8
- Use **Black** formatter (max line length: 100)
- Use **isort** for import sorting
- Use **flake8** for linting
- Add type hints where appropriate

```bash
# Format code
black app/ tests/

# Sort imports
isort app/ tests/

# Lint
flake8 app/ tests/ --max-line-length=100
```

### TypeScript/JavaScript (Frontend)

- Follow ESLint rules
- Use TypeScript for new components
- Use functional components with hooks
- Add proper type annotations

```bash
# Lint
npm run lint
```

## Testing

### Backend Tests

```bash
cd backend
pytest tests/ -v --cov=app
```

### Writing Tests

- Place tests in `backend/tests/`
- Name test files `test_*.py`
- Use descriptive test names
- Mock external API calls
- Aim for >70% code coverage

## Submitting Changes

1. **Commit your changes**
   ```bash
   git add .
   git commit -m "feat: add amazing feature"
   ```

   **Commit Message Format:**
   - `feat:` New feature
   - `fix:` Bug fix
   - `docs:` Documentation changes
   - `test:` Adding tests
   - `refactor:` Code refactoring
   - `style:` Code style changes
   - `chore:` Maintenance tasks

2. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

3. **Open a Pull Request**
   - Go to GitHub and click "New Pull Request"
   - Provide a clear description of your changes
   - Reference any related issues
   - Wait for code review

## Pull Request Guidelines

- **One feature per PR** - Keep PRs focused
- **Update tests** - Add/update tests for your changes
- **Update docs** - Update README/docs if needed
- **Pass CI checks** - Ensure all tests and lints pass
- **Respond to feedback** - Address reviewer comments

## Development Tips

### Running with Docker

```bash
# Build and run all services
docker-compose up --build

# Run specific service
docker-compose up backend
```

### Debugging

- **Backend:** Use Python debugger or logging
- **Frontend:** Use browser DevTools and React DevTools

### Common Issues

**Backend won't start:**
- Check your `.env` file has `ANTHROPIC_API_KEY`
- Ensure all dependencies are installed

**Frontend build fails:**
- Delete `node_modules` and `.next`
- Run `npm install` again
- Check `NEXT_PUBLIC_API_URL` in `.env.local`

## Questions?

- Open an issue for bugs or feature requests
- Start a discussion for questions
- Check existing issues before creating new ones

## License

By contributing, you agree that your contributions will be licensed under the same license as the project.

---

Thank you for contributing to HedgeAI! 🚀
