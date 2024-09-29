"""Simulation pipeline."""

from kedro.pipeline import Pipeline, node
from .nodes import (
    create_players, 
    assign_decks_to_players, 
    simulate_player_matches)

def create_simulation_pipeline(**kwargs) -> Pipeline:
    return Pipeline(
        [
            node(
                func=create_players,
                inputs="params:simulation.n_players",
                outputs="players",
                name="create_players_node"
            ),
            node(
                func=assign_decks_to_players,
                inputs=["players", 
                        "sampled_decks", 
                        "params:simulation.log_folder"],
                outputs="players_with_decks",
                name="assign_decks_node"
            ),
            node(
                func=simulate_player_matches,
                inputs=["params:simulation", 
                        "players_with_decks"],
                outputs="matches_df",
                name="simulate_player_matches_node"
            )
        ]
    )
