from kfp import dst, compiler, Client
from kfp.dsl import Dataset, Output, OutputPath, InputPath

import warnings


# Define Container Component using custom Docker image
@dsl.container_component
def generate_file(str_amount: int, output_path: Output[Dataset]):
    return dsl.ContainerSpec(
        image='custom-kfp-component:latest',
        command=['python', 'app.py'],
        args=[
            '--str_amount', str_amount,
            '--output_path', output_path.path
        ]
    )

# Define Python Component to print the file
@dsl.component(base_image="python:3.12",
    pip_index_urls=["https://internal-repo", "https://internal-repo/repository/repo-name/simple"],
    packages_to_install=[]
)
def print_file(input_path: Dataset):
    with open(input_path.path, 'r') as f:
        for line in f:
            print(line.strip())

# Create Pipeline
@dsl.pipeline(
    name='Hello World Pipeline',
    description='A pipeline that generates and prints a hello world file.'
)
def hello_world_pipeline(str_amount: int) -> Dataset:
    generate_task = generate_file(str_amount=str_amount)
    print_task = print_file(input_path=generate_task.outputs['output_path'])
    return generate_task.outputs['output_path'] # Pipeline can be used as a component

# Compile the Pipeline
compiler.Compiler().compile(
    pipeline_func=hello_world_pipeline,
    package_path='hello_world_pipeline_custom_image.yaml'
)

# Run the Pipeline
warnings simplefilter(action='ignore', category=FutureWarning) # Ignore kfp version warning
run = Client().create_run_from_pipeline_package(
    'hello_world_pipeline_custom_image.yaml',
    experiment_name="Default",
    arguments={'str_amount': 4}
)
