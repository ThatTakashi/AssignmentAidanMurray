// AuthContext keeps the logged-in user and JWT tokens in React state
// (and mirrors tokens to localStorage so they survive page refreshes).
import { createContext, useContext, useState, useEffect } from 'react'
import api from '../api'

const AuthContext = createContext(null)

export function AuthProvider({ children }) {
  // user = { id, username, email, is_staff } or null when logged out
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)

  // On first load, check localStorage for a token and fetch /api/me/ to restore the session after a page refresh.
  useEffect(() => {
    const token = localStorage.getItem('access_token')
    if (token) {
      api.get('/me/')
        .then((res) => setUser(res.data))
        .catch(() => {
          // Clear the stored token data if it is expired
          localStorage.removeItem('access_token')
          localStorage.removeItem('refresh_token')
        })
        .finally(() => setLoading(false))
    } else {
      setLoading(false)
    }
  }, [])

  // Login: exchange username/password for JWT tokens, then load user info
  const login = async (username, password) => {
    const res = await api.post('/token/', { username, password })
    localStorage.setItem('access_token', res.data.access)
    localStorage.setItem('refresh_token', res.data.refresh)
    const me = await api.get('/me/')
    setUser(me.data)
    return me.data
  }

  // Register a new patient account, then log the new account in automatically
  const register = async (username, email, password) => {
    await api.post('/register/', { username, email, password })
    return login(username, password)
  }

  // Logout
  // Clear token storage and reset user state
  const logout = () => {
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    setUser(null)
  }

  return (
    <AuthContext.Provider value={{ user, loading, login, register, logout }}>
      {children}
    </AuthContext.Provider>
  )
}

// Allow all components to get user details
export function useAuth() {
  return useContext(AuthContext)
}
