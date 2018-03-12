import json
from Schemas import JobInputSchema


def data_loader(input_data):
    """
    This method loads the input data into Job.

    Args:
        input_data: This is the input data parameter.

    Returns:
        This returns a Job Object.
    """
    schema = JobInputSchema()
    job_input = schema.load(input_data)
    return job_input


if __name__ == '__main__':
    data = json.load(open('data.json'))
    job = data_loader(data)
    print('Job Filled')