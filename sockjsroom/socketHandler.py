#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
  Add to SockJS-tornado the multi-room support
"""

from sockjs.tornado import SockJSConnection
from jsonParser import Parser
from structure import Struct

import logging

try:
    import json
except ImportError:
    import simplejson as json

# Limit import
__all__ = ["SockJSDefaultHandler", "SockJSRoomHandler"]

class SockJSDefaultHandler(SockJSConnection):
    """ Default handler """
    _parser = Parser()

    def on_message(self, data):
        """ Parsing data, and try to call responding message """
        # Trying to parse response
        data = json.loads(data)
        if not data["name"] is None:
            logging.debug("%s: receiving message %s" % (data["name"], data["data"]))
            fct = getattr(self, "on_" + data["name"])
            try:
                res = fct(Struct(data["data"]))
            except:
                # We try without Struct item (on transaction request this can happend)
                res = fct(data["data"])
            if res is not None:
                self.write_message(res)
        else:
            logging.error("SockJSDefaultHandler: data.name was null")

    def publish(self, name, data, userList):
        """ Publish data """
        # Publish data to all room users
        self.broadcast(userList, {
            "name": name,
            "data": SockJSDefaultHandler._parser.encode(data)
        })



class SockJSRoomHandler(SockJSDefaultHandler):
    """ Room handler """
    _room   = {}

    def _gcls(self):
        """ Get the classname """
        return self.__class__.__name__

    def join(self, _id):
        """ Join a room """
        if not SockJSRoomHandler._room.has_key(self._gcls() + _id):
            SockJSRoomHandler._room[self._gcls() + _id] = set()
        SockJSRoomHandler._room[self._gcls() + _id].add(self)

    def leave(self, _id):
        """ Leave a room """
        if SockJSRoomHandler._room.has_key(self._gcls() + _id):
            SockJSRoomHandler._room[self._gcls() + _id].remove(self)
            if len(SockJSRoomHandler._room[self._gcls() + _id]) == 0:
                del SockJSRoomHandler._room[self._gcls() + _id]

    def getRoom(self, _id):
        """ Retrieve a room from it's id """
        if SockJSRoomHandler._room.has_key(self._gcls() + _id):
            return SockJSRoomHandler._room[self._gcls() + _id]
        return None

    def publishToRoom(self, roomId, name, data, userList=None):
        """ Publish to given room data submitted """
        if userList is None:
            userList = self.getRoom(roomId)

        # Publish data to all room users
        logging.debug("%s: broadcasting (name: %s, data: %s, number of users: %s)" % (self._gcls(), name, data, len(userList)))
        self.broadcast(userList, {
            "name": name,
            "data": SockJSRoomHandler._parser.encode(data)
        })

    def publishToOther(self, roomId, name, data):
        """ Publish to only other people than myself """
        tmpList = self.getRoom(roomId)
        # Select everybody except me
        userList = [x for x in tmpList if x is not self]
        self.publishToRoom(roomId, name, data, userList)

    def publishToMyself(self, roomId, name, data):
        """ Publish to only myself """
        self.publishToRoom(roomId, name, data, [self])

    def isInRoom(self, _id):
        """ Check a given user is in given room """
        if SockJSRoomHandler._room.has_key(self._gcls() + _id):
            if self in SockJSRoomHandler._room[self._gcls() + _id]:
                return True
        return False
