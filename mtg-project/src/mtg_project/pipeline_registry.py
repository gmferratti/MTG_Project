"""Project pipelines."""
from kedro.pipeline import Pipeline, pipeline
from src.mtg_project.pipelines.webscraping.pipeline import create_webscraping_pipeline
from src.mtg_project.pipelines.simulation.pipeline import create_simulation_pipeline
from src.mtg_project.pipelines.modeling.pipeline import create_modeling_pipeline
#from src.mtg_project.pipelines.inference.pipeline import inference_pipeline

def register_pipelines() -> dict[str, Pipeline]:
    
    webscraping_pipeline = create_webscraping_pipeline()
    simulation_pipeline = create_simulation_pipeline()
    modeling_pipeline = create_modeling_pipeline()

    complete_pipeline = pipeline(
            pipe= webscraping_pipeline + simulation_pipeline + modeling_pipeline
        )
    
    return {
        "__default__": complete_pipeline,
        "webscraping": webscraping_pipeline,
        "simulation": simulation_pipeline,
        "modeling": modeling_pipeline,
#        'inference': inference_pipeline
    }
