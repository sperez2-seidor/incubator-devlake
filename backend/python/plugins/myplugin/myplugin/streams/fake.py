import json
from datetime import datetime
from myplugin.models import FakePipeline

from myplugin.models import FakeConnection, FakeProject, FakeScopeConfig, FakePipeline
from pydevlake import Plugin, Stream, RemoteScopeGroup, DomainType, TestConnectionResult
from pydevlake.domain_layer.devops import CicdScope, CICDPipeline, CICDStatus, CICDResult, CICDType\

class FakePipelineStream(Stream):
    tool_model = FakePipeline
    domain_types = [DomainType.CICD]

    def collect(self, state, context):
        for p in self.generate_fake_pipelines():
            yield json.loads(p.json()), {}

    def convert(self, pipeline: FakePipeline, ctx):
        env = ctx.scope_config.env
        yield CICDPipeline(
            name=pipeline.id,
            status=self.convert_status(pipeline.state),
            finished_date=pipeline.finished_at,
            result=self.convert_result(pipeline.state),
            duration_sec=self.duration(pipeline),
            environment=env,
            type=CICDType.BUILD
        )

    def convert_status(self, state: FakePipeline.State):
        if state == FakePipeline.State.FAILURE or state == FakePipeline.State.SUCCESS:
            return CICDStatus.DONE
        else:
            return CICDStatus.IN_PROGRESS

    def convert_result(self, state: FakePipeline.State):
        if state == FakePipeline.State.SUCCESS:
            return CICDResult.SUCCESS
        elif state == FakePipeline.State.FAILURE:
            return CICDResult.FAILURE
        else:
            return None

    def duration(self, pipeline: FakePipeline):
        if pipeline.finished_at:
            return (pipeline.finished_at - pipeline.started_at).seconds
        return None

    @classmethod
    def generate_fake_pipelines(cls) -> list[FakePipeline]:
        states = [FakePipeline.State.SUCCESS, FakePipeline.State.FAILURE, FakePipeline.State.PENDING]
        fake_pipelines = []
        for i in range(250):
            fake_pipelines.append(FakePipeline(
                id=i,
                state=states[i % len(states)],
                started_at=datetime(2023, 1, 10, 11, 0, 0, microsecond=i),
                finished_at=datetime(2023, 1, 10, 11, 3, 0, microsecond=i),
            ))
        return fake_pipelines