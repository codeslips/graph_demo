import axios from 'axios'
import type { AxiosInstance, AxiosRequestConfig } from 'axios'

const request: AxiosInstance = axios.create({
  baseURL: '/api/v1',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// Request interceptor
request.interceptors.request.use(
  (config) => {
    // Add auth token or other headers here if needed
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor
request.interceptors.response.use(
  (response) => {
    return response.data
  },
  (error) => {
    // Handle errors globally here
    console.error('API Error:', error)
    return Promise.reject(error)
  }
)

export default request

