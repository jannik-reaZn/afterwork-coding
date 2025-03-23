from faker import Faker

from backend.features.hangman.domain.models import HangmanLanguages, HangmanStatus


class Hangman:
    # TODO: remove total_tries Number
    def __init__(self, language: str, total_tries: int = 6):
        self.total_tries: int = total_tries
        self.language: str = language
        self.random_word: str = self.generate_random_word(language)
        self.guessed_letters: set[str] = set()
        self.is_game_won_status = False

    def return_values(self) -> HangmanStatus:
        return HangmanStatus(
            random_word=self.random_word,
            total_tries=self.total_tries,
            guessed_letters=self.guessed_letters,
            is_game_won_status=self.is_game_won_status,
        )

    def initiate_game(self):
        return self.return_values()

    def generate_random_word(self, language) -> str:
        fake = Faker(language)
        return fake.word()

    def is_game_won(self) -> bool:
        return True if self.guessed_letters == set(self.random_word) else False

    def is_game_lost(self) -> bool:
        return True if self.total_tries <= 0 else False

    def update_game(self, guessed_letter: str):

        if self.is_game_lost():
            return self.return_values()

        if guessed_letter not in self.guessed_letters:
            self.guessed_letters.add(guessed_letter)
            if guessed_letter not in self.random_word:
                self.total_tries -= 1

        if self.is_game_won():
            self.is_game_won_status = True
            return self.return_values()

        return self.return_values()


hangman = Hangman(language=HangmanLanguages.ENGLISH.value)

hangman_status = hangman.initiate_game()
print("Initiate Game: ", hangman_status)
print()

hangman_status = hangman.update_game(guessed_letter="h")
print("Update Game: ", hangman_status)

hangman_status = hangman.update_game(guessed_letter="o")
print("Update Game: ", hangman_status)

hangman_status = hangman.update_game(guessed_letter="u")
print("Update Game: ", hangman_status)

hangman_status = hangman.update_game(guessed_letter="s")
print("Update Game: ", hangman_status)

hangman_status = hangman.update_game(guessed_letter="e")
print("Update Game: ", hangman_status)
