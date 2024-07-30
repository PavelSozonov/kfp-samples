# Install required library
# !pip install kfp

# Import required libraries
import kfp
from kfp import dsl
from kfp.dsl import Dataset, Output
from kfp.v2 import compiler
from kfp.v2.google.client import AIPlatformClient

# Define the pipeline steps
@dsl.component
def generate_file(str_amount: int, output_path: Output[Dataset]):
    with open(output_path.path, 'w') as f:
        for _ in range(str_amount):
            f.write("hello world\n")

@dsl.component
def print_file(input_path: Dataset):
    with open(input_path.path, 'r') as f:
        for line in f:
            print(line.strip())

# Create the pipeline
@dsl.pipeline(
    name='Hello World Pipeline',
    description='A pipeline that generates and prints a hello world file.'
)
def hello_world_pipeline(str_amount: int):
    generate_task = generate_file(str_amount=str_amount)
    print_task = print_file(input_path=generate_task.outputs['output_path'])

# Compile the pipeline
compiler.Compiler().compile(
    pipeline_func=hello_world_pipeline,
    package_path='hello_world_pipeline.json'
)

# Specify the project and region where you want to run the pipeline
PROJECT_ID = 'your-gcp-project-id'
REGION = 'your-gcp-region'

# Initialize the AI Platform (Unified) client
api_client = AIPlatformClient(
    project_id=PROJECT_ID,
    region=REGION,
)

# Run the pipeline
response = api_client.create_run_from_job_spec(
    job_spec_path='hello_world_pipeline.json',
    pipeline_root='gs://your-bucket/pipeline-root',
    parameter_values={'str_amount': 5},
)
