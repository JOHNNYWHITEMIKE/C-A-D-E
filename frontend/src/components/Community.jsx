import { useState, useEffect } from 'react'
import './Community.css'

const BASE = 'http://localhost:8000'

function Community() {
  const [info, setInfo] = useState(null)
  const [members, setMembers] = useState([])
  const [announcements, setAnnouncements] = useState([])
  const [proposals, setProposals] = useState([])

  const [newMember, setNewMember] = useState('')
  const [newAnnouncement, setNewAnnouncement] = useState('')
  const [newProposal, setNewProposal] = useState('')
  const [error, setError] = useState(null)

  useEffect(() => {
    fetchAll()
  }, [])

  const fetchAll = async () => {
    try {
      const [infoRes, membersRes, announcementsRes, proposalsRes] = await Promise.all([
        fetch(`${BASE}/community/info`),
        fetch(`${BASE}/community/members`),
        fetch(`${BASE}/community/announcements`),
        fetch(`${BASE}/community/proposals`),
      ])
      setInfo(await infoRes.json())
      setMembers((await membersRes.json()).members || [])
      setAnnouncements((await announcementsRes.json()).announcements || [])
      setProposals((await proposalsRes.json()).proposals || [])
    } catch (err) {
      setError('Could not load community data')
    }
  }

  const addMember = async (e) => {
    e.preventDefault()
    if (!newMember.trim()) return
    try {
      const res = await fetch(`${BASE}/community/members`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name: newMember.trim() }),
      })
      if (!res.ok) {
        const d = await res.json()
        setError(d.detail)
        return
      }
      const data = await res.json()
      setMembers(data.members)
      setNewMember('')
      setError(null)
      fetchInfo()
    } catch (err) {
      setError(String(err))
    }
  }

  const removeMember = async (name) => {
    try {
      await fetch(`${BASE}/community/members/${encodeURIComponent(name)}`, { method: 'DELETE' })
      setMembers(prev => prev.filter(m => m !== name))
      fetchInfo()
    } catch (err) {
      setError(String(err))
    }
  }

  const postAnnouncement = async (e) => {
    e.preventDefault()
    if (!newAnnouncement.trim()) return
    try {
      const res = await fetch(`${BASE}/community/announcements`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: newAnnouncement.trim() }),
      })
      const data = await res.json()
      setAnnouncements(data.announcements)
      setNewAnnouncement('')
      fetchInfo()
    } catch (err) {
      setError(String(err))
    }
  }

  const submitProposal = async (e) => {
    e.preventDefault()
    if (!newProposal.trim()) return
    try {
      await fetch(`${BASE}/community/proposals`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ description: newProposal.trim() }),
      })
      setNewProposal('')
      const res = await fetch(`${BASE}/community/proposals`)
      setProposals((await res.json()).proposals || [])
      fetchInfo()
    } catch (err) {
      setError(String(err))
    }
  }

  const vote = async (proposalId, voteFor) => {
    try {
      const res = await fetch(`${BASE}/community/proposals/${proposalId}/vote`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ vote_for: voteFor }),
      })
      const data = await res.json()
      setProposals(prev => prev.map(p => p.id === proposalId ? data.proposal : p))
    } catch (err) {
      setError(String(err))
    }
  }

  const fetchInfo = async () => {
    const res = await fetch(`${BASE}/community/info`)
    setInfo(await res.json())
  }

  return (
    <div className="community">
      <h2 className="page-title">Community</h2>

      {error && (
        <div className="community-error">
          {error}
          <button onClick={() => setError(null)}>✕</button>
        </div>
      )}

      {info && (
        <div className="community-info-bar">
          <span>🏛️ <strong>{info.name}</strong></span>
          <span>👥 {info.member_count} members</span>
          <span>📢 {info.announcement_count} announcements</span>
          <span>🗳️ {info.proposal_count} proposals</span>
        </div>
      )}

      <div className="community-grid">

        {/* Members */}
        <div className="community-card">
          <h3>Members</h3>
          <form onSubmit={addMember} className="community-form">
            <input
              type="text"
              placeholder="Add member name…"
              value={newMember}
              onChange={e => setNewMember(e.target.value)}
            />
            <button type="submit">Add</button>
          </form>
          <ul className="member-list">
            {members.length === 0 && <li className="empty">No members yet</li>}
            {members.map(m => (
              <li key={m} className="member-item">
                <span>👤 {m}</span>
                <button className="remove-btn" onClick={() => removeMember(m)}>✕</button>
              </li>
            ))}
          </ul>
        </div>

        {/* Announcements */}
        <div className="community-card">
          <h3>Announcements</h3>
          <form onSubmit={postAnnouncement} className="community-form">
            <input
              type="text"
              placeholder="Post an announcement…"
              value={newAnnouncement}
              onChange={e => setNewAnnouncement(e.target.value)}
            />
            <button type="submit">Post</button>
          </form>
          <ul className="announcement-list">
            {announcements.length === 0 && <li className="empty">No announcements yet</li>}
            {[...announcements].reverse().map((a, i) => (
              <li key={i} className="announcement-item">📢 {a}</li>
            ))}
          </ul>
        </div>

        {/* Proposals */}
        <div className="community-card proposals-card">
          <h3>Proposals</h3>
          <form onSubmit={submitProposal} className="community-form">
            <input
              type="text"
              placeholder="Submit a proposal…"
              value={newProposal}
              onChange={e => setNewProposal(e.target.value)}
            />
            <button type="submit">Submit</button>
          </form>
          <ul className="proposal-list">
            {proposals.length === 0 && <li className="empty">No proposals yet</li>}
            {proposals.map(p => (
              <li key={p.id} className="proposal-item">
                <div className="proposal-description">🗳️ {p.description}</div>
                <div className="proposal-votes">
                  <button className="vote-btn for" onClick={() => vote(p.id, true)}>
                    👍 {p.votes_for}
                  </button>
                  <button className="vote-btn against" onClick={() => vote(p.id, false)}>
                    👎 {p.votes_against}
                  </button>
                </div>
              </li>
            ))}
          </ul>
        </div>

      </div>
    </div>
  )
}

export default Community
