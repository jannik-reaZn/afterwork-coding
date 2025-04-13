export interface HangmanGame {
  randomWord: string;
  totalTries: number;
  guessedLetters: Array<string>;
  isGameWonStatus: boolean;
}
