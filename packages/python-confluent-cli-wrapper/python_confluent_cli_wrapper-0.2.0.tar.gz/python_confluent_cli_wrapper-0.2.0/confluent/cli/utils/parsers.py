from enum import Enum
from json import encoder, decoder
import ruamel.yaml

def parseAsciiTable(ascii_table: str, strip: bool = True):
  header = []
  data = []
  for line in ascii_table.split('\n'):
    if '-+-' in line: continue
    cells = list(filter(lambda x: x!='|', line.split('|')))
    
    if(strip): cells = list(map(lambda c: c.strip(), cells))
    if not header:
      header = cells
      continue
    data.append(cells)
    
  return header, data


class OutputEnum(Enum):
  human = 1
  json = 2
  yaml = 3

class OutputParser:
  def __new__(cls, *args, **kwargs):
    return super().__new__(cls)
  
  def __init__(self):
    self._jdecoder = decoder.JSONDecoder()
    self._jencoder = encoder.JSONEncoder(indent=2)
    self._yaml = ruamel.yaml.YAML()

  def parseOutput(self, result: list, output = OutputEnum.human):
    match output:
      case OutputEnum.human:
        return parseAsciiTable(result[0].decode())
      case OutputEnum.json:
        return self._jdecoder.decode(result[0].decode())
      case OutputEnum.yaml:
        return self._yaml.load(result[0].decode())
      
