import responses

from pyfakefs.fake_filesystem_unittest import Patcher
from pytest import fixture

from ritdu_slacker.api import SlackClient
from ritdu_slacker.cli import SlackMessageCLI


@fixture
def mocked_responses():
    with responses.RequestsMock() as rsps:
        yield rsps


@fixture
def slack():
    yield SlackClient()


@fixture
def cli(slack):
    yield SlackMessageCLI(slack)

@fixture
def fs():
    with Patcher(allow_root_user=False) as patcher:
        yield patcher.fs
