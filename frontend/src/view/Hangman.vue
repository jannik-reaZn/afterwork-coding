<template>
  <h1>Hangman</h1>
  <div v-if="store.game">
    <div class="grid gap-2">
      <p>{{ store.game?.wordToGuess }}</p>
      <span v-for="(letter, index) in store.game?.wordToGuess" :key="index">
        {{ store.game?.guessedLetters.includes(letter) ? letter : "_" }}
      </span>
      <p>Number of tries left: {{ store.game?.remainingTries }}</p>
      <Button
        v-for="letter in alphabet"
        :key="letter"
        :label="letter"
        class="p-2"
        @click="guessLetter(letter)"
      />
    </div>
  </div>
  <div v-else>
    <Button @click="store.startGame" label="Start game" />
  </div>
</template>

<script setup lang="ts">
import { useHangmanStore } from "@/store/hangman";
const store = useHangmanStore();

const alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ".split("");

function guessLetter(guessedLetter: string) {
  store.guessLetter(guessedLetter);
}
</script>

<style scoped></style>
