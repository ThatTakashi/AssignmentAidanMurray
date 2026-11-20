// Register page: creates a patient account via /api/register/
import { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'

export default function Register() {
  const [username, setUsername] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const { register } = useAuth()
  const navigate = useNavigate()

  // Logic to handle clicking the submit button
  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    try {
      await register(username, email, password)
      // Handles page redirection
      // All users created here are not admins, thus no admin dashboard logic is needed
      navigate('/dashboard')
    } catch (err) {
      // Show the first validation error returned by the API
      const msgs = err.response?.data
      setError(typeof msgs === 'object' ? JSON.stringify(msgs) : 'Registration failed.')
    }
  }


  // Actual page content, includes the registration form and link to the login page
  return (
    <div className="container" style={{ maxWidth: 400 }}>
      <div className="card">
        <h2>Register</h2>
        {/* Registration form elements */}
        <form onSubmit={handleSubmit}>
          <label>Username</label>
          <input value={username} onChange={(e) => setUsername(e.target.value)} required />
          <label>Email</label>
          <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} required />
          <label>Password (min 8 chars)</label>
          <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} minLength={8} required />
          {/* Error element (hidden by default) */}
          {error && <p className="error">{error}</p>}
          <button type="submit" style={{ width: '100%' }}>Register</button>
        </form>
        <p className="muted">Already registered? <Link to="/login">Login here >></Link></p>
      </div>
    </div>
  )
}
