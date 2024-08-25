import unittest
from mtgsdk import Card, Set
from classes.deck import Deck
from classes.hand import Hand
from classes.plays import Plays
from classes.player import Player

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
        
        self.hand = Hand()  # Inicializa a mão vazia
        self.player = Player(name="Test Player", deck=self.deck)  # Inicializa o jogador
        self.tracker = Plays()  # Inicializa o tracker de jogadas

    def test_add_and_remove_card(self):
        # Testa a adição e remoção de cartas da mão
        card = Card.where(name='Black Lotus').all()[0]
        self.hand.add_card(card)
        self.assertIn(card, self.hand.cards)
        self.hand.remove_card(card)
        self.assertNotIn(card, self.hand.cards)

    def test_play_land(self):
        # Testa se é possível jogar um terreno corretamente
        swamp = Card.where(name='Swamp').all()[0]
        self.hand.add_card(swamp)
        self.assertTrue(self.hand.play_land(swamp, self.tracker, self.player))
        self.assertEqual(self.player.lands_played, 1)
        self.assertNotIn(swamp, self.hand.cards)

    def test_play_land_with_extra_lands(self):
        # Testa se é possível jogar terrenos extras se permitido
        swamp = Card.where(name='Swamp').all()[0]
        forest = Card.where(name='Forest').all()[0]
        self.hand.add_card(swamp)
        self.hand.add_card(forest)
        
        self.assertTrue(self.hand.play_land(swamp, self.tracker, self.player))
        self.player.allow_extra_land(1)  # Permite jogar um terreno extra
        self.assertTrue(self.hand.play_land(forest, self.tracker, self.player))
        self.assertEqual(self.player.lands_played, 2)
        self.assertNotIn(swamp, self.hand.cards)
        self.assertNotIn(forest, self.hand.cards)

    def test_play_spell(self):
        # Testa se uma mágica pode ser jogada corretamente
        black_lotus = Card.where(name='Black Lotus').all()[0]  # Custo de mana 0
        relentless_rats = Card.where(name='Relentless Rats').all()[0]  # Custo de mana 3
        
        self.hand.add_card(black_lotus)
        self.hand.add_card(relentless_rats)
        
        self.assertTrue(self.hand.play_spell(self.tracker, available_mana=3))
        self.assertNotIn(black_lotus, self.hand.cards)
        self.assertNotIn(relentless_rats, self.hand.cards)

    def test_play_spell_with_insufficient_mana(self):
        # Testa se nenhuma mágica é jogada quando há mana insuficiente
        relentless_rats = Card.where(name='Relentless Rats').all()[0]  # Custo de mana 3
        
        self.hand.add_card(relentless_rats)
        
        self.assertFalse(self.hand.play_spell(self.tracker, available_mana=2))
        self.assertIn(relentless_rats, self.hand.cards)

if __name__ == '__main__':
    unittest.main()
