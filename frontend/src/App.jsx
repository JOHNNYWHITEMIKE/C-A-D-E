import { useState } from 'react'
import { BrowserRouter as Router, Routes, Route, Link, useLocation } from 'react-router-dom'
import './App.css'
import Dashboard from './components/Dashboard'
import AgentBuilder from './components/AgentBuilder'
import AgentList from './components/AgentList'
import Projects from './components/Projects'
import Documentation from './components/Documentation'
import Community from './components/Community'
import ExecutionHistory from './components/ExecutionHistory'

const NAV_ITEMS = [
  { path: '/', label: 'Dashboard' },
  { path: '/agents', label: 'Agents' },
  { path: '/builder', label: 'Agent Builder' },
  { path: '/projects', label: 'Projects' },
  { path: '/history', label: 'Execution History' },
  { path: '/community', label: 'Community' },
  { path: '/docs', label: 'Documentation' },
]

function NavLink({ path, label }) {
  const location = useLocation()
  const active = location.pathname === path || (path !== '/' && location.pathname.startsWith(path))
  return (
    <Link to={path} className={`nav-item ${active ? 'nav-active' : ''}`}>{label}</Link>
  )
}

function App() {
  const [sidebarOpen, setSidebarOpen] = useState(true)

  return (
    <Router>
      <div className="app">
        <nav className="navbar">
          <div className="navbar-brand">
            <h1>C-A-D-E</h1>
            <p className="subtitle">Community Application Development Environment</p>
          </div>
          <div className="navbar-links">
            <a href="https://github.com/JOHNNYWHITEMIKE/C-A-D-E" target="_blank" rel="noopener noreferrer">
              GitHub
            </a>
          </div>
        </nav>

        <div className="main-container">
          <aside className={`sidebar ${sidebarOpen ? 'open' : 'closed'}`}>
            <button className="sidebar-toggle" onClick={() => setSidebarOpen(!sidebarOpen)}>
              {sidebarOpen ? '◀' : '▶'}
            </button>
            {sidebarOpen && (
              <nav className="sidebar-nav">
                {NAV_ITEMS.map(item => (
                  <NavLink key={item.path} {...item} />
                ))}
              </nav>
            )}
          </aside>

          <main className="content">
            <Routes>
              <Route path="/" element={<Dashboard />} />
              <Route path="/agents" element={<AgentList />} />
              <Route path="/builder" element={<AgentBuilder />} />
              <Route path="/projects" element={<Projects />} />
              <Route path="/history" element={<ExecutionHistory />} />
              <Route path="/community" element={<Community />} />
              <Route path="/docs" element={<Documentation />} />
            </Routes>
          </main>
        </div>
      </div>
    </Router>
  )
}

export default App
