import unittest
from mtgsdk import Card, Set
from deck.deck import Deck
from hand import Hand

class TestHand(unittest.TestCase):
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
        
        self.hand = Hand(self.deck)

    def test_draw_seven_cards(self):
        # Testa se o método draw_cards sorteia 7 cartas corretamente
        self.hand.draw_cards(7)
        self.assertEqual(len(self.hand.cards), 7)
        self.assertEqual(len(self.deck), 53)  # O deck deve ter 53 cartas restantes

    def test_draw_insufficient_cards(self):
        # Testa se o método draw_cards levanta um erro quando não há cartas suficientes no deck
        self.deck.cards = self.deck.cards[:5]  # Reduz o número de cartas no deck para 5
        with self.assertRaises(ValueError):
            self.hand.draw_cards(7)

    def test_hand_repr(self):
        # Testa a representação em string da mão
        self.hand.draw_cards(7)
        self.assertIn("Hand(7 cards:", repr(self.hand))

if __name__ == '__main__':
    unittest.main()
