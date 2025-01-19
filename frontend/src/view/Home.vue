<template>
  <div class="card">
    <button type="button" @click="count++">count is {{ count }}</button>
  </div>
  <div>
    <RouterLink to="/example">Go to Example View</RouterLink>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
const count = ref(0);
</script>

<style scoped></style>
