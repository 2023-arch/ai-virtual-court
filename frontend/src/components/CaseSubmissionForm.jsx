import { useState } from 'react'

const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8000'

const defaultCase = {
  case_id: 'AVC-2026-001',
  case_name: 'Acme Corp v. ByteWorks LLC',
  case_type: 'Breach of Contract',
  currency: 'USD',
  dispute_amount: 85000,
  max_claim_amount: 100000,
  burden_of_proof: 'Preponderance of the evidence',
  applicable_laws: ['State contract law'],
  remedies_available: ['Compensatory damages'],
  jurisdiction: {
    court_level: 'Superior Court',
    state_province: 'California',
    country: 'USA'
  },
  plaintiff: {
    name: 'Acme Corp',
    brief_description: 'Acme hired ByteWorks for software delivery by May 1, 2025.',
    legal_basis: 'Material breach of contract obligations.',
    evidence_summary: 'Contract, invoice history, and QA reports.',
    relief_sought: ['Compensatory damages'],
    key_timeline: [{ date: '2025-01-10', event: 'SOW executed' }]
  },
  defendant: {
    name: 'ByteWorks LLC',
    brief_description: 'Acme changed scope repeatedly.',
    defense_statement: 'Delays were plaintiff-caused and excused.',
    evidence_summary: 'Change logs and status emails.'
  }
}

export default function CaseSubmissionForm({ onTrialCreated }) {
  const [payload, setPayload] = useState(JSON.stringify(defaultCase, null, 2))
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    setLoading(true)
    try {
      const case_data = JSON.parse(payload)
      const res = await fetch(`${API_BASE}/trial/start`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ case_data, enable_research: false })
      })
      if (!res.ok) {
        throw new Error(`Request failed with status ${res.status}`)
      }
      const data = await res.json()
      onTrialCreated(data)
    } catch (err) {
      setError(String(err.message || err))
    } finally {
      setLoading(false)
    }
  }

  return (
    <section className="card">
      <h2>1) Submit Case</h2>
      <form onSubmit={handleSubmit}>
        <textarea value={payload} onChange={(e) => setPayload(e.target.value)} />
        <div style={{ marginTop: 8 }}>
          <button type="submit" disabled={loading}>{loading ? 'Starting...' : 'Start Trial'}</button>
        </div>
      </form>
      {error && <p style={{ color: 'crimson' }}>{error}</p>}
    </section>
  )
}
