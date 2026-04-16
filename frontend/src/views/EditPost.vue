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

        <div class="form-row">
          <div class="form-group half">
            <label for="category">分类</label>
            <select id="category" v-model="form.category" required>
              <option value="前端">前端</option>
              <option value="后端">后端</option>
              <option value="数据库">数据库</option>
              <option value="其它">其它</option>
            </select>
          </div>

          <div class="form-group half">
            <label for="tags">标签</label>
            <select id="tags" v-model="selectedTags" multiple class="tag-select">
              <option value="JS">JS</option>
              <option value="Python">Python</option>
              <option value="Java">Java</option>
              <option value="Node">Node</option>
              <option value="数据库">数据库</option>
            </select>
            <small class="help-text">按住 Ctrl/Command 键可多选</small>
          </div>
        </div>

        <div class="form-group">
          <label for="summary">摘要</label>
          <textarea
            id="summary"
            v-model="form.summary"
            placeholder="请输入文章摘要（可选，用于SEO和列表展示）"
            rows="3"
          ></textarea>
        </div>

        <div class="form-group">
          <div class="editor-header">
            <label>内容</label>
            <div class="editor-tabs">
              <button
                type="button"
                :class="['tab-btn', { active: activeTab === 'edit' }]"
                @click="activeTab = 'edit'"
              >
                编辑
              </button>
              <button
                type="button"
                :class="['tab-btn', { active: activeTab === 'preview' }]"
                @click="activeTab = 'preview'"
              >
                预览
              </button>
            </div>
          </div>

          <!-- 富文本编辑器 -->
          <div v-show="activeTab === 'edit'" class="editor-wrapper">
            <Toolbar
              :editor="editorRef"
              :defaultConfig="toolbarConfig"
              mode="default"
              class="editor-toolbar"
            />
            <Editor
              :defaultConfig="editorConfig"
              mode="default"
              v-model="form.content"
              @onCreated="handleCreated"
              @onChange="handleChange"
              class="editor-content"
            />
          </div>

          <!-- 预览区域 -->
          <div v-show="activeTab === 'preview'" class="preview-wrapper">
            <div class="preview-content" v-html="form.content"></div>
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
import { ref, shallowRef, onBeforeUnmount, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { postApi } from '../api'
import '@wangeditor/editor/dist/css/style.css'
import { Editor, Toolbar } from '@wangeditor/editor-for-vue'

const route = useRoute()
const router = useRouter()
const post = ref(null)
const loading = ref(true)
const error = ref(null)
const submitting = ref(false)
const activeTab = ref('edit')
const selectedTags = ref([])
const form = ref({
  title: '',
  summary: '',
  content: '',
  category: '其它',
  tags: ''
})

// 监听标签选择变化
watch(selectedTags, (newVal) => {
  form.value.tags = newVal.join(',')
})

// 编辑器配置
const editorRef = shallowRef()
const toolbarConfig = {}
const editorConfig = {
  placeholder: '请输入文章内容...',
  scroll: false,
  MENU_CONF: {}
}

const handleCreated = (editor) => {
  editorRef.value = editor
  // 如果有内容，设置到编辑器中
  if (form.value.content) {
    editor.setHtml(form.value.content)
  }
}

const handleChange = (editor) => {
  form.value.content = editor.getHtml()
}

onBeforeUnmount(() => {
  const editor = editorRef.value
  if (editor) {
    editor.destroy()
  }
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
    // 设置选中的标签
    if (response.data.tags) {
      selectedTags.value = response.data.tags.split(',').map(tag => tag.trim()).filter(tag => tag)
    }
    // 如果编辑器已创建，设置内容
    if (editorRef.value) {
      editorRef.value.setHtml(form.value.content)
    }
  } catch (err) {
    error.value = '加载文章失败'
    console.error(err)
  } finally {
    loading.value = false
  }
}

const handleSubmit = async () => {
  if (!form.value.content.trim() || form.value.content === '<p><br></p>') {
    alert('请输入文章内容')
    return
  }

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
  gap: 1rem;
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
select {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
  font-family: inherit;
}

input[type="text"]:focus,
textarea:focus,
select:focus {
  outline: none;
  border-color: #3498db;
}

.tag-select {
  min-height: 100px;
}

.help-text {
  color: #999;
  font-size: 0.85rem;
  margin-top: 0.25rem;
  display: block;
}

.editor-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
}

.editor-tabs {
  display: flex;
  gap: 0.5rem;
}

.tab-btn {
  padding: 0.5rem 1rem;
  border: 1px solid #ddd;
  background: white;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s;
}

.tab-btn.active {
  background: #3498db;
  color: white;
  border-color: #3498db;
}

.editor-wrapper {
  border: 1px solid #ccc;
  z-index: 100;
}

.editor-toolbar {
  border-bottom: 1px solid #ccc;
}

.editor-content {
  min-height: 400px;
}

.preview-wrapper {
  border: 1px solid #ddd;
  border-radius: 4px;
  min-height: 400px;
  padding: 1rem;
  background: #f9f9f9;
}

.preview-content {
  background: white;
  padding: 2rem;
  border-radius: 4px;
  min-height: 360px;
}

.preview-content :deep(h1),
.preview-content :deep(h2),
.preview-content :deep(h3),
.preview-content :deep(h4),
.preview-content :deep(h5),
.preview-content :deep(h6) {
  color: #2c3e50;
  margin: 1.5rem 0 1rem;
}

.preview-content :deep(p) {
  margin-bottom: 1rem;
  line-height: 1.8;
}

.preview-content :deep(img) {
  max-width: 100%;
  height: auto;
}

.preview-content :deep(pre) {
  background: #f8f9fa;
  padding: 1rem;
  border-radius: 4px;
  overflow-x: auto;
}

.preview-content :deep(code) {
  background: #f8f9fa;
  padding: 0.2rem 0.4rem;
  border-radius: 3px;
  font-family: monospace;
}

.preview-content :deep(blockquote) {
  border-left: 4px solid #3498db;
  padding-left: 1rem;
  margin-left: 0;
  color: #666;
}

.form-actions {
  display: flex;
  gap: 1rem;
  margin-top: 2rem;
}

.btn {
  padding: 0.75rem 1.5rem;
  border-radius: 4px;
  font-size: 1rem;
  cursor: pointer;
  text-decoration: none;
  display: inline-block;
  transition: all 0.3s;
}

.btn-primary {
  background: #3498db;
  color: white;
  border: none;
}

.btn-primary:hover:not(:disabled) {
  background: #2980b9;
}

.btn-primary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-secondary {
  background: #95a5a6;
  color: white;
}

.btn-secondary:hover {
  background: #7f8c8d;
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
