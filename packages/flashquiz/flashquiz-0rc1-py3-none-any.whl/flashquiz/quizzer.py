from flashquiz.flashcards.parser import from_csv
from flashquiz.args import handle_args
from flashquiz.gui import GUI


def main():
    args = handle_args()
    game = GUI(args).init_screen()
    deck = from_csv(args.file)
    deck.init_cards(args.cards_front, args.cards_back, args.font)
    run = True
    while run:
        game.screen.fill((0, 0, 0))

        card_in_focus = deck.get_first_card()
        card_in_focus.draw(game.screen)
        game.render(card_in_focus)

        run, deck = game.handle_events(deck)

    game.quit()


if __name__ == '__main__':
    main()
