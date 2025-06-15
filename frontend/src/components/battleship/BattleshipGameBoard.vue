<template>
  <!-- Column -->
  <div v-for="_ in props.size">
    <!-- Row -->
    <div class="size-6 border-1" v-for="_ in props.size"></div>
  </div>
</template>

<script setup lang="ts">
// TODO: Change with value from BE
const DEFAULT_SIZE = 10;
const props = defineProps({
  size: {
    type: Number,
    default: DEFAULT_SIZE,
  },
});
</script>

<style scoped></style>
