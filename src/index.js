#!/usr/bin/env node

/**
 * C.A.D.E - Community Application Development Environment
 * Main entry point for the development environment
 */

import { CADECore } from './core/cade-core.js';
import { Logger } from './utils/logger.js';

const logger = new Logger('CADE');

/**
 * Initialize and start the C.A.D.E. environment
 */
async function main() {
  try {
    logger.info('Starting C.A.D.E. - Community Application Development Environment');
    logger.info('Version: 1.0.0');
    
    const cade = new CADECore();
    await cade.initialize();
    
    logger.success('C.A.D.E. initialized successfully!');
    logger.info('Environment is ready for development');
    
    // Display available modules
    const modules = cade.getAvailableModules();
    if (modules.length > 0) {
      logger.info('Available modules:');
      modules.forEach(module => {
        logger.info(`  - ${module.name}: ${module.description}`);
      });
    }
    
  } catch (error) {
    logger.error('Failed to initialize C.A.D.E.:', error.message);
    process.exit(1);
  }
}

// Run if this is the main module
if (import.meta.url === `file://${process.argv[1]}`) {
  main();
}

export { main };
