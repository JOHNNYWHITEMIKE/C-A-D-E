import { useState, useEffect } from 'react'
import './ExecutionHistory.css'

const BASE = 'http://localhost:8000'

const STATUS_COLOR = {
  completed: '#00c48c',
  failed: '#ff6b6b',
  simulated: '#f0a500',
  running: '#00d9ff',
  pending: '#888',
  error: '#ff6b6b',
}

function ExecutionHistory() {
  const [executions, setExecutions] = useState([])
  const [selected, setSelected] = useState(null)
  const [agentFilter, setAgentFilter] = useState('')
  const [loading, setLoading] = useState(true)

  useEffect(() => { fetchExecutions() }, [])

  const fetchExecutions = async () => {
    setLoading(true)
    try {
      const res = await fetch(`${BASE}/executions?limit=100`)
      const data = await res.json()
      setExecutions(data.executions || [])
    } catch (e) {
      console.error(e)
    } finally {
      setLoading(false)
    }
  }

  const openLogs = async (ex) => {
    // Refresh from API to get latest logs
    try {
      const res = await fetch(`${BASE}/executions/${ex.id}`)
      const data = await res.json()
      setSelected(data.execution || ex)
    } catch (e) {
      setSelected(ex)
    }
  }

  const filtered = executions.filter(ex =>
    !agentFilter ||
    ex.agent_name?.toLowerCase().includes(agentFilter.toLowerCase()) ||
    ex.agent_id?.toLowerCase().includes(agentFilter.toLowerCase())
  )

  const statusCounts = executions.reduce((acc, ex) => {
    acc[ex.status] = (acc[ex.status] || 0) + 1
    return acc
  }, {})

  return (
    <div className="exec-history">
      <div className="history-header">
        <h2 className="page-title">Execution History</h2>
        <button className="btn-secondary" onClick={fetchExecutions}>↻ Refresh</button>
      </div>

      {/* Summary bar */}
      <div className="status-bar">
        {Object.entries(statusCounts).map(([status, count]) => (
          <span key={status} className="status-pill" style={{ borderColor: STATUS_COLOR[status] + '44', color: STATUS_COLOR[status] }}>
            {status}: {count}
          </span>
        ))}
        <span className="status-pill total">total: {executions.length}</span>
      </div>

      <input
        type="text"
        className="history-search"
        placeholder="🔍 Filter by agent name…"
        value={agentFilter}
        onChange={e => setAgentFilter(e.target.value)}
      />

      {loading ? (
        <p className="loading-text">Loading…</p>
      ) : filtered.length === 0 ? (
        <div className="no-execs">
          <p>No executions yet. Run an agent from the Agents page to see history here.</p>
        </div>
      ) : (
        <div className="exec-list">
          {filtered.map(ex => (
            <div key={ex.id} className="exec-item" onClick={() => openLogs(ex)}>
              <span className="ex-dot" style={{ background: STATUS_COLOR[ex.status] || '#888' }} />
              <div className="ex-main">
                <span className="ex-agent">{ex.agent_name || ex.agent_id}</span>
                <span className="ex-id">{ex.id.slice(0, 8)}…</span>
              </div>
              <span className="ex-status" style={{ color: STATUS_COLOR[ex.status] || '#888' }}>{ex.status}</span>
              <span className="ex-time">
                {ex.started_at ? new Date(ex.started_at).toLocaleString() : '–'}
              </span>
              <span className="ex-caret">›</span>
            </div>
          ))}
        </div>
      )}

      {/* Log drawer */}
      {selected && (
        <div className="log-drawer-overlay" onClick={() => setSelected(null)}>
          <div className="log-drawer" onClick={e => e.stopPropagation()}>
            <div className="drawer-header">
              <div>
                <h3>{selected.agent_name || selected.agent_id}</h3>
                <span className="drawer-id">ID: {selected.id}</span>
              </div>
              <button className="modal-close" onClick={() => setSelected(null)}>✕</button>
            </div>

            <div className="drawer-meta">
              <span className="dm-badge" style={{ background: STATUS_COLOR[selected.status] + '22', color: STATUS_COLOR[selected.status], border: `1px solid ${STATUS_COLOR[selected.status]}44` }}>
                {selected.status}
              </span>
              {selected.exit_code !== undefined && selected.exit_code !== -1 && (
                <span className="dm-item">exit: {selected.exit_code}</span>
              )}
              {selected.started_at && (
                <span className="dm-item">started: {new Date(selected.started_at).toLocaleString()}</span>
              )}
              {selected.finished_at && (
                <span className="dm-item">finished: {new Date(selected.finished_at).toLocaleString()}</span>
              )}
              {selected.container_id && (
                <span className="dm-item">container: {selected.container_id.slice(0, 12)}</span>
              )}
            </div>

            {selected.input_data && Object.keys(selected.input_data).length > 0 && (
              <div className="drawer-section">
                <h4>Input</h4>
                <pre className="log-pre">{JSON.stringify(selected.input_data, null, 2)}</pre>
              </div>
            )}

            <div className="drawer-section">
              <h4>Logs</h4>
              <pre className="log-pre">{selected.logs || '(no output captured)'}</pre>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default ExecutionHistory
