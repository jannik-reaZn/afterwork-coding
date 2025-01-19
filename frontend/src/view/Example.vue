<template>
  <div>
    <p>{{ data }}</p>
    <button @click="loadData">Fetch Data</button>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import { fetchData } from "../api/exampleService.ts";

const data = ref<string | null>(null);

async function loadData() {
  try {
    const response = await fetchData("/");
    console.log("response", response);
    data.value = response.message;
  } catch (error) {
    console.error("Failed to load data:", error);
  }
}
</script>
