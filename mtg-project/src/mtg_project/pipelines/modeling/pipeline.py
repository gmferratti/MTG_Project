from kedro.pipeline import node, Pipeline
from .nodes import (
    get_deck_zip_from_web,
    pp_decks_from_json_files,
    sample_decks)

def create_pipeline(**kwargs) -> Pipeline:
    return Pipeline(
        [
            node(
                func=get_deck_zip_from_web,
                inputs=[
                    "params:global.user.project_path",
                    "params:preprocessing.webscraper.zip_url",
                    "params:preprocessing.webscraper.zip_folder"
                ],
                outputs=None,
                name="get_deck_zip_from_web_node"
            ),
            node(
                func=pp_decks_from_json_files,
                inputs=[
                    "decks_json_partitioned",
                    "params:preprocessing.webscraper.deck_cards",
                    "params:preprocessing.webscraper.log_folder"
                ],
                outputs="decks_txt_partitioned",
                name="pp_decks_from_json_files_node"
            ),
            node(
                func=sample_decks,
                inputs=[
                    "decks_txt_partitioned",
                    "params:preprocessing.webscraper.sample_size_ratio",
                    "params:preprocessing.webscraper.log_folder"
                ],
                outputs="sampled_decks",
                name="sampling_decks_node"
            ),
            # PLACEHOLDER, SAVE TO DB 
        ]
    )