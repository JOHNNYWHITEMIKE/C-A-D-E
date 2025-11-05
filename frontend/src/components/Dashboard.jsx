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
          <div className="stat-icon">🤖</div>
          <div className="stat-value">{stats.totalAgents}</div>
          <div className="stat-label">Total Agents</div>
        </div>
        
        <div className="stat-card">
          <div className="stat-icon">📁</div>
          <div className="stat-value">{stats.totalProjects}</div>
          <div className="stat-label">Projects</div>
        </div>
        
        <div className="stat-card">
          <div className="stat-icon">⚡</div>
          <div className="stat-value">{stats.activeAgents}</div>
          <div className="stat-label">Active Agents</div>
        </div>
      </div>

      <div className="welcome-section">
        <h3>Welcome to C-A-D-E</h3>
        <p>
          The Community Application Development Environment is your platform for building,
          testing, and deploying AI agents. Explore our features:
        </p>
        <ul className="feature-list">
          <li>🔧 <strong>Agent Builder:</strong> Create custom AI agents with visual tools</li>
          <li>🤖 <strong>Agent Library:</strong> Browse and use pre-built agents</li>
          <li>📁 <strong>Project Management:</strong> Organize your AI applications</li>
          <li>🚀 <strong>Deploy & Execute:</strong> Run agents in a secure environment</li>
          <li>📚 <strong>Documentation:</strong> Learn from comprehensive guides</li>
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
