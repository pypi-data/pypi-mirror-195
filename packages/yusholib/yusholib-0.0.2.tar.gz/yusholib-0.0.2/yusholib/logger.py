from typing import Literal
from pystyle import Colors

class Logger:
  
  w = Colors.white
  r = Colors.red
  y = Colors.yellow
  c = Colors.cyan
  g = Colors.green
  re = Colors.reset
  
  separator = f'{re}{w}:: '
  
  err_prefix = f'{re}{r}ERROR   {separator}'
  wrn_prefix = f'{re}{y}WARN    {separator}'
  suc_prefix = f'{re}{g}SUCCESS {separator}'
  inf_prefix = f'{re}{c}INFO    {separator}'
  dbg_prefix = f'{re}{w}DEBUG   {separator}'
  
  def __init__(self, level: Literal['error', 'warn', 'success', 'info', 'debug']):
    if level == 'error':
        self.level = 0
    elif level == 'warn':
        self.level = 1
    elif level == 'success' or level =='info':
        self.level = 2
    elif level == 'debug':
        self.level = 3

  def error(self, message):
    if 0 <= self.level:
      print(f'{self.err_prefix}{message}{self.re}')

  def warn(self, message):
    if 1 <= self.level:
      print(f'{self.wrn_prefix}{message}{self.re}')

  def success(self, message):
    if 2 <= self.level:
      print(f'{self.suc_prefix}{message}{self.re}')
    
  def info(self, message):
    if 2 <= self.level:
      print(f'{self.inf_prefix}{message}{self.re}')

  def debug(self, message):
    if 3 <= self.level:
      print(f'{self.dbg_prefix}{message}{self.re}')
  
