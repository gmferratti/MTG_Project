from kedro.pipeline import Pipeline, node

from .nodes import (
    feature_engineering,
    feature_selection,
    fit_model,
    predict_and_evaluate_model,
    train_test_split,
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
                inputs=[
                    "features_df",
                    "params:modeling.feature_engineering.feat_corr_threshold",
                ],
                outputs=["selected_features_df", "selected_features_cols"],
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
                name="split_train_test_node",
            ),
            node(
                func=fit_model,
                inputs=[
                    "train_features",
                    "train_target",
                    "params:modeling.model_selection.params_grid",
                ],
                outputs=["best_model", "best_hiper_params"],
                name="fit_decision_tree_model_node",
            ),
            node(
                func=predict_and_evaluate_model,
                inputs=["best_model", "test_features", "test_target"],
                outputs=["predicted_target", "shap_values", "error_metrics"],
                name="predict_and_evaluate_model_node",
            ),
        ]
    )
