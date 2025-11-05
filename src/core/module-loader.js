/**
 * ModuleLoader - Loads and manages development modules
 */

import { Logger } from '../utils/logger.js';

export class ModuleLoader {
  constructor() {
    this.logger = new Logger('ModuleLoader');
    this.modules = [];
  }

  /**
   * Load available modules
   */
  async loadModules() {
    this.logger.info('Loading modules...');
    
    // Core modules that come with C.A.D.E.
    this.modules = [
      {
        name: 'web-dev',
        description: 'Web development tools and templates',
        version: '1.0.0',
        enabled: true
      },
      {
        name: 'api-builder',
        description: 'REST API scaffolding and tools',
        version: '1.0.0',
        enabled: true
      },
      {
        name: 'collaboration',
        description: 'Team collaboration features',
        version: '1.0.0',
        enabled: true
      },
      {
        name: 'testing',
        description: 'Testing framework integration',
        version: '1.0.0',
        enabled: true
      }
    ];

    this.logger.success(`Loaded ${this.modules.length} modules`);
  }

  /**
   * Get all loaded modules
   * @returns {Array} Array of module objects
   */
  getModules() {
    return this.modules.filter(m => m.enabled);
  }

  /**
   * Get a specific module by name
   * @param {string} moduleName - Name of the module
   * @returns {Object|null} Module object or null if not found
   */
  getModule(moduleName) {
    return this.modules.find(m => m.name === moduleName) || null;
  }

  /**
   * Enable a module
   * @param {string} moduleName - Name of the module to enable
   */
  enableModule(moduleName) {
    const module = this.getModule(moduleName);
    if (module) {
      module.enabled = true;
      this.logger.info(`Module "${moduleName}" enabled`);
    }
  }

  /**
   * Disable a module
   * @param {string} moduleName - Name of the module to disable
   */
  disableModule(moduleName) {
    const module = this.getModule(moduleName);
    if (module) {
      module.enabled = false;
      this.logger.info(`Module "${moduleName}" disabled`);
    }
  }
}
