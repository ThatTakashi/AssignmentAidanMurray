// BrowseDoctors page
import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import api from '../api'

export default function BrowseDoctors() {
  const [doctors, setDoctors] = useState([])
  const [selectedDoctor, setSelectedDoctor] = useState(null)
  const [slots, setSlots] = useState([])
  const [message, setMessage] = useState('')
  const navigate = useNavigate()

  // Load all doctors on page load
  useEffect(() => {
    api.get('/doctors/').then((res) => setDoctors(res.data)).catch(() => {})
  }, [])

  // When a doctor is clicked, get their available slots
  const pickDoctor = (doctor) => {
    setSelectedDoctor(doctor)
    setMessage('')
    api.get('/slots/', { params: { doctor: doctor.id, is_available: 'true' } })
      .then((res) => setSlots(res.data))
      .catch(() => setSlots([]))
  }

  // Book the chosen slot using /api/appointments/{ slot: id }
  const book = async (slotId) => {
    setMessage('')
    try {
      // Try to create a booking for the selected slot
      await api.post('/appointments/', { slot: slotId })
      setMessage('Appointment booked successfully!')
      setTimeout(() => navigate('/dashboard'), 800)
    } catch (err) {
      // Display error to user if there is an issue booking the slot
      setMessage(err.response?.data?.detail || 'Could not book this slot.')
    }
  }

  // Actual page content
  return (
    <div className="container">
      <h2>Book an Appointment</h2>
      {message && <p className="success-msg">{message}</p>}

      {/* Doctor list */}
      <div className="card">
        <h3>1. Choose a Doctor</h3>
        <div className="row">
          {doctors.map((d) => (
            <button
              key={d.id}
              onClick={() => pickDoctor(d)}
              style={selectedDoctor?.id === d.id ? { background: '#27ae60' } : {}}
            >
              Dr. {d.name} - {d.speciality}
            </button>
          ))}
          {doctors.length === 0 && <p className="muted">No doctors available.</p>}
        </div>
      </div>

      {/* Available slots for the selected doctor */}
      {selectedDoctor && (
        <div className="card">
          <h3>2. Choose a Time Slot - Dr. {selectedDoctor.name}</h3>
          {slots.length === 0 ? (
            <p className="muted">No available slots.</p>
          ) : (
            <table>
              <thead><tr><th>Date</th><th>Start</th><th>End</th><th></th></tr></thead>
              <tbody>
              {/* Show all of the time slots for the selected doctor in a table */}
                {slots.map((s) => (
                  <tr key={s.id}>
                    <td>{s.date}</td>
                    <td>{s.start_time}</td>
                    <td>{s.end_time}</td>
                    <td><button className="success" onClick={() => book(s.id)}>Book</button></td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>
      )}
    </div>
  )
}
