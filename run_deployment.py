import click
from typing import cast 
from rich import print
from zenml.integrations.mlflow.mlflow_utils import get_tracking_uri
from zenml.integrations.mlflow.model_deployers.mlflow_model_deployer import (
    MLFlowModelDeployer,
)
from zenml.integrations.mlflow.services import MLFlowDeploymentService
from pipelines.deployment_pipeline import continuous_deployment_pipeline, inference_pipeline


DEPLOY = 'deploy'
PREDICT = 'predict'
DEPLOY_AND_PREDICT = 'deploy_and_predict'

@click.command()
@click.option(
    '--config',
    '-c',
    type=click.Choice([DEPLOY, PREDICT, DEPLOY_AND_PREDICT]),
    default=DEPLOY_AND_PREDICT,
    help='You can choose to deploy the model, predict or both'
)

@click.option(
    '--min-accuracy',
    default=0.92,
    help='Minimum accuracy to deploy the model'
)

def main(config: str, min_accuracy: float):
    mlflow_model_deployer_component = MLFlowModelDeployer.get_active_model_deployer()
    deploy = config == DEPLOY or config == DEPLOY_AND_PREDICT
    predict = config == PREDICT or config == DEPLOY_AND_PREDICT

    if deploy:
        continuous_deployment_pipeline(
            data_path='/Users/alphaprime/programming/projects/ml-ops/data/olist_customers_dataset.csv',
            min_accuracy=min_accuracy,
            workers=3,
            timeout=60,)
    if predict:
        inference_pipeline(
            pipeline_name='continuous_deployment_pipeline',
            pipeline_step_name='mlflow_model_deployer_step',
        )

    
    print(
        "You can run:\n"
        f"[italic green]    mlflow ui --backend-store-uri {get_tracking_uri()}"
        "\n[/italic green]to inspect your experiment runs within the MLFlow UI.\n."
    )

    existing_services = mlflow_model_deployer_component.find_model_server(
        pipeline_name='continuous_deployment_pipeline',
        pipeline_step_name='mlflow_model_deployer_step',
        model_name='model',
    )

    if existing_services:
        service = cast(MLFlowDeploymentService, existing_services[0])
        if service.is_running():
            print(
                f"The MLFlow model server is running locally as a daemon "
                f"process service and accepts inference requests ar: \n"
                f"{service.prediction_url}\n"
                f"To stop service, run "
                f"[italic green]`zenml model-deployer models delete "
                f"{str(service.uuid)}`[/italic green]."
            )
        elif service.is_failed:
            print(
                f"The MLFlow model server is in a failed state. "
                f" Last State: '{service.status.state.value}'\n"
                f" Last Error: '{service.status.last_error}'"
            )
        else:
            print(
                f"The MLFlow model server is not running. "
                f"The deployment pipeline must run first to train the model and deploy it."
                f"Execute the same command with the `--deploy` argument to deploy model."
            )

if __name__ == '__main__':
    main()