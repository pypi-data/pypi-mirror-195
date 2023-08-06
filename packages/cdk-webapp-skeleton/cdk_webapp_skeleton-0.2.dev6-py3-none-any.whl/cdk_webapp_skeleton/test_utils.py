from aws_cdk import (
    assertions
)
import json


def print_template(template: assertions.Template):
    print(json.dumps(template.to_json(), indent=4))
