from subprocess import Popen, PIPE
import shlex
from confluent.cli.commands.login import confluent_cli
from utils.parsers import OutputParser, OutputEnum

class KafkaCluster:
  def __new__(cls, *args, **kwargs):
    return super().__new__(cls)
  
  def __init__(self):
    self._parser = OutputParser()

  def list(self, env: str = '--all', parse: bool = True, output: OutputEnum = OutputEnum.human): 
    if(not env == '--all'): 
      command_line = f'{confluent_cli} kafka cluster list --environment {env} --output {output.name}'
    else:
      command_line = f'{confluent_cli} kafka cluster list --all --output {output.name}'
      
    args = shlex.split(command_line)
    pipe = Popen(args=args, stdout=PIPE)
    result = pipe.communicate()
    
    if(not parse): return result
    
    return self._parser(result, output)

