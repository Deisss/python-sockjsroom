#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
  Simple MongoDB parser for output pretty JSON with ObjectID support
"""

try:
    import json
except ImportError:
    import simplejson as json

Parser = None

# Limit import
__all__ = ["Parser"]

class DefaultJsonParser(json.JSONEncoder):
    """ Create a basic JSON parser instance """
    def default(self, obj):
        """ Output data """
        # Printer for datetime object
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()

        # Switch to default handler
        return json.JSONEncoder.default(self, obj)

# Setting parser to default one
Parser = DefaultJsonParser

try:
    import bson.objectid

    # Import was a success, we add Mongo ObjectId compatibility
    class MongoJsonParser(DefaultJsonParser):
        """ Specific MongoDB manage ObjectId """
        def default(self, obj):
            """ Output data """

            # Printer for MongoDB ObjectId
            if isinstance(obj, bson.objectid.ObjectId):
                return str(obj)

            return DefaultJsonParser.default(self, obj)

    # Switch parser to new mongo supported one
    Parser = MongoJsonParser

except importError:
    pass
