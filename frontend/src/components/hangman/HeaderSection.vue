<template>
  <div class="flex-1"></div>
  <h1 class="flex-1 text-center text-3xl font-bold">Hangman</h1>
  <div class="flex-1 px-2 text-right">
    <Button
      class="border-black-alpha-90 bg-white"
      icon="pi pi-question"
      size="small"
      rounded
      @click="showDialog = true"
    />
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
const showDialog = ref(false);
</script>
