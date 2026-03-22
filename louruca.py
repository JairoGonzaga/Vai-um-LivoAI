# 1. Import the library
from inference_sdk import InferenceHTTPClient

# 2. Connect to your workflow
client = InferenceHTTPClient(
    api_url="https://serverless.roboflow.com",
    api_key="vBDnfqqqASCDVMmOQrwa"
)

# 3. Run your workflow on an image
result = client.run_workflow(
    workspace_name="jairo-s-workspace",
    workflow_id="custom-workflow",
    images={
        "image": "aaa.jpeg" # Path to your image file
    },
    use_cache=True # Speeds up repeated requests
)

# 4. Get your results
print(result)
