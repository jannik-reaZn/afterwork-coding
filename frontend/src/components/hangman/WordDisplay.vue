<template>
  <span
    v-for="(letter, index) in store.game?.randomWord"
    :key="index"
    class="text-4xl"
  >
    {{ store.game?.guessedLetters.includes(letter) ? `${letter} ` : "_ " }}
  </span>
</template>

<script setup lang="ts">
import { useHangmanStore } from "@/store/hangman";
const store = useHangmanStore();
</script>
