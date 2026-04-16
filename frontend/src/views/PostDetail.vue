<template>
  <div class="post-detail">
    <div v-if="loading" class="loading">加载中...</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <div v-else-if="post" class="post-content">
      <h1 class="post-title">{{ post.title }}</h1>
      <div class="post-meta">
        <span class="post-category">分类：{{ post.category || '其它' }}</span>
        <span v-if="post.tags" class="post-tags">
          标签：
          <span v-for="tag in formatTags(post.tags)" :key="tag" class="tag">{{ tag }}</span>
        </span>
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

const formatTags = (tagsString) => {
  if (!tagsString) return []
  return tagsString.split(',').map(tag => tag.trim()).filter(tag => tag)
}

// 更新 meta 标签
const updateMetaTags = () => {
  if (!post.value) return
  
  const title = post.value.title
  const description = post.value.summary || post.value.content.substring(0, 150).replace(/<[^>]*>/g, '') + '...'
  const keywords = post.value.tags || ''
  
  // 更新 title
  document.title = `${title} - 我的博客`
  
  // 更新或创建 meta description
  let metaDescription = document.querySelector('meta[name="description"]')
  if (!metaDescription) {
    metaDescription = document.createElement('meta')
    metaDescription.setAttribute('name', 'description')
    document.head.appendChild(metaDescription)
  }
  metaDescription.setAttribute('content', description)
  
  // 更新或创建 meta keywords
  let metaKeywords = document.querySelector('meta[name="keywords"]')
  if (!metaKeywords) {
    metaKeywords = document.createElement('meta')
    metaKeywords.setAttribute('name', 'keywords')
    document.head.appendChild(metaKeywords)
  }
  metaKeywords.setAttribute('content', keywords)
}

const loadPost = async () => {
  try {
    loading.value = true
    error.value = null
    const response = await postApi.getPost(route.params.id)
    post.value = response.data
    updateMetaTags()
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

// 当路由参数变化时重新加载
watch(() => route.params.id, () => {
  loadPost()
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

.post-meta {
  color: #999;
  font-size: 0.9rem;
  margin-bottom: 2rem;
  padding-bottom: 2rem;
  border-bottom: 1px solid #eee;
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
}

.post-category {
  background: #3498db;
  color: white;
  padding: 0.25rem 0.75rem;
  border-radius: 4px;
}

.post-tags {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.tag {
  background: #ecf0f1;
  color: #7f8c8d;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
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
.post-body :deep(h3),
.post-body :deep(h4),
.post-body :deep(h5),
.post-body :deep(h6) {
  color: #2c3e50;
  margin: 1.5rem 0 1rem;
}

.post-body :deep(p) {
  margin-bottom: 1rem;
}

.post-body :deep(img) {
  max-width: 100%;
  height: auto;
  border-radius: 4px;
}

.post-body :deep(pre) {
  background: #f8f9fa;
  padding: 1rem;
  border-radius: 4px;
  overflow-x: auto;
}

.post-body :deep(code) {
  background: #f8f9fa;
  padding: 0.2rem 0.4rem;
  border-radius: 3px;
  font-family: monospace;
}

.post-body :deep(blockquote) {
  border-left: 4px solid #3498db;
  padding-left: 1rem;
  margin-left: 0;
  color: #666;
}

.post-body :deep(ul),
.post-body :deep(ol) {
  padding-left: 2rem;
  margin-bottom: 1rem;
}

.back-link {
  margin-top: 3rem;
  padding-top: 2rem;
  border-top: 1px solid #eee;
}

.back-link a {
  color: #3498db;
  text-decoration: none;
  transition: color 0.3s;
}

.back-link a:hover {
  color: #2980b9;
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
