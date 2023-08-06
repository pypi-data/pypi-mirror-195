import aws_cdk as cdk
from constructs import Construct


class BranchCICDStack(cdk.Stack):
    def __init__(self, scope: Construct):
        super().__init__(scope, "CICDStack")


