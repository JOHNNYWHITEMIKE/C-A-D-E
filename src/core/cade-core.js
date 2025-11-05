/**
 * CADECore - Core functionality for the Community Application Development Environment
 */

import { ProjectManager } from './project-manager.js';
import { ModuleLoader } from './module-loader.js';
import { Logger } from '../utils/logger.js';

export class CADECore {
  constructor() {
    this.logger = new Logger('CADECore');
    this.projectManager = new ProjectManager();
    this.moduleLoader = new ModuleLoader();
    this.initialized = false;
  }

  /**
   * Initialize the C.A.D.E. environment
   */
  async initialize() {
    if (this.initialized) {
      this.logger.warn('C.A.D.E. is already initialized');
      return;
    }

    this.logger.info('Initializing C.A.D.E. Core...');
    
    // Load available modules
    await this.moduleLoader.loadModules();
    
    // Initialize project manager
    await this.projectManager.initialize();
    
    this.initialized = true;
    this.logger.success('Core initialization complete');
  }

  /**
   * Get list of available modules
   * @returns {Array} Array of module information
   */
  getAvailableModules() {
    return this.moduleLoader.getModules();
  }

  /**
   * Create a new project
   * @param {string} projectName - Name of the project
   * @param {Object} options - Project configuration options
   */
  async createProject(projectName, options = {}) {
    return await this.projectManager.createProject(projectName, options);
  }

  /**
   * Get current environment status
   * @returns {Object} Status information
   */
  getStatus() {
    return {
      initialized: this.initialized,
      modules: this.moduleLoader.getModules().length,
      version: '1.0.0'
    };
  }
}
