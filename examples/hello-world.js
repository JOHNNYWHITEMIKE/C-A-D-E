/**
 * C.A.D.E. Hello World Example
 * This example demonstrates basic usage of the C.A.D.E. environment
 */

import { CADECore } from '../src/core/cade-core.js';

async function helloWorld() {
  console.log('=== C.A.D.E. Hello World Example ===\n');
  
  // Create a new C.A.D.E. instance
  const cade = new CADECore();
  
  // Initialize the environment
  await cade.initialize();
  
  // Get environment status
  const status = cade.getStatus();
  console.log('Environment Status:', status);
  
  // List available modules
  console.log('\nAvailable Modules:');
  const modules = cade.getAvailableModules();
  modules.forEach(module => {
    console.log(`  - ${module.name}: ${module.description}`);
  });
  
  // Create a sample project
  console.log('\nCreating a sample project...');
  const project = await cade.createProject('hello-world-app', {
    type: 'web',
    framework: 'vanilla'
  });
  
  console.log('Project created:', project);
  console.log('\n=== Example Complete ===');
}

helloWorld().catch(console.error);
