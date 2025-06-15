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
import { computed } from "vue";
import GameCard from "@/components/GameCard.vue";

import { useI18n } from "vue-i18n";
const { t } = useI18n();

const games = computed(() => [
  {
    id: 1,
    title: t("hangman.title"),
    content: t("hangman.description"),
    navigateTo: "/hangman",
    showButton: true,
  },
  {
    id: 2,
    title: "Battleship",
    content:
      "Battleship is a classic game where players try to sink each other's ships.",
    navigateTo: "/battleship",
    showButton: true,
  },
  {
    id: 3,
    title: t("card.moreGames.title"),
    content: t("card.moreGames.description"),
    navigateTo: null,
    showButton: false,
  },
]);
</script>

<style scoped>
.auto-fit-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(15rem, 1fr));
}
</style>
