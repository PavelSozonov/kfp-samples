# HDFS File Download Component for Kubeflow Pipelines

This component downloads a file from HDFS using WebHDFS and saves it to a local path. It is designed to be used as part of a Kubeflow Pipeline.

## Component Description

The component accepts the following inputs:
- `delegation_token`: The delegation token for accessing HDFS.
- `hdfs_file_path`: The path to the file in HDFS.
- `local_file_path`: The local path where the file should be saved.

## Instructions

### 1. Setting Up the Component

1. **Set Up Kubeflow Pipelines:**
   Ensure you have Kubeflow Pipelines v2 set up and configured.

2. **Create the Component:**
   Save the provided script into a Python file, for example, `download_file_from_hdfs_component.py`.

3. **Compile and Run the Pipeline:**
   Compile the pipeline and run it in your Kubeflow Pipelines instance. The example pipeline provided demonstrates how to use the component.

### 2. Obtaining a Delegation Token

To interact with HDFS using WebHDFS, you need to obtain a delegation token. Follow these steps:

1. **Authenticate with Kerberos:**
   Use `kinit` to authenticate with your Kerberos principal.

   ```bash
   kinit your-kerberos-principal
   ```

2. **Obtain the Delegation Token:**
   Use `curl` to obtain a delegation token from WebHDFS.

   ```bash
   curl -i -L -k --negotiate -u : "http://<your-namenode-host>:<port>/webhdfs/v1/?op=GETDELEGATIONTOKEN"
   ```

   Replace `<your-namenode-host>` and `<port>` with the appropriate values for your HDFS WebHDFS endpoint.

   The response will contain the delegation token which you will use as input to the component.

## Example Usage

### Python Script

```python
import kfp
from kfp.v2.dsl import component, Input, Output, Dataset
from kfp.v2 import dsl

@component(
    packages_to_install=['requests'],
    base_image='python:3.12'
)
def download_file_from_hdfs(delegation_token: str, hdfs_file_path: str, local_file_path: Output[Dataset]):
    # ... (implementation)

if __name__ == "__main__":
    @dsl.pipeline(
        name='HDFS File Download Pipeline',
        description='A pipeline to download a file from HDFS using WebHDFS'
    )
    def hdfs_download_pipeline(delegation_token: str, hdfs_file_path: str):
        download_file_from_hdfs(
            delegation_token=delegation_token,
            hdfs_file_path=hdfs_file_path,
            local_file_path=dsl.Output(dsl.Dataset, "local_file")
        )

    kfp.v2.compiler.Compiler().compile(hdfs_download_pipeline, 'hdfs_download_pipeline.yaml')
```

Replace `<your-namenode-host>` and `<port>` with the appropriate values for your HDFS WebHDFS endpoint. Ensure that the WebHDFS service is accessible and properly configured to accept the delegation token for authentication.
