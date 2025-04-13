<template>
  <div class="flex flex-1 text-center">
    <template v-if="isGameOver">
      <div class="flex flex-1 flex-col items-center justify-center">
        <HangmanGameOver @game-over="handleGameOver" />
      </div>
    </template>

    <template v-else>
      <div class="w-full">
        <HeaderSection @help-click="showDialog = true" />

        <img
          class="mx-auto size-100"
          :src="currentHangmanImage"
          :alt="`Hangman progress: ${store.game?.totalTries} tries left`"
        />

        <WordDisplay
          :random-word="store.game?.randomWord"
          :guessed-letters="store.game?.guessedLetters"
        />

        <p class="my-3">Number of tries left: {{ store.game?.totalTries }}</p>

        <LetterButtons
          :alphabet="store.alphabet"
          :guessed-letters="store.game?.guessedLetters"
          @guess="store.guessLetter"
        />
      </div>
    </template>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from "vue";
import { useHangmanStore } from "@/store/hangman";
import HangmanGameOver from "@/components/hangman/HangmanGameOver.vue";
import HeaderSection from "@/components/hangman/HeaderSection.vue";
import WordDisplay from "@/components/hangman/WordDisplay.vue";
import LetterButtons from "@/components/hangman/LetterButtons.vue";

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

// Emit to notify the parent component when the game is over.
interface Emits {
  (e: "game-over"): void;
}
const emit = defineEmits<Emits>();

const handleGameOver = () => {
  emit("game-over");
};

// Props
const showDialog = ref(false);

const store = useHangmanStore();

// Computed property to check if the game is over.
const isGameOver = computed(
  () => store.game?.totalTries === 0 || store.game?.isGameWonStatus
);

// Computes the current hangman image based on the number of tries left.
const currentHangmanImage = computed(() => {
  const triesLeft = store.game?.totalTries ?? 0;
  const maxIndex = hangmanImages.length - 1;
  const index = Math.min(maxIndex, Math.max(0, maxIndex - triesLeft));
  return hangmanImages[index];
});

// Fetches the alphabet when the component is mounted.
onMounted(async () => {
  await store.getAlphabet();
});
</script>

<style scoped></style>
