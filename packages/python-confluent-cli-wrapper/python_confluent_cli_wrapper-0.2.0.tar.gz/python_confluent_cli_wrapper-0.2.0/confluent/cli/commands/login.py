from subprocess import Popen, PIPE
import shlex
import os

confluent_cli=os.getenv('CONFLUENT_CLI') or '/usr/bin/confluent'

def login() -> str:
  command_line = f'{confluent_cli} login'
  args = shlex.split(command_line)
  pipe = Popen(args=args, stdout=PIPE)
  return pipe.communicate()[0]



