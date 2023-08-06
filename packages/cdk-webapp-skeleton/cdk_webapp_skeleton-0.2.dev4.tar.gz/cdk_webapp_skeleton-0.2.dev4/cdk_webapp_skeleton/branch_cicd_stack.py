import aws_cdk as cdk
from aws_cdk import (
    pipelines as pipelines,
    aws_codebuild as codebuild,
    aws_ssm as ssm,
    aws_iam as iam,
    aws_s3 as s3,
)
from constructs import Construct


class BranchCICDStack(cdk.Stack):
    def __init__(self, scope: Construct, source: pipelines.CodePipelineSource=None):
        super().__init__(scope, "CICDStack")

        assert source is not None

        cache_bucket = s3.Bucket(
            self,
            "CacheBucket",
            removal_policy=cdk.RemovalPolicy.DESTROY,
            auto_delete_objects=True,
        )

        synth_step = pipelines.ShellStep(
            "Synth",
            input=source,
            # env={"BRANCH": deploy_env.github_branch(), },
            commands=["./synth.sh"]
        )
        cdk_pipeline = pipelines.CodePipeline(
            self,
            "Pipeline",  # Pipeline name gets the stack name prepended
            synth=synth_step,
            code_build_defaults=pipelines.CodeBuildOptions(
                build_environment=codebuild.BuildEnvironment(
                    compute_type=codebuild.ComputeType.SMALL
                ),
                cache=codebuild.Cache.bucket(cache_bucket),
            ),
            cross_account_keys=False
        )
