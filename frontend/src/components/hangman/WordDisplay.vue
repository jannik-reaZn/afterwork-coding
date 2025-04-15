<template>
  <div class="flex w-full flex-col items-center justify-center">
    <div class="flex flex-wrap justify-center">
      <div
        v-for="(word, wordIndex) in wordsArray"
        :key="`word-${wordIndex}`"
        class="mx-1 flex"
      >
        <span
          v-for="(letter, letterIndex) in word"
          :key="`letter-${wordIndex}-${letterIndex}`"
          class="inline-block w-[1.1ch] text-center font-mono text-4xl"
        >
          {{ displayLetter(letter) }}
        </span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from "vue";
import { useHangmanStore } from "@/store/hangman";
const store = useHangmanStore();
const alwaysVisible = [" ", "-", ".", ",", "!", "?"];

// Group the letters by words to keep connected words together
const wordsArray = computed(() => {
  const fullText = store?.game?.randomWord || "";
  // Split by spaces while preserving spaces as separate items
  const words = fullText.match(/\S+|\s+/g) || [];
  // Split each word into letters
  return words.map((word) => word.split(""));
});

function displayLetter(letter: string) {
  return alwaysVisible.includes(letter) ||
    store?.game?.guessedLetters.includes(letter)
    ? letter
    : "_";
}
</script>
