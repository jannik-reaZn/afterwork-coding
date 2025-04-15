<template>
  <span
    v-for="(letter, index) in wordArray"
    :key="index"
    class="inline-block w-[1.1ch] text-center font-mono text-4xl"
  >
    {{ displayLetter(letter) }}
  </span>
</template>

<script setup lang="ts">
import { computed } from "vue";
import { useHangmanStore } from "@/store/hangman";
const store = useHangmanStore();
const alwaysVisible = [" ", "-", ".", ",", "!", "?"];

const wordArray = computed(() => store?.game?.randomWord.split(""));

function displayLetter(letter: string) {
  return alwaysVisible.includes(letter) ||
    store?.game?.guessedLetters.includes(letter)
    ? letter
    : "_";
}
</script>
