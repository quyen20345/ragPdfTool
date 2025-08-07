// frontend/src/services/api.js
import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
});

// Document API
export const documentAPI = {
  upload: (formData) => api.post('/api/documents/', formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  }),
  list: () => api.get('/api/documents/'),
  get: (id) => api.get(`/api/documents/${id}`),
  delete: (id) => api.delete(`/api/documents/${id}`)
};

// Chat API
export const chatAPI = {
  createSession: (data) => api.post('/api/chat/sessions', data),
  listSessions: () => api.get('/api/chat/sessions'),
  getSession: (id) => api.get(`/api/chat/sessions/${id}`),
  deleteSession: (id) => api.delete(`/api/chat/sessions/${id}`),
  getMessages: (sessionId) => api.get(`/api/chat/sessions/${sessionId}/messages`),
  query: (data) => api.post('/api/chat/query', data)
};

// Health API
export const healthAPI = {
  check: () => api.get('/health')
};

export default api;
