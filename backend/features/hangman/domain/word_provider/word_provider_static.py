class WordProviderStatic:
    """
    A static word provider that returns a predefined list of words.
    """

    def __init__(self, word: str):
        self.word = word

    def get_random_word(self) -> str:
        return self.word
