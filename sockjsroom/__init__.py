"""
  SockJSRoom allow to manage multi room system above
  sockjs_tornado one. it aims also to automatically
  handle JSON encode/decode, including MongoDB ObjectId
  if available...
"""

__version__ = "0.0.2"

from httpJsonHandler import JsonDefaultHandler
from socketHandler import SockJSDefaultHandler, SockJSRoomHandler
from structure import Struct
from jsonParser import Parser