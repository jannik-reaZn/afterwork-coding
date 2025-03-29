<template>
  <div class="text-center">
    <h1>Hangman</h1>
    <Button
      class="border-black-alpha-90 bg-white"
      icon="pi pi-question"
      rounded
      @click="showDialog = true"
    />
    <HangmanHelpDialog v-model="showDialog" />

    {{ store.game }}
    <img class="mx-auto size-80" :src="currentHangmanImage" alt="Hangman" />

    <span v-for="(letter, index) in store.game?.random_word" :key="index">
      {{ store.game?.guessed_letters.has(letter) ? letter : "_" }}
    </span>

    <p>Number of tries left: {{ store.game?.total_tries }}</p>
    <Button
      v-for="letter in alphabet"
      :key="letter"
      :label="letter"
      :disabled="store.game?.guessed_letters.has(letter)"
      class="p-2"
      @click="store.guessLetter(letter)"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from "vue";
import { useHangmanStore } from "@/store/hangman";
const store = useHangmanStore();

// Components
import HangmanHelpDialog from "@/components/hangman/HangmanHelpDialog.vue";

// Assets
import hangman0 from "@/assets/hangman-0.svg";
import hangman1 from "@/assets/hangman-1.svg";
import hangman2 from "@/assets/hangman-2.svg";
import hangman3 from "@/assets/hangman-3.svg";
import hangman4 from "@/assets/hangman-4.svg";
import hangman5 from "@/assets/hangman-5.svg";
import hangman6 from "@/assets/hangman-6.svg";

// TODO remove as soon as the backend is implemented
const NUMBER_OF_TRIES = 6;

const hangmanImages = [
  hangman0,
  hangman1,
  hangman2,
  hangman3,
  hangman4,
  hangman5,
  hangman6,
];

/**
 * Computes the current hangman image based on the number of tries left.
 *
 * @returns {string} The URL or path of the current hangman image.
 *
 * The function calculates the index of the hangman image to display by
 * subtracting the remaining tries from the total number of tries.
 * It then returns the image at that index from the hangmanImages array.
 */
const currentHangmanImage = computed(() => {
  const triesLeft = store.game?.total_tries ?? NUMBER_OF_TRIES;
  const numberOfTotalTries = NUMBER_OF_TRIES; // TODO remove NUMBER_OF_TRIES as soon as the backend is implemented
  const index = Math.abs(numberOfTotalTries - triesLeft);
  return hangmanImages[index];
});

const showDialog = ref(false);

const alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ".split("");
</script>

<style scoped></style>
