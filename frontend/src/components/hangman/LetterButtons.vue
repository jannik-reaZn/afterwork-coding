<template>
  <div
    v-for="(row, rowIndex) in keyboardLayout"
    :key="rowIndex"
    class="flex justify-center"
  >
    <Button
      v-for="letter in row"
      :key="letter"
      :label="letter"
      :disabled="store.game?.guessedLetters.includes(letter)"
      size="small"
      class="m-1"
      @click="store.guessLetter(letter)"
    />
  </div>
</template>

<script setup lang="ts">
import { computed } from "vue";
import { useHangmanStore } from "@/store/hangman";
import { LanguageKeys } from "@/models/hangmanSettings";

const store = useHangmanStore();

const keyboardLayout = computed(() => {
  // Use backend-provided layout if available
  if (store.alphabetSettings?.layoutHints) {
    return store.alphabetSettings.layoutHints.map((row: string) =>
      row.split("")
    );
  }

  // Fallback to frontend's default layouts
  const defaultLayouts: Partial<Record<LanguageKeys, string[]>> = {
    german: ["QWERTZUIOPÜß", "ASDFGHJKLÖÄ", "YXCVBNM"],
    english: ["QWERTYUIOP", "ASDFGHJKL", "ZXCVBNM"],
  };

  return (
    defaultLayouts[store.currentLanguage]?.map((row) => row.split("")) ||
    defaultLayouts.english?.map((row) => row.split(""))
  );
});
</script>

<style scoped></style>
