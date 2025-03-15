export interface HangmanGame {
  gameId: string;
  numberOfTotalTries: number;
  wordToGuess: string;
  remainingTries: number;
  guessedLetters: string[];
}
