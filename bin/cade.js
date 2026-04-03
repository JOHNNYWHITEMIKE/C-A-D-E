#!/usr/bin/env node

/**
 * C.A.D.E. CLI - Command Line Interface
 * Provides command-line access to C.A.D.E. functionality
 */

import { CADECore } from '../src/core/cade-core.js';
import { Logger } from '../src/utils/logger.js';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const logger = new Logger('CADE-CLI');

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

function readCliHelpFile() {
  const helpFile = path.resolve(__dirname, '../docs/CLI_HELP.md');
  if (!fs.existsSync(helpFile)) return null;
  return fs.readFileSync(helpFile, 'utf8');
}

function showManSummary() {
  console.log(`
C.A.D.E. Manual

Manual page source: man/cade.1
Extended help: docs/CLI_HELP.md

Tip: On Unix-like systems you can view the page with:
  man ./man/cade.1
`);
}

/**
 * Display help information
 */
function showHelp() {
  const helpFile = readCliHelpFile();
  if (helpFile) {
    console.log(helpFile);
    return;
  }

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
  man               Show manual summary

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

      case 'man':
        showManSummary();
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
