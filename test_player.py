import unittest
from mtgsdk import Card, Set
from deck.deck import Deck
from player import Player

class TestPlayer(unittest.TestCase):
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
        
        self.player = Player("Alice", self.deck)

    def test_initial_draw(self):
        # Testa se o jogador saca 7 cartas corretamente no início do jogo
        self.player.hand.draw_cards()
        self.assertEqual(len(self.player.hand.cards), 7)
        self.assertEqual(len(self.deck), 53)  # O deck deve ter 53 cartas restantes

    def test_mulligan(self):
        # Testa se o jogador faz mulligan corretamente
        self.player.hand.draw_cards()  # Desenha 7 cartas iniciais
        self.player.mulligan()  # Deve reduzir para 6 cartas
        self.assertEqual(len(self.player.hand.cards), 6)
        self.player.mulligan()  # Deve reduzir para 5 cartas
        self.assertEqual(len(self.player.hand.cards), 5)

    def test_mulligan_to_zero(self):
        # Testa se o jogador pode continuar fazendo mulligans até 0 cartas
        self.player.hand.draw_cards()  # Desenha 7 cartas iniciais
        for _ in range(7):  # Fazer mulligan 7 vezes
            self.player.mulligan()
        self.assertEqual(len(self.player.hand.cards), 0)

    def test_invalid_deck(self):
        # Testa se a criação de um jogador falha com um deck inválido
        invalid_deck = Deck(allowed_sets=self.allowed_sets, allowed_colors=self.allowed_colors)
        with self.assertRaises(ValueError):
            Player("Bob", invalid_deck)  # Deve levantar um erro porque o deck é inválido (vazio)

if __name__ == '__main__':
    unittest.main()
