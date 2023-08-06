import builtins
import json
import os
import sys

import pytest
import responses


def test_no_arguments(capsys, cli):
    sys.argv = [
        'ritdu-slacker',
    ]

    with pytest.raises(SystemExit):
        cli.main()

    out, _ = capsys.readouterr()

    assert out == """Usage: ritdu-slacker [OPTIONS] COMMAND [ARGS]...

  CLI tool send/update slack messages and send files

Options:
  -h, --help  Show this message and exit.
  --version   Show the version and exit.

Commands:
  file     Command to send file to thread
  message  Command to send message, reply to thread or reply and...
"""


def test_message_slack_channel_no_thread(capsys, cli, mocked_responses):
    sys.argv = [
        'ritdu-slacker',
        'message',
        '--workspace',
        'myworkspace',
        '--channel',
        'mychannel',
        '--text',
        'Update in progress',
        '--thread-uuid',
        '30D06A8F-B6BE-43BD-BE75-8716C26C1102',
        '--thread-broadcast',
    ]

    response_payload = {
        'ok': True,
        'channel': 'C123456',
        'message': {
            'text': 'Update in progress',
            'type': 'message',
        },
    }

    mocked_responses.add(
        responses.POST,
        'https://slacker.cube-services.net/api/message-template',
        json=response_payload
    )

    with pytest.raises(SystemExit):
        cli.main()

    out, _ = capsys.readouterr()

    assert out == json.dumps(response_payload) + "\n"


def test_message_replace_message(capsys, cli, mocked_responses):
    sys.argv = [
        'ritdu-slacker',
        'message',
        '--workspace',
        'myworkspace',
        '--channel',
        'mychannel',
        '--text',
        'Update in progress',
        '--message-uuid',
        '30D06A8F-B6BE-43BD-BE75-8716C26C1102',
    ]

    response_payload = {
        'ok': True,
        'channel': 'C123456',
        'message': {
            'text': 'Update in progress',
            'type': 'message',
        },
    }

    mocked_responses.add(
        responses.POST,
        'https://slacker.cube-services.net/api/message-template',
        json=response_payload
    )

    with pytest.raises(SystemExit):
        cli.main()

    out, _ = capsys.readouterr()
    assert out == json.dumps(response_payload) + "\n"


def test_file(capsys, cli, fs, mocked_responses):
    sys.argv = [
        'ritdu-slacker',
        'file',
        '--workspace',
        'myworkspace',
        '--channel',
        'mychannel',
        '--text',
        'Oops!',
        '--file',
        '/tmp/errorlog.txt',
        '--thread-uuid',
        '30D06A8F-B6BE-43BD-BE75-8716C26C1102',
    ]

    fs.create_file('/tmp/errorlog.txt', contents='This is a test')

    response_payload = {
        'ok': True,
        'channel': 'C123456',
        'message': {
            'text': 'Oops!',
            'type': 'message',
        },
    }

    mocked_responses.add(
        responses.POST,
        'https://slacker.cube-services.net/api/message-template',
        json=response_payload
    )

    with pytest.raises(SystemExit):
        cli.main()

    out, _ = capsys.readouterr()
    assert out == json.dumps(response_payload) + "\n"
