"""Modeling constants."""

derived_feats = [
    "cum_spent_mana", 
    "cum_mana_pool", 
    "spent_mana", 
    "mana_pool"
]

key_cols = [
    "name",
    "deck_name",
    "match",
    "turn"
]

final_feats_cols = [
    'mulligan_count',
    'lands_played',
    'spells_played',
    'hand_size',
    'spell_ratio',
    'land_ratio',
    'W',
    'U',
    'B',
    'R',
    'G',
]