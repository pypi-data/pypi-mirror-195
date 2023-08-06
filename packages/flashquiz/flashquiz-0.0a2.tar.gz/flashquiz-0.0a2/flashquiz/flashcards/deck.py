from .card import Card
from pygame.sprite import Group as SpriteGroup


class Deck:
    def __init__(self):
        self.cards = SpriteGroup()
        self.card_in_focus = SpriteGroup()

    def add_card(self, question: str, answer: str):
        """:param question the question for the Card to add to the deck
            :param answer the Card's answer"""
        self.cards.add(Card().set_fields(question, answer))
        return self

    def add_card_from_list(self, add: [str]):
        """:param add list of two strings formatted [question, answer]"""
        self.cards.add(Card().set_fields(add[0], add[1]))
        return self

    def add_card_from_obj(self, add: Card):
        """:param add the Card object to add to this deck"""
        self.cards.add(add)
        return self

    def init_cards(self, front: str, back: str, font: str):
        """Set the background images for all self.cards
        :param front .jpg (500x250) pixels to use for the front
        :param back .jpg to use for the back
        :param font name of the pygame font to load"""
        for card in self.cards:
            card.set_imgs(front, back)
            card.load_text(font)

    def get_first_card(self) -> SpriteGroup:
        temp_group = SpriteGroup()
        temp_group.add(self.cards.sprites()[0])
        return temp_group

    def move_to_back(self, mv_card: Card):
        self.unflip()
        self.cards.remove(mv_card)
        self.cards.add(mv_card)

    def move_first_to_back(self):
        return self.move_to_back(self.cards.sprites()[0])

    def move_to_front(self, mv_card: Card):
        self.unflip()
        grouplist = []
        for c in self.cards:
            grouplist.append(c)
        grouplist.remove(mv_card)
        grouplist.insert(0, mv_card)
        tempgroup = SpriteGroup()
        for c in grouplist:
            tempgroup.add(c)
        self.cards = tempgroup

    def unflip(self):
        for card in self.cards:
            if card.flipped:
                card.flip()

    def move_last_to_front(self):
        return self.move_to_front(self.cards.sprites()[-1])

    def print(self):
        """Print each question: answer in the deck"""
        for card in self.cards:
            print(f"{card.question}: {card.answer}")
