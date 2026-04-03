import { useState, useEffect } from 'react'
import { useNavigate, useSearchParams } from 'react-router-dom'
import Editor from '@monaco-editor/react'
import './AgentBuilder.css'

const BASE = 'http://localhost:8000'

function AgentBuilder() {
  const navigate = useNavigate()
  const [searchParams] = useSearchParams()
  const editId = searchParams.get('id')
  const isEdit = Boolean(editId)

  const [agentData, setAgentData] = useState({
    id: '',
    name: '',
    description: '',
    category: 'Autonomous Agents',
    framework: 'Custom',
    language: 'Python',
    code: '# Your agent code here\n\ndef main():\n    print("Hello from C-A-D-E!")\n\nif __name__ == "__main__":\n    main()',
    docker_image: '',
  })
  const [categories, setCategories] = useState([])
  const [frameworks, setFrameworks] = useState([])
  const [saving, setSaving] = useState(false)
  const [error, setError] = useState(null)

  useEffect(() => {
    fetchCategories()
    fetchFrameworks()
    if (isEdit) fetchAgent(editId)
  }, [editId])

  const fetchCategories = async () => {
    try {
      const res = await fetch(`${BASE}/categories`)
      const data = await res.json()
      setCategories(data.categories || [])
    } catch (e) { /* ignore */ }
  }

  const fetchFrameworks = async () => {
    try {
      const res = await fetch(`${BASE}/frameworks`)
      const data = await res.json()
      setFrameworks(data.frameworks || [])
    } catch (e) { /* ignore */ }
  }

  const fetchAgent = async (id) => {
    try {
      const res = await fetch(`${BASE}/agents/${id}`)
      if (!res.ok) { setError('Agent not found'); return }
      const data = await res.json()
      const a = data.agent
      setAgentData({
        id: a.id,
        name: a.name,
        description: a.description,
        category: a.category,
        framework: a.framework,
        language: a.language,
        code: a.code || '',
        docker_image: a.docker_image || '',
      })
    } catch (e) {
      setError('Failed to load agent')
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setSaving(true)
    setError(null)
    try {
      let res
      if (isEdit) {
        res = await fetch(`${BASE}/agents/${editId}`, {
          method: 'PUT',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(agentData),
        })
      } else {
        const payload = { ...agentData, id: agentData.id || undefined }
        res = await fetch(`${BASE}/agents`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload),
        })
      }
      if (res.ok) {
        navigate('/agents')
      } else {
        const d = await res.json()
        setError(d.detail || 'Save failed')
      }
    } catch (e) {
      setError(String(e))
    } finally {
      setSaving(false)
    }
  }

  const templates = {
    Python: '# Your agent code here\n\ndef main():\n    print("Hello from C-A-D-E!")\n\nif __name__ == "__main__":\n    main()',
    JavaScript: '// Your agent code here\n\nfunction main() {\n    console.log("Hello from C-A-D-E!");\n}\n\nmain();',
    TypeScript: '// Your agent code here\n\nfunction main(): void {\n    console.log("Hello from C-A-D-E!");\n}\n\nmain();',
  }

  const loadTemplate = (lang) => {
    setAgentData({ ...agentData, language: lang, code: templates[lang] || templates.Python })
  }

  return (
    <div className="agent-builder">
      <h2 className="page-title">{isEdit ? 'Edit Agent' : 'Agent Builder'}</h2>

      {error && <div className="builder-error">{error}</div>}

      <div className="builder-container">
        <form onSubmit={handleSubmit} className="agent-form">
          <div className="form-section">
            <h3>Basic Information</h3>

            {!isEdit && (
              <div className="form-group">
                <label>Agent ID (optional – auto-generated if blank)</label>
                <input
                  type="text"
                  value={agentData.id}
                  onChange={e => setAgentData({ ...agentData, id: e.target.value })}
                  placeholder="my-agent-01"
                />
              </div>
            )}

            <div className="form-group">
              <label>Agent Name *</label>
              <input
                type="text"
                value={agentData.name}
                onChange={e => setAgentData({ ...agentData, name: e.target.value })}
                placeholder="My Awesome Agent"
                required
              />
            </div>

            <div className="form-group">
              <label>Description *</label>
              <textarea
                value={agentData.description}
                onChange={e => setAgentData({ ...agentData, description: e.target.value })}
                placeholder="Describe what your agent does…"
                rows="3"
                required
              />
            </div>

            <div className="form-row">
              <div className="form-group">
                <label>Category</label>
                <select
                  value={agentData.category}
                  onChange={e => setAgentData({ ...agentData, category: e.target.value })}
                >
                  {categories.map(cat => <option key={cat} value={cat}>{cat}</option>)}
                </select>
              </div>
              <div className="form-group">
                <label>Framework</label>
                <select
                  value={agentData.framework}
                  onChange={e => setAgentData({ ...agentData, framework: e.target.value })}
                >
                  {frameworks.map(fw => <option key={fw} value={fw}>{fw}</option>)}
                </select>
              </div>
            </div>

            <div className="form-group">
              <label>Docker Image (optional – for container execution)</label>
              <input
                type="text"
                value={agentData.docker_image}
                onChange={e => setAgentData({ ...agentData, docker_image: e.target.value })}
                placeholder="ghcr.io/org/my-agent:latest"
              />
            </div>

            <div className="form-group">
              <label>Programming Language</label>
              <div className="language-buttons">
                {Object.keys(templates).map(lang => (
                  <button
                    key={lang}
                    type="button"
                    className={agentData.language === lang ? 'active' : ''}
                    onClick={() => loadTemplate(lang)}
                  >{lang}</button>
                ))}
              </div>
            </div>
          </div>

          <div className="form-section">
            <h3>Code Editor</h3>
            <div className="editor-container">
              <Editor
                height="400px"
                language={agentData.language.toLowerCase()}
                theme="vs-dark"
                value={agentData.code}
                onChange={v => setAgentData({ ...agentData, code: v || '' })}
                options={{ minimap: { enabled: false }, fontSize: 14, lineNumbers: 'on', scrollBeyondLastLine: false, automaticLayout: true }}
              />
            </div>
          </div>

          <div className="form-actions">
            <button type="submit" className="btn-primary" disabled={saving}>
              {saving ? 'Saving…' : isEdit ? 'Save Changes' : 'Create Agent'}
            </button>
            <button type="button" className="btn-secondary" onClick={() => navigate('/agents')}>
              Cancel
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}

export default AgentBuilder
  const [agentData, setAgentData] = useState({
    id: '',
    name: '',
    description: '',
    category: 'Autonomous Agents',
    framework: 'LangChain',
    language: 'Python',
    code: '# Your agent code here\n\ndef main():\n    print("Hello from C-A-D-E!")\n    pass\n\nif __name__ == "__main__":\n    main()'
  })

  const [categories, setCategories] = useState([])
  const [frameworks, setFrameworks] = useState([])

  useEffect(() => {
    fetchCategories()
    fetchFrameworks()
  }, [])

  const fetchCategories = async () => {
    try {
      const response = await fetch('http://localhost:8000/categories')
      const data = await response.json()
      setCategories(data.categories || [])
    } catch (error) {
      console.error('Error fetching categories:', error)
    }
  }

  const fetchFrameworks = async () => {
    try {
      const response = await fetch('http://localhost:8000/frameworks')
      const data = await response.json()
      setFrameworks(data.frameworks || [])
    } catch (error) {
      console.error('Error fetching frameworks:', error)
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    
    // Generate a more robust ID using timestamp + random component
    // For production, consider using UUID library
    const agentId = agentData.id || `agent_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`
    
    const agent = {
      ...agentData,
      id: agentId
    }

    try {
      const response = await fetch('http://localhost:8000/agents', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(agent),
      })

      if (response.ok) {
        alert('Agent created successfully!')
        window.location.href = '/agents'
      } else {
        alert('Failed to create agent')
      }
    } catch (error) {
      console.error('Error creating agent:', error)
      alert('Error creating agent')
    }
  }

  const handleCodeChange = (value) => {
    setAgentData({ ...agentData, code: value })
  }

  const templates = {
    'Python': '# Your agent code here\n\ndef main():\n    print("Hello from C-A-D-E!")\n    pass\n\nif __name__ == "__main__":\n    main()',
    'JavaScript': '// Your agent code here\n\nfunction main() {\n    console.log("Hello from C-A-D-E!");\n}\n\nmain();',
    'TypeScript': '// Your agent code here\n\nfunction main(): void {\n    console.log("Hello from C-A-D-E!");\n}\n\nmain();'
  }

  const loadTemplate = (lang) => {
    setAgentData({ 
      ...agentData, 
      language: lang,
      code: templates[lang] || templates['Python']
    })
  }

  return (
    <div className="agent-builder">
      <h2 className="page-title">Agent Builder</h2>

      <div className="builder-container">
        <form onSubmit={handleSubmit} className="agent-form">
          <div className="form-section">
            <h3>Basic Information</h3>
            
            <div className="form-group">
              <label>Agent Name</label>
              <input
                type="text"
                value={agentData.name}
                onChange={(e) => setAgentData({ ...agentData, name: e.target.value })}
                placeholder="My Awesome Agent"
                required
              />
            </div>

            <div className="form-group">
              <label>Description</label>
              <textarea
                value={agentData.description}
                onChange={(e) => setAgentData({ ...agentData, description: e.target.value })}
                placeholder="Describe what your agent does..."
                rows="3"
                required
              />
            </div>

            <div className="form-row">
              <div className="form-group">
                <label>Category</label>
                <select
                  value={agentData.category}
                  onChange={(e) => setAgentData({ ...agentData, category: e.target.value })}
                >
                  {categories.map(cat => (
                    <option key={cat} value={cat}>{cat}</option>
                  ))}
                </select>
              </div>

              <div className="form-group">
                <label>Framework</label>
                <select
                  value={agentData.framework}
                  onChange={(e) => setAgentData({ ...agentData, framework: e.target.value })}
                >
                  {frameworks.map(fw => (
                    <option key={fw} value={fw}>{fw}</option>
                  ))}
                </select>
              </div>
            </div>

            <div className="form-group">
              <label>Programming Language</label>
              <div className="language-buttons">
                {Object.keys(templates).map(lang => (
                  <button
                    key={lang}
                    type="button"
                    className={agentData.language === lang ? 'active' : ''}
                    onClick={() => loadTemplate(lang)}
                  >
                    {lang}
                  </button>
                ))}
              </div>
            </div>
          </div>

          <div className="form-section">
            <h3>Code Editor</h3>
            <div className="editor-container">
              <Editor
                height="400px"
                language={agentData.language.toLowerCase()}
                theme="vs-dark"
                value={agentData.code}
                onChange={handleCodeChange}
                options={{
                  minimap: { enabled: false },
                  fontSize: 14,
                  lineNumbers: 'on',
                  scrollBeyondLastLine: false,
                  automaticLayout: true,
                }}
              />
            </div>
          </div>

          <div className="form-actions">
            <button type="submit" className="btn-primary">
              Create Agent
            </button>
            <button type="button" className="btn-secondary" onClick={() => window.location.href = '/agents'}>
              Cancel
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}

export default AgentBuilder
