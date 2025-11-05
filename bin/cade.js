#!/usr/bin/env node

/**
 * C.A.D.E. CLI - Command Line Interface
 * Provides command-line access to C.A.D.E. functionality
 */

import { CADECore } from '../src/core/cade-core.js';
import { Logger } from '../src/utils/logger.js';

const logger = new Logger('CADE-CLI');

/**
 * Display help information
 */
function showHelp() {
  console.log(`
C.A.D.E. - Community Application Development Environment
Version: 1.0.0

Usage: cade [command] [options]

Commands:
  init              Initialize C.A.D.E. environment
  create <name>     Create a new project
  list              List available modules
  status            Show environment status
  help              Show this help message

Examples:
  cade init
  cade create my-app
  cade list
  cade status

For more information, visit: https://github.com/JOHNNYWHITEMIKE/C-A-D-E
`);
}

/**
 * Main CLI handler
 */
async function cli() {
  const args = process.argv.slice(2);
  const command = args[0];

  try {
    const cade = new CADECore();

    switch (command) {
      case 'init':
        logger.info('Initializing C.A.D.E. environment...');
        await cade.initialize();
        logger.success('Environment initialized successfully!');
        break;

      case 'create':
        const projectName = args[1];
        if (!projectName) {
          logger.error('Project name is required');
          logger.info('Usage: cade create <project-name>');
          process.exit(1);
        }
        await cade.initialize();
        const project = await cade.createProject(projectName);
        logger.success(`Project "${project.name}" created successfully`);
        break;

      case 'list':
        await cade.initialize();
        const modules = cade.getAvailableModules();
        logger.info('Available modules:');
        modules.forEach(module => {
          console.log(`  • ${module.name} (v${module.version}) - ${module.description}`);
        });
        break;

      case 'status':
        await cade.initialize();
        const status = cade.getStatus();
        logger.info('C.A.D.E. Status:');
        console.log(`  Initialized: ${status.initialized ? 'Yes' : 'No'}`);
        console.log(`  Version: ${status.version}`);
        console.log(`  Modules: ${status.modules}`);
        break;

      case 'help':
      case '--help':
      case '-h':
        showHelp();
        break;

      default:
        if (command) {
          logger.error(`Unknown command: ${command}`);
        }
        showHelp();
        process.exit(command ? 1 : 0);
    }
  } catch (error) {
    logger.error('Command failed:', error.message);
    process.exit(1);
  }
}

cli();
