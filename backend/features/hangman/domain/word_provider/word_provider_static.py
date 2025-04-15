class WordProviderStatic:
    """
    A static word provider that returns a predefined text content.
    """

    def __init__(self, word: str):
        self.word = word

    def get_random_content(self) -> str:
        """
        Returns the predefined text content.

        Returns:
            str: The predefined word or sentence.
        """
        return self.word
