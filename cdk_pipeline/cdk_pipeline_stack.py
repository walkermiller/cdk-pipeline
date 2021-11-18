from aws_cdk import (
    core as cdk,
    aws_codebuild as codebuild,
    aws_codecommit as codecommit,
    aws_s3 as s3,
    pipelines
)

class CdkPipelineStack(cdk.Stack):
    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        ## Use an existing repo if it exists, otherwise create a new one
        code_commit_source = codecommit.Repository(self, "NewRepo", repository_name=self.node.try_get_context('repo'))

        pipeline = pipelines.CodePipeline(self,
            id='Pipeline',
            pipeline_name=self.node.try_get_context('repo'),
            self_mutation=False,
            synth=pipelines.ShellStep(
                id="cdksynth",
                commands=[
                        "pip install -r requirements.txt",
                        "npm install -g aws-cdk",
                        "cdk synth"
                    ],
                input=pipelines.CodePipelineSource.code_commit(
                        repository=code_commit_source,
                        branch="main")
            ))
        pipeline.add_stage(MyApp(self,"Dev"))

class S3Bucket(cdk.Stack):
    def __init__(self, scope, id):
        super().__init__(scope, id)
        s3.Bucket(self, id="Bucket")

class MyApp(cdk.Stage):
    def __init__(self, scope, id, *, env=None, outdir=None):
        super().__init__(scope, id, env=env, outdir=outdir)
        bucket_stack = S3Bucket(self, "NucketStack")
