from pygame.font import SysFont


class Text:
    """Manages all text to display onscreen (except for flashcards text)"""
    def __init__(self, text, font, size, red, green, blue):
        self.text = text
        self.field = SysFont(font, size, italic=False, bold=False)
        self.sprite = self.field.render(self.text, True, (red, green, blue))
        self.rect = self.sprite.get_rect()
