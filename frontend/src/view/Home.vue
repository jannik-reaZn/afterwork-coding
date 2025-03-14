<template>
  <div class="grid gap-4 pb-8 m-2 auto-fit-grid">
    <GameCard :navigateTo="'/hangman'" :show-button="true" class="custom-card">
      <template #title> Hangman </template>
      <template #content>
        Hangman is a guessing game one player. A word, phrase, or sentence is
        randomly generated and the player tries to guess it by suggesting
        letters or numbers within a certain number of guesses.
      </template>
    </GameCard>
    <GameCard :show-button="false" class="custom-card">
      <template #title> More games </template>
      <template #content> More games to come! </template>
    </GameCard>
  </div>
</template>

<script setup lang="ts">
import GameCard from "@/components/GameCard.vue";
</script>

<style scoped>
.auto-fit-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(15rem, 1fr));
}
</style>
