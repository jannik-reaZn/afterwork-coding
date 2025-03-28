from backend.features.hangman.domain.models import HangmanLanguages
from backend.features.hangman.domain.services import HangmanService
from backend.features.hangman.domain.services.word_provider import WordProviderFaker

if __name__ == "__main__":
    word_provider_faker = WordProviderFaker(language=HangmanLanguages.ENGLISH.value)

    hangman = HangmanService(word_provider=word_provider_faker)

    hangman_status = hangman.start_game()
    print("Initiate Game: ", hangman_status)
    print()

    hangman_status = hangman.update_game(hangman_status, guessed_letter="h")
    print("Update Game: ", hangman_status)

    hangman_status = hangman.update_game(hangman_status, guessed_letter="o")
    print("Update Game: ", hangman_status)

    hangman_status = hangman.update_game(hangman_status, guessed_letter="u")
    print("Update Game: ", hangman_status)

    hangman_status = hangman.update_game(hangman_status, guessed_letter="s")
    print("Update Game: ", hangman_status)

    hangman_status = hangman.update_game(hangman_status, guessed_letter="e")
    print("Update Game: ", hangman_status)
