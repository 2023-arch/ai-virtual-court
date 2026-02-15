const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8000'

export default function LiveTrialViewer({ trial, onTrialUpdate }) {
  const handleStep = async () => {
    const res = await fetch(`${API_BASE}/trial/step`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ trial_id: trial.trial_id })
    })
    if (!res.ok) {
      return
    }
    const data = await res.json()
    onTrialUpdate(data)
  }

  return (
    <section className="card">
      <h2>2) Live Trial Viewer</h2>
      {!trial && <p>Start a trial to view proceedings.</p>}
      {trial && (
        <>
          <p><strong>Trial ID:</strong> {trial.trial_id}</p>
          <p><strong>Case ID:</strong> {trial.case_id}</p>
          <button onClick={handleStep} disabled={trial.complete}>
            {trial.complete ? 'Trial Complete' : 'Advance Trial'}
          </button>
          <div style={{ marginTop: 12 }}>
            {trial.transcript.map((entry, idx) => (
              <div key={idx} className="card" style={{ marginBottom: 8 }}>
                <strong>{entry.role}</strong>
                <pre>{entry.message}</pre>
              </div>
            ))}
          </div>
        </>
      )}
    </section>
  )
}
