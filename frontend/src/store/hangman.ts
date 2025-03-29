import { defineStore } from "pinia";
import { ref } from "vue";

import { startHangmanGame, guessLetterHangmanGame } from "@/api/hangmanApi";
import { HangmanGame } from "@/models/hangmanModel";

export const useHangmanStore = defineStore("hangmanStore", () => {
  const game = ref<HangmanGame | null>(null);

  async function startGame(tries: number, language: string) {
    try {
      const response = await startHangmanGame(tries, language);
      game.value = response as HangmanGame;
    } catch (error: any) {
      return error;
    }
  }

  async function guessLetter(guessedLetter: string) {
    if (!game.value) {
      return;
    }

    try {
      const response = await guessLetterHangmanGame(guessedLetter);
      game.value = response as HangmanGame;
    } catch (error: any) {
      return error;
    }
  }

  return { game, startGame, guessLetter };
});
