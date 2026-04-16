<template>
  <div class="post-detail">
    <div v-if="loading" class="loading">加载中...</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <div v-else-if="post" class="post-content">
      <div class="post-header">
        <span class="post-category">{{ post.category || '未分类' }}</span>
        <h1 class="post-title">{{ post.title }}</h1>
        <div class="post-meta">
          <span class="post-date">发布于：{{ formatDate(post.created_at) }}</span>
          <span v-if="post.updated_at" class="update-date">
            更新于：{{ formatDate(post.updated_at) }}
          </span>
        </div>
        <div class="post-tags">
          <span v-for="tag in getTags(post.tags)" :key="tag" class="tag">{{ tag }}</span>
        </div>
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

const getTags = (tags) => {
  if (!tags) return []
  return tags.split(',').filter(t => t.trim())
}

const updateMetaTags = () => {
  if (!post.value) return
  
  document.title = post.value.title
  
  let metaDesc = document.querySelector('meta[name="description"]')
  if (!metaDesc) {
    metaDesc = document.createElement('meta')
    metaDesc.name = 'description'
    document.head.appendChild(metaDesc)
  }
  const summary = post.value.summary || post.value.content.replace(/<[^>]*>/g, '').substring(0, 150)
  metaDesc.content = summary
  
  let metaKeywords = document.querySelector('meta[name="keywords"]')
  if (!metaKeywords) {
    metaKeywords = document.createElement('meta')
    metaKeywords.name = 'keywords'
    document.head.appendChild(metaKeywords)
  }
  metaKeywords.content = post.value.tags || post.value.category || '技术博客'
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

watch(post, () => {
  updateMetaTags()
})
</script>

<style scoped>
.post-content {
  background: #fff;
  padding: 3rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.post-header {
  margin-bottom: 2rem;
  padding-bottom: 2rem;
  border-bottom: 1px solid #eee;
}

.post-category {
  display: inline-block;
  background: #3498db;
  color: #fff;
  padding: 0.3rem 1rem;
  border-radius: 20px;
  font-size: 0.9rem;
  margin-bottom: 1rem;
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
  margin-bottom: 1rem;
}

.post-date, .update-date {
  margin-right: 1.5rem;
}

.post-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.post-tags .tag {
  background: #f0f4f8;
  color: #3498db;
  padding: 0.25rem 0.75rem;
  border-radius: 15px;
  font-size: 0.85rem;
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

.post-body :deep(p) {
  margin: 1rem 0;
}

.post-body :deep(code) {
  background: #f0f0f0;
  padding: 0.2rem 0.4rem;
  border-radius: 3px;
  font-size: 0.9em;
}

.post-body :deep(pre) {
  background: #2c3e50;
  color: #fff;
  padding: 1rem;
  border-radius: 4px;
  overflow-x: auto;
}

.post-body :deep(pre code) {
  background: transparent;
  color: inherit;
}

.post-body :deep(img) {
  max-width: 100%;
  height: auto;
  border-radius: 4px;
}

.post-body :deep(blockquote) {
  border-left: 4px solid #3498db;
  padding-left: 1rem;
  margin: 1rem 0;
  color: #666;
  font-style: italic;
}

.post-body :deep(ul),
.post-body :deep(ol) {
  margin: 1rem 0;
  padding-left: 2rem;
}

.post-body :deep(li) {
  margin: 0.5rem 0;
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
