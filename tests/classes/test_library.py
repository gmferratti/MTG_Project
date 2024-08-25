import unittest
from mtgsdk import Card, Set
from classes.deck import Deck
from classes.library import Library

class TestLibrary(unittest.TestCase):

    def setUp(self):
        # Configurando um deck válido para uso nos testes
        self.allowed_sets = [Set.find('LEA'), Set.find('2ED'), Set.find('10E')]
        self.allowed_colors = {'W', 'U', 'B', 'R', 'G'}
        self.deck = Deck(allowed_sets=self.allowed_sets, allowed_colors=self.allowed_colors, exception_cards=['Relentless Rats'])

        # Adicionando 60 cartas ao deck
        black_lotus = Card.where(name='Black Lotus').all()[0]
        swamp = Card.where(name='Swamp').all()[0]
        relentless_rats = Card.where(name='Relentless Rats').all()[0]
        for _ in range(4):
            self.deck.add_card(black_lotus)
        for _ in range(24):
            self.deck.add_card(swamp)
        for _ in range(32):
            self.deck.add_card(relentless_rats)
        
        self.library = Library(self.deck)

    def test_library_initialization(self):
        # Testa se a biblioteca é inicializada corretamente com as cartas do deck
        self.assertEqual(len(self.library), 60)
        self.assertEqual(self.library.cards[0].name, 'Black Lotus')
    
    def test_draw_card(self):
        # Testa se a carta é retirada corretamente da biblioteca ao comprar
        card_drawn = self.library.draw_card()
        self.assertEqual(card_drawn.name, 'Black Lotus')
        self.assertEqual(len(self.library), 59)

    def test_return_card(self):
        # Testa se uma carta pode ser retornada para a biblioteca
        card_drawn = self.library.draw_card()
        self.library.return_card(card_drawn)
        self.assertEqual(len(self.library), 60)
        self.assertEqual(self.library.cards[-1].name, 'Black Lotus')

    def test_shuffle(self):
        # Testa se a biblioteca pode ser embaralhada
        original_order = self.library.cards[:]
        self.library.shuffle()
        shuffled_order = self.library.cards
        self.assertNotEqual(original_order, shuffled_order)

    def test_draw_from_empty_library(self):
        # Testa se uma exceção é levantada ao tentar comprar uma carta de uma biblioteca vazia
        self.library.cards = []
        with self.assertRaises(ValueError):
            self.library.draw_card()

    def test_invalid_deck_initialization(self):
        # Testa se uma exceção é levantada ao tentar inicializar a biblioteca com um deck inválido
        empty_deck = Deck(allowed_sets=self.allowed_sets, allowed_colors=self.allowed_colors)
        with self.assertRaises(ValueError):
            Library(empty_deck)

if __name__ == '__main__':
    unittest.main()
