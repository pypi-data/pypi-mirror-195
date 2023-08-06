# contains class for flashcards with question and answers
from pygame.sprite import Sprite
from pygame.font import SysFont
from pygame.image import load


class Card(Sprite):
    def __init__(self):
        super().__init__()
        self.x, self.y = 110, 120
        self.font, self.text_sprite, self.text_rect = None, None, None
        self.question, self.answer = None, None
        self.rect, self.image = None, None
        self.front, self.back = None, None
        self.flipped = False

    def set_fields(self, question: str, answer: str):
        self.question, self.answer = question, answer
        return self

    def set_pos(self, x: int, y: int):
        self.x, self.y = x, y

    def set_imgs(self, front: str, back: str):
        self.front, self.back = front, back
        self.refresh_img()

    def load_text(self, font):
        self.font = SysFont(font, 30, italic=False, bold=False)
        self.text_sprite = self.font.render(self.question, True, (255, 255, 255))
        self.text_rect = self.text_sprite.get_rect()

    def render_text(self):
        if self.flipped:
            txt = self.answer
        else:
            txt = self.question
        self.text_rect.center = (self.x + 250, self.y + 100)
        self.text_sprite = self.font.render(txt, True, (255, 255, 255))
        return self.text_sprite, self.text_rect

    def refresh_img(self):
        if self.flipped:
            self.image = load(self.back)
        else:
            self.image = load(self.front)
        self.rect = self.image.get_rect()

    def flip(self):
        self.flipped = not self.flipped
        self.refresh_img()

    def update(self) -> None:
        """Override pygame's default sprite update()"""
        self.rect.x, self.rect.y = self.x, self.y

