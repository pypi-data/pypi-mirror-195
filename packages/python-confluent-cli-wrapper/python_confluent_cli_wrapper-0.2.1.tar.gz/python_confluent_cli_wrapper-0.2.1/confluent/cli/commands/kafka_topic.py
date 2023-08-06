from subprocess import Popen, PIPE
import shlex
from confluent.cli.commands.login import confluent_cli, login
from confluent.cli.utils.parsers import OutputParser, OutputEnum

class KafkaTopic:
  def __new__(cls, *args, **kwargs):
    return super().__new__(cls)
  
  def __init__(self):
    self._parser = OutputParser()

  def list(self, cluster: str, env: str, parse: bool = True, output: OutputEnum = OutputEnum.human): 
    login()
    command_line = f'{confluent_cli} kafka topic list --environment {env} --cluster {cluster} --output {output.name}'
    args = shlex.split(command_line)
    pipe = Popen(args=args, stdout=PIPE)
    result = pipe.communicate()
    
    if(not parse): return result
    
    return self._parser(result, output)

  def describe(self, cluster: str, topic: str, env: str, parse: bool = True, output: OutputEnum = OutputEnum.human): 
    login()
    command_line = f'{confluent_cli} kafka topic describe {topic} --environment {env} --cluster {cluster} --output {output.name}'
    args = shlex.split(command_line)
    pipe = Popen(args=args, stdout=PIPE)
    result = pipe.communicate()
    
    if(not parse): return result
    
    return self._parser(result, output)
