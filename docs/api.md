# C.A.D.E. API Documentation

## CADECore

The main class for interacting with the C.A.D.E. environment.

### Constructor

```javascript
const cade = new CADECore();
```

### Methods

#### `initialize()`

Initialize the C.A.D.E. environment.

**Returns:** `Promise<void>`

**Example:**
```javascript
await cade.initialize();
```

#### `getAvailableModules()`

Get a list of all available modules.

**Returns:** `Array<Module>`

**Example:**
```javascript
const modules = cade.getAvailableModules();
modules.forEach(m => console.log(m.name));
```

#### `createProject(projectName, options)`

Create a new project.

**Parameters:**
- `projectName` (string): Name of the project
- `options` (Object): Configuration options
  - `type` (string): Project type (default: 'web')
  - `framework` (string): Framework to use (default: 'vanilla')

**Returns:** `Promise<Project>`

**Example:**
```javascript
const project = await cade.createProject('my-app', {
  type: 'web',
  framework: 'react'
});
```

#### `getStatus()`

Get the current status of the environment.

**Returns:** `Object`
- `initialized` (boolean): Whether the environment is initialized
- `modules` (number): Number of loaded modules
- `version` (string): C.A.D.E. version

**Example:**
```javascript
const status = cade.getStatus();
console.log(`Initialized: ${status.initialized}`);
```

## ProjectManager

Manages project creation and storage.

### Methods

#### `initialize()`

Initialize the project manager.

**Returns:** `Promise<void>`

#### `createProject(projectName, options)`

Create a new project.

**Parameters:**
- `projectName` (string): Name of the project
- `options` (Object): Project configuration

**Returns:** `Promise<Project>`

**Throws:** Error if project already exists

#### `getProjects()`

Get all projects.

**Returns:** `Array<Project>`

#### `getProject(projectName)`

Get a specific project by name.

**Parameters:**
- `projectName` (string): Name of the project

**Returns:** `Project | null`

## ModuleLoader

Manages module loading and lifecycle.

### Methods

#### `loadModules()`

Load all available modules.

**Returns:** `Promise<void>`

#### `getModules()`

Get all enabled modules.

**Returns:** `Array<Module>`

#### `getModule(moduleName)`

Get a specific module by name.

**Parameters:**
- `moduleName` (string): Name of the module

**Returns:** `Module | null`

#### `enableModule(moduleName)`

Enable a module.

**Parameters:**
- `moduleName` (string): Name of the module to enable

#### `disableModule(moduleName)`

Disable a module.

**Parameters:**
- `moduleName` (string): Name of the module to disable

## Logger

Provides logging functionality with colored output.

### Constructor

```javascript
const logger = new Logger('MyContext');
```

### Methods

#### `info(message, ...args)`

Log an informational message (cyan).

#### `success(message, ...args)`

Log a success message (green).

#### `warn(message, ...args)`

Log a warning message (yellow).

#### `error(message, ...args)`

Log an error message (red).

#### `debug(message, ...args)`

Log a debug message (magenta). Only shown when `DEBUG` env var is set.

## Types

### Module

```javascript
{
  name: string,
  description: string,
  version: string,
  enabled: boolean
}
```

### Project

```javascript
{
  name: string,
  created: string,  // ISO 8601 timestamp
  type: string,
  framework: string,
  // ...additional options
}
```

## CLI Commands

### `cade init`

Initialize the C.A.D.E. environment.

### `cade create <name>`

Create a new project with the specified name.

### `cade list`

List all available modules.

### `cade status`

Show the current environment status.

### `cade help`

Display help information.
