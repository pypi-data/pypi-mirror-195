__package__ = 'exp'

# ------- start -------
from confattr import ConfigFileCommand, Include
ConfigFileCommand.delete_command_type(Include)
# ------- end -------

from confattr import Message
Message.__str__ = Message.format_msg_line  # type: ignore [assignment]

from os.path import dirname, join
with open(join(dirname(__file__), 'example.py'), 'rt') as f:
	exec(f.read())
