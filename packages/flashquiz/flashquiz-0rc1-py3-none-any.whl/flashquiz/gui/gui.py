import pygame
from ..flashcards import Deck, Card
from pygame.sprite import Group as SpriteGroup


class GUI:
    def __init__(self, opts):
        self.screen, self.clock = None, None
        self.window_name = opts.title
        self.dimensions = (opts.w, opts.h)
        self.FPS = opts.fps

    def reset_clock(self):
        self.clock = pygame.time.Clock()

    def init_screen(self):
        pygame.init()
        self.reset_clock()
        self.screen = pygame.display.set_mode(self.dimensions)
        pygame.display.set_caption(self.window_name)
        return self

    def handle_events(self, deck: Deck):
        for event in pygame.event.get():
            keys = pygame.key.get_pressed()
            if event.type == pygame.MOUSEBUTTONDOWN:
                deck.cards.sprites()[0].flip()
            if keys[pygame.K_RIGHT]:
                deck.move_first_to_back()
            if keys[pygame.K_LEFT]:
                deck.move_last_to_front()
            if keys[pygame.K_ESCAPE] or event.type == pygame.QUIT:
                return False, deck
        return True, deck

    def render(self, group: SpriteGroup):
        self.clock.tick(self.FPS)
        for card in group:
            card.update()
            sprite, rect = card.render_text()
            self.screen.blit(sprite, rect)
        pygame.display.update()

    def render_card(self, card: Card):
        self.clock.tick(self.FPS)
        card.update()
        sprite, rect = card.render_text()
        self.screen.blit(sprite, rect)
        pygame.display.update()

    @staticmethod
    def get_mouse_pos() -> (int, int):
        return pygame.mouse.get_pos()

    @staticmethod
    def quit():
        pygame.quit()
