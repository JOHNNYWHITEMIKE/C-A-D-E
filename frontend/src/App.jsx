import { useState } from 'react'
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom'
import './App.css'
import Dashboard from './components/Dashboard'
import AgentBuilder from './components/AgentBuilder'
import AgentList from './components/AgentList'
import Projects from './components/Projects'
import Documentation from './components/Documentation'

function App() {
  const [sidebarOpen, setSidebarOpen] = useState(true)

  return (
    <Router>
      <div className="app">
        <nav className="navbar">
          <div className="navbar-brand">
            <h1>🤖 C-A-D-E</h1>
            <p className="subtitle">Community Application Development Environment</p>
          </div>
          <div className="navbar-links">
            <a href="https://github.com/jim-schwoebel/awesome_ai_agents" target="_blank" rel="noopener noreferrer">
              AI Agents Resources
            </a>
          </div>
        </nav>

        <div className="main-container">
          <aside className={`sidebar ${sidebarOpen ? 'open' : 'closed'}`}>
            <button 
              className="sidebar-toggle"
              onClick={() => setSidebarOpen(!sidebarOpen)}
            >
              {sidebarOpen ? '◀' : '▶'}
            </button>
            {sidebarOpen && (
              <nav className="sidebar-nav">
                <Link to="/" className="nav-item">📊 Dashboard</Link>
                <Link to="/agents" className="nav-item">🤖 Agents</Link>
                <Link to="/builder" className="nav-item">🔧 Agent Builder</Link>
                <Link to="/projects" className="nav-item">📁 Projects</Link>
                <Link to="/docs" className="nav-item">📚 Documentation</Link>
              </nav>
            )}
          </aside>

          <main className="content">
            <Routes>
              <Route path="/" element={<Dashboard />} />
              <Route path="/agents" element={<AgentList />} />
              <Route path="/builder" element={<AgentBuilder />} />
              <Route path="/projects" element={<Projects />} />
              <Route path="/docs" element={<Documentation />} />
            </Routes>
          </main>
        </div>
      </div>
    </Router>
  )
}

export default App
