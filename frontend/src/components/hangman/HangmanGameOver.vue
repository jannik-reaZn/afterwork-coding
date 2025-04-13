<template>
  <h1 :class="gameStatusClass" class="mb-8 text-3xl font-bold">
    {{ gameStatusMessage }}
  </h1>
  <p>The word was:</p>
  <p class="text-2xl">{{ store.game?.randomWord }}</p>
  <Button
    label="Play Again"
    class="mt-5"
    @click="emit('game-over')"
    size="small"
  />
</template>

<script setup lang="ts">
import { computed } from "vue";
import { useHangmanStore } from "@/store/hangman";

const emit = defineEmits(["game-over"]);

const store = useHangmanStore();

const gameStatusMessage = computed(() =>
  store.game?.isGameWonStatus ? "You Won!" : "Game Over"
);

const gameStatusClass = computed(() =>
  store.game?.isGameWonStatus ? "text-green-700" : "text-red-500"
);
</script>
