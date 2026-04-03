import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import './Dashboard.css'

const BASE = 'http://localhost:8000'

function Dashboard() {
  const navigate = useNavigate()
  const [stats, setStats] = useState(null)
  const [error, setError] = useState(null)

  useEffect(() => { fetchStats() }, [])

  const fetchStats = async () => {
    try {
      const res = await fetch(`${BASE}/dashboard/stats`)
      if (!res.ok) throw new Error('Failed')
      setStats(await res.json())
    } catch (e) {
      setError('Could not load dashboard stats – is the backend running?')
    }
  }

  const taskTotal = stats
    ? Object.values(stats.orchestrator.task_counts).reduce((a, b) => a + b, 0)
    : 0

  const statusColor = { completed: '#00c48c', failed: '#ff6b6b', simulated: '#f0a500', running: '#00d9ff', pending: '#888' }

  return (
    <div className="dashboard">
      <h2 className="page-title">Dashboard</h2>
      {error && <p className="error-text">{error}</p>}

      <div className="stats-grid">
        {[
          { icon: 'AI', value: stats?.agents.total, label: 'Total Agents' },
          { icon: 'PR', value: stats?.projects.total, label: 'Projects' },
          { icon: '▶', value: stats?.executions.total, label: 'Executions' },
          { icon: '✅', value: stats?.executions.completed, label: 'Completed' },
          { icon: 'OC', value: stats?.orchestrator.foundation_agents, label: 'Orchestrator Agents' },
          { icon: '👥', value: stats?.community.member_count, label: 'Community Members' },
        ].map(({ icon, value, label }) => (
          <div key={label} className="stat-card">
            <div className="stat-icon">{icon}</div>
            <div className="stat-value">{value ?? '–'}</div>
            <div className="stat-label">{label}</div>
          </div>
        ))}
      </div>

      {stats && !stats.docker_available && (
        <div className="info-banner warn">
          ⚠️ Docker is not available – agent executions will be <strong>simulated</strong>.
          Start the Docker daemon to enable real container runs.
        </div>
      )}

      {stats && stats.executions.recent?.length > 0 && (
        <div className="recent-section">
          <div className="section-header">
            <h3>Recent Executions</h3>
            <button className="link-btn" onClick={() => navigate('/history')}>View all →</button>
          </div>
          <div className="exec-table">
            {stats.executions.recent.map(ex => (
              <div key={ex.id} className="exec-row">
                <span className="exec-status-dot" style={{ background: statusColor[ex.status] || '#888' }} />
                <span className="exec-agent">{ex.agent_name || ex.agent_id}</span>
                <span className="exec-status-text" style={{ color: statusColor[ex.status] || '#888' }}>{ex.status}</span>
                <span className="exec-time">{ex.started_at ? new Date(ex.started_at).toLocaleString() : ''}</span>
                <button className="link-btn" onClick={() => navigate('/history')}>Logs</button>
              </div>
            ))}
          </div>
        </div>
      )}

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
        <ul className="feature-list">
          <li><strong>Agent Builder:</strong> Create custom AI agents with visual tools</li>
          <li><strong>Agent Library:</strong> Browse, run, and manage agents loaded from the manifest</li>
          <li><strong>Project Management:</strong> Group agents into projects</li>
          <li><strong>Deploy & Execute:</strong> Run Docker-backed agents and view live logs</li>
          <li><strong>Execution History:</strong> Full log trail for every run</li>
          <li><strong>Community:</strong> Governance, proposals, and announcements</li>
        </ul>
      </div>

      <div className="quick-actions">
        <h3>Quick Actions</h3>
        <div className="action-buttons">
          <button onClick={() => navigate('/builder')}>Create New Agent</button>
          <button onClick={() => navigate('/agents')}>Browse Agents</button>
          <button onClick={() => navigate('/history')}>Execution History</button>
          <button onClick={() => navigate('/community')}>Community</button>
        </div>
      </div>
    </div>
  )
}

export default Dashboard
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
