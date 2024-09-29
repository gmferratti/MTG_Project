""" General knowledge of Magic the Gathering translated into Python constants. """

mtg_formats = {
    "Standard": {
        "Deck Size": {"Minimum": 60, "Maximum": "No limit"},
        "Max Copies per Card": 4,
        "Min Lands": 20,
        "Max Lands": 26,
    },
    "Commander": {
        "Deck Size": {"Minimum": 100, "Maximum": 100},
        "Max Copies per Card": 1,
        "Min Lands": 35,
        "Max Lands": 40,
    },
    "Modern": {
        "Deck Size": {"Minimum": 60, "Maximum": "No limit"},
        "Max Copies per Card": 4,
        "Min Lands": 20,
        "Max Lands": 26,
    },
    "Legacy": {
        "Deck Size": {"Minimum": 60, "Maximum": "No limit"},
        "Max Copies per Card": 4,
        "Min Lands": 20,
        "Max Lands": 26,
    },
    "Vintage": {
        "Deck Size": {"Minimum": 60, "Maximum": "No limit"},
        "Max Copies per Card": 4,
        "Min Lands": 20,
        "Max Lands": 26,
    },
    "Draft": {
        "Deck Size": {"Minimum": 40, "Maximum": "No limit"},
        "Max Copies per Card": "No limit",
        "Min Lands": 16,
        "Max Lands": 18,
    },
    "Sealed": {
        "Deck Size": {"Minimum": 40, "Maximum": "No limit"},
        "Max Copies per Card": "No limit",
        "Min Lands": 16,
        "Max Lands": 18,
    },
}

land_colors = {
    'Forest': {'G'},  # Green
    'Island': {'U'},  # Blue
    'Mountain': {'R'},  # Red
    'Plains': {'W'},  # White
    'Swamp': {'B'},  # Black
}

color_combinations = {
    "monowhite": {"w": 1, "u": 0, "b": 0, "r": 0, "g": 0},  # W
    "monoblue": {"w": 0, "u": 1, "b": 0, "r": 0, "g": 0},  # U
    "monoblack": {"w": 0, "u": 0, "b": 1, "r": 0, "g": 0},  # B
    "monored": {"w": 0, "u": 0, "b": 0, "r": 1, "g": 0},  # R
    "monogreen": {"w": 0, "u": 0, "b": 0, "r": 0, "g": 1},  # G
    "azorius": {"w": 1, "u": 1, "b": 0, "r": 0, "g": 0},  # WU
    "dimir": {"w": 0, "u": 1, "b": 1, "r": 0, "g": 0},  # UB
    "rakdos": {"w": 0, "u": 0, "b": 1, "r": 1, "g": 0},  # BR
    "gruul": {"w": 0, "u": 0, "b": 0, "r": 1, "g": 1},  # RG
    "selesnya": {"w": 1, "u": 0, "b": 0, "r": 0, "g": 1},  # GW
    "orzhov": {"w": 1, "u": 0, "b": 1, "r": 0, "g": 0},  # WB
    "izzet": {"w": 0, "u": 1, "b": 0, "r": 1, "g": 0},  # UR
    "golgari": {"w": 0, "u": 0, "b": 1, "r": 0, "g": 1},  # BG
    "boros": {"w": 1, "u": 0, "b": 0, "r": 1, "g": 0},  # WR
    "simic": {"w": 0, "u": 1, "b": 0, "r": 0, "g": 1},  # UG
    "esper": {"w": 1, "u": 1, "b": 1, "r": 0, "g": 0},  # WUB
    "grixis": {"w": 0, "u": 1, "b": 1, "r": 1, "g": 0},  # UBR
    "jund": {"w": 0, "u": 0, "b": 1, "r": 1, "g": 1},  # BRG
    "naya": {"w": 1, "u": 0, "b": 0, "r": 1, "g": 1},  # RGW
    "bant": {"w": 1, "u": 1, "b": 0, "r": 0, "g": 1},  # GWU
    "mardu": {"w": 1, "u": 0, "b": 1, "r": 1, "g": 0},  # WBR
    "temur": {"w": 0, "u": 1, "b": 0, "r": 1, "g": 1},  # URG
    "abzan": {"w": 1, "u": 0, "b": 1, "r": 0, "g": 1},  # WBG
    "jeskai": {"w": 1, "u": 1, "b": 0, "r": 1, "g": 0},  # WUR
    "sultai": {"w": 0, "u": 1, "b": 1, "r": 0, "g": 1},  # UBG
    "five color": {"w": 1, "u": 1, "b": 1, "r": 1, "g": 1},  # WUBRG
    "all colors": {"w": 1, "u": 1, "b": 1, "r": 1, "g": 1},  # WUBRG
}

color_combinations_abbreviated = {
    "wu": {"w": 1, "u": 1, "b": 0, "r": 0, "g": 0},
    "uw": {"w": 1, "u": 1, "b": 0, "r": 0, "g": 0},  # Azorius
    "ub": {"w": 0, "u": 1, "b": 1, "r": 0, "g": 0},
    "bu": {"w": 0, "u": 1, "b": 1, "r": 0, "g": 0},  # Dimir
    "br": {"w": 0, "u": 0, "b": 1, "r": 1, "g": 0},
    "rb": {"w": 0, "u": 0, "b": 1, "r": 1, "g": 0},  # Rakdos
    "rg": {"w": 0, "u": 0, "b": 0, "r": 1, "g": 1},
    "gr": {"w": 0, "u": 0, "b": 0, "r": 1, "g": 1},  # Gruul
    "gw": {"w": 1, "u": 0, "b": 0, "r": 0, "g": 1},
    "wg": {"w": 1, "u": 0, "b": 0, "r": 0, "g": 1},  # Selesnya
    "wb": {"w": 1, "u": 0, "b": 1, "r": 0, "g": 0},
    "bw": {"w": 1, "u": 0, "b": 1, "r": 0, "g": 0},  # Orzhov
    "ur": {"w": 0, "u": 1, "b": 0, "r": 1, "g": 0},
    "ru": {"w": 0, "u": 1, "b": 0, "r": 1, "g": 0},  # Izzet
    "bg": {"w": 0, "u": 0, "b": 1, "r": 0, "g": 1},
    "gb": {"w": 0, "u": 0, "b": 1, "r": 0, "g": 1},  # Golgari
    "rw": {"w": 1, "u": 0, "b": 0, "r": 1, "g": 0},
    "wr": {"w": 1, "u": 0, "b": 0, "r": 1, "g": 0},  # Boros
    "ug": {"w": 0, "u": 1, "b": 0, "r": 0, "g": 1},
    "gu": {"w": 0, "u": 1, "b": 0, "r": 0, "g": 1},  # Simic
    "wub": {"w": 1, "u": 1, "b": 1, "r": 0, "g": 0},
    "wbu": {"w": 1, "u": 1, "b": 1, "r": 0, "g": 0},
    "uwb": {"w": 1, "u": 1, "b": 1, "r": 0, "g": 0},
    "ubw": {"w": 1, "u": 1, "b": 1, "r": 0, "g": 0},
    "buw": {"w": 1, "u": 1, "b": 1, "r": 0, "g": 0},  # Esper
    "ubr": {"w": 0, "u": 1, "b": 1, "r": 1, "g": 0},
    "urb": {"w": 0, "u": 1, "b": 1, "r": 1, "g": 0},
    "bur": {"w": 0, "u": 1, "b": 1, "r": 1, "g": 0},
    "bru": {"w": 0, "u": 1, "b": 1, "r": 1, "g": 0},
    "rbu": {"w": 0, "u": 1, "b": 1, "r": 1, "g": 0},
    "rub": {"w": 0, "u": 1, "b": 1, "r": 1, "g": 0},  # Grixis
    "brg": {"w": 0, "u": 0, "b": 1, "r": 1, "g": 1},
    "bgr": {"w": 0, "u": 0, "b": 1, "r": 1, "g": 1},
    "rbg": {"w": 0, "u": 0, "b": 1, "r": 1, "g": 1},
    "rgb": {"w": 0, "u": 0, "b": 1, "r": 1, "g": 1},
    "grb": {"w": 0, "u": 0, "b": 1, "r": 1, "g": 1},
    "gbr": {"w": 0, "u": 0, "b": 1, "r": 1, "g": 1},  # Jund
    "rgw": {"w": 1, "u": 0, "b": 0, "r": 1, "g": 1},
    "rwg": {"w": 1, "u": 0, "b": 0, "r": 1, "g": 1},
    "grw": {"w": 1, "u": 0, "b": 0, "r": 1, "g": 1},
    "gwr": {"w": 1, "u": 0, "b": 0, "r": 1, "g": 1},
    "wrg": {"w": 1, "u": 0, "b": 0, "r": 1, "g": 1},
    "wgr": {"w": 1, "u": 0, "b": 0, "r": 1, "g": 1},  # Naya
    "gwu": {"w": 1, "u": 1, "b": 0, "r": 0, "g": 1},
    "guw": {"w": 1, "u": 1, "b": 0, "r": 0, "g": 1},
    "wgu": {"w": 1, "u": 1, "b": 0, "r": 0, "g": 1},
    "wug": {"w": 1, "u": 1, "b": 0, "r": 0, "g": 1},
    "ugw": {"w": 1, "u": 1, "b": 0, "r": 0, "g": 1},
    "uwg": {"w": 1, "u": 1, "b": 0, "r": 0, "g": 1},  # Bant
    "wbr": {"w": 1, "u": 0, "b": 1, "r": 1, "g": 0},
    "wrb": {"w": 1, "u": 0, "b": 1, "r": 1, "g": 0},
    "bwr": {"w": 1, "u": 0, "b": 1, "r": 1, "g": 0},
    "brw": {"w": 1, "u": 0, "b": 1, "r": 1, "g": 0},
    "rwb": {"w": 1, "u": 0, "b": 1, "r": 1, "g": 0},
    "rbw": {"w": 1, "u": 0, "b": 1, "r": 1, "g": 0},  # Mardu
    "urg": {"w": 0, "u": 1, "b": 0, "r": 1, "g": 1},
    "ugr": {"w": 0, "u": 1, "b": 0, "r": 1, "g": 1},
    "rug": {"w": 0, "u": 1, "b": 0, "r": 1, "g": 1},
    "rgu": {"w": 0, "u": 1, "b": 0, "r": 1, "g": 1},
    "gru": {"w": 0, "u": 1, "b": 0, "r": 1, "g": 1},
    "gur": {"w": 0, "u": 1, "b": 0, "r": 1, "g": 1},  # Temur
    "wbg": {"w": 1, "u": 0, "b": 1, "r": 0, "g": 1},
    "wgb": {"w": 1, "u": 0, "b": 1, "r": 0, "g": 1},
    "bwg": {"w": 1, "u": 0, "b": 1, "r": 0, "g": 1},
    "bgw": {"w": 1, "u": 0, "b": 1, "r": 0, "g": 1},
    "gwb": {"w": 1, "u": 0, "b": 1, "r": 0, "g": 1},
    "gbw": {"w": 1, "u": 0, "b": 1, "r": 0, "g": 1},  # Abzan
    "wur": {"w": 1, "u": 1, "b": 0, "r": 1, "g": 0},
    "wru": {"w": 1, "u": 1, "b": 0, "r": 1, "g": 0},
    "uwr": {"w": 1, "u": 1, "b": 0, "r": 1, "g": 0},
    "urw": {"w": 1, "u": 1, "b": 0, "r": 1, "g": 0},
    "rwu": {"w": 1, "u": 1, "b": 0, "r": 1, "g": 0},
    "ruw": {"w": 1, "u": 1, "b": 0, "r": 1, "g": 0},  # Jeskai
    "ubg": {"w": 0, "u": 1, "b": 1, "r": 0, "g": 1},
    "ugb": {"w": 0, "u": 1, "b": 1, "r": 0, "g": 1},
    "bug": {"w": 0, "u": 1, "b": 1, "r": 0, "g": 1},
    "bgu": {"w": 0, "u": 1, "b": 1, "r": 0, "g": 1},
    "gbu": {"w": 0, "u": 1, "b": 1, "r": 0, "g": 1},
    "gub": {"w": 0, "u": 1, "b": 1, "r": 0, "g": 1},  # Sultai
}
