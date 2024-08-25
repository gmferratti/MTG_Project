import unittest
from mtgsdk import Card, Set
from deck import Deck  # Certifique-se de que deck.py está no mesmo diretório

class TestDeck(unittest.TestCase):
    """
    Classe de teste para a classe Deck. Esta classe testa as funcionalidades básicas de um deck de Magic: The Gathering.
    """

    def setUp(self):
        """
        Configuração inicial para os testes. Adiciona sets e cores permitidas ao deck e cria uma instância de Deck.
        """
        # Adicionando sets que cobrem os cards utilizados nos testes
        self.allowed_sets = [Set.find('LEA'), Set.find('2ED'), Set.find('10E')]  # 10E é para 'Relentless Rats'
        self.allowed_colors = {'W', 'U', 'B', 'R', 'G'}
        self.deck = Deck(allowed_sets=self.allowed_sets, allowed_colors=self.allowed_colors, exception_cards=['Relentless Rats'])

    def test_add_card(self):
        """
        Testa se um card pode ser adicionado ao deck corretamente e se o número de cards no deck está correto.
        """
        black_lotus = Card.where(name='Black Lotus').all()[0]
        self.deck.add_card(black_lotus)
        self.assertEqual(len(self.deck), 1)
        self.assertIn(black_lotus, self.deck.cards)

    def test_add_card_exceeding_limit(self):
        """
        Testa se adicionar mais de 4 cópias de um card não-exceção levanta um erro.
        """
        black_lotus = Card.where(name='Black Lotus').all()[0]
        for _ in range(4):
            self.deck.add_card(black_lotus)
        # Tentar adicionar uma 5ª cópia de Black Lotus deve levantar um ValueError
        with self.assertRaises(ValueError):
            self.deck.add_card(black_lotus)

    def test_add_exception_card(self):
        """
        Testa se um card na lista de exceções pode ter mais de 4 cópias no deck.
        """
        relentless_rats = Card.where(name='Relentless Rats').all()[0]
        for _ in range(10):
            self.deck.add_card(relentless_rats)
        # Verifica se 10 cópias de Relentless Rats foram adicionadas corretamente
        self.assertEqual(self.deck.cards.count(relentless_rats), 10)

    def test_add_card_invalid_set(self):
        """
        Testa se adicionar um card de um set não permitido levanta um erro.
        """
        # Usando um card que certamente não está nos sets permitidos
        invalid_set_card = Card.where(name='Goblin Electromancer').all()[0]  # Supõe-se que não está nos sets permitidos
        # Tentar adicionar um card de um set não permitido deve levantar um ValueError
        with self.assertRaises(ValueError):
            self.deck.add_card(invalid_set_card)

    def test_add_decklist(self):
        """
        Testa se um decklist completo pode ser adicionado ao deck corretamente.
        """
        decklist = {
            'Relentless Rats': 10,
            'Black Lotus': 1
        }
        # Adiciona o decklist ao deck e verifica se o número total de cards está correto
        self.deck.add_decklist(decklist)
        self.assertEqual(len(self.deck), 11)

    def test_remove_card(self):
        """
        Testa se um card pode ser removido do deck corretamente.
        """
        black_lotus = Card.where(name='Black Lotus').all()[0]
        self.deck.add_card(black_lotus)
        self.deck.remove_card(black_lotus)
        # Verifica se o deck está vazio após a remoção do único card
        self.assertEqual(len(self.deck), 0)
        self.assertNotIn(black_lotus, self.deck.cards)

    def test_is_valid(self):
        """
        Testa a função is_valid para verificar se um deck com 60 cards é válido.
        """
        black_lotus = Card.where(name='Black Lotus').all()[0]
        
        # Adicionar 4 cópias de Black Lotus
        for _ in range(4):
            self.deck.add_card(black_lotus)
        
        # Adicionar outros cards para completar até 60 cards no deck
        another_card = Card.where(name='Relentless Rats').all()[0]
        for _ in range(36):
            self.deck.add_card(another_card)
        
        # Adicionar 20 Swamps para suportar as cartas pretas
        swamp = Card.where(name='Swamp').all()[0]
        for _ in range(20):
            self.deck.add_card(swamp)

        # Verificar se o deck é válido com exatamente 60 cards
        self.assertTrue(self.deck.is_valid())
        
        # Adicionar mais cards até o máximo permitido de 80
        for _ in range(20):  # Adicionando 20 cards para chegar a 80
            self.deck.add_card(another_card)
        
        # Verificar se o deck ainda é válido com 80 cards
        self.assertTrue(self.deck.is_valid())

        # Adicionar mais um card para exceder o limite de 80 cards
        with self.assertRaises(ValueError):
            self.deck.add_card(another_card)
        
        # Após tentar adicionar mais um card, o deck ainda deve ser considerado válido, pois a adição não foi permitida
        self.assertTrue(self.deck.is_valid())


if __name__ == '__main__':
    unittest.main()
