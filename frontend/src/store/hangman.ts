import { defineStore } from "pinia";
import { ref } from "vue";

import { startHangmanGame, updateHangmanGame } from "@/api/hangmanApi";
import { HangmanGame } from "@/models/hangmanModel";

export const useHangmanStore = defineStore("hangmanStore", () => {
  const game = ref<HangmanGame | null>(null);

  async function startGame() {
    try {
      const response = await startHangmanGame();
      game.value = response as HangmanGame;
    } catch (error: any) {
      return error;
    }
  }

  async function guessLetter(guessedLetter: string) {
    if (!game.value) {
      return;
    }

    const payload = {
      gameId: game.value.gameId,
      guessedLetter,
    };

    try {
      const response = await updateHangmanGame(payload);
      game.value = response as HangmanGame;
    } catch (error: any) {
      return error;
    }
  }

  return { game, startGame, guessLetter };
});
