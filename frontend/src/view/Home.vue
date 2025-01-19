<template>
  <div class="card">
    <button type="button" @click="increment">
      count is {{ counterStore.count }}
    </button>
  </div>
  <div>
    <RouterLink to="/example">Go to Example View</RouterLink>
  </div>
</template>

<script setup lang="ts">
import { useCounterStore } from "@/store/counter";

const counterStore = useCounterStore();

const increment = () => {
  counterStore.increment();
};
</script>

<style scoped></style>
