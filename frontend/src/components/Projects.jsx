import { useState, useEffect } from 'react'
import './Projects.css'

const BASE = 'http://localhost:8000'

function Projects() {
  const [projects, setProjects] = useState([])
  const [allAgents, setAllAgents] = useState([])
  const [showCreate, setShowCreate] = useState(false)
  const [editProject, setEditProject] = useState(null)
  const [deleteTarget, setDeleteTarget] = useState(null)
  const [newProject, setNewProject] = useState({ name: '', description: '', agents: [] })
  const [error, setError] = useState(null)

  useEffect(() => { fetchProjects(); fetchAgents() }, [])

  const fetchProjects = async () => {
    try {
      const res = await fetch(`${BASE}/projects`)
      const data = await res.json()
      setProjects(data.projects || [])
    } catch (e) { console.error(e) }
  }

  const fetchAgents = async () => {
    try {
      const res = await fetch(`${BASE}/agents`)
      const data = await res.json()
      setAllAgents(data.agents || [])
    } catch (e) { console.error(e) }
  }

  const handleCreate = async (e) => {
    e.preventDefault()
    setError(null)
    try {
      const res = await fetch(`${BASE}/projects`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name: newProject.name, description: newProject.description, agents: newProject.agents }),
      })
      if (!res.ok) { const d = await res.json(); setError(d.detail); return }
      fetchProjects()
      setShowCreate(false)
      setNewProject({ name: '', description: '', agents: [] })
    } catch (e) { setError(String(e)) }
  }

  const handleUpdateAgents = async (projectId, agentIds) => {
    await fetch(`${BASE}/projects/${projectId}/agents`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ agents: agentIds }),
    })
    fetchProjects()
    setEditProject(null)
  }

  const handleDelete = async () => {
    if (!deleteTarget) return
    await fetch(`${BASE}/projects/${deleteTarget.id}`, { method: 'DELETE' })
    setDeleteTarget(null)
    fetchProjects()
  }

  const toggleAgent = (agentId, setFn) => {
    setFn(prev => ({
      ...prev,
      agents: prev.agents.includes(agentId)
        ? prev.agents.filter(id => id !== agentId)
        : [...prev.agents, agentId],
    }))
  }

  return (
    <div className="projects">
      <div className="projects-header">
        <h2 className="page-title">Projects</h2>
        <button className="btn-primary" onClick={() => { setShowCreate(!showCreate); setError(null) }}>
          {showCreate ? 'Cancel' : '+ New Project'}
        </button>
      </div>

      {error && <div className="project-error">{error}</div>}

      {showCreate && (
        <div className="create-form">
          <h3>Create New Project</h3>
          <form onSubmit={handleCreate}>
            <div className="form-group">
              <label>Project Name *</label>
              <input
                type="text"
                value={newProject.name}
                onChange={e => setNewProject({ ...newProject, name: e.target.value })}
                placeholder="My AI Project"
                required
              />
            </div>
            <div className="form-group">
              <label>Description *</label>
              <textarea
                value={newProject.description}
                onChange={e => setNewProject({ ...newProject, description: e.target.value })}
                placeholder="Describe your project…"
                rows="3"
                required
              />
            </div>
            <div className="form-group">
              <label>Assign Agents</label>
              <div className="agent-checkboxes">
                {allAgents.map(a => (
                  <label key={a.id} className="agent-checkbox-item">
                    <input
                      type="checkbox"
                      checked={newProject.agents.includes(a.id)}
                      onChange={() => toggleAgent(a.id, setNewProject)}
                    />
                    <span>{a.name}</span>
                    {!a.available && <span className="unavail-hint">(unavailable)</span>}
                  </label>
                ))}
                {allAgents.length === 0 && <span className="no-agents-hint">No agents yet</span>}
              </div>
            </div>
            <button type="submit" className="btn-primary">Create Project</button>
          </form>
        </div>
      )}

      <div className="projects-grid">
        {projects.length === 0 ? (
          <div className="no-projects"><p>No projects yet. Create your first project!</p></div>
        ) : projects.map(project => (
          <div key={project.id} className="project-card">
            <h3>{project.name}</h3>
            <p className="project-desc">{project.description}</p>
            <div className="project-agents">
              {project.agents.length === 0
                ? <span className="no-agents-hint">No agents assigned</span>
                : project.agents.map(agentId => {
                    const a = allAgents.find(x => x.id === agentId)
                    return (
                      <span key={agentId} className={`project-agent-chip ${a?.available ? 'avail' : 'unavail'}`}>
                        {a?.name || agentId}
                      </span>
                    )
                  })
              }
            </div>
            <div className="project-actions">
              <button className="btn-secondary" onClick={() => setEditProject({ ...project })}>Manage Agents</button>
              <button className="btn-danger" onClick={() => setDeleteTarget(project)}>Delete</button>
            </div>
          </div>
        ))}
      </div>

      {/* ── Edit Agents Modal ─────────────────────────────────────────── */}
      {editProject && (
        <div className="modal-overlay" onClick={() => setEditProject(null)}>
          <div className="modal" onClick={e => e.stopPropagation()}>
            <div className="modal-header">
              <h3>Manage Agents – {editProject.name}</h3>
              <button className="modal-close" onClick={() => setEditProject(null)}>✕</button>
            </div>
            <div className="agent-checkboxes">
              {allAgents.map(a => (
                <label key={a.id} className="agent-checkbox-item">
                  <input
                    type="checkbox"
                    checked={editProject.agents.includes(a.id)}
                    onChange={() => setEditProject(prev => ({
                      ...prev,
                      agents: prev.agents.includes(a.id)
                        ? prev.agents.filter(id => id !== a.id)
                        : [...prev.agents, a.id],
                    }))}
                  />
                  <span>{a.name}</span>
                  {!a.available && <span className="unavail-hint">(unavailable)</span>}
                </label>
              ))}
            </div>
            <div className="modal-actions">
              <button className="btn-primary" onClick={() => handleUpdateAgents(editProject.id, editProject.agents)}>Save</button>
              <button className="btn-secondary" onClick={() => setEditProject(null)}>Cancel</button>
            </div>
          </div>
        </div>
      )}

      {/* ── Delete Confirmation ───────────────────────────────────────── */}
      {deleteTarget && (
        <div className="modal-overlay" onClick={() => setDeleteTarget(null)}>
          <div className="modal modal-sm" onClick={e => e.stopPropagation()}>
            <h3>Delete "{deleteTarget.name}"?</h3>
            <p style={{ color: '#aaa', margin: '1rem 0' }}>This cannot be undone.</p>
            <div className="modal-actions">
              <button className="btn-danger" onClick={handleDelete}>Delete</button>
              <button className="btn-secondary" onClick={() => setDeleteTarget(null)}>Cancel</button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default Projects
