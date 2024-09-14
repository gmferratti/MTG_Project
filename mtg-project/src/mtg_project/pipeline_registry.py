"""Project pipelines."""
from kedro.pipeline import Pipeline
from src.mtg_project.pipelines.webscraping.pipeline import create_pipeline

def register_pipelines() -> dict[str, Pipeline]:
    return {
        "__default__": create_pipeline(),
        "webscraping": create_pipeline(),
    }
