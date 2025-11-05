# Contributing to C-A-D-E

Thank you for your interest in contributing to C-A-D-E! This guide will help you get started.

## Code of Conduct

By participating in this project, you agree to:
- Be respectful and inclusive
- Provide constructive feedback
- Focus on what is best for the community
- Show empathy towards other contributors

## How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported
2. Use the GitHub issue tracker
3. Provide detailed information:
   - Steps to reproduce
   - Expected behavior
   - Actual behavior
   - Screenshots if applicable
   - Environment details (OS, browser, versions)

### Suggesting Features

1. Check if the feature has been suggested
2. Open a GitHub issue with the "enhancement" label
3. Describe:
   - The problem you're trying to solve
   - Your proposed solution
   - Alternative solutions considered
   - Additional context

### Contributing Code

#### Getting Started

1. Fork the repository
2. Clone your fork:
```bash
git clone https://github.com/YOUR-USERNAME/C-A-D-E.git
cd C-A-D-E
```

3. Add upstream remote:
```bash
git remote add upstream https://github.com/JOHNNYWHITEMIKE/C-A-D-E.git
```

4. Create a new branch:
```bash
git checkout -b feature/your-feature-name
```

#### Development Setup

**Backend:**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

**Docker:**
```bash
docker-compose up -d
```

#### Making Changes

1. Make your changes
2. Follow the coding standards
3. Test your changes
4. Update documentation if needed
5. Commit with clear messages

#### Commit Messages

Use clear, descriptive commit messages:
```
feat: add user authentication system
fix: resolve agent execution timeout
docs: update API documentation
style: format code with prettier
refactor: simplify agent creation logic
test: add unit tests for agent service
```

Prefixes:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Formatting, no code change
- `refactor`: Code restructuring
- `test`: Adding tests
- `chore`: Maintenance

#### Pull Request Process

1. Update your branch:
```bash
git fetch upstream
git rebase upstream/main
```

2. Push to your fork:
```bash
git push origin feature/your-feature-name
```

3. Create a Pull Request:
   - Use a clear title
   - Describe your changes
   - Reference related issues
   - Add screenshots if applicable
   - Request review from maintainers

4. Address review feedback
5. Wait for approval and merge

### Coding Standards

#### Python (Backend)

- Follow PEP 8
- Use type hints
- Write docstrings
- Keep functions small and focused
- Use meaningful variable names

Example:
```python
from typing import List, Dict, Any

def analyze_data(data: List[int]) -> Dict[str, Any]:
    """
    Analyze numerical data and return statistics.
    
    Args:
        data: List of integers to analyze
        
    Returns:
        Dictionary containing statistical results
    """
    return {
        "count": len(data),
        "total": sum(data),
        "average": sum(data) / len(data)
    }
```

#### JavaScript/React (Frontend)

- Use ES6+ features
- Follow React best practices
- Use functional components with hooks
- Keep components small and reusable
- Use meaningful component names

Example:
```javascript
import { useState, useEffect } from 'react';

function AgentCard({ agent }) {
  const [isLoading, setIsLoading] = useState(false);
  
  useEffect(() => {
    // Effect logic
  }, []);
  
  return (
    <div className="agent-card">
      <h3>{agent.name}</h3>
      <p>{agent.description}</p>
    </div>
  );
}

export default AgentCard;
```

#### CSS

- Use BEM naming convention when applicable
- Keep specificity low
- Use CSS variables for theming
- Mobile-first responsive design
- Comment complex styles

### Testing

#### Backend Tests

```bash
cd backend
pytest
```

Write tests for:
- API endpoints
- Business logic
- Data validation
- Error handling

#### Frontend Tests

```bash
cd frontend
npm test
```

Write tests for:
- Components
- User interactions
- API integration
- Routing

### Documentation

Update documentation when:
- Adding new features
- Changing API endpoints
- Modifying configuration
- Updating dependencies

Files to update:
- `README.md` - Main documentation
- `docs/API.md` - API changes
- `docs/SETUP.md` - Setup changes
- `FEATURES.md` - New features
- Code comments - Complex logic

### Adding Sample Agents

To add a new sample agent:

1. Edit `backend/sample_data.py`
2. Add your agent to `get_sample_agents()`:

```python
{
    "id": "my-agent",
    "name": "My Agent",
    "description": "What it does",
    "category": "Category",
    "framework": "Framework",
    "language": "Python",
    "code": """# Your code here
def main():
    # Implementation
    pass
"""
}
```

3. Test the agent loads correctly
4. Update documentation

### Project Structure

```
C-A-D-E/
├── backend/
│   ├── main.py              # FastAPI application
│   ├── sample_data.py       # Sample agents
│   ├── requirements.txt     # Python dependencies
│   └── Dockerfile          # Backend container
├── frontend/
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── App.jsx        # Main app
│   │   └── main.jsx       # Entry point
│   ├── package.json       # Node dependencies
│   └── Dockerfile        # Frontend container
├── docs/                 # Documentation
├── docker-compose.yml   # Multi-container setup
└── README.md           # Main documentation
```

## Review Process

1. **Automated Checks**: CI/CD runs tests
2. **Code Review**: Maintainer reviews code
3. **Testing**: Changes are tested
4. **Documentation**: Docs are reviewed
5. **Approval**: PR is approved
6. **Merge**: Changes are merged

## Getting Help

- **Documentation**: Check docs first
- **Issues**: Search existing issues
- **Discussions**: Use GitHub Discussions
- **Contact**: Reach out to maintainers

## Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md
- Mentioned in release notes
- Credited in commits

## License

By contributing, you agree that your contributions will be licensed under the GPL-3.0 License.

## Questions?

Feel free to:
- Open an issue
- Start a discussion
- Contact the maintainers

Thank you for contributing to C-A-D-E! 🎉
