// Root component: defines all client-side routes.
import { Routes, Route, Navigate } from 'react-router-dom'
import { useAuth } from './context/AuthContext'
import Navbar from './components/Navbar.jsx'
import Login from './pages/Login.jsx'
import Register from './pages/Register.jsx'
import PatientDashboard from './pages/PatientDashboard.jsx'
import BrowseDoctors from './pages/BrowseDoctors.jsx'
import AdminDashboard from './pages/AdminDashboard.jsx'

// ProtectedRoute sends unauthenticated users to /login
function ProtectedRoute({ children }) {
  const { user, loading } = useAuth()
  if (loading) return <p style={{ padding: 20 }}>Loading...</p>
  if (!user) return <Navigate to="/login" replace />
  return children
}

// AdminRoute additionally requires is_staff
function AdminRoute({ children }) {
  const { user } = useAuth()
  if (!user?.is_staff) return <Navigate to="/dashboard" replace />
  return children
}

export default function App() {
  return (
    <>
      <Navbar />
      <Routes>
        {/* Public pages */}
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />

        {/* Patient pages (any logged-in user) */}
        <Route path="/dashboard" element={<ProtectedRoute><PatientDashboard /></ProtectedRoute>} />
        <Route path="/doctors" element={<ProtectedRoute><BrowseDoctors /></ProtectedRoute>} />

        {/* Administrator dashboard (staff only) */}
        <Route path="/admin" element={<ProtectedRoute><AdminRoute><AdminDashboard /></AdminRoute></ProtectedRoute>} />

        {/* Default redirect */}
        <Route path="*" element={<Navigate to="/dashboard" replace />} />
      </Routes>
    </>
  )
}
