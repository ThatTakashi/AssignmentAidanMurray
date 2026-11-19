// Shared Axios instance for all API calls.
// - baseURL comes from VITE_API_URL (set on Render) or defaults to
//   the local Django dev server through the Vite proxy.
// - An interceptor automatically attaches the JWT access token
//   to every request, so pages don't have to handle auth headers.
import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || '/api',
})

// Attach the stored access token to every outgoing request
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

export default api
