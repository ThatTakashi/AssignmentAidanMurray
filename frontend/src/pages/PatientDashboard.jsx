// Patient dashboard: lists the logged-in patient's appointments.
// Patients can update notes and cancel their own scheduled appointments.
import { useEffect, useState } from 'react'
import api from '../api'

export default function PatientDashboard() {
  const [appointments, setAppointments] = useState([])
  const [error, setError] = useState('')

  // Load appointments from GET /api/appointments/
  // Each user can only see their appointments
  const load = () => {
    api.get('/appointments/')
      .then((res) => setAppointments(res.data))
      .catch(() => setError('Failed to load appointments.'))
  }

  useEffect(() => { load() }, [])

  // Cancel an appointment by changing status = 'cancelled'
  const cancel = async (id) => {
    try {
      await api.patch(`/appointments/${id}/`, { status: 'cancelled' })
      load()
    } catch {
      setError('Could not cancel appointment.')
    }
  }

  // Update the notes field on an appointment
  const saveNotes = async (id, notes) => {
    try {
      await api.patch(`/appointments/${id}/`, { notes })
      load()
    } catch {
      setError('Could not update notes.')
    }
  }

  return (
    <div className="container">
      <h2>My Appointments</h2>
      {error && <p className="error">{error}</p>}
      <div className="card">
        {/* Check if the user has appointments (if not show a message prompting them to make a booking) */}
        {appointments.length === 0 ? (
          <p className="muted">No appointments yet. <a href="/doctors">Book one here</a>.</p>
        ) : (
          <table>
            <thead>
              <tr><th>Doctor</th><th>Date</th><th>Time</th><th>Status</th><th>Notes</th><th></th></tr>
            </thead>
            <tbody>
              {appointments.map((a) => (
                <tr key={a.id}>
                  <td>{a.doctor_name}</td>
                  <td>{a.slot_date}</td>
                  <td>{a.slot_start} - {a.slot_end}</td>
                  <td><span className={`badge ${a.status}`}>{a.status}</span></td>
                  <td>
                    {a.status === 'scheduled' ? (
                      <input
                        defaultValue={a.notes || ''}
                        placeholder="Add notes..."
                        onBlur={(e) => saveNotes(a.id, e.target.value)}
                        style={{ marginBottom: 0 }}
                      />
                    ) : (a.notes || '-')}
                  </td>
                  <td>
                    {a.status === 'scheduled' && (
                      <button className="danger" onClick={() => cancel(a.id)}>Cancel</button>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  )
}
