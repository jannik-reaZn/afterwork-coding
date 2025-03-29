<template>
  <HangmanStartDialog v-model="showSetupDialog" />
  <HangmanGame v-show="!showSetupDialog" />
</template>

<script setup lang="ts">
import { ref } from "vue";

// Components
import HangmanStartDialog from "@/components/hangman/HangmanStartDialog.vue";
import HangmanGame from "@/components/hangman/HangmanGame.vue";

const showSetupDialog = ref(true);
</script>

<style scoped></style>
