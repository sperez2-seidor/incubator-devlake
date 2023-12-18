import os
import pytest

from pydevlake.testing import assert_valid_plugin, assert_plugin_run

from myplugin.models import CommerceCloudConnection
from myplugin.main import MyPlugin, MyPluginScopeConfig

from unittest import TestCase

def test_valid_plugin():
    assert_valid_plugin(MyPlugin())



def test_valid_plugin_and_connection():
    token = os.environ.get('COMMERCE_CLOUD_TOKEN')
    if not(token):
        pytest.skip("No Commerce Cloud token provided")


    subscription_code = os.environ.get('COMMERCE_CLOUD_SUBSCRIPTION_CODE')
    if not(subscription_code):
        pytest.skip("No Commerce Cloud subscription code provided")

    plugin = MyPlugin()
    connection = CommerceCloudConnection(id=1, name='test_connection', token=token, subscription_code=subscription_code)
    scope_config = MyPluginScopeConfig(id=1, name='test_config')
    assert_plugin_run(plugin, connection, scope_config)