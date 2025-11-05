import { useState, useEffect } from 'react'
import './AgentList.css'

function AgentList() {
  const [agents, setAgents] = useState([])
  const [filter, setFilter] = useState('all')
  const [searchTerm, setSearchTerm] = useState('')

  useEffect(() => {
    fetchAgents()
  }, [])

  const fetchAgents = async () => {
    try {
      const response = await fetch('http://localhost:8000/agents')
      const data = await response.json()
      setAgents(data.agents || [])
    } catch (error) {
      console.error('Error fetching agents:', error)
    }
  }

  const filteredAgents = agents.filter(agent => {
    const matchesSearch = agent.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         agent.description.toLowerCase().includes(searchTerm.toLowerCase())
    const matchesFilter = filter === 'all' || agent.category === filter
    return matchesSearch && matchesFilter
  })

  const categories = [
    'all',
    'Autonomous Agents',
    'Code Generation',
    'Data Analysis',
    'Web Automation',
    'NLP & Chat'
  ]

  return (
    <div className="agent-list">
      <h2 className="page-title">AI Agents</h2>

      <div className="filters">
        <input
          type="text"
          placeholder="🔍 Search agents..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          className="search-input"
        />
        
        <div className="category-filters">
          {categories.map(cat => (
            <button
              key={cat}
              className={`filter-btn ${filter === cat ? 'active' : ''}`}
              onClick={() => setFilter(cat)}
            >
              {cat === 'all' ? 'All' : cat}
            </button>
          ))}
        </div>
      </div>

      <div className="agents-grid">
        {filteredAgents.length === 0 ? (
          <div className="no-agents">
            <p>No agents found. Create your first agent!</p>
            <button onClick={() => window.location.href = '/builder'}>
              Create Agent
            </button>
          </div>
        ) : (
          filteredAgents.map(agent => (
            <div key={agent.id} className="agent-card">
              <div className="agent-header">
                <h3>{agent.name}</h3>
                <span className="agent-category">{agent.category}</span>
              </div>
              <p className="agent-description">{agent.description}</p>
              <div className="agent-meta">
                <span className="meta-item">📦 {agent.framework}</span>
                <span className="meta-item">💻 {agent.language}</span>
              </div>
              <div className="agent-actions">
                <button className="btn-primary">Run</button>
                <button className="btn-secondary">View</button>
                <button className="btn-secondary">Edit</button>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  )
}

export default AgentList
