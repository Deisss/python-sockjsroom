#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
  Easy JSON support for tornado RequestHandler
"""


import tornado.web, urllib
from jsonParser import Parser

try:
    import json
except ImportError:
    import simplejson as json

# Limit import
__all__ = ["JsonDefaultHandler"]

class JsonDefaultHandler(tornado.web.RequestHandler):
    """ Base Json Handler for tornado """
    __parser = None

    def getBody(self):
        """ Extract body json """
        data = None
        try:
            data = json.loads(self.request.body)
        except:
            data = json.loads(urllib.unquote_plus(self.request.body))
        return data

    def write(self, obj):
        """ Print object on output """
        accept = self.request.headers.get("Accept")
        if "json" in accept:
            if JsonDefaultHandler.__parser is None:
                JsonDefaultHandler.__parser = Parser()
            super(JsonDefaultHandler, self).write(JsonDefaultHandler.__parser.encode(obj))
            return
        # If we are not in json mode
        super(JsonDefaultHandler, self).write(obj)