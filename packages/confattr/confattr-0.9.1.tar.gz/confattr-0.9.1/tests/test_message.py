#!../venv/bin/pytest -s

from confattr import Message, NotificationLevel

import pytest

@pytest.fixture(autouse=True)
def reset() -> None:
	Message.reset()



def test__show_file_name_on_first() -> None:
	m = Message(NotificationLevel.ERROR, 'error', file_name='foo')

	assert str(m) == '''\
While loading foo:
error'''

def test__dont_repeat_file_name() -> None:
	messages = [
		Message(NotificationLevel.ERROR, 'info', file_name='/tmp/foo'),
		Message(NotificationLevel.ERROR, 'error', file_name='/tmp/foo'),
	]

	assert '\n'.join(str(m) for m in messages) == '''\
While loading /tmp/foo:
info
error'''

def test__different_file_names() -> None:
	messages = [
		Message(NotificationLevel.ERROR, 'info', file_name='/tmp/foo'),
		Message(NotificationLevel.ERROR, 'error', file_name='/tmp/foo'),
		Message(NotificationLevel.ERROR, 'another error', file_name='/tmp/bar'),
	]

	assert '\n'.join(str(m) for m in messages) == '''\
While loading /tmp/foo:
info
error

While loading /tmp/bar:
another error'''



def test__no_file_name() -> None:
	messages = [
		Message(NotificationLevel.ERROR, 'info'),
		Message(NotificationLevel.ERROR, 'error'),
		Message(NotificationLevel.ERROR, 'another error'),
	]

	assert '\n'.join(str(m) for m in messages) == '''\
info
error
another error'''

def test__no_file_name_after_file_name() -> None:
	messages = [
		Message(NotificationLevel.ERROR, 'info', file_name='foo'),
		Message(NotificationLevel.ERROR, 'error', file_name='foo'),
		Message(NotificationLevel.ERROR, 'another error'),
	]

	assert '\n'.join(str(m) for m in messages) == '''\
While loading foo:
info
error

another error'''


def test__reset() -> None:
	m = Message(NotificationLevel.ERROR, 'error', file_name='foo')

	assert str(m) == '''\
While loading foo:
error'''

	Message.reset()
	assert str(m) == '''\
While loading foo:
error'''
