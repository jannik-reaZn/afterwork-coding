<template>
  <div class="text-center">
    <h1>Hangman</h1>
    <Button
      class="bg-white border-black-alpha-90"
      icon="pi pi-question"
      rounded
      @click="showDialog = true"
    />
    <HangmanHelpDialog v-model="showDialog" />

    <div v-if="store.game">
      <span v-for="(letter, index) in store.game?.wordToGuess" :key="index">
        {{ store.game?.guessedLetters.includes(letter) ? letter : "_" }}
      </span>
      <p>Number of tries left: {{ store.game?.remainingTries }}</p>
      <Button
        v-for="letter in alphabet"
        :key="letter"
        :label="letter"
        :disabled="store.game?.guessedLetters.includes(letter)"
        class="p-2"
        @click="guessLetter(letter)"
      />
    </div>
    <div v-else>
      <Button @click="store.startGame" label="Start game" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import HangmanHelpDialog from "@/components/HangmanHelpDialog.vue";
import { useHangmanStore } from "@/store/hangman";
const store = useHangmanStore();

const showDialog = ref(false);

const alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ".split("");

function guessLetter(guessedLetter: string) {
  store.guessLetter(guessedLetter);
}
</script>

<style scoped></style>
