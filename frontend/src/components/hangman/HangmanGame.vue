<template>
  <div class="flex flex-1 text-center">
    <div
      class="flex flex-1 flex-col items-center justify-center"
      v-if="store.game?.total_tries === 0 || store.game?.is_game_won_status"
    >
      <h1
        :class="
          store.game?.is_game_won_status ? 'text-green-700' : 'text-red-500'
        "
        class="mb-8 text-3xl font-bold"
      >
        {{ store.game?.is_game_won_status ? "You Won!" : "Game Over" }}
      </h1>
      <p>The word was:</p>
      <p class="text-2xl">{{ store.game?.random_word }}</p>
      <Button
        label="Play Again"
        class="mt-5"
        @click="emit('game-over')"
        size="small"
      />
    </div>
    <div v-else class="w-full">
      <div class="my-4 flex items-center">
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
        <HangmanHelpDialog v-model="showDialog" />
      </div>

      <img class="mx-auto size-100" :src="currentHangmanImage" alt="Hangman" />

      <span
        v-for="(letter, index) in store.game?.random_word"
        :key="index"
        class="text-4xl"
      >
        {{ store.game?.guessed_letters.includes(letter) ? `${letter} ` : "_ " }}
      </span>

      <p class="my-3">Number of tries left: {{ store.game?.total_tries }}</p>
      <Button
        v-for="letter in alphabet"
        :key="letter"
        :label="letter"
        :disabled="store.game?.guessed_letters.includes(letter)"
        size="small"
        class="m-1"
        @click="store.guessLetter(letter)"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from "vue";
import { useHangmanStore } from "@/store/hangman";
const store = useHangmanStore();

// Components
import HangmanHelpDialog from "@/components/hangman/HangmanHelpDialog.vue";

// Assets
import hangman1 from "@/assets/hangman-1.svg";
import hangman2 from "@/assets/hangman-2.svg";
import hangman3 from "@/assets/hangman-3.svg";
import hangman4 from "@/assets/hangman-4.svg";
import hangman5 from "@/assets/hangman-5.svg";
import hangman6 from "@/assets/hangman-6.svg";
import hangman7 from "@/assets/hangman-7.svg";
import hangman8 from "@/assets/hangman-8.svg";
import hangman9 from "@/assets/hangman-9.svg";
import hangman10 from "@/assets/hangman-10.svg";

const emit = defineEmits(["game-over"]);

const hangmanImages = [
  hangman1,
  hangman2,
  hangman3,
  hangman4,
  hangman5,
  hangman6,
  hangman7,
  hangman8,
  hangman9,
  hangman10,
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
  const triesLeft = store.game?.total_tries;
  const index = hangmanImages.length - triesLeft - 1;
  return hangmanImages[index];
});

const showDialog = ref(false);

const alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ".split("");
</script>

<style scoped></style>
