import { useState, useEffect } from 'react'
import './Dashboard.css'

function Dashboard() {
  const [stats, setStats] = useState(null)
  const [error, setError] = useState(null)

  useEffect(() => {
    fetchStats()
  }, [])

  const fetchStats = async () => {
    try {
      const response = await fetch('http://localhost:8000/dashboard/stats')
      if (!response.ok) throw new Error('Failed to fetch stats')
      const data = await response.json()
      setStats(data)
    } catch (err) {
      console.error('Error fetching stats:', err)
      setError('Could not load dashboard stats')
    }
  }

  const taskTotal = stats
    ? Object.values(stats.orchestrator.task_counts).reduce((a, b) => a + b, 0)
    : 0

  return (
    <div className="dashboard">
      <h2 className="page-title">Dashboard</h2>

      {error && <p className="error-text">{error}</p>}

      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-icon">AI</div>
          <div className="stat-value">{stats ? stats.agents.total : '–'}</div>
          <div className="stat-label">Total Agents</div>
        </div>

        <div className="stat-card">
          <div className="stat-icon">PR</div>
          <div className="stat-value">{stats ? stats.projects.total : '–'}</div>
          <div className="stat-label">Projects</div>
        </div>

        <div className="stat-card">
          <div className="stat-icon">OC</div>
          <div className="stat-value">{stats ? stats.orchestrator.foundation_agents : '–'}</div>
          <div className="stat-label">Orchestrator Agents</div>
        </div>

        <div className="stat-card">
          <div className="stat-icon">TK</div>
          <div className="stat-value">{taskTotal}</div>
          <div className="stat-label">Tasks Processed</div>
        </div>

        <div className="stat-card">
          <div className="stat-icon">CM</div>
          <div className="stat-value">{stats ? stats.community.member_count : '–'}</div>
          <div className="stat-label">Community Members</div>
        </div>

        <div className="stat-card">
          <div className="stat-icon">VP</div>
          <div className="stat-value">{stats ? stats.community.proposal_count : '–'}</div>
          <div className="stat-label">Proposals</div>
        </div>
      </div>

      {stats && (
        <div className="orchestrator-section">
          <h3>Orchestrator Status</h3>
          <div className="info-row">
            <span className="info-label">Recommendation:</span>
            <span className="info-value">{stats.orchestrator.monetization_recommendation}</span>
          </div>
          {Object.keys(stats.orchestrator.agents_by_role).length > 0 && (
            <div className="role-grid">
              {Object.entries(stats.orchestrator.agents_by_role).map(([role, count]) => (
                <span key={role} className="role-chip">{role}: {count}</span>
              ))}
            </div>
          )}
        </div>
      )}

      <div className="welcome-section">
        <h3>Welcome to C-A-D-E</h3>
        <p>
          The Community Application Development Environment is your platform for building,
          testing, and deploying AI agents. Explore our features:
        </p>
        <ul className="feature-list">
          <li><strong>Agent Builder:</strong> Create custom AI agents with visual tools</li>
          <li><strong>Agent Library:</strong> Browse and use pre-built agents</li>
          <li><strong>Project Management:</strong> Organize your AI applications</li>
          <li><strong>Deploy & Execute:</strong> Run agents via the CADE v3 orchestrator</li>
          <li><strong>Community:</strong> Governance, proposals, and announcements</li>
          <li><strong>Documentation:</strong> Learn from comprehensive guides</li>
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
          <button onClick={() => window.location.href = '/community'}>
            Community
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
