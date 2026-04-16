<template>
  <div class="post-detail">
    <div v-if="loading" class="loading">加载中...</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <div v-else-if="post" class="post-content">
      <h1 class="post-title">{{ post.title }}</h1>
      <div class="post-tags">
        <span v-if="post.category" class="category-badge">{{ post.category }}</span>
        <span v-for="tag in parseTags(post.tags)" :key="tag" class="tag-badge">{{ tag }}</span>
      </div>
      <div class="post-meta">
        <span class="post-date">发布于：{{ formatDate(post.created_at) }}</span>
        <span v-if="post.updated_at" class="update-date">
          更新于：{{ formatDate(post.updated_at) }}
        </span>
      </div>
      <div class="post-body" v-html="post.content"></div>
      <div class="back-link">
        <router-link to="/">← 返回首页</router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import { postApi } from '../api'

const route = useRoute()
const post = ref(null)
const loading = ref(true)
const error = ref(null)

const formatDate = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const parseTags = (tagsStr) => {
  if (!tagsStr) return []
  return tagsStr.split(',').map(t => t.trim()).filter(t => t)
}

const updateMetaTags = (postData) => {
  if (!postData) return
  
  document.title = postData.title + ' - 博客'
  
  let description = postData.summary || postData.content.replace(/<[^>]*>/g, '').substring(0, 160)
  
  let metaDescription = document.querySelector('meta[name="description"]')
  if (!metaDescription) {
    metaDescription = document.createElement('meta')
    metaDescription.name = 'description'
    document.head.appendChild(metaDescription)
  }
  metaDescription.content = description
  
  let metaKeywords = document.querySelector('meta[name="keywords"]')
  if (!metaKeywords) {
    metaKeywords = document.createElement('meta')
    metaKeywords.name = 'keywords'
    document.head.appendChild(metaKeywords)
  }
  const keywords = []
  if (postData.category) keywords.push(postData.category)
  if (postData.tags) keywords.push(...parseTags(postData.tags))
  metaKeywords.content = keywords.join(',')
}

const loadPost = async () => {
  try {
    loading.value = true
    error.value = null
    const response = await postApi.getPost(route.params.id)
    post.value = response.data
    updateMetaTags(response.data)
  } catch (err) {
    error.value = '加载文章失败，请稍后重试'
    console.error(err)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadPost()
})

watch(() => route.params.id, () => {
  if (route.params.id) {
    loadPost()
  }
})
</script>

<style scoped>
.post-content {
  background: #fff;
  padding: 3rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.post-title {
  font-size: 2.5rem;
  color: #2c3e50;
  margin-bottom: 1rem;
  line-height: 1.3;
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
  font-size: 0.85rem;
}

.tag-badge {
  background-color: #e8f4f8;
  color: #2980b9;
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.85rem;
}

.post-meta {
  color: #999;
  font-size: 0.9rem;
  margin-bottom: 2rem;
  padding-bottom: 2rem;
  border-bottom: 1px solid #eee;
}

.post-date, .update-date {
  margin-right: 1.5rem;
}

.post-body {
  font-size: 1.1rem;
  line-height: 1.8;
  color: #333;
}

.post-body :deep(h1),
.post-body :deep(h2),
.post-body :deep(h3) {
  margin: 1.5rem 0 1rem;
  color: #2c3e50;
}

.post-body :deep(h1) {
  font-size: 1.8rem;
}

.post-body :deep(h2) {
  font-size: 1.5rem;
}

.post-body :deep(h3) {
  font-size: 1.3rem;
}

.post-body :deep(p) {
  margin: 1rem 0;
}

.post-body :deep(ul),
.post-body :deep(ol) {
  margin: 1rem 0;
  padding-left: 2rem;
}

.post-body :deep(li) {
  margin: 0.5rem 0;
}

.post-body :deep(code) {
  background: #f4f4f4;
  padding: 0.2rem 0.4rem;
  border-radius: 3px;
  font-family: 'Courier New', monospace;
  font-size: 0.9em;
}

.post-body :deep(pre) {
  background: #f4f4f4;
  padding: 1rem;
  border-radius: 4px;
  overflow-x: auto;
  margin: 1rem 0;
}

.post-body :deep(pre code) {
  background: none;
  padding: 0;
}

.post-body :deep(blockquote) {
  border-left: 4px solid #3498db;
  padding-left: 1rem;
  margin: 1.5rem 0;
  color: #666;
  font-style: italic;
}

.post-body :deep(a) {
  color: #3498db;
  text-decoration: none;
}

.post-body :deep(a:hover) {
  text-decoration: underline;
}

.post-body :deep(img) {
  max-width: 100%;
  height: auto;
  border-radius: 4px;
  margin: 1rem 0;
}

.post-body :deep(table) {
  width: 100%;
  border-collapse: collapse;
  margin: 1rem 0;
}

.post-body :deep(th),
.post-body :deep(td) {
  border: 1px solid #ddd;
  padding: 0.75rem;
  text-align: left;
}

.post-body :deep(th) {
  background: #f8f9fa;
  font-weight: 600;
}

.back-link {
  margin-top: 3rem;
  padding-top: 2rem;
  border-top: 1px solid #eee;
}

.back-link a {
  color: #3498db;
  text-decoration: none;
  font-size: 1rem;
}

.back-link a:hover {
  text-decoration: underline;
}

.loading, .error {
  text-align: center;
  padding: 3rem;
  color: #666;
}

.error {
  color: #e74c3c;
}
</style>
