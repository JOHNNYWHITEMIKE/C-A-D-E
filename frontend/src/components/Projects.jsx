import { useState, useEffect } from 'react'
import './Projects.css'

function Projects() {
  const [projects, setProjects] = useState([])
  const [showCreateForm, setShowCreateForm] = useState(false)
  const [newProject, setNewProject] = useState({
    id: '',
    name: '',
    description: '',
    agents: []
  })

  useEffect(() => {
    fetchProjects()
  }, [])

  const fetchProjects = async () => {
    try {
      const response = await fetch('http://localhost:8000/projects')
      const data = await response.json()
      setProjects(data.projects || [])
    } catch (error) {
      console.error('Error fetching projects:', error)
    }
  }

  const handleCreateProject = async (e) => {
    e.preventDefault()
    
    const project = {
      ...newProject,
      id: Date.now().toString()
    }

    try {
      const response = await fetch('http://localhost:8000/projects', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(project),
      })

      if (response.ok) {
        fetchProjects()
        setShowCreateForm(false)
        setNewProject({ id: '', name: '', description: '', agents: [] })
      }
    } catch (error) {
      console.error('Error creating project:', error)
    }
  }

  return (
    <div className="projects">
      <div className="projects-header">
        <h2 className="page-title">Projects</h2>
        <button onClick={() => setShowCreateForm(!showCreateForm)}>
          {showCreateForm ? 'Cancel' : '+ New Project'}
        </button>
      </div>

      {showCreateForm && (
        <div className="create-form">
          <h3>Create New Project</h3>
          <form onSubmit={handleCreateProject}>
            <div className="form-group">
              <label>Project Name</label>
              <input
                type="text"
                value={newProject.name}
                onChange={(e) => setNewProject({ ...newProject, name: e.target.value })}
                placeholder="My AI Project"
                required
              />
            </div>
            <div className="form-group">
              <label>Description</label>
              <textarea
                value={newProject.description}
                onChange={(e) => setNewProject({ ...newProject, description: e.target.value })}
                placeholder="Describe your project..."
                rows="3"
                required
              />
            </div>
            <button type="submit">Create Project</button>
          </form>
        </div>
      )}

      <div className="projects-grid">
        {projects.length === 0 ? (
          <div className="no-projects">
            <p>No projects yet. Create your first project!</p>
          </div>
        ) : (
          projects.map(project => (
            <div key={project.id} className="project-card">
              <h3>{project.name}</h3>
              <p>{project.description}</p>
              <div className="project-meta">
                <span>🤖 {project.agents.length} agents</span>
              </div>
              <div className="project-actions">
                <button className="btn-primary">Open</button>
                <button className="btn-secondary">Edit</button>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  )
}

export default Projects
