import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  headers: {
    'Content-Type': 'application/json',
  },
})

export const postApi = {
  getPosts(params) {
    return api.get('/posts', { params })
  },
  
  getPost(id) {
    return api.get(`/posts/${id}`)
  },
  
  createPost(data) {
    return api.post('/posts', data)
  },
  
  updatePost(id, data) {
    return api.put(`/posts/${id}`, data)
  },
  
  deletePost(id) {
    return api.delete(`/posts/${id}`)
  }
}
