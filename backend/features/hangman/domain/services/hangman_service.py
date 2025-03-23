from backend.features.hangman.domain.models import HangmanStatus


class Hangman:
    # TODO: remove total_tries Number
    def __init__(self, total_tries: int = 6):
        self.total_tries: int = total_tries
        self.random_word: str = self.generate_random_word()
        self.guessed_letters: set[str] = set()

    def return_values(self) -> HangmanStatus:
        return HangmanStatus(
            random_word=self.random_word,
            total_tries=self.total_tries,
            guessed_letters=self.guessed_letters,
        )

    def initiate_game(self):
        return self.return_values()

    def generate_random_word(self) -> str:
        return "house"

    def is_game_finished(self) -> bool:
        return True if self.total_tries <= 0 else False

    #    if self.total_tries <= 0:
    #       return True
    #   return False

    def update_game(self, guessed_letter: str):

        if self.is_game_finished():
            return self.return_values()

        if guessed_letter not in self.guessed_letters:
            self.guessed_letters.add(guessed_letter)
            if guessed_letter not in self.random_word:
                self.total_tries -= 1

        return self.return_values()


hangman = Hangman()

hangman_status = hangman.initiate_game()
print("Initiate Game: ", hangman_status)
print()

hangman_status = hangman.update_game(guessed_letter="a")
print("Update Game: ", hangman_status)

hangman_status = hangman.update_game(guessed_letter="a")
print("Update Game: ", hangman_status)

hangman_status = hangman.update_game(guessed_letter="b")
print("Update Game: ", hangman_status)

hangman_status = hangman.update_game(guessed_letter="h")
print("Update Game: ", hangman_status)
