# ritdu-slacker
pip installable bin to interact with the Ringier SA internal interface for slack.
Provides both CLI and Native Lib functionality.

## Motivation
- Single implementation of a wrapper around our internal slack interface.

## Installation
```bash
$ pip install ritdu-slacker
```

## Usage

### CLI
To send a message to a slack channel from within a thread:
```bash
$ ritdu-slacker message --workspace "${SLACK_WORKSPACE}" --channel "${SLACK_CHANNEL//#}" --text "Update in progress" --thread-uuid "${thread_uuid}" --thread-broadcast
```

To replace a message send a new one with the same message-uuid:
```bash
$ ritdu-slacker message --workspace "${SLACK_WORKSPACE}" --channel "${SLACK_CHANNEL//#}" --text "Update complete!" --message-uuid "${message_uuid}"
```

To send a message and file to a thread in a slack channel:
```bash
$ ritdu-slacker file --workspace "${SLACK_WORKSPACE}" --channel "${SLACK_CHANNEL//#}" --text "Oops!" --file "/tmp/errorlog.txt" --thread-uuid "${thread_uuid}"
```

### Python

```
from ritdu_slacker.api import SlackClient
client = SlackClient()
client.post_message("via python api","ringier-southafrica","#pe-alerts")
{'message_uuid': '9890b802-fac3-4e61-bbe8-b53cc17fc581', 'message_ts': '1677473299.255969', 'thread_uuid': '9890b802-fac3-4e61-bbe8-b53cc17fc581', 'thread_ts': '1677473299.255969', 'channel': 'CV3JFH08J'}
```

## Development

To setup your development environment:

```
$ make setup-dev
```

Running make on its own generates help documentation:

```
$ make
build                Build the package
check                Check the package
clean                Clean the package
dev                  Setup development environment
format               Format the code
install-prod         Install production dependencies
install              Install all dependencies
lint                 Lint the code
lock                 Update dependency lockfile
publish              Publish the package
test                 Test the package
version              Generate version from GitHub tag
vscode               Update VSCode settings
```

Please read the _Makefile_ to see what each task does.
