export interface HangmanGame {
  gameId: string;
  wordToGuess: string;
  remainingTries: number;
  guessedLetters: string[];
}
