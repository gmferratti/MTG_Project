import unittest
from mtgsdk import Card, Set
from classes.deck import Deck

class TestDeck(unittest.TestCase):
    """
    Classe de teste para a classe Deck. Esta classe testa as funcionalidades básicas de um deck de Magic: The Gathering.
    """
    def setUp(self):
        """
        Configuração inicial para os testes. Adiciona sets e cores permitidas ao deck e cria uma instância de Deck.
        """
        # Adicionando sets que cobrem os cards utilizados nos testes
        self.allowed_sets = [
            Set.find('LEA'),   # Black Lotus, etc.
            Set.find('2ED'),   # Dark Ritual, etc.
            Set.find('10E'),   # Relentless Rats
            Set.find('2X2'),   # Double Masters (para Brainstorm, Thoughtseize, etc.)
            Set.find('M21'),   # Core Set 2021 (para Opt, etc.)
            Set.find('STA'),    # Strixhaven Mystical Archive (Counterspell, etc.)
            Set.find("C18"),
            Set.find("7ED")
        ]
        
        # Só evitando cartas brancas
        self.allowed_colors = {'U', 'B', 'R', 'G'}

        # Utilizando o formato Standard como exemplo
        self.deck = Deck(format_name="Standard", allowed_sets=self.allowed_sets, allowed_colors=self.allowed_colors, exception_cards=['Relentless Rats'])


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

    def test_is_valid_standard_deck(self):
        """
        Testa a função is_valid para verificar se um deck com 60 cards é válido no formato Standard.
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
        
    def test_is_valid_commander_deck(self):
        """
        Testa a função is_valid para verificar se um deck de Commander com 100 cards é válido.
        """
        # Criando um deck no formato Commander
        commander_deck = Deck(format_name="Commander", allowed_sets=self.allowed_sets, allowed_colors=self.allowed_colors, exception_cards=['Relentless Rats'])
        
        relentless_rats = Card.where(name='Relentless Rats').all()[0]
        
        # Adiciona 99 Relentless Rats (supondo que são exceção e podem ter mais de uma cópia)
        for _ in range(64):
            commander_deck.add_card(relentless_rats)
        
        # Adiciona 1 Swamp para completar 100 cartas
        swamp = Card.where(name='Swamp').all()[0]
        for _ in range(36):
            commander_deck.add_card(swamp)

        # Verificar se o deck é válido com exatamente 100 cards
        self.assertTrue(commander_deck.is_valid())

    def test_is_valid_exceeds_max_lands(self):
        """
        Testa se um deck com número de terrenos superior ao máximo permitido levanta um erro.
        """
        # Criando um deck no formato Standard com limite de 26 terrenos
        self.deck = Deck(format_name="Standard", 
                        allowed_sets=self.allowed_sets, 
                        allowed_colors=self.allowed_colors,
                        exception_cards=['Relentless Rats'])
        swamp = Card.where(name='Swamp').all()[0]

        # Adiciona terrenos até o máximo permitido de 26
        for _ in range(26):
            self.deck.add_card(swamp)
        
        # Adiciona 34 outras cartas para completar 60 cartas no deck
        rl_rats = Card.where(name='Relentless Rats').all()[0]
        for _ in range(34):
            self.deck.add_card(rl_rats)

        # Verificar se o deck é válido com exatamente 60 cards
        self.assertTrue(self.deck.is_valid())

        # Tentar adicionar um terreno além do limite deve levantar um ValueError
        with self.assertRaises(ValueError):
            self.deck.add_card(swamp)

        # Verifique novamente se o deck é válido após a tentativa falha de adicionar mais um terreno
        self.assertTrue(self.deck.is_valid())

    def test_deck_with_two_colors_and_artifacts(self):
        """
        Testa a função is_valid para um deck com duas cores e artefatos.
        Verifica se o deck é válido quando possui cartas de duas cores e artefatos.
        """
        # Especificando os conjuntos permitidos
        self.allowed_sets = [
            Set.find('10E'),
            Set.find('2ED'),
            Set.find('2XM'),
            Set.find('C18'),
            Set.find('7ED'),
            Set.find('2X2')
        ]
        
        self.deck = Deck(format_name="Standard", allowed_sets=self.allowed_sets, allowed_colors={'U', 'B'})
        
        island = Card.where(name='Island').all()[0]
        swamp = Card.where(name='Swamp').all()[0]
        
        # Cartas Azuis
        blue_card1 = Card.where(name='Opt').all()[0]
        blue_card2 = Card.where(name='Counterspell').all()[0]
        blue_card3 = Card.where(name='Brainstorm').all()[0]
        blue_card4 = Card.where(name='Ponder').all()[0]
        
        # Cartas Pretas
        black_card1 = Card.where(name='Duress').all()[0]
        black_card2 = Card.where(name='Dark Ritual').all()[0]
        black_card3 = Card.where(name='Thoughtseize').all()[0]
        black_card4 = Card.where(name='Inquisition of Kozilek').all()[0]
        
        artifact_card = Card.where(name='Sol Ring').all()[0]

        # Adiciona 24 terrenos
        for _ in range(12):
            self.deck.add_card(island)
        for _ in range(12):
            self.deck.add_card(swamp)
        
        # Adiciona 16 cartas azuis (4 de cada)
        for _ in range(4):
            self.deck.add_card(blue_card1)
            self.deck.add_card(blue_card2)
            self.deck.add_card(blue_card3)
            self.deck.add_card(blue_card4)
        
        # Adiciona 16 cartas pretas (4 de cada)
        for _ in range(4):
            self.deck.add_card(black_card1)
            self.deck.add_card(black_card2)
            self.deck.add_card(black_card3)
            self.deck.add_card(black_card4)

        # Adiciona 4 artefatos
        for _ in range(4):
            self.deck.add_card(artifact_card)
        
        self.assertTrue(self.deck.is_valid())

if __name__ == '__main__':
    unittest.main()
