/**
 * ProjectManager - Manages project creation and configuration
 */

import { Logger } from '../utils/logger.js';

export class ProjectManager {
  constructor() {
    this.logger = new Logger('ProjectManager');
    this.projects = new Map();
  }

  /**
   * Initialize the project manager
   */
  async initialize() {
    this.logger.info('Initializing Project Manager...');
    // Future: Load existing projects from config
    this.logger.success('Project Manager ready');
  }

  /**
   * Create a new project
   * @param {string} projectName - Name of the project
   * @param {Object} options - Configuration options
   */
  async createProject(projectName, options = {}) {
    if (this.projects.has(projectName)) {
      throw new Error(`Project "${projectName}" already exists`);
    }

    this.logger.info(`Creating project: ${projectName}`);

    const project = {
      name: projectName,
      created: new Date().toISOString(),
      type: options.type || 'web',
      framework: options.framework || 'vanilla',
      ...options
    };

    this.projects.set(projectName, project);
    this.logger.success(`Project "${projectName}" created successfully`);

    return project;
  }

  /**
   * Get all projects
   * @returns {Array} List of projects
   */
  getProjects() {
    return Array.from(this.projects.values());
  }

  /**
   * Get a specific project
   * @param {string} projectName - Name of the project
   * @returns {Object|null} Project object or null if not found
   */
  getProject(projectName) {
    return this.projects.get(projectName) || null;
  }
}
