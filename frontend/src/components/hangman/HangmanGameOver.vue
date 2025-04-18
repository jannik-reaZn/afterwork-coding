<template>
  <h1 :class="gameStatusClass" class="mb-8 text-3xl font-bold">
    {{ gameStatusMessage }}
  </h1>
  <p>{{ $t("hangman.reveal") }}</p>
  <p class="text-2xl">{{ store.game?.randomWord }}</p>
  <Button
    :label="$t('hangman.playAgain')"
    class="mt-5"
    @click="emit('game-over')"
    size="small"
  />
</template>

<script setup lang="ts">
import { computed } from "vue";

// Store
import { useHangmanStore } from "@/store/hangman";
const store = useHangmanStore();

// Internationalization
import { useI18n } from "vue-i18n";
const { t } = useI18n();

const emit = defineEmits(["game-over"]);

const gameStatusMessage = computed(() =>
  store.game?.isGameWonStatus ? t("hangman.won") : t("hangman.lost")
);

const gameStatusClass = computed(() =>
  store.game?.isGameWonStatus ? "text-green-700" : "text-red-500"
);
</script>
