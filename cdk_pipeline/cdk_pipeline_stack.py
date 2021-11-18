from aws_cdk import (
    core as cdk,
    aws_codebuild as codebuild,
    aws_codecommit as codecommit,
    pipelines
)

class CdkPipelineStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        code_commit_source = codecommit.Repository.from_repository_name(self, "ExRepo", repository_name=self.node.try_get_context('repo')) if codecommit.Repository.from_repository_name(self, "TmpRepo", repository_name=self.node.try_get_context('repo')) else codecommit.Repository(self, "NewRepo", repo_name=self.node.try_get_context('repo'))

        

        pipeline = pipelines.CodePipeline(self,
            id='Pipeline',
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