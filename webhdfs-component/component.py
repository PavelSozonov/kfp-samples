import kfp
from kfp.v2.dsl import component, Input, Output, Dataset
from kfp.v2 import dsl
import requests

@component(
    packages_to_install=['requests'],
    base_image='python:3.12'
)
def download_file_from_hdfs(delegation_token: str, hdfs_file_path: str, local_file_path: Output[Dataset]):
    """
    Downloads a file from HDFS using WebHDFS.

    Args:
        delegation_token (str): Delegation token for accessing HDFS.
        hdfs_file_path (str): Path to the file in HDFS.
        local_file_path (Output[Dataset]): Local path where the file should be saved.
    """
    # Construct WebHDFS URL
    webhdfs_url = f"http://<your-namenode-host>:<port>/webhdfs/v1{hdfs_file_path}?op=OPEN&delegation={delegation_token}"

    # Send the GET request to WebHDFS
    response = requests.get(webhdfs_url, allow_redirects=True)

    # Check if the request was successful
    if response.status_code == 200:
        # Write the content to the local file
        with open(local_file_path.path, 'wb') as f:
            f.write(response.content)
    else:
        raise Exception(f"Failed to download file from HDFS. Status code: {response.status_code}, Response: {response.text}")

if __name__ == "__main__":
    # Define the pipeline
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

    # Compile the pipeline
    kfp.v2.compiler.Compiler().compile(hdfs_download_pipeline, 'hdfs_download_pipeline.yaml')
