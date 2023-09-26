import boto3
import json
from config import Config

boto3.setup_default_session(profile_name="market-mind-julian")


def invoke_sagemaker_endpoint(data):
    client = boto3.client("sagemaker-runtime")
    response = client.invoke_endpoint(
        EndpointName=Config.MODEL_ENDPOINT,
        Body=json.dumps({"inputs": data, "parameters": {"top_k": None}}),
        ContentType="application/json",
    )
    result = response["Body"].read().decode("utf-8")

    return result
