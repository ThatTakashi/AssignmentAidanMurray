// Top navigation bar: shows app name, links, and login/logout state.
import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'

export default function Navbar() {
  const { user, logout } = useAuth()
  const navigate = useNavigate()

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  return (
    <nav style={styles.nav}>
      <Link to="/dashboard" style={styles.brand}>Piki Ora Medical Centre</Link>
      <div style={styles.links}>
        {user ? (
          <>
            <Link to="/dashboard">My Appointments</Link>
            <Link to="/doctors">Book Appointment</Link>
            {user.is_staff && <Link to="/admin">Admin Dashboard</Link>}
            <p>Hello, <span style={styles.user}>{user.username}</span></p>
            <button onClick={handleLogout} style={styles.btn}>Logout</button>
          </>
        ) : (
          <>
            <Link to="/login">Login</Link>
            <Link to="/register">Register</Link>
          </>
        )}
      </div>
    </nav>
  )
}

// Inline styles
const styles = {
  nav: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: '12px 24px',
    background: '#1f3a5f',
    color: '#fff',
  },
  brand: {
    color: '#fff',
    fontWeight: 'bold',
    fontSize: '18px',
    textDecoration: 'none' },
  links: {
    display: 'flex',
    gap: '16px',
    alignItems: 'center' },
  user: { fontStyle: 'italic' },
  btn: {
    padding: '6px 12px',
    border: 'none',
    borderRadius: '100px',
    background: '#c8766e',
    color: '#fff', cursor: 'pointer',
  },
}
