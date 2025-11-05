import { useState, useEffect } from 'react'
import './Dashboard.css'

function Dashboard() {
  const [stats, setStats] = useState({
    totalAgents: 0,
    totalProjects: 0,
    activeAgents: 0
  })

  useEffect(() => {
    // Fetch stats from API
    fetchStats()
  }, [])

  const fetchStats = async () => {
    try {
      const response = await fetch('http://localhost:8000/agents')
      const data = await response.json()
      setStats({
        totalAgents: data.agents.length,
        totalProjects: 0,
        activeAgents: 0
      })
    } catch (error) {
      console.error('Error fetching stats:', error)
    }
  }

  return (
    <div className="dashboard">
      <h2 className="page-title">Dashboard</h2>
      
      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-icon">AI</div>
          <div className="stat-value">{stats.totalAgents}</div>
          <div className="stat-label">Total Agents</div>
        </div>
        
        <div className="stat-card">
          <div className="stat-icon">PR</div>
          <div className="stat-value">{stats.totalProjects}</div>
          <div className="stat-label">Projects</div>
        </div>
        
        <div className="stat-card">
          <div className="stat-icon">AC</div>
          <div className="stat-value">{stats.activeAgents}</div>
          <div className="stat-label">Active Agents</div>
        </div>
      </div>

      <div className="welcome-section">
        <h3>Welcome to C-A-D-E</h3>
        <p>
          Your Autonomous Agent Studio + Infrastructure Layer. Build, test, deploy, and orchestrate
          AI agents from a single unified environment. Explore our capabilities:
        </p>
        <ul className="feature-list">
          <li><strong>Agent Builder:</strong> Create autonomous agents with Monaco editor</li>
          <li><strong>Multi-Agent Orchestration:</strong> Coordinate multiple agents in projects</li>
          <li><strong>Framework Support:</strong> LangChain, AutoGPT, CrewAI, and more</li>
          <li><strong>Deploy & Execute:</strong> Run agents in isolated Docker environments</li>
          <li><strong>API Integration:</strong> RESTful endpoints for agent lifecycle management</li>
        </ul>
      </div>

      <div className="quick-actions">
        <h3>Quick Actions</h3>
        <div className="action-buttons">
          <button onClick={() => window.location.href = '/builder'}>
            Create New Agent
          </button>
          <button onClick={() => window.location.href = '/agents'}>
            Browse Agents
          </button>
          <button onClick={() => window.location.href = '/docs'}>
            View Documentation
          </button>
        </div>
      </div>
    </div>
  )
}

export default Dashboard
