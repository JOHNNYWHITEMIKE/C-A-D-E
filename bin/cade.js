#!/usr/bin/env node

/**
 * C.A.D.E. CLI – Command Line Interface
 * All agent and execution commands call the backend REST API.
 */

import { CADECore } from '../src/core/cade-core.js';
import { ApiClient } from '../src/core/api-client.js';
import { Logger } from '../src/utils/logger.js';

const logger = new Logger('CADE-CLI');
const api = new ApiClient();

function showHelp() {
  console.log(`
C.A.D.E. – Community Application Development Environment
Version: 1.0.0

Usage: cade [command] [options]

Commands:
  init                        Initialise C.A.D.E. environment
  status                      Show environment and backend status
  list                        List available modules

  agents list                 List all agents from the backend
  agents run <id> [json]      Run an agent by ID (optional JSON input)
  agents get <id>             Get details of a single agent

  executions list             List recent executions
  executions logs <id>        Show logs for an execution

  help                        Show this help message

Examples:
  cade agents list
  cade agents run web-scraper-01
  cade agents run web-scraper-01 '{"target_urls":["https://example.com"]}'
  cade executions list
  cade executions logs <uuid>

For more information: https://github.com/JOHNNYWHITEMIKE/C-A-D-E
`);
}

async function cli() {
  const args = process.argv.slice(2);
  const command = args[0];
  const sub = args[1];

  try {
    switch (command) {

      // ── Core commands ────────────────────────────────────────────────────

      case 'init': {
        logger.info('Initialising C.A.D.E. environment…');
        const cade = new CADECore();
        await cade.initialize();
        logger.success('Environment initialised!');
        break;
      }

      case 'status': {
        logger.info('Fetching backend status…');
        const info = await api.get('/');
        console.log(`  Name   : ${info.name}`);
        console.log(`  Version: ${info.version}`);
        console.log(`  Status : ${info.status}`);
        console.log(`  Docker : ${info.docker_available ? '✅ available' : '❌ not available (simulated mode)'}`);
        break;
      }

      case 'list': {
        const cade = new CADECore();
        await cade.initialize();
        const modules = cade.getAvailableModules();
        logger.info('Available modules:');
        modules.forEach(m => console.log(`  • ${m.name} (v${m.version}) – ${m.description}`));
        break;
      }

      // ── Agent commands ───────────────────────────────────────────────────

      case 'agents': {
        if (!sub || sub === 'list') {
          const data = await api.get('/agents');
          const agents = data.agents || [];
          logger.info(`${agents.length} agents:`);
          agents.forEach(a => {
            const avail = a.available ? '✅' : '⬜';
            console.log(`  ${avail} ${a.id.padEnd(28)} ${a.name}`);
          });
          break;
        }

        if (sub === 'get') {
          const id = args[2];
          if (!id) { logger.error('Usage: cade agents get <id>'); process.exit(1); }
          const data = await api.get(`/agents/${id}`);
          const a = data.agent;
          console.log(`\nAgent: ${a.name}`);
          console.log(`  ID         : ${a.id}`);
          console.log(`  Category   : ${a.category}`);
          console.log(`  Available  : ${a.available}`);
          console.log(`  Docker     : ${a.docker_image || '(none)'}`);
          console.log(`  Skills     : ${(a.skills || []).join(', ')}`);
          console.log(`  Description: ${a.description}`);
          break;
        }

        if (sub === 'run') {
          const id = args[2];
          if (!id) { logger.error('Usage: cade agents run <id> [json-input]'); process.exit(1); }
          let inputData = {};
          if (args[3]) {
            try { inputData = JSON.parse(args[3]); } catch {
              logger.error('Third argument must be valid JSON'); process.exit(1);
            }
          }
          logger.info(`Submitting execution for agent: ${id}`);
          const data = await api.post('/agents/execute', { agent_id: id, input_data: inputData });
          const execId = data.execution_id;
          console.log(`  Execution ID: ${execId}`);
          console.log(`  Status      : ${data.status}`);
          logger.info('Polling for results…');

          // Poll until done
          let done = false;
          while (!done) {
            await new Promise(r => setTimeout(r, 2000));
            const poll = await api.get(`/executions/${execId}`);
            const ex = poll.execution;
            const status = ex.status;
            process.stdout.write(`\r  Status: ${status}        `);
            if (!['pending', 'running'].includes(status)) {
              done = true;
              console.log('');
              logger.success(`Execution ${status}`);
              if (ex.logs) {
                console.log('\n── Logs ──────────────────────────────────────');
                console.log(ex.logs);
                console.log('──────────────────────────────────────────────');
              }
            }
          }
          break;
        }

        logger.error(`Unknown agents sub-command: ${sub}`);
        showHelp();
        process.exit(1);
        break;
      }

      // ── Execution commands ───────────────────────────────────────────────

      case 'executions': {
        if (!sub || sub === 'list') {
          const data = await api.get('/executions?limit=20');
          const execs = data.executions || [];
          logger.info(`${execs.length} recent executions:`);
          execs.forEach(ex => {
            const ts = ex.started_at ? new Date(ex.started_at).toLocaleString() : '–';
            console.log(`  ${ex.status.padEnd(12)} ${ex.id.slice(0, 8)}  ${ex.agent_name || ex.agent_id}  ${ts}`);
          });
          break;
        }

        if (sub === 'logs') {
          const id = args[2];
          if (!id) { logger.error('Usage: cade executions logs <execution-id>'); process.exit(1); }
          const data = await api.get(`/executions/${id}`);
          const ex = data.execution;
          if (!ex) { logger.error('Execution not found'); process.exit(1); }
          console.log(`\nExecution: ${ex.id}`);
          console.log(`  Agent  : ${ex.agent_name || ex.agent_id}`);
          console.log(`  Status : ${ex.status}`);
          console.log(`  Exit   : ${ex.exit_code}`);
          if (ex.logs) {
            console.log('\n── Logs ──────────────────────────────────────');
            console.log(ex.logs);
            console.log('──────────────────────────────────────────────');
          } else {
            console.log('(no logs captured)');
          }
          break;
        }

        logger.error(`Unknown executions sub-command: ${sub}`);
        showHelp();
        process.exit(1);
        break;
      }

      case 'help':
      case '--help':
      case '-h':
        showHelp();
        break;

      default:
        if (command) logger.error(`Unknown command: ${command}`);
        showHelp();
        process.exit(command ? 1 : 0);
    }

  } catch (error) {
    if (error.code === 'ECONNREFUSED') {
      logger.error('Cannot connect to backend. Is `uvicorn main:app` running on port 8000?');
    } else {
      logger.error('Command failed:', error.message);
    }
    process.exit(1);
  }
}

cli();
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
