import sagemaker
import boto3
from sagemaker.huggingface.model import HuggingFaceModel
from sagemaker.serverless import ServerlessInferenceConfig

# set up aws credentials
boto3.setup_default_session(profile_name="market-mind-julian")
session = boto3.Session(profile_name="market-mind-julian")
sess = sagemaker.Session(boto_session=session)
# sagemaker session bucket -> used for uploading data, models and logs
# sagemaker will automatically create this bucket if it not exists
sagemaker_session_bucket = None
if sagemaker_session_bucket is None and sess is not None:
    # set to default bucket if a bucket name is not given
    sagemaker_session_bucket = sess.default_bucket()

# get role with permissions to create an Endpoint
try:
    role = sagemaker.get_execution_role()
except ValueError:
    iam = session.client("iam")
    role = iam.get_role(RoleName="sagemaker_execution_role")["Role"]["Arn"]

sess = sagemaker.Session(default_bucket=sagemaker_session_bucket, boto_session=session)

print(f"sagemaker role arn: {role}")
print(f"sagemaker bucket: {sess.default_bucket()}")
print(f"sagemaker session region: {sess.boto_region_name}")


# Hub Model configuration. <https://huggingface.co/models>
hub = {
    "HF_MODEL_ID": "j-hartmann/emotion-english-distilroberta-base",
    "HF_TASK": "text-classification",
}

# create Hugging Face Model Class
huggingface_model = HuggingFaceModel(
    env=hub,  # configuration for loading model from Hub
    role=role,  # iam role with permissions to create an Endpoint
    transformers_version="4.26",  # transformers version used
    pytorch_version="1.13",  # pytorch version used
    py_version="py39",  # python version used
)

# set up serverless inference configuration
serverless_config = ServerlessInferenceConfig(
    memory_size_in_mb=3072,
    max_concurrency=3,
)

# deploy the endpoint endpoint
predictor = huggingface_model.deploy(serverless_inference_config=serverless_config)

# test the endpoint
res = predictor.predict(
    data={"inputs": ["good", "bad", "okay"], "parameters": {"top_k": None}}
)
print(res)
