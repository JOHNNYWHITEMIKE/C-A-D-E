import { useState, useEffect } from 'react'
import './AgentList.css'

function AgentList() {
  const [agents, setAgents] = useState([])
  const [filter, setFilter] = useState('all')
  const [searchTerm, setSearchTerm] = useState('')
  const [executing, setExecuting] = useState(null)
  const [execResult, setExecResult] = useState(null)

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

  const runAgent = async (agentId) => {
    setExecuting(agentId)
    setExecResult(null)
    try {
      const response = await fetch('http://localhost:8000/agents/execute', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ agent_id: agentId, input_data: {} }),
      })
      const data = await response.json()
      setExecResult(data)
    } catch (error) {
      console.error('Error executing agent:', error)
      setExecResult({ status: 'error', orchestrator_result: String(error) })
    } finally {
      setExecuting(null)
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

      {execResult && (
        <div className={`exec-result ${execResult.status === 'success' ? 'exec-success' : 'exec-error'}`}>
          <div className="exec-result-header">
            <strong>Orchestrator result</strong>
            <button className="exec-close" onClick={() => setExecResult(null)}>✕</button>
          </div>
          <div className="exec-result-body">
            <span className={`exec-status-badge ${execResult.status}`}>{execResult.status}</span>
            <code>{execResult.orchestrator_result}</code>
            {execResult.task_id && (
              <div className="exec-task-id">Task ID: {execResult.task_id}</div>
            )}
          </div>
        </div>
      )}

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
                <button
                  className="btn-primary"
                  onClick={() => runAgent(agent.id)}
                  disabled={executing === agent.id}
                >
                  {executing === agent.id ? 'Running…' : 'Run'}
                </button>
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
