""" General knowledge of Magic the Gathering translated into Python constants. """

mtg_formats = {
    "Standard": {
        "Deck Size": {
            "Minimum": 60,
            "Maximum": "No limit"
        },
        "Max Copies per Card": 4,
        "Min Lands": 20,
        "Max Lands": 26
    },
    "Commander": {
        "Deck Size": {
            "Minimum": 100,
            "Maximum": 100
        },
        "Max Copies per Card": 1,
        "Min Lands": 35,
        "Max Lands": 40
    },
    "Modern": {
        "Deck Size": {
            "Minimum": 60,
            "Maximum": "No limit"
        },
        "Max Copies per Card": 4,
        "Min Lands": 20,
        "Max Lands": 26
    },
    "Legacy": {
        "Deck Size": {
            "Minimum": 60,
            "Maximum": "No limit"
        },
        "Max Copies per Card": 4,
        "Min Lands": 20,
        "Max Lands": 26
    },
    "Vintage": {
        "Deck Size": {
            "Minimum": 60,
            "Maximum": "No limit"
        },
        "Max Copies per Card": 4,
        "Min Lands": 20,
        "Max Lands": 26
    },
    "Draft": {
        "Deck Size": {
            "Minimum": 40,
            "Maximum": "No limit"
        },
        "Max Copies per Card": "No limit",
        "Min Lands": 16,
        "Max Lands": 18
    },
    "Sealed": {
        "Deck Size": {
            "Minimum": 40,
            "Maximum": "No limit"
        },
        "Max Copies per Card": "No limit",
        "Min Lands": 16,
        "Max Lands": 18
    }
}

land_colors = {
    'Forest': {'G'},  # Green
    'Island': {'U'},  # Blue
    'Mountain': {'R'},  # Red
    'Plains': {'W'},  # White
    'Swamp': {'B'}   # Black
}

color_combinations = {
    "Monowhite": {"W": 1, "U": 0, "B": 0, "R": 0, "G": 0},  # W
    "Monoblue": {"W": 0, "U": 1, "B": 0, "R": 0, "G": 0},   # U
    "Monoblack": {"W": 0, "U": 0, "B": 1, "R": 0, "G": 0},  # B
    "Monored": {"W": 0, "U": 0, "B": 0, "R": 1, "G": 0},    # R
    "Monogreen": {"W": 0, "U": 0, "B": 0, "R": 0, "G": 1},  # G
    "Azorius": {"W": 1, "U": 1, "B": 0, "R": 0, "G": 0},    # WU
    "Dimir": {"W": 0, "U": 1, "B": 1, "R": 0, "G": 0},      # UB
    "Rakdos": {"W": 0, "U": 0, "B": 1, "R": 1, "G": 0},     # BR
    "Gruul": {"W": 0, "U": 0, "B": 0, "R": 1, "G": 1},      # RG
    "Selesnya": {"W": 1, "U": 0, "B": 0, "R": 0, "G": 1},   # GW
    "Orzhov": {"W": 1, "U": 0, "B": 1, "R": 0, "G": 0},     # WB
    "Izzet": {"W": 0, "U": 1, "B": 0, "R": 1, "G": 0},      # UR
    "Golgari": {"W": 0, "U": 0, "B": 1, "R": 0, "G": 1},    # BG
    "Boros": {"W": 1, "U": 0, "B": 0, "R": 1, "G": 0},      # WR
    "Simic": {"W": 0, "U": 1, "B": 0, "R": 0, "G": 1},      # UG
    "Esper": {"W": 1, "U": 1, "B": 1, "R": 0, "G": 0},      # WUB
    "Grixis": {"W": 0, "U": 1, "B": 1, "R": 1, "G": 0},     # UBR
    "Jund": {"W": 0, "U": 0, "B": 1, "R": 1, "G": 1},       # BRG
    "Naya": {"W": 1, "U": 0, "B": 0, "R": 1, "G": 1},       # RGW
    "Bant": {"W": 1, "U": 1, "B": 0, "R": 0, "G": 1},       # GWU
    "Mardu": {"W": 1, "U": 0, "B": 1, "R": 1, "G": 0},      # WBR
    "Temur": {"W": 0, "U": 1, "B": 0, "R": 1, "G": 1},      # URG
    "Abzan": {"W": 1, "U": 0, "B": 1, "R": 0, "G": 1},      # WBG
    "Jeskai": {"W": 1, "U": 1, "B": 0, "R": 1, "G": 0},     # WUR
    "Sultai": {"W": 0, "U": 1, "B": 1, "R": 0, "G": 1},     # UBG
    "Five Color": {"W": 1, "U": 1, "B": 1, "R": 1, "G": 1}  # WUBRG
}


color_combinations_abbreviated = {
    "WU": {"W": 1, "U": 1, "B": 0, "R": 0, "G": 0},
    "UW": {"W": 1, "U": 1, "B": 0, "R": 0, "G": 0},  # Azorius

    "UB": {"W": 0, "U": 1, "B": 1, "R": 0, "G": 0},
    "BU": {"W": 0, "U": 1, "B": 1, "R": 0, "G": 0},  # Dimir

    "BR": {"W": 0, "U": 0, "B": 1, "R": 1, "G": 0},
    "RB": {"W": 0, "U": 0, "B": 1, "R": 1, "G": 0},  # Rakdos

    "RG": {"W": 0, "U": 0, "B": 0, "R": 1, "G": 1},
    "GR": {"W": 0, "U": 0, "B": 0, "R": 1, "G": 1},  # Gruul

    "GW": {"W": 1, "U": 0, "B": 0, "R": 0, "G": 1},
    "WG": {"W": 1, "U": 0, "B": 0, "R": 0, "G": 1},  # Selesnya

    "WB": {"W": 1, "U": 0, "B": 1, "R": 0, "G": 0},
    "BW": {"W": 1, "U": 0, "B": 1, "R": 0, "G": 0},  # Orzhov

    "UR": {"W": 0, "U": 1, "B": 0, "R": 1, "G": 0},
    "RU": {"W": 0, "U": 1, "B": 0, "R": 1, "G": 0},  # Izzet

    "BG": {"W": 0, "U": 0, "B": 1, "R": 0, "G": 1},
    "GB": {"W": 0, "U": 0, "B": 1, "R": 0, "G": 1},  # Golgari

    "RW": {"W": 1, "U": 0, "B": 0, "R": 1, "G": 0},
    "WR": {"W": 1, "U": 0, "B": 0, "R": 1, "G": 0},  # Boros

    "UG": {"W": 0, "U": 1, "B": 0, "R": 0, "G": 1},
    "GU": {"W": 0, "U": 1, "B": 0, "R": 0, "G": 1},  # Simic

    "WUB": {"W": 1, "U": 1, "B": 1, "R": 0, "G": 0},
    "WBU": {"W": 1, "U": 1, "B": 1, "R": 0, "G": 0},
    "UWB": {"W": 1, "U": 1, "B": 1, "R": 0, "G": 0},
    "UBW": {"W": 1, "U": 1, "B": 1, "R": 0, "G": 0},
    "BWR": {"W": 1, "U": 1, "B": 1, "R": 0, "G": 0},
    "BUW": {"W": 1, "U": 1, "B": 1, "R": 0, "G": 0},  # Esper

    "UBR": {"W": 0, "U": 1, "B": 1, "R": 1, "G": 0},
    "URB": {"W": 0, "U": 1, "B": 1, "R": 1, "G": 0},
    "BUR": {"W": 0, "U": 1, "B": 1, "R": 1, "G": 0},
    "BRU": {"W": 0, "U": 1, "B": 1, "R": 1, "G": 0},
    "RBU": {"W": 0, "U": 1, "B": 1, "R": 1, "G": 0},
    "RUB": {"W": 0, "U": 1, "B": 1, "R": 1, "G": 0},  # Grixis

    "BRG": {"W": 0, "U": 0, "B": 1, "R": 1, "G": 1},
    "BGR": {"W": 0, "U": 0, "B": 1, "R": 1, "G": 1},
    "RBG": {"W": 0, "U": 0, "B": 1, "R": 1, "G": 1},
    "RGB": {"W": 0, "U": 0, "B": 1, "R": 1, "G": 1},
    "GRB": {"W": 0, "U": 0, "B": 1, "R": 1, "G": 1},
    "GBR": {"W": 0, "U": 0, "B": 1, "R": 1, "G": 1},  # Jund

    "RGW": {"W": 1, "U": 0, "B": 0, "R": 1, "G": 1},
    "RWG": {"W": 1, "U": 0, "B": 0, "R": 1, "G": 1},
    "GRW": {"W": 1, "U": 0, "B": 0, "R": 1, "G": 1},
    "GWR": {"W": 1, "U": 0, "B": 0, "R": 1, "G": 1},
    "WRG": {"W": 1, "U": 0, "B": 0, "R": 1, "G": 1},
    "WGR": {"W": 1, "U": 0, "B": 0, "R": 1, "G": 1},  # Naya

    "GWU": {"W": 1, "U": 1, "B": 0, "R": 0, "G": 1},
    "GUW": {"W": 1, "U": 1, "B": 0, "R": 0, "G": 1},
    "WGU": {"W": 1, "U": 1, "B": 0, "R": 0, "G": 1},
    "WUG": {"W": 1, "U": 1, "B": 0, "R": 0, "G": 1},
    "UGW": {"W": 1, "U": 1, "B": 0, "R": 0, "G": 1},
    "UWG": {"W": 1, "U": 1, "B": 0, "R": 0, "G": 1},  # Bant

    "WBR": {"W": 1, "U": 0, "B": 1, "R": 1, "G": 0},
    "WRB": {"W": 1, "U": 0, "B": 1, "R": 1, "G": 0},
    "BWR": {"W": 1, "U": 0, "B": 1, "R": 1, "G": 0},
    "BRW": {"W": 1, "U": 0, "B": 1, "R": 1, "G": 0},
    "RWB": {"W": 1, "U": 0, "B": 1, "R": 1, "G": 0},
    "RBW": {"W": 1, "U": 0, "B": 1, "R": 1, "G": 0},  # Mardu

    "URG": {"W": 0, "U": 1, "B": 0, "R": 1, "G": 1},
    "UGR": {"W": 0, "U": 1, "B": 0, "R": 1, "G": 1},
    "RUG": {"W": 0, "U": 1, "B": 0, "R": 1, "G": 1},
    "RGU": {"W": 0, "U": 1, "B": 0, "R": 1, "G": 1},
    "GRU": {"W": 0, "U": 1, "B": 0, "R": 1, "G": 1},
    "GUR": {"W": 0, "U": 1, "B": 0, "R": 1, "G": 1},  # Temur

    "WBG": {"W": 1, "U": 0, "B": 1, "R": 0, "G": 1},
    "WGB": {"W": 1, "U": 0, "B": 1, "R": 0, "G": 1},
    "BWG": {"W": 1, "U": 0, "B": 1, "R": 0, "G": 1},
    "BGW": {"W": 1, "U": 0, "B": 1, "R": 0, "G": 1},
    "GWB": {"W": 1, "U": 0, "B": 1, "R": 0, "G": 1},
    "GBW": {"W": 1, "U": 0, "B": 1, "R": 0, "G": 1},  # Abzan

    "WUR": {"W": 1, "U": 1, "B": 0, "R": 1, "G": 0},
    "WRU": {"W": 1, "U": 1, "B": 0, "R": 1, "G": 0},
    "UWR": {"W": 1, "U": 1, "B": 0, "R": 1, "G": 0},
    "URW": {"W": 1, "U": 1, "B": 0, "R": 1, "G": 0},
    "RWU": {"W": 1, "U": 1, "B": 0, "R": 1, "G": 0},
    "RUW": {"W": 1, "U": 1, "B": 0, "R": 1, "G": 0},  # Jeskai

    "UBG": {"W": 0, "U": 1, "B": 1, "R": 0, "G": 1},
    "UGB": {"W": 0, "U": 1, "B": 1, "R": 0, "G": 1},
    "BUG": {"W": 0, "U": 1, "B": 1, "R": 0, "G": 1},
    "BGU": {"W": 0, "U": 1, "B": 1, "R": 0, "G": 1},
    "GBU": {"W": 0, "U": 1, "B": 1, "R": 0, "G": 1},
    "GUB": {"W": 0, "U": 1, "B": 1, "R": 0, "G": 1},  # Sultai
}

