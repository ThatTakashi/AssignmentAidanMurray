// Login page: posts credentials to /api/token/ via AuthContext.login()
import { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'

export default function Login() {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const { login } = useAuth()
  const navigate = useNavigate()

  // Logic for when the submit button is clicked
  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    try {
      const user = await login(username, password)
      // Page redirect
      // Staff go to the admin dashboard, patients to their dashboard
      navigate(user.is_staff ? '/admin' : '/dashboard')
    } catch (err) {
      // 401 = wrong credentials; anything else (404, network, CORS) shows the status
      setError(
        err.response?.status === 401
          ? 'Invalid username or password.'
          : `Login failed (error ${err.response?.status || 'network'}). Check the API URL.`
      )
    }
  }

  // Actual page content, includes the login form and link to the register page
  return (
    <div className="container" style={{ maxWidth: 400 }}>
      <div className="card">
        <h2>Login</h2>
        {/* Login form elements */}
        <form onSubmit={handleSubmit}>
          <label>Username</label>
          <input value={username} onChange={(e) => setUsername(e.target.value)} required />
          <label>Password</label>
          <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} required />
          {/* Error element (hidden by default) */}
          {error && <p className="error">{error}</p>}
          <button type="submit" style={{ width: '100%' }}>Login</button>
        </form>
        <p className="muted">No account? <Link to="/register">Register here >></Link></p>
      </div>
    </div>
  )
}
