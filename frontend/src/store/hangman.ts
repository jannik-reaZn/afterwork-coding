import { defineStore } from "pinia";
import { ref } from "vue";

import {
  startHangmanGame,
  guessLetterHangmanGame,
  getHangmanSettings,
  getHangmanGameAlphabet,
} from "@/api/hangmanApi";
import { HangmanGame } from "@/models/hangmanModel";
import { HangmanSettings } from "@/models/hangmanSettings";
import { GameResult } from "@/models/hangmanGameResult";

export const useHangmanStore = defineStore("hangmanStore", () => {
  // State
  const currentLanguage = ref<string>("");
  const settings = ref<HangmanSettings>();
  const game = ref<HangmanGame>();
  const lastGameResult = ref<GameResult | null>(null);
  const alphabet = ref<string[]>([]);

  // Actions
  async function getSettings() {
    try {
      settings.value = await getHangmanSettings();
    } catch (error) {
      return error;
    }
  }

  async function getAlphabet() {
    if (!settings.value) {
      return;
    }
    try {
      const response = await getHangmanGameAlphabet(currentLanguage.value);
      alphabet.value = response.alphabet;
    } catch (error: any) {
      return error;
    }
  }

  async function startGame(tries: number, language: string) {
    try {
      resetGameState();
      resetAlphabet();
      resetCurrentLanguage();
      currentLanguage.value = language.toLowerCase();
      game.value = await startHangmanGame(tries, language.toLowerCase());
      console.log("Game started", game.value);
    } catch (error: any) {
      return error;
    }
  }

  async function guessLetter(guessedLetter: string) {
    if (!game.value) {
      return;
    }

    try {
      game.value = await guessLetterHangmanGame(guessedLetter, game.value);
      checkGameCompletion();
    } catch (error: any) {
      return error;
    }
  }

  // Private helpers
  function resetGameState() {
    lastGameResult.value = null;
  }

  function resetAlphabet() {
    alphabet.value = [];
  }

  function resetCurrentLanguage() {
    currentLanguage.value = "";
  }

  function checkGameCompletion() {
    if (!game.value) return;

    if (game.value.totalTries === 0 || game.value.isGameWonStatus) {
      lastGameResult.value = {
        word: game.value.randomWord,
        won: game.value.isGameWonStatus,
      };
    }
  }

  return {
    // State
    settings,
    alphabet,
    game,
    lastGameResult,
    // Actions
    getSettings,
    getAlphabet,
    startGame,
    guessLetter,
  };
});
