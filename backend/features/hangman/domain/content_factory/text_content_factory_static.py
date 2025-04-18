class TextContentFactoryStatic:
    """
    A static text content provider that returns a predefined text content.
    """

    def __init__(
        self,
        text_content: str,
    ):
        self.text_content = text_content

    def get_random_content(self) -> str:
        """
        Returns the predefined text content.

        Returns:
            str: The predefined text content (word or sentence).
        """
        return self.text_content
