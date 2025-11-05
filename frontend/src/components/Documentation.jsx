import './Documentation.css'

function Documentation() {
  return (
    <div className="documentation">
      <h2 className="page-title">Documentation</h2>

      <div className="doc-content">
        <section className="doc-section">
          <h3>Getting Started with C-A-D-E</h3>
          <p>
            C-A-D-E (Community Application Development Environment) is a comprehensive platform
            for building, testing, and deploying AI agents. This guide will help you get started
            with creating your first AI agent.
          </p>
        </section>

        <section className="doc-section">
          <h3>What is C-A-D-E?</h3>
          <p>
            C-A-D-E (Community of Autonomous AI Agent Development Environment) is an open-source
            orchestration platform — a complete DevOps + IDE + agent-hub for autonomous AI agents. It provides:
          </p>
          <ul>
            <li>🧠 <strong>AI Agent Frameworks:</strong> LangChain, AutoGPT, CrewAI, and more</li>
            <li>⚙️ <strong>Developer Tools:</strong> FastAPI backend, React frontend, Monaco editor</li>
            <li>🧰 <strong>Automation Layer:</strong> CLI + Dockerized environment</li>
            <li>☁️ <strong>Remote Integration:</strong> GitHub syncing + API endpoints</li>
            <li>🧩 <strong>Multi-Agent Orchestration:</strong> Coordinate multiple agents in projects</li>
            <li>📊 <strong>Monitoring & Analytics:</strong> Dashboard for agent performance tracking</li>
          </ul>
        </section>

        <section className="doc-section">
          <h3>Creating Your First Agent</h3>
          <ol>
            <li>
              <strong>Navigate to Agent Builder:</strong> Click on "Agent Builder" in the sidebar
            </li>
            <li>
              <strong>Fill in Basic Information:</strong>
              <ul>
                <li>Agent Name: Give your agent a descriptive name</li>
                <li>Description: Explain what your agent does</li>
                <li>Category: Select the appropriate category</li>
                <li>Framework: Choose your preferred AI framework</li>
              </ul>
            </li>
            <li>
              <strong>Write Your Code:</strong> Use the built-in Monaco editor to write your agent logic
            </li>
            <li>
              <strong>Save and Deploy:</strong> Click "Create Agent" to save your agent
            </li>
          </ol>
        </section>

        <section className="doc-section">
          <h3>Agent Categories</h3>
          <div className="categories-grid">
            <div className="category-item">
              <h4>Autonomous Agents</h4>
              <p>Self-directed agents that can plan and execute tasks independently</p>
            </div>
            <div className="category-item">
              <h4>Code Generation</h4>
              <p>Agents that write, review, and optimize code</p>
            </div>
            <div className="category-item">
              <h4>Data Analysis</h4>
              <p>Agents for analyzing and visualizing data</p>
            </div>
            <div className="category-item">
              <h4>Web Automation</h4>
              <p>Agents that automate web browsing and interactions</p>
            </div>
          </div>
        </section>

        <section className="doc-section">
          <h3>AI Frameworks Supported</h3>
          <ul>
            <li><strong>LangChain:</strong> Build applications with LLMs through composability</li>
            <li><strong>AutoGPT:</strong> Autonomous GPT-4 experiments</li>
            <li><strong>CrewAI:</strong> Orchestrate AI agents working together</li>
            <li><strong>OpenAI:</strong> Direct integration with OpenAI APIs</li>
            <li><strong>Anthropic Claude:</strong> Integration with Claude models</li>
            <li><strong>HuggingFace:</strong> Access to thousands of open-source models</li>
          </ul>
        </section>

        <section className="doc-section">
          <h3>Working with Projects</h3>
          <p>
            Projects enable multi-agent orchestration — coordinate multiple agents working together:
          </p>
          <ol>
            <li><strong>Create a Project:</strong> Define your multi-agent application from the Projects page</li>
            <li><strong>Add Agents:</strong> Select agents to work together in your project</li>
            <li><strong>Configure Communication:</strong> Define how agents interact via REST/WebSocket</li>
            <li><strong>Orchestrate Workflows:</strong> Set up agent coordination and task distribution</li>
            <li><strong>Deploy:</strong> Launch your complete AI orchestration system</li>
          </ol>
          <p>
            <strong>Use Cases:</strong>
          </p>
          <ul>
            <li>Multi-agent systems with specialized roles</li>
            <li>Complex workflows requiring agent collaboration</li>
            <li>Distributed task processing</li>
            <li>Agent communication and data sharing</li>
          </ul>
        </section>

        <section className="doc-section">
          <h3>Resources</h3>
          <ul>
            <li>
              <a href="https://github.com/jim-schwoebel/awesome_ai_agents" target="_blank" rel="noopener noreferrer">
                Awesome AI Agents Repository
              </a>
            </li>
            <li>
              <a href="https://langchain.com" target="_blank" rel="noopener noreferrer">
                LangChain Documentation
              </a>
            </li>
            <li>
              <a href="https://www.crewai.com" target="_blank" rel="noopener noreferrer">
                CrewAI Documentation
              </a>
            </li>
          </ul>
        </section>

        <section className="doc-section">
          <h3>Best Practices</h3>
          <ul>
            <li>Start with simple agents and gradually increase complexity</li>
            <li>Test your agents thoroughly before deployment</li>
            <li>Use appropriate error handling in your agent code</li>
            <li>Document your agents for community sharing</li>
            <li>Follow security best practices when handling API keys</li>
          </ul>
        </section>

        <section className="doc-section">
          <h3>Contributing</h3>
          <p>
            C-A-D-E is open-source and welcomes contributions! You can:
          </p>
          <ul>
            <li>Share your agents with the community</li>
            <li>Report bugs and suggest features</li>
            <li>Contribute to the codebase</li>
            <li>Improve documentation</li>
          </ul>
        </section>
      </div>
    </div>
  )
}

export default Documentation
