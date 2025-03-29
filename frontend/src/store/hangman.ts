import { defineStore } from "pinia";
import { ref } from "vue";

import { startHangmanGame, guessLetterHangmanGame } from "@/api/hangmanApi";
import { HangmanGame } from "@/models/hangmanModel";

export const useHangmanStore = defineStore("hangmanStore", () => {
  const game = ref<HangmanGame>();
  const lastGameResult = ref<{ word: string; won: boolean } | null>(null);

  async function startGame(tries: number, language: string) {
    try {
      lastGameResult.value = null;
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
      const response = await guessLetterHangmanGame(guessedLetter, game.value);
      game.value = response as HangmanGame;

      if (game.value.total_tries === 0 || game.value.is_game_won_status) {
        lastGameResult.value = {
          word: game.value.random_word,
          won: game.value.is_game_won_status,
        };
      }
    } catch (error: any) {
      return error;
    }
  }

  return { game, lastGameResult, startGame, guessLetter };
});
