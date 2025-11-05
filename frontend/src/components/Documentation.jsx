import './Documentation.css'

function Documentation() {
  return (
    <div className="documentation">
      <h2 className="page-title">Documentation</h2>

      <div className="doc-content">
        <section className="doc-section">
          <h3>🚀 Getting Started with C-A-D-E</h3>
          <p>
            C-A-D-E (Community Application Development Environment) is a comprehensive platform
            for building, testing, and deploying AI agents. This guide will help you get started
            with creating your first AI agent.
          </p>
        </section>

        <section className="doc-section">
          <h3>📖 What is C-A-D-E?</h3>
          <p>
            C-A-D-E is an open-source platform that provides:
          </p>
          <ul>
            <li>Visual agent builder with code editor</li>
            <li>Support for multiple AI frameworks (LangChain, AutoGPT, CrewAI, etc.)</li>
            <li>Project management for organizing AI applications</li>
            <li>Agent execution environment</li>
            <li>Community-driven agent library</li>
          </ul>
        </section>

        <section className="doc-section">
          <h3>🔧 Creating Your First Agent</h3>
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
          <h3>🤖 Agent Categories</h3>
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
          <h3>📚 AI Frameworks Supported</h3>
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
          <h3>📁 Working with Projects</h3>
          <p>
            Projects help you organize multiple agents working together:
          </p>
          <ol>
            <li>Create a new project from the Projects page</li>
            <li>Add agents to your project</li>
            <li>Configure agent interactions and workflows</li>
            <li>Deploy your complete AI application</li>
          </ol>
        </section>

        <section className="doc-section">
          <h3>🔗 Resources</h3>
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
          <h3>💡 Best Practices</h3>
          <ul>
            <li>Start with simple agents and gradually increase complexity</li>
            <li>Test your agents thoroughly before deployment</li>
            <li>Use appropriate error handling in your agent code</li>
            <li>Document your agents for community sharing</li>
            <li>Follow security best practices when handling API keys</li>
          </ul>
        </section>

        <section className="doc-section">
          <h3>🤝 Contributing</h3>
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
