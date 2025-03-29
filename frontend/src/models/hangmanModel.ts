export interface HangmanGame {
  random_word: string;
  total_tries: number;
  guessed_letters: Set<string>;
  is_game_won_status: boolean;
}
