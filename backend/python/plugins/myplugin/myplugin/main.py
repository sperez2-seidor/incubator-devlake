from typing import Iterable
from pydantic import SecretStr

import pydevlake as dl
from pydevlake.domain_layer.devops import CicdScope
from myplugin.api import CommerceCloudAPI

from myplugin.models import CommerceCloudConnection
from myplugin.streams.fake import FakePipelineStream

class MyPluginScopeConfig(dl.ScopeConfig):
    pass

class MyPluginToolScope(dl.ToolScope):
    type: str

class MyScope(dl.DomainScope):
    name: str
    description: str

class MyPlugin(dl.Plugin):
    connection_type = CommerceCloudConnection
    tool_scope_type = MyPluginToolScope
    scope_config_type = MyPluginScopeConfig
    streams = [FakePipelineStream]

    def domain_scopes(self, tool_scope: MyScope) -> Iterable[dl.DomainScope]:
        yield CicdScope(
            name=tool_scope.name,
            description=tool_scope.description,
            url="dummy_url",
        )

    def remote_scope_groups(self, connection: CommerceCloudConnection) -> Iterable[dl.RemoteScopeGroup]:
        yield dl.RemoteScopeGroup(
            id=connection.subscription_code,
            name=connection.name,
        )

    def remote_scopes(self, connection: CommerceCloudConnection, group_id: str) -> Iterable[MyPluginToolScope]:
        api = CommerceCloudAPI(connection)
        environments = api.get_environments()
        for environment in environments:
            yield MyPluginToolScope(
                id=environment['code'],
                name=environment['name'],
                type=environment['type'],
            )

    def test_connection(self, connection: CommerceCloudConnection) -> dl.TestConnectionResult:
        api = CommerceCloudAPI(connection)
        response = api.get_environments()
        return dl.TestConnection.from_api_response(response)


if __name__ == '__main__':
    MyPlugin.start()
