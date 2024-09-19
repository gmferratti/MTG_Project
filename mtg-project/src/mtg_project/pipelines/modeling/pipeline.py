from kedro.pipeline import node, Pipeline
from .nodes import (
    feature_engineering,
    feature_selection,
    train_test_split
)

def create_modeling_pipeline(**kwargs) -> Pipeline:
    return Pipeline(
        [
            node(
                func=feature_engineering,
                inputs=["matches_df"],
                outputs="features_df",
                name="feature_engineering_node",
            ),
            node(
                func=feature_selection,
                inputs=["features_df", 
                        "params:modeling.feature_engineering.feat_corr_threshold"],
                outputs=["selected_features_df",
                         "selected_features_cols"],
                name="feature_selection_node",
            ),
            node(
                func=train_test_split,
                inputs=[
                    "selected_features_df",
                    "params:modeling.feature_selection.target_column",
                    "selected_features_cols",
                    "params:modeling.feature_selection.hide_players",
                    "params:modeling.feature_selection.n_test_players",
                    "params:modeling.feature_selection.hide_advanced_turns",
                    "params:modeling.feature_selection.turn_threshold",
                ],
                outputs=[
                    "train_features",
                    "test_features",
                    "train_target",
                    "test_target",
                ],
                name="split_train_test_node"
            ),
        ]
    )