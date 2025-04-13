<template>
  <div class="flex items-center py-5">
    <div class="flex-1 px-5 text-start">
      <Button
        @click="$router.back()"
        icon="pi pi-arrow-left"
        size="small"
        rounded
      >
      </Button>
    </div>
    <h1 class="flex-1 text-center text-3xl font-bold">Hangman</h1>
    <div class="flex-1 px-5 text-right">
      <Button
        class="border-black-alpha-90 bg-white"
        icon="pi pi-question"
        size="small"
        rounded
        @click="showDialog = true"
      />
      <HangmanHelpDialog v-model="showDialog" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import HangmanHelpDialog from "@/components/hangman/HangmanHelpDialog.vue";

const showDialog = ref(false);
</script>
