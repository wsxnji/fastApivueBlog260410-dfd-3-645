<template>
  <div class="home">
    <div class="search-section">
      <div class="search-box">
        <input
          v-model="searchQuery"
          type="text"
          placeholder="搜索文章（标题、内容、标签）..."
          @keyup.enter="handleSearch"
          class="search-input"
        />
        <button @click="handleSearch" class="search-btn">搜索</button>
        <button @click="clearSearch" class="clear-btn">清除</button>
      </div>
    </div>

    <div class="filter-section">
      <div class="filter-group">
        <label>分类：</label>
        <select v-model="selectedCategory" @change="handleFilter" class="filter-select">
          <option value="">全部</option>
          <option v-for="cat in categories" :key="cat" :value="cat">{{ cat }}</option>
        </select>
      </div>
      <div class="filter-group">
        <label>标签：</label>
        <select v-model="selectedTag" @change="handleFilter" class="filter-select">
          <option value="">全部</option>
          <option v-for="tag in tags" :key="tag" :value="tag">{{ tag }}</option>
        </select>
      </div>
    </div>

    <h1 class="page-title">最新文章</h1>
    <div v-if="loading" class="loading">加载中...</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <div v-else class="posts-grid">
      <div v-for="post in posts" :key="post.id" class="post-card">
        <h2 class="post-title">
          <router-link :to="`/post/${post.id}`">{{ post.title }}</router-link>
        </h2>
        <div class="post-tags">
          <span v-if="post.category" class="category-badge">{{ post.category }}</span>
          <span v-for="tag in parseTags(post.tags)" :key="tag" class="tag-badge">{{ tag }}</span>
        </div>
        <p class="post-summary">{{ post.summary || post.content.substring(0, 150) + '...' }}</p>
        <div class="post-meta">
          <span class="post-date">{{ formatDate(post.created_at) }}</span>
        </div>
      </div>
    </div>
    <div v-if="posts.length === 0 && !loading" class="no-posts">
      <p>暂无文章</p>
    </div>

    <div v-if="totalPages > 1" class="pagination">
      <button 
        :disabled="currentPage === 1" 
        @click="changePage(currentPage - 1)"
        class="page-btn"
      >
        上一页
      </button>
      <span class="page-info">第 {{ currentPage }} / {{ totalPages }} 页</span>
      <button 
        :disabled="currentPage === totalPages" 
        @click="changePage(currentPage + 1)"
        class="page-btn"
      >
        下一页
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { postApi } from '../api'

const posts = ref([])
const loading = ref(true)
const error = ref(null)
const currentPage = ref(1)
const totalPages = ref(1)
const total = ref(0)
const pageSize = 3

const searchQuery = ref('')
const selectedCategory = ref('')
const selectedTag = ref('')

const categories = ['前端', '后端', '数据库', '其它']
const tags = ['JS', 'Python', 'Java', 'Node', '数据库']

const formatDate = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

const parseTags = (tagsStr) => {
  if (!tagsStr) return []
  return tagsStr.split(',').map(t => t.trim()).filter(t => t)
}

const loadPosts = async () => {
  try {
    loading.value = true
    error.value = null
    const params = {
      page: currentPage.value,
      page_size: pageSize
    }
    if (searchQuery.value) {
      params.search = searchQuery.value
    }
    if (selectedCategory.value) {
      params.category = selectedCategory.value
    }
    if (selectedTag.value) {
      params.tag = selectedTag.value
    }
    const response = await postApi.getPosts(params)
    posts.value = response.data.posts
    total.value = response.data.total
    totalPages.value = response.data.total_pages
  } catch (err) {
    error.value = '加载文章失败，请稍后重试'
    console.error(err)
  } finally {
    loading.value = false
  }
}

const handleSearch = () => {
  currentPage.value = 1
  loadPosts()
}

const clearSearch = () => {
  searchQuery.value = ''
  selectedCategory.value = ''
  selectedTag.value = ''
  currentPage.value = 1
  loadPosts()
}

const handleFilter = () => {
  currentPage.value = 1
  loadPosts()
}

const changePage = (page) => {
  currentPage.value = page
  loadPosts()
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

onMounted(() => {
  loadPosts()
})
</script>

<style scoped>
.search-section {
  margin-bottom: 2rem;
}

.search-box {
  display: flex;
  gap: 0.5rem;
  max-width: 600px;
  margin: 0 auto;
}

.search-input {
  flex: 1;
  padding: 0.75rem 1rem;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  font-size: 1rem;
  transition: border-color 0.3s;
}

.search-input:focus {
  outline: none;
  border-color: #3498db;
}

.search-btn, .clear-btn {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 1rem;
  transition: background-color 0.3s;
}

.search-btn {
  background-color: #3498db;
  color: white;
}

.search-btn:hover {
  background-color: #2980b9;
}

.clear-btn {
  background-color: #95a5a6;
  color: white;
}

.clear-btn:hover {
  background-color: #7f8c8d;
}

.filter-section {
  display: flex;
  gap: 2rem;
  margin-bottom: 2rem;
  justify-content: center;
  flex-wrap: wrap;
}

.filter-group {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.filter-group label {
  font-weight: 600;
  color: #2c3e50;
}

.filter-select {
  padding: 0.5rem 1rem;
  border: 2px solid #e0e0e0;
  border-radius: 6px;
  font-size: 0.9rem;
  cursor: pointer;
}

.filter-select:focus {
  outline: none;
  border-color: #3498db;
}

.page-title {
  font-size: 2rem;
  margin-bottom: 2rem;
  color: #2c3e50;
}

.posts-grid {
  display: grid;
  gap: 2rem;
}

.post-card {
  background: #fff;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  transition: transform 0.3s, box-shadow 0.3s;
}

.post-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}

.post-title {
  font-size: 1.5rem;
  margin-bottom: 0.75rem;
}

.post-title a {
  color: #2c3e50;
  text-decoration: none;
  transition: color 0.3s;
}

.post-title a:hover {
  color: #3498db;
}

.post-tags {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
  margin-bottom: 1rem;
}

.category-badge {
  background-color: #3498db;
  color: white;
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.8rem;
}

.tag-badge {
  background-color: #e8f4f8;
  color: #2980b9;
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.8rem;
}

.post-summary {
  color: #666;
  line-height: 1.6;
  margin-bottom: 1rem;
}

.post-meta {
  color: #999;
  font-size: 0.9rem;
}

.loading, .error, .no-posts {
  text-align: center;
  padding: 3rem;
  color: #666;
}

.error {
  color: #e74c3c;
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 1rem;
  margin-top: 2rem;
}

.page-btn {
  padding: 0.5rem 1.5rem;
  border: 2px solid #3498db;
  background-color: white;
  color: #3498db;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.3s;
}

.page-btn:hover:not(:disabled) {
  background-color: #3498db;
  color: white;
}

.page-btn:disabled {
  border-color: #ccc;
  color: #ccc;
  cursor: not-allowed;
}

.page-info {
  color: #666;
  font-size: 0.9rem;
}
</style>
