// Administrator dashboard
// Tabs: Doctors (CRUD), Slots (create/delete), Appointments (view/update/cancel).
import { useEffect, useState } from 'react'
import api from '../api'

export default function AdminDashboard() {
  const [tab, setTab] = useState('doctors')
  // Create tabs on the admin dashboard page
  return (
    <div className="container">
      <h2>Admin Dashboard</h2>
      <div className="tabs">
        <button className={tab === 'doctors' ? 'active' : ''} onClick={() => setTab('doctors')}>Doctors</button>
        <button className={tab === 'slots' ? 'active' : ''} onClick={() => setTab('slots')}>Slots</button>
        <button className={tab === 'appointments' ? 'active' : ''} onClick={() => setTab('appointments')}>Appointments</button>
      </div>
      {tab === 'doctors' && <DoctorsTab />}
      {tab === 'slots' && <SlotsTab />}
      {tab === 'appointments' && <AppointmentsTab />}
    </div>
  )
}

// ---------- DOCTORS TAB ----------
function DoctorsTab() {
  const [doctors, setDoctors] = useState([])
  const [form, setForm] = useState({ name: '', speciality: '', email: '', phone: '' })
  const [editingId, setEditingId] = useState(null)
  const [error, setError] = useState('')

  // Load all doctors
  const load = () => api.get('/doctors/').then((r) => setDoctors(r.data)).catch(() => {})
  useEffect(() => { load() }, [])

  const reset = () => { setForm({ name: '', speciality: '', email: '', phone: '' }); setEditingId(null) }

  // Create (POST) or update (PATCH) a doctor
  const save = async (e) => {
    e.preventDefault()
    setError('')
    try {
      if (editingId) {
        await api.patch(`/doctors/${editingId}/`, form)
      } else {
        await api.post('/doctors/', form)
      }
      reset(); load()
    } catch { setError('Could not save doctor.') }
  }

  const edit = (d) => {
    setEditingId(d.id)
    setForm({ name: d.name, speciality: d.speciality, email: d.email, phone: d.phone })
  }

  const remove = async (id) => {
    if (!window.confirm('Delete this doctor and all their slots?')) return
    await api.delete(`/doctors/${id}/`)
    load()
  }

  // Doctor tab content
  return (
    <>
      <div className="card">
        <h3>{editingId ? 'Edit Doctor' : 'Add Doctor'}</h3>
        <form onSubmit={save}>
          <div className="row">
            <div><label>Name</label><input value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} required /></div>
            <div><label>Speciality</label><input value={form.speciality} onChange={(e) => setForm({ ...form, speciality: e.target.value })} required /></div>
          </div>
          <div className="row">
            <div><label>Email</label><input type="email" value={form.email} onChange={(e) => setForm({ ...form, email: e.target.value })} required /></div>
            <div><label>Phone</label><input value={form.phone} onChange={(e) => setForm({ ...form, phone: e.target.value })} required /></div>
          </div>
          {error && <p className="error">{error}</p>}
          <button type="submit">{editingId ? 'Update' : 'Add Doctor'}</button>
          {editingId && <button type="button" onClick={reset} style={{ marginLeft: 8, background: '#888' }}>Cancel</button>}
        </form>
      </div>
      <div className="card">
        <h3>All Doctors</h3>
        <table>
          <thead><tr><th>Name</th><th>Speciality</th><th>Email</th><th>Phone</th><th></th></tr></thead>
          <tbody>
            {doctors.map((d) => (
              <tr key={d.id}>
                <td>Dr. {d.name}</td><td>{d.speciality}</td><td>{d.email}</td><td>{d.phone}</td>
                <td>
                  <button onClick={() => edit(d)} style={{ marginRight: 6 }}>Edit</button>
                  <button className="danger" onClick={() => remove(d.id)}>Delete</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </>
  )
}

// ---------- SLOTS TAB ----------
function SlotsTab() {
  const [doctors, setDoctors] = useState([])
  const [slots, setSlots] = useState([])
  const [form, setForm] = useState({ doctor: '', date: '', start_time: '', end_time: '' })
  const [error, setError] = useState('')

  const load = () => {
    api.get('/doctors/').then((r) => setDoctors(r.data)).catch(() => {})
    api.get('/slots/').then((r) => setSlots(r.data)).catch(() => {})
  }
  useEffect(() => { load() }, [])

  // Create a new appointment slot
  const add = async (e) => {
    e.preventDefault()
    setError('')
    try {
      await api.post('/slots/', { ...form, doctor: Number(form.doctor) })
      setForm({ doctor: '', date: '', start_time: '', end_time: '' })
      load()
    } catch { setError('Could not create slot (check for duplicates).') }
  }

  const remove = async (id) => {
    await api.delete(`/slots/${id}/`)
    load()
  }

  // Slot tab content
  return (
    <>
      <div className="card">
        <h3>Add Appointment Slot</h3>
        <form onSubmit={add}>
          <div className="row">
            <div>
              <label>Doctor</label>
              <select value={form.doctor} onChange={(e) => setForm({ ...form, doctor: e.target.value })} required>
                <option value="">Select...</option>
                {doctors.map((d) => <option key={d.id} value={d.id}>Dr. {d.name}</option>)}
              </select>
            </div>
            <div><label>Date</label><input type="date" value={form.date} onChange={(e) => setForm({ ...form, date: e.target.value })} required /></div>
          </div>
          <div className="row">
            <div><label>Start Time</label><input type="time" value={form.start_time} onChange={(e) => setForm({ ...form, start_time: e.target.value })} required /></div>
            <div><label>End Time</label><input type="time" value={form.end_time} onChange={(e) => setForm({ ...form, end_time: e.target.value })} required /></div>
          </div>
          {error && <p className="error">{error}</p>}
          <button type="submit">Add Slot</button>
        </form>
      </div>
      <div className="card">
        <h3>All Slots</h3>
        <table>
          <thead><tr><th>Doctor</th><th>Date</th><th>Time</th><th>Available</th><th></th></tr></thead>
          <tbody>
            {slots.map((s) => (
              <tr key={s.id}>
                <td>{s.doctor_name}</td><td>{s.date}</td>
                <td>{s.start_time} - {s.end_time}</td>
                <td>{s.is_available ? 'Yes' : 'No'}</td>
                <td><button className="danger" onClick={() => remove(s.id)}>Delete</button></td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </>
  )
}

// ---------- APPOINTMENTS TAB ----------
function AppointmentsTab() {
  const [appointments, setAppointments] = useState([])
  const [error, setError] = useState('')

  // Get all appointments
  const load = () => api.get('/appointments/').then((r) => setAppointments(r.data)).catch(() => {})
  useEffect(() => { load() }, [])

  // Admin can change status or notes on any appointment
  const update = async (id, data) => {
    try {
      await api.patch(`/appointments/${id}/`, data)
      load()
    } catch { setError('Update failed.') }
  }

  const cancel = (id) => update(id, { status: 'cancelled' })

  // Appointment tab content
  return (
    <div className="card">
      <h3>All Appointments</h3>
      {error && <p className="error">{error}</p>}
      <table>
        <thead><tr><th>Patient</th><th>Doctor</th><th>Date</th><th>Time</th><th>Status</th><th>Notes</th><th></th></tr></thead>
        <tbody>
          {appointments.map((a) => (
            <tr key={a.id}>
              <td>{a.patient_username}</td>
              <td>{a.doctor_name}</td>
              <td>{a.slot_date}</td>
              <td>{a.slot_start} - {a.slot_end}</td>
              <td>
                <select
                  value={a.status}
                  onChange={(e) => update(a.id, { status: e.target.value })}
                  style={{ marginBottom: 0, width: 'auto' }}
                >
                  <option value="scheduled">Scheduled</option>
                  <option value="cancelled">Cancelled</option>
                </select>
              </td>
              <td>
                <input
                  defaultValue={a.notes || ''}
                  onBlur={(e) => update(a.id, { notes: e.target.value })}
                  style={{ marginBottom: 0 }}
                />
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
    </div>
  )
}
