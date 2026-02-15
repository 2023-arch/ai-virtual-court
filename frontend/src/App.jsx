import { useState } from 'react'
import CaseSubmissionForm from './components/CaseSubmissionForm'
import LiveTrialViewer from './components/LiveTrialViewer'

export default function App() {
  const [trial, setTrial] = useState(null)

  return (
    <main className="container">
      <h1>AI Virtual Court</h1>
      <CaseSubmissionForm onTrialCreated={setTrial} />
      <LiveTrialViewer trial={trial} onTrialUpdate={setTrial} />
    </main>
  )
}
