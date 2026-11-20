// Shared Axios instance for all API calls.
import axios from 'axios'

// Create the api instance with axios at /api
// baseURL comes from VITE_API_URL
const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || '/api',
})

// Attach the stored access token to every outgoing request
// This token proves that the user has access to the api
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

export default api
