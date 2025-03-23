class Hangman:
    # TODO: remove total_tries Number
    def __init__(self, total_tries: int = 6):
        self.total_tries: int = total_tries
        self.random_word: str = self.generate_random_word()
        self.guessed_letters: list[str] = []

    def initiate_game(self):
        return self.random_word, self.total_tries

    def generate_random_word(self) -> str:
        return "house"

    def is_game_finished(self) -> bool:
        return True if self.total_tries <= 0 else False

    #    if self.total_tries <= 0:
    #       return True
    #   return False

    def update_game(self, guessed_letter: str):
        if not self.is_game_finished():
            self.guessed_letters.append(guessed_letter)
            if guessed_letter not in self.random_word:
                self.total_tries -= 1
        else:
            # returne to TitlePage
            pass


hangman = Hangman()
random_word, total_tries = hangman.initiate_game()
print(random_word)
print(total_tries)
