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
  
  getPaginatedPosts(page = 1, pageSize = 3) {
    return api.get('/posts/paginated', { params: { page, page_size: pageSize } })
  },
  
  searchPosts(keyword, page = 1) {
    return api.get('/posts/search', { params: { keyword, page } })
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
