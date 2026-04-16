<template>
  <div class="edit-post">
    <h1 class="page-title">编辑文章</h1>
    <div v-if="loading" class="loading">加载中...</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <div v-else-if="post" class="form-container">
      <form @submit.prevent="handleSubmit">
        <div class="form-group">
          <label for="title">标题</label>
          <input
            id="title"
            v-model="form.title"
            type="text"
            placeholder="请输入文章标题"
            required
          />
        </div>

        <div class="form-group">
          <label for="summary">摘要</label>
          <textarea
            id="summary"
            v-model="form.summary"
            placeholder="请输入文章摘要（可选）"
            rows="3"
          ></textarea>
        </div>

        <div class="form-row">
          <div class="form-group half">
            <label for="category">分类</label>
            <select id="category" v-model="form.category" class="form-select">
              <option v-for="cat in categories" :key="cat" :value="cat">{{ cat }}</option>
            </select>
          </div>

          <div class="form-group half">
            <label for="tags">标签</label>
            <div class="tags-selector">
              <label v-for="tag in availableTags" :key="tag" class="tag-checkbox">
                <input type="checkbox" :value="tag" v-model="selectedTags" />
                <span class="tag-label">{{ tag }}</span>
              </label>
            </div>
          </div>
        </div>

        <div class="form-group">
          <label>内容</label>
          <div class="editor-container">
            <div class="editor-toolbar">
              <button type="button" @click="showPreview = !showPreview" class="preview-toggle">
                {{ showPreview ? '隐藏预览' : '显示预览' }}
              </button>
            </div>
            <div class="editor-wrapper" :class="{ 'with-preview': showPreview }">
              <div class="editor-panel">
                <QuillEditor
                  v-model:content="form.content"
                  contentType="html"
                  theme="snow"
                  toolbar="full"
                  class="quill-editor"
                />
              </div>
              <div v-if="showPreview" class="preview-panel">
                <h3 class="preview-title">预览</h3>
                <div class="preview-content" v-html="form.content"></div>
              </div>
            </div>
          </div>
        </div>

        <div class="form-actions">
          <button type="submit" class="btn btn-primary" :disabled="submitting">
            {{ submitting ? '保存中...' : '保存修改' }}
          </button>
          <router-link to="/admin" class="btn btn-secondary">取消</router-link>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { postApi } from '../api'
import { QuillEditor } from '@vueup/vue-quill'
import '@vueup/vue-quill/dist/vue-quill.snow.css'

const route = useRoute()
const router = useRouter()
const post = ref(null)
const loading = ref(true)
const error = ref(null)
const submitting = ref(false)
const showPreview = ref(false)
const selectedTags = ref([])

const form = ref({
  title: '',
  summary: '',
  content: '',
  category: '其它',
  tags: ''
})

const categories = ['前端', '后端', '数据库', '其它']
const availableTags = ['JS', 'Python', 'Java', 'Node', '数据库']

watch(selectedTags, (newTags) => {
  form.value.tags = newTags.join(',')
})

const loadPost = async () => {
  try {
    loading.value = true
    error.value = null
    const response = await postApi.getPost(route.params.id)
    post.value = response.data
    form.value = {
      title: response.data.title,
      summary: response.data.summary || '',
      content: response.data.content,
      category: response.data.category || '其它',
      tags: response.data.tags || ''
    }
    if (response.data.tags) {
      selectedTags.value = response.data.tags.split(',').map(t => t.trim()).filter(t => t)
    }
  } catch (err) {
    error.value = '加载文章失败'
    console.error(err)
  } finally {
    loading.value = false
  }
}

const handleSubmit = async () => {
  try {
    submitting.value = true
    await postApi.updatePost(route.params.id, form.value)
    alert('文章更新成功！')
    router.push('/admin')
  } catch (err) {
    alert('更新失败，请稍后重试')
    console.error(err)
  } finally {
    submitting.value = false
  }
}

onMounted(() => {
  loadPost()
})
</script>

<style scoped>
.page-title {
  font-size: 2rem;
  margin-bottom: 2rem;
  color: #2c3e50;
}

.form-container {
  background: #fff;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-row {
  display: flex;
  gap: 2rem;
}

.form-group.half {
  flex: 1;
}

label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 600;
  color: #2c3e50;
}

input[type="text"],
textarea,
select.form-select {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
  box-sizing: border-box;
}

input[type="text"]:focus,
textarea:focus {
  outline: none;
  border-color: #3498db;
}

.tags-selector {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.tag-checkbox {
  display: flex;
  align-items: center;
  cursor: pointer;
}

.tag-checkbox input {
  display: none;
}

.tag-label {
  padding: 0.4rem 0.8rem;
  border: 2px solid #3498db;
  border-radius: 20px;
  font-size: 0.9rem;
  transition: all 0.3s;
  background: white;
  color: #3498db;
}

.tag-checkbox input:checked + .tag-label {
  background: #3498db;
  color: white;
}

.editor-container {
  border: 1px solid #ddd;
  border-radius: 4px;
  overflow: hidden;
}

.editor-toolbar {
  background: #f8f9fa;
  padding: 0.5rem;
  border-bottom: 1px solid #ddd;
}

.preview-toggle {
  padding: 0.5rem 1rem;
  background: #3498db;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9rem;
}

.preview-toggle:hover {
  background: #2980b9;
}

.editor-wrapper {
  display: flex;
  min-height: 400px;
}

.editor-wrapper.with-preview {
  min-height: 500px;
}

.editor-panel {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.editor-wrapper.with-preview .editor-panel {
  width: 50%;
  border-right: 1px solid #ddd;
}

.quill-editor {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.quill-editor :deep(.ql-container) {
  flex: 1;
  font-size: 16px;
}

.quill-editor :deep(.ql-editor) {
  min-height: 300px;
}

.preview-panel {
  width: 50%;
  padding: 1rem;
  background: #fafafa;
  overflow-y: auto;
}

.preview-title {
  font-size: 1rem;
  color: #666;
  margin-bottom: 1rem;
  padding-bottom: 0.5rem;
  border-bottom: 2px solid #3498db;
}

.preview-content {
  line-height: 1.8;
  color: #333;
}

.preview-content :deep(h1),
.preview-content :deep(h2),
.preview-content :deep(h3) {
  margin: 1rem 0 0.5rem;
  color: #2c3e50;
}

.preview-content :deep(p) {
  margin: 0.5rem 0;
}

.preview-content :deep(ul),
.preview-content :deep(ol) {
  margin: 0.5rem 0;
  padding-left: 1.5rem;
}

.preview-content :deep(code) {
  background: #f4f4f4;
  padding: 0.2rem 0.4rem;
  border-radius: 3px;
  font-family: monospace;
}

.preview-content :deep(pre) {
  background: #f4f4f4;
  padding: 1rem;
  border-radius: 4px;
  overflow-x: auto;
}

.preview-content :deep(blockquote) {
  border-left: 4px solid #3498db;
  padding-left: 1rem;
  margin: 1rem 0;
  color: #666;
}

.form-actions {
  display: flex;
  gap: 1rem;
  margin-top: 2rem;
}

.btn {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  cursor: pointer;
  text-decoration: none;
  display: inline-block;
  text-align: center;
}

.btn-primary {
  background-color: #3498db;
  color: white;
}

.btn-primary:hover {
  background-color: #2980b9;
}

.btn-primary:disabled {
  background-color: #95a5a6;
  cursor: not-allowed;
}

.btn-secondary {
  background-color: #95a5a6;
  color: white;
}

.btn-secondary:hover {
  background-color: #7f8c8d;
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
