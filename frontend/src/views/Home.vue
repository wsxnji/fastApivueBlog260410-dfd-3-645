<template>
  <div class="home">
    <div class="search-section">
      <h1 class="page-title">技术博客</h1>
      <div class="search-box">
        <input
          v-model="searchKeyword"
          type="text"
          placeholder="搜索文章标题、内容或标签..."
          @keyup.enter="handleSearch"
        />
        <button @click="handleSearch" class="search-btn">搜索</button>
      </div>
    </div>
    
    <div v-if="loading" class="loading">加载中...</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <div v-else class="posts-grid">
      <div v-for="post in posts" :key="post.id" class="post-card">
        <div class="post-category" :class="getCategoryClass(post.category)">{{ post.category || '未分类' }}</div>
        <h2 class="post-title">
          <router-link :to="`/post/${post.id}`">{{ post.title }}</router-link>
        </h2>
        <p class="post-summary">{{ post.summary || post.content.substring(0, 150) + '...' }}</p>
        <div class="post-tags">
          <span v-for="tag in getTags(post.tags)" :key="tag" class="tag">{{ tag }}</span>
        </div>
        <div class="post-meta">
          <span class="post-date">{{ formatDate(post.created_at) }}</span>
        </div>
      </div>
    </div>
    
    <div v-if="totalPages > 1" class="pagination">
      <button @click="changePage(currentPage - 1)" :disabled="currentPage === 1" class="page-btn">上一页</button>
      <span class="page-info">第 {{ currentPage }} 页 / 共 {{ totalPages }} 页</span>
      <button @click="changePage(currentPage + 1)" :disabled="currentPage === totalPages" class="page-btn">下一页</button>
    </div>
    
    <div v-if="posts.length === 0 && !loading" class="no-posts">
      <p>{{ searchKeyword ? '未找到相关文章' : '暂无文章' }}</p>
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
const searchKeyword = ref('')

const formatDate = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

const getTags = (tags) => {
  if (!tags) return []
  return tags.split(',').filter(t => t.trim())
}

const getCategoryClass = (category) => {
  const classes = {
    '前端': 'category-frontend',
    '后端': 'category-backend',
    '数据库': 'category-database',
    '其它': 'category-other'
  }
  return classes[category] || 'category-other'
}

const loadPosts = async () => {
  try {
    loading.value = true
    error.value = null
    const response = await postApi.getPaginatedPosts(currentPage.value, 3)
    posts.value = response.data.posts
    totalPages.value = response.data.total_pages
  } catch (err) {
    error.value = '加载文章失败，请稍后重试'
    console.error(err)
  } finally {
    loading.value = false
  }
}

const handleSearch = async () => {
  if (!searchKeyword.value.trim()) {
    currentPage.value = 1
    loadPosts()
    return
  }
  
  try {
    loading.value = true
    error.value = null
    currentPage.value = 1
    const response = await postApi.searchPosts(searchKeyword.value)
    posts.value = response.data.posts
    totalPages.value = response.data.total_pages
  } catch (err) {
    error.value = '搜索失败，请稍后重试'
    console.error(err)
  } finally {
    loading.value = false
  }
}

const changePage = (page) => {
  currentPage.value = page
  if (searchKeyword.value) {
    handleSearch()
  } else {
    loadPosts()
  }
  window.scrollTo(0, 0)
}

onMounted(() => {
  loadPosts()
})
</script>

<style scoped>
.search-section {
  text-align: center;
  margin-bottom: 3rem;
}

.page-title {
  font-size: 2.5rem;
  margin-bottom: 1.5rem;
  color: #2c3e50;
}

.search-box {
  display: flex;
  max-width: 600px;
  margin: 0 auto;
  gap: 0.5rem;
}

.search-box input {
  flex: 1;
  padding: 1rem 1.5rem;
  border: 2px solid #ddd;
  border-radius: 30px;
  font-size: 1rem;
  transition: border-color 0.3s;
}

.search-box input:focus {
  outline: none;
  border-color: #3498db;
}

.search-btn {
  padding: 1rem 2rem;
  background: #3498db;
  color: #fff;
  border: none;
  border-radius: 30px;
  cursor: pointer;
  font-size: 1rem;
  transition: background-color 0.3s;
}

.search-btn:hover {
  background: #2980b9;
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

.post-category {
  display: inline-block;
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.85rem;
  margin-bottom: 1rem;
  color: #fff;
}

.category-frontend {
  background: #e74c3c;
}

.category-backend {
  background: #3498db;
}

.category-database {
  background: #27ae60;
}

.category-other {
  background: #95a5a6;
}

.post-title {
  font-size: 1.5rem;
  margin-bottom: 1rem;
}

.post-title a {
  color: #2c3e50;
  text-decoration: none;
  transition: color 0.3s;
}

.post-title a:hover {
  color: #3498db;
}

.post-summary {
  color: #666;
  line-height: 1.6;
  margin-bottom: 1rem;
}

.post-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.tag {
  background: #f0f4f8;
  color: #3498db;
  padding: 0.25rem 0.75rem;
  border-radius: 15px;
  font-size: 0.85rem;
}

.post-meta {
  color: #999;
  font-size: 0.9rem;
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 1rem;
  margin-top: 3rem;
}

.page-btn {
  padding: 0.75rem 1.5rem;
  background: #3498db;
  color: #fff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.page-btn:hover:not(:disabled) {
  background: #2980b9;
}

.page-btn:disabled {
  background: #bdc3c7;
  cursor: not-allowed;
}

.page-info {
  color: #666;
}

.loading, .error, .no-posts {
  text-align: center;
  padding: 3rem;
  color: #666;
}

.error {
  color: #e74c3c;
}
</style>
