from typing import List, Tuple
import card
from card import Card
from deck import Deck
from player import Player


def game_flow(players):
    hart_staus = False
    current_player_index = find_three_clubs(players)

    for i in range(0, 13):
        lead_card = None

        cards_played = []
        for j in range(len(players)):
            if hart_staus == False:
                for c in cards_played:
                    if c[2].suit == Deck.suits['hearts']:
                        hart_staus = True
            forst_hond = (i == 0)
            card_played = play_card(cards_played, players[current_player_index], lead_card, hart_staus, forst_hond)
            if j == 0:
                lead_card = card_played
            cards_played.append((current_player_index, players[current_player_index], card_played))
            current_player_index = (current_player_index + 1) % len(players)

        current_player_index = leader(cards_played, lead_card)
        print("Trick winner: ", players[current_player_index])


def find_three_clubs(players):
    playerindex = 0
    for player in players:
        for c in player.cards:
            if c.suit == Deck.suits['clubs'] and c.value == 3:
                return playerindex
        playerindex += 1

def leader(player_and_card: List[Tuple], lead_card):
    # if card not same suit then kill th0em immediately
    # else then compare numbers and hui0ghest wins, kill the rest
    def suit_same(player_and_card_tuple: Tuple):
        return lead_card.suit == player_and_card_tuple[2].suit

    cards_with_the_special_one_and_only_lead_suit = filter(suit_same, player_and_card)

    def value_vinnnnnnnnnnnnnnnnnnnnnnnnnner(player_and_card_tuple: Tuple):
        return player_and_card_tuple[2].value

    vinner = max(cards_with_the_special_one_and_only_lead_suit, key=value_vinnnnnnnnnnnnnnnnnnnnnnnnnner)
    return vinner[0]


def play_card(cards_played: List[Card], player: Player, lead_card, hart_staus, forst_hond):
    # use input validation for playable cards
    def if_card_allowed(card: Card, lead_card: Card, hond: List[Card], hart_staus: bool, forst_hond: bool):
        hond_suits = set([c.suit for c in hond])
        if lead_card is None:
            # first player of hand
            if forst_hond:
                return card.suit == Deck.suits['clubs'] and card.value == 3
            if card.suit == Deck.suits['hearts']:
                if hart_staus:
                    return True
                else:
                    # can only break hearts if have no other suits
                    for s in hond_suits:
                        if s != Deck.suits['hearts']:
                            return False
        if forst_hond:
            if card.suit == Deck.suits['hearts'] or (card.name == 'Q' and card.suit == Deck.suits['spades']):
                # no point cards on first hand
                return False
        if card.suit == lead_card.suit:
            return True
        else:
            return lead_card.suit not in hond_suits

    def ai(lead_card: Card, hond: List[Card], hart_staus: bool, forst_hond: bool):
        for c in hond:
            if if_card_allowed(c, lead_card, hond, hart_staus, forst_hond):
                return c
        raise RuntimeError('no valid card!!! ')

    while True:
        print(" Trick: ", [c[2] for c in cards_played])
        print(f'\n\n{player.name}\n')
        print(''.join(["{:>3}{}".format(c.name, c.suit) for c in player.cards]))
        print(''.join(["{0:4}".format(idx) for idx in range(len(player.cards))]))
        if player.ai:
            card = ai(lead_card, player.cards, hart_staus, forst_hond)
        else:
            card_input = input('wat card do u wanna play\n(0 for first, etc)\n')
            card = player.cards[int(card_input)]
        if if_card_allowed(card, lead_card, player.cards, hart_staus, forst_hond):
            player.cards.remove(card)
            return card
        else:
            print("Card not allowed")
player_names = ['twistan', 'troy', 'daddie', 'mummie']
deck = Deck()
hands = deck.deal(len(player_names), 13)
players = [
        Player(name, hand)
        for name, hand in zip(player_names, hands)
    ]
game_flow(players)

        # second player picks what clubs they want to play
        # if no clubs the have player pick card of their choice
        # if card o' choice is hearts then break hearts
        # when hearts break then players are allowed to lead with hearts
        # second - 4 players doe same, following same condition
        # player with the highest clubs move in play cards to their take pile variable
        # once done then player places a card of their choice and cycle continues until 13 rounds is done
        # once thirteen rounds done then count take pile
        # each heart in pile adds 1 to player points
        # player with queen o' spades gains thirteen points
        # player with least points wins
