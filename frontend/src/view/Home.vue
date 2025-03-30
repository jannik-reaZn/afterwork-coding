<template>
  <div class="auto-fit-grid m-2 grid gap-4 pb-8">
    <GameCard
      v-for="game in games"
      :key="game.id"
      :navigateTo="game.navigateTo"
      :show-button="game.showButton"
    >
      <template #title> {{ game.title }} </template>
      <template #content> {{ game.content }} </template>
    </GameCard>
  </div>
</template>

<script setup lang="ts">
import GameCard from "@/components/GameCard.vue";

const games = [
  {
    id: 1,
    title: "Hangman",
    content:
      "Hangman is a guessing game one player. A word is randomly generated and the player tries to guess it by suggesting letters or numbers within a certain number of guesses.",
    navigateTo: "/hangman",
    showButton: true,
  },
  {
    id: 2,
    title: "More games",
    content: "More games to come!",
    navigateTo: null,
    showButton: false,
  },
];
</script>

<style scoped>
.auto-fit-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(15rem, 1fr));
}
</style>
