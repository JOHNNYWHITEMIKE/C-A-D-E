# Getting Started with C.A.D.E.

## Overview

C.A.D.E. (Community Application Development Environment) is a collaborative development platform designed to streamline the application development process for teams and communities.

## Installation

### Prerequisites
- Node.js 16.0.0 or higher
- npm or yarn package manager

### Setup

1. Clone the repository:
```bash
git clone https://github.com/JOHNNYWHITEMIKE/C-A-D-E.git
cd C-A-D-E
```

2. Install dependencies (if any):
```bash
npm install
```

## Quick Start

### Using the CLI

Initialize the environment:
```bash
node bin/cade.js init
```

Create a new project:
```bash
node bin/cade.js create my-app
```

List available modules:
```bash
node bin/cade.js list
```

Check environment status:
```bash
node bin/cade.js status
```

### Using as a Library

```javascript
import { CADECore } from './src/core/cade-core.js';

// Create and initialize C.A.D.E.
const cade = new CADECore();
await cade.initialize();

// Create a new project
const project = await cade.createProject('my-app', {
  type: 'web',
  framework: 'vanilla'
});

// Get available modules
const modules = cade.getAvailableModules();
console.log('Available modules:', modules);
```

## Examples

Check out the `examples/` directory for sample code:
- `hello-world.js` - Basic usage example

Run an example:
```bash
node examples/hello-world.js
```

## Core Concepts

### Modules

C.A.D.E. includes several built-in modules:
- **web-dev**: Web development tools and templates
- **api-builder**: REST API scaffolding and tools
- **collaboration**: Team collaboration features
- **testing**: Testing framework integration

### Projects

Projects are managed by the ProjectManager and can be configured with various options like type and framework.

### Logger

A built-in logger provides colored console output for better visibility during development.

## Next Steps

- Explore the [API Documentation](./api.md)
- Read about [Architecture](./architecture.md)
- Contribute to the project on [GitHub](https://github.com/JOHNNYWHITEMIKE/C-A-D-E)

## Support

For issues and questions, please visit our [GitHub Issues](https://github.com/JOHNNYWHITEMIKE/C-A-D-E/issues) page.
