from aws_cdk import (
    core as cdk,
    aws_codebuild as codebuild,
    aws_codecommit as codecommit,
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
            synth= pipelines.ShellStep(
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