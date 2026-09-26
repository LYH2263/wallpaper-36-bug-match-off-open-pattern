<script setup>
import { onMounted, ref } from 'vue'
import { getJSON, postJSON } from '../api'
const s = ref({}); const defaultMatch = ref(true); const saved = ref(false)
onMounted(async () => {
  s.value = await getJSON('/api/settings')
  defaultMatch.value = String(s.value.default_match_pattern ?? '1') === '1'
})
async function save() {
  s.value = await postJSON('/api/settings', { default_match_pattern: defaultMatch.value })
  saved.value = true
}
</script>
<template>
  <div class="page"><h1>设置</h1>
  <label><input type="checkbox" v-model="defaultMatch" /> 默认对花（新测算的初始开关，不影响已保存记录）</label>
  <button @click="save">保存</button><span v-if="saved"> 已保存</span>
  <pre>{{ s }}</pre></div>
</template>
