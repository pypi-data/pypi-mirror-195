"""
    Define various processes for the Portable Bridge Notation (PBN) format.

    This handles BfG specific items, e.g. the "Bids" token.
    (Standard PBN has the "Auction" Token.)
"""

import os
from termcolor import cprint

from datetime import datetime
from bridgeobjects import Hand, Call, Auction, SEATS
from bfgcardplay import Board
from ..source.player import Player

PBN_VERSION = '2.1'
CREATOR = 'Bid for Game'

MODULE_COLOUR = 'cyan'

class PBN(object):
    """Create a PBN object."""
    SUITS = {'NT': -1, 'S': 0, 'H': 1, 'D': 2, 'C': 3, -1: 'NT', 0: 'S', 1: 'H', 2: 'D', 3: 'C'}

    def __init__(self, event='', site='', date=''):
        self.event = event
        self.site = site
        if not date:
            date = datetime.now()
        self.date = date
        self.board_count = 0

    def boards_from_path(self, path):
        """Return a list of boards given the path to the .pbn file."""
        boards = []
        if path:
            if os.path.isfile(path):
                with open(path, 'r') as f_event:
                    event_lines = f_event.readlines()
                    boards = self.deal_list(event_lines)
        return boards

    def deal_list(self, file_lines, north_first_hand=True):
        """Return a list of BfG Deals generated from the file_lines list."""
        test_boards = []
        board = None
        board_description = ''
        for row in file_lines:
            text_in_row = self._text_in_row(row)
            if not text_in_row:
                if board:
                    board.description = board_description
                    test_boards.append(board)
            elif row.startswith('[Board'):
                description = row[len('Board')+3:-3]
                board_description = description
            elif row.startswith('[Dealer'):
                dealer = row[len('Dealer')+3:-3]
            elif row.startswith('[Deal'):
                board = self._get_board_from_row(row, north_first_hand)
            if board:
                if row.startswith('[Bids'):
                    board.auction = Auction()
                    bids = row[len('Bids')+3:-3]
                    bid_list = bids.split(' ')
                    board.auction.calls = [Call(call) for call in bid_list]
        if board:
            board.description = board_description
            test_boards.append(board)
        return test_boards

    def _get_board_from_row(self, row, north_first_hand):
        """Return a Board object from a string."""
        deal_string = row[7:-3]
        dealer = deal_string[0][0]
        #######
        if north_first_hand:
            norths_hand = 0
        else:
            norths_hand = SEATS.index(dealer)
        #######
        raw_hands = deal_string[2:].split(" ")
        board = Board()
        board.dealer = dealer
        for hand_string in raw_hands:
            hand_list = self._pbn_hand_list(hand_string)
            hand = Hand(hand_list)

            board.hands[norths_hand] = hand
            board.players[norths_hand] = Player(board, hand)

            norths_hand += 1
            norths_hand %= 4
        return board

    @staticmethod
    def _text_in_row(row):
        """
        Return the text in a string after the removal of 'semi-space' characters.
        """
        delete_chars = [9, 32, 13, 10]
        text_in_row = row
        for delete_char in delete_chars:
            text_in_row = text_in_row.replace(chr(delete_char), "")
        return text_in_row

    def _pbn_hand_list(self, hand_string):
        """Return a list for each hand in bfg format."""
        hand_list = []
        hand_cards = hand_string.split(".")
        for index, suit_cards in enumerate(hand_cards):
            suit = self.SUITS[index]
            for card in suit_cards:
                card_name = card+suit
                hand_list.append(card_name)
        return hand_list

    def save_boards(self, boards, path):
        """Save a list of boards to the path."""
        file_rows = self.get_file_rows(boards)
        rows = "\n".join(file_rows)
        with open(path, 'w') as f_pbn_event:
            f_pbn_event.writelines(rows)

    def get_file_rows(self, boards):
        """Return a list of strings in PBN format generated by a list of boards."""
        file_rows = []
        first_row = True
        for board in boards:
            file_rows.extend(self._get_board_rows(board, first_row))
            first_row = False
        return file_rows

    @staticmethod
    def _get_header_rows():
        """Return a list of strings in PBN format header."""
        header_rows = [f'% PBN {PBN_VERSION}',
                       '% EXPORT',
                       '% Content-type: text/pbn; charset=ISO-8859-1',
                       f'% Creator: {CREATOR}',
                       '%']
        return header_rows

    def _get_board_rows(self, board, first_row=False):
        """Return a list of strings in PBN format generated by a board."""
        self.board_count += 1
        board_rows = []
        if first_row:
            board_rows.append(f'[Event "{self.event}"]')
            board_rows.append(f'[Site "{self.site}"]')
            board_rows.append(f'[Date "{self.date:%Y.%m.%d}"]')
        board_rows.append(f'[Board "{self.board_count} {board.identifier}"]')
        board_rows.append(f'[Dealer "{board.dealer}"]')
        board_rows.append(f'[Deal "{board.dealer}:{self._get_pbn_hands(board)}"]')
        board_rows.append('')
        return board_rows

    def _get_pbn_hands(self, board):
        """Return a board as a string in pbn format."""
        hand_list = []
        offset = SEATS.index(board.dealer)

        for _ in range(4):
            hand = board.hands[offset]
            cards = self._card_values_from_hand(hand)
            suit_list = self._suit_list_from_card_list(cards)
            hand_list.append('.'.join(suit_list))
            offset += 1
            offset %= 4
        board_string = ' '.join(hand_list)
        return board_string

    def _card_values_from_hand(self, hand):
        """
        Return a list of card values by suit for a hand.
        e.g. 8S, 7S, 5S, 9H, 6H ... converts to
        [['8', '7', '5'], ['9', '6'] ...
        """
        cards = [[], [], [], []]
        for card in hand.cards:
            card_value = card.name[0]
            suit = card.name[1]
            cards[self.SUITS[suit]].append(card_value)
        return cards

    @staticmethod
    def _suit_list_from_card_list(card_list):
        """
        Return a list of cards in suits from the card_list.
        e.g. [['8', '7', '5'], ['9', '6'] ... ... converts to
        ['875', '96', ...]
        """
        suit_list = []
        for index in range(4):
            suit_list.append(''.join(card_list[index]))
        return suit_list
