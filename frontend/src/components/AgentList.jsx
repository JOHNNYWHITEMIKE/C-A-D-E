import { useState, useEffect, useRef } from 'react'
import { useNavigate } from 'react-router-dom'
import './AgentList.css'

const BASE = 'http://localhost:8000'

function AgentList() {
  const navigate = useNavigate()
  const [agents, setAgents] = useState([])
  const [filter, setFilter] = useState('all')
  const [searchTerm, setSearchTerm] = useState('')

  // Run dialog state
  const [runAgent, setRunAgent] = useState(null)
  const [runInput, setRunInput] = useState('')
  const [execId, setExecId] = useState(null)
  const [execStatus, setExecStatus] = useState(null)
  const [execLogs, setExecLogs] = useState('')
  const pollRef = useRef(null)

  // View dialog state
  const [viewAgent, setViewAgent] = useState(null)

  // Delete confirmation
  const [deleteTarget, setDeleteTarget] = useState(null)

  useEffect(() => { fetchAgents() }, [])

  const fetchAgents = async () => {
    try {
      const res = await fetch(`${BASE}/agents`)
      const data = await res.json()
      setAgents(data.agents || [])
    } catch (e) {
      console.error('Error fetching agents:', e)
    }
  }

  // ── Run flow ──────────────────────────────────────────────────────────────

  const openRunDialog = (agent) => {
    setRunAgent(agent)
    setRunInput('')
    setExecId(null)
    setExecStatus(null)
    setExecLogs('')
  }

  const closeRunDialog = () => {
    if (pollRef.current) clearInterval(pollRef.current)
    setRunAgent(null)
    setExecId(null)
    setExecStatus(null)
    setExecLogs('')
  }

  const startRun = async () => {
    let input = {}
    if (runInput.trim()) {
      try { input = JSON.parse(runInput) } catch {
        alert('Input must be valid JSON (or leave blank for no input)')
        return
      }
    }
    setExecStatus('pending')
    setExecLogs('')
    try {
      const res = await fetch(`${BASE}/agents/execute`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ agent_id: runAgent.id, input_data: input }),
      })
      const data = await res.json()
      if (data.execution_id) {
        setExecId(data.execution_id)
        setExecStatus('running')
        startPolling(data.execution_id)
      } else {
        setExecStatus('error')
        setExecLogs(JSON.stringify(data, null, 2))
      }
    } catch (e) {
      setExecStatus('error')
      setExecLogs(String(e))
    }
  }

  const startPolling = (id) => {
    if (pollRef.current) clearInterval(pollRef.current)
    pollRef.current = setInterval(async () => {
      try {
        const res = await fetch(`${BASE}/executions/${id}`)
        const data = await res.json()
        const exc = data.execution
        setExecStatus(exc.status)
        setExecLogs(exc.logs || '')
        if (!['pending', 'running'].includes(exc.status)) {
          clearInterval(pollRef.current)
        }
      } catch (e) {
        clearInterval(pollRef.current)
        setExecStatus('error')
      }
    }, 2000)
  }

  // ── Delete ────────────────────────────────────────────────────────────────

  const confirmDelete = async () => {
    if (!deleteTarget) return
    await fetch(`${BASE}/agents/${deleteTarget.id}`, { method: 'DELETE' })
    setDeleteTarget(null)
    fetchAgents()
  }

  // ── Filtering ─────────────────────────────────────────────────────────────

  const categories = ['all', ...new Set(agents.map(a => a.category).filter(Boolean))]

  const filtered = agents.filter(a => {
    const matchSearch =
      a.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      (a.description || '').toLowerCase().includes(searchTerm.toLowerCase())
    const matchFilter = filter === 'all' || a.category === filter
    return matchSearch && matchFilter
  })

  // ── Render ────────────────────────────────────────────────────────────────

  const statusColor = { completed: '#00c48c', failed: '#ff6b6b', simulated: '#f0a500', running: '#00d9ff', pending: '#888', error: '#ff6b6b' }

  return (
    <div className="agent-list">
      <div className="list-header">
        <h2 className="page-title">AI Agents</h2>
        <button className="btn-primary" onClick={() => navigate('/builder')}>+ New Agent</button>
      </div>

      <div className="filters">
        <input
          type="text"
          placeholder="🔍 Search agents…"
          value={searchTerm}
          onChange={e => setSearchTerm(e.target.value)}
          className="search-input"
        />
        <div className="category-filters">
          {categories.map(cat => (
            <button
              key={cat}
              className={`filter-btn ${filter === cat ? 'active' : ''}`}
              onClick={() => setFilter(cat)}
            >{cat === 'all' ? 'All' : cat}</button>
          ))}
        </div>
      </div>

      <div className="agents-grid">
        {filtered.length === 0 ? (
          <div className="no-agents">
            <p>No agents found.</p>
            <button onClick={() => navigate('/builder')}>Create Agent</button>
          </div>
        ) : filtered.map(agent => (
          <div key={agent.id} className={`agent-card ${agent.available ? '' : 'agent-unavailable'}`}>
            <div className="agent-header">
              <h3>{agent.name}</h3>
              <span className="agent-category">{agent.category}</span>
            </div>
            {!agent.available && (
              <div className="unavailable-badge">Image not yet available</div>
            )}
            <p className="agent-description">{agent.description}</p>
            {agent.skills?.length > 0 && (
              <div className="skill-chips">
                {agent.skills.slice(0, 4).map(s => (
                  <span key={s} className="skill-chip">{s}</span>
                ))}
                {agent.skills.length > 4 && <span className="skill-chip">+{agent.skills.length - 4}</span>}
              </div>
            )}
            <div className="agent-meta">
              <span className="meta-item">📦 {agent.framework}</span>
              <span className="meta-item">💻 {agent.language}</span>
              {agent.source === 'manifest' && <span className="meta-item source-badge">manifest</span>}
            </div>
            <div className="agent-actions">
              <button
                className="btn-primary"
                onClick={() => openRunDialog(agent)}
                disabled={!agent.available}
                title={agent.available ? 'Run agent' : 'Docker image not available'}
              >Run</button>
              <button className="btn-secondary" onClick={() => setViewAgent(agent)}>View</button>
              <button className="btn-secondary" onClick={() => navigate(`/builder?id=${agent.id}`)}>Edit</button>
              {agent.source !== 'manifest' && (
                <button className="btn-danger" onClick={() => setDeleteTarget(agent)}>Delete</button>
              )}
            </div>
          </div>
        ))}
      </div>

      {/* ── Run Dialog ─────────────────────────────────────────────────── */}
      {runAgent && (
        <div className="modal-overlay" onClick={closeRunDialog}>
          <div className="modal" onClick={e => e.stopPropagation()}>
            <div className="modal-header">
              <h3>Run: {runAgent.name}</h3>
              <button className="modal-close" onClick={closeRunDialog}>✕</button>
            </div>

            {!execId ? (
              <>
                <p className="modal-hint">
                  Optionally provide JSON input data for the agent:
                </p>
                <textarea
                  className="run-input"
                  placeholder={'{\n  "target_urls": ["https://example.com"],\n  "data_fields": ["title", "price"]\n}'}
                  value={runInput}
                  onChange={e => setRunInput(e.target.value)}
                  rows={6}
                />
                <div className="modal-actions">
                  <button className="btn-primary" onClick={startRun}>▶ Run</button>
                  <button className="btn-secondary" onClick={closeRunDialog}>Cancel</button>
                </div>
              </>
            ) : (
              <>
                <div className="exec-status-row">
                  <span className="exec-status-dot" style={{ background: statusColor[execStatus] || '#888' }} />
                  <span style={{ color: statusColor[execStatus] || '#888', textTransform: 'capitalize' }}>
                    {execStatus}
                  </span>
                  {['pending', 'running'].includes(execStatus) && (
                    <span className="spinner" />
                  )}
                  <span className="exec-id-hint">ID: {execId.slice(0, 8)}…</span>
                </div>

                <pre className="exec-logs">{execLogs || '(waiting for output…)'}</pre>

                <div className="modal-actions">
                  {!['pending', 'running'].includes(execStatus) && (
                    <button className="btn-secondary" onClick={() => navigate('/history')}>
                      View in History
                    </button>
                  )}
                  <button className="btn-secondary" onClick={closeRunDialog}>Close</button>
                </div>
              </>
            )}
          </div>
        </div>
      )}

      {/* ── View Dialog ────────────────────────────────────────────────── */}
      {viewAgent && (
        <div className="modal-overlay" onClick={() => setViewAgent(null)}>
          <div className="modal modal-wide" onClick={e => e.stopPropagation()}>
            <div className="modal-header">
              <h3>{viewAgent.name}</h3>
              <button className="modal-close" onClick={() => setViewAgent(null)}>✕</button>
            </div>
            <div className="view-grid">
              <div className="view-row"><span className="vk">Category</span><span>{viewAgent.category}</span></div>
              <div className="view-row"><span className="vk">Framework</span><span>{viewAgent.framework}</span></div>
              <div className="view-row"><span className="vk">Language</span><span>{viewAgent.language}</span></div>
              <div className="view-row"><span className="vk">Source</span><span>{viewAgent.source}</span></div>
              <div className="view-row"><span className="vk">Available</span><span>{viewAgent.available ? '✅ yes' : '❌ no'}</span></div>
              {viewAgent.docker_image && (
                <div className="view-row"><span className="vk">Docker Image</span><code>{viewAgent.docker_image}</code></div>
              )}
              {viewAgent.skills?.length > 0 && (
                <div className="view-row"><span className="vk">Skills</span><span>{viewAgent.skills.join(', ')}</span></div>
              )}
              {viewAgent.capabilities?.length > 0 && (
                <div className="view-row"><span className="vk">Capabilities</span><span>{viewAgent.capabilities.join(', ')}</span></div>
              )}
              <div className="view-row"><span className="vk">Description</span><span>{viewAgent.description}</span></div>
            </div>
            {viewAgent.code && (
              <pre className="code-preview">{viewAgent.code}</pre>
            )}
            <div className="modal-actions">
              <button className="btn-primary" onClick={() => { setViewAgent(null); navigate(`/builder?id=${viewAgent.id}`) }}>Edit</button>
              <button className="btn-secondary" onClick={() => setViewAgent(null)}>Close</button>
            </div>
          </div>
        </div>
      )}

      {/* ── Delete Confirmation ────────────────────────────────────────── */}
      {deleteTarget && (
        <div className="modal-overlay" onClick={() => setDeleteTarget(null)}>
          <div className="modal modal-sm" onClick={e => e.stopPropagation()}>
            <h3>Delete "{deleteTarget.name}"?</h3>
            <p style={{ color: '#aaa', margin: '1rem 0' }}>This cannot be undone.</p>
            <div className="modal-actions">
              <button className="btn-danger" onClick={confirmDelete}>Delete</button>
              <button className="btn-secondary" onClick={() => setDeleteTarget(null)}>Cancel</button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default AgentList
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
