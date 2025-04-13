<template>
  <Button
    v-for="letter in store.alphabet"
    :key="letter"
    :label="letter"
    :disabled="store.game?.guessedLetters.includes(letter)"
    size="small"
    class="m-1"
    @click="store.guessLetter(letter)"
  />
</template>

<script setup lang="ts">
import { useHangmanStore } from "@/store/hangman";
const store = useHangmanStore();
</script>
