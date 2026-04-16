<template>
  <div class="create-post">
    <h1 class="page-title">新建文章</h1>
    <div class="form-container">
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
          <div class="form-group">
            <label>分类</label>
            <select v-model="form.category" class="form-select">
              <option value="">请选择分类</option>
              <option v-for="cat in categories" :key="cat" :value="cat">{{ cat }}</option>
            </select>
          </div>
          
          <div class="form-group">
            <label>标签</label>
            <div class="tags-group">
              <label v-for="tag in allTags" :key="tag" class="tag-checkbox">
                <input
                  type="checkbox"
                  :value="tag"
                  :checked="selectedTags.includes(tag)"
                  @change="toggleTag(tag)"
                />
                {{ tag }}
              </label>
            </div>
          </div>
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
        
        <div class="form-group">
          <label>内容</label>
          <div class="editor-tabs">
            <button
              type="button"
              class="tab-btn"
              :class="{ active: activeTab === 'edit' }"
              @click="activeTab = 'edit'"
            >
              编辑
            </button>
            <button
              type="button"
              class="tab-btn"
              :class="{ active: activeTab === 'preview' }"
              @click="activeTab = 'preview'"
            >
              预览
            </button>
          </div>
          
          <div v-if="activeTab === 'edit'" class="editor-container">
            <Toolbar
              style="border-bottom: 1px solid #ccc"
              :editor="editorRef"
              :defaultConfig="toolbarConfig"
              mode="default"
            />
            <Editor
              style="height: 500px; overflow-y: hidden;"
              v-model="form.content"
              :defaultConfig="editorConfig"
              mode="default"
              @onCreated="handleEditorCreated"
            />
          </div>
          
          <div v-else class="preview-container">
            <div class="preview-content" v-html="form.content"></div>
          </div>
        </div>
        
        <div class="form-actions">
          <button type="submit" class="btn btn-primary" :disabled="submitting">
            {{ submitting ? '提交中...' : '发布文章' }}
          </button>
          <router-link to="/admin" class="btn btn-secondary">取消</router-link>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, onBeforeUnmount } from 'vue'
import { useRouter } from 'vue-router'
import { postApi } from '../api'
import { Editor, Toolbar } from '@wangeditor/editor-for-vue'

const router = useRouter()
const submitting = ref(false)
const activeTab = ref('edit')
const editorRef = ref()
const categories = ['前端', '后端', '数据库', '其它']
const allTags = ['JS', 'Python', 'Java', 'Node', '数据库']
const selectedTags = ref([])

const form = ref({
  title: '',
  summary: '',
  content: '',
  category: '',
  tags: ''
})

const toolbarConfig = {
  excludeKeys: ['group-video']
}

const editorConfig = {
  placeholder: '请输入文章内容...',
  MENU_CONF: {
    uploadImage: {
      server: '/api/upload/image',
      fieldName: 'file',
      maxFileSize: 10 * 1024 * 1024,
      maxNumberOfFiles: 10,
      allowedFileTypes: ['image/*'],
      timeout: 30 * 1000,
      withCredentials: false,
      onSuccess(file, res) {
        console.log(`${file.name} 上传成功`)
      },
      onError(file, err, res) {
        console.error(`${file.name} 上传失败`, err, res)
        alert(`图片 ${file.name} 上传失败`)
      }
    }
  }
}

const handleEditorCreated = (editor) => {
  editorRef.value = editor
}

const toggleTag = (tag) => {
  const index = selectedTags.value.indexOf(tag)
  if (index > -1) {
    selectedTags.value.splice(index, 1)
  } else {
    selectedTags.value.push(tag)
  }
  form.value.tags = selectedTags.value.join(',')
}

const handleSubmit = async () => {
  try {
    submitting.value = true
    await postApi.createPost(form.value)
    alert('文章发布成功！')
    router.push('/admin')
  } catch (err) {
    alert('发布失败，请稍后重试')
    console.error(err)
  } finally {
    submitting.value = false
  }
}

onBeforeUnmount(() => {
  const editor = editorRef.value
  if (editor == null) return
  editor.destroy()
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

.form-row {
  display: grid;
  grid-template-columns: 1fr 2fr;
  gap: 1.5rem;
}

.form-group {
  margin-bottom: 1.5rem;
}

label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 600;
  color: #2c3e50;
}

input,
textarea,
.form-select {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
  font-family: inherit;
  transition: border-color 0.3s;
  box-sizing: border-box;
}

input:focus,
textarea:focus,
.form-select:focus {
  outline: none;
  border-color: #3498db;
}

.form-select {
  background: #fff;
  cursor: pointer;
}

.tags-group {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
}

.tag-checkbox {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-weight: normal;
  cursor: pointer;
}

.tag-checkbox input {
  width: auto;
}

.editor-tabs {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.tab-btn {
  padding: 0.5rem 1.5rem;
  border: 1px solid #ddd;
  background: #f8f9fa;
  border-radius: 4px 4px 0 0;
  cursor: pointer;
  transition: all 0.3s;
}

.tab-btn.active {
  background: #3498db;
  color: #fff;
  border-color: #3498db;
}

.editor-container {
  border: 1px solid #ccc;
  border-radius: 0 4px 4px 4px;
  overflow: hidden;
  background: #fff;
}

.editor-container :deep(.w-e-toolbar) {
  background: #f8f9fa;
  border-bottom: 1px solid #e9ecef;
  z-index: 10;
  flex-wrap: wrap;
}

.editor-container :deep(.w-e-text-container) {
  background: #fff;
  min-height: 450px;
}

.editor-container :deep(.w-e-text-placeholder) {
  color: #999;
  font-style: italic;
}

.preview-container {
  border: 1px solid #ccc;
  border-radius: 0 4px 4px 4px;
  padding: 1.5rem;
  min-height: 500px;
  background: #fafafa;
}

.preview-content {
  line-height: 1.8;
}

.preview-content :deep(h1),
.preview-content :deep(h2),
.preview-content :deep(h3) {
  margin: 1.5rem 0 1rem;
  color: #2c3e50;
}

.preview-content :deep(p) {
  margin: 1rem 0;
}

.preview-content :deep(code) {
  background: #f0f0f0;
  padding: 0.2rem 0.4rem;
  border-radius: 3px;
  font-size: 0.9em;
}

.preview-content :deep(pre) {
  background: #2c3e50;
  color: #fff;
  padding: 1rem;
  border-radius: 4px;
  overflow-x: auto;
}

.preview-content :deep(pre code) {
  background: transparent;
  color: inherit;
}

.form-actions {
  display: flex;
  gap: 1rem;
  margin-top: 2rem;
}

.btn {
  padding: 0.75rem 2rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  text-decoration: none;
  display: inline-block;
  transition: all 0.3s;
  font-size: 1rem;
}

.btn-primary {
  background-color: #3498db;
  color: #fff;
}

.btn-primary:hover {
  background-color: #2980b9;
}

.btn-primary:disabled {
  background-color: #bdc3c7;
  cursor: not-allowed;
}

.btn-secondary {
  background-color: #95a5a6;
  color: #fff;
}

.btn-secondary:hover {
  background-color: #7f8c8d;
}
</style>
