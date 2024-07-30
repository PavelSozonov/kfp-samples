from kfp import dsl
from kfp.v2 import compiler
from kfp.v2.dsl import Output, Dataset

# Define Container Component using custom Docker image
@dsl.component(
    base_image='your-docker-repo/hello-world-app:latest'
)
def generate_file(str_amount: int, output_path: Output[Dataset]):
    # This component will use the Docker container to run app.py
    # The Docker image should handle the file generation based on the provided arguments
    pass

# Define Python Component to print the file
@dsl.component
def print_file(input_path: Dataset):
    with open(input_path.path, 'r') as f:
        for line in f:
            print(line.strip())

# Create Pipeline
@dsl.pipeline(
    name='Hello World Pipeline',
    description='A pipeline that generates and prints a hello world file.'
)
def hello_world_pipeline(str_amount: int):
    generate_task = generate_file(str_amount=str_amount)
    print_task = print_file(input_path=generate_task.outputs['output_path'])

# Compile the Pipeline
compiler.Compiler().compile(
    pipeline_func=hello_world_pipeline,
    package_path='hello_world_pipeline.json'
)
