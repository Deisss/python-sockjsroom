#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
  Handle basic Dict to object convertion
"""

# Limit import
__all__ = ["Struct"]

class Struct:
    """ The recursive class for building and representing objects with. """
    def __init__(self, obj):
        self._createObject(obj)

    def _createObject(self, obj):
        for k, v in obj.iteritems():
            if isinstance(v, dict):
                setattr(self, k, Struct(v))
            else:
                setattr(self, k, v)

    def __getitem__(self, val):
        return self.__dict__[val]

    def __setitem__(self, key, val):
        setattr(self, key, val)

    def __delitem__(self, val):
        try:
            del self.__dict__[val]
        except:
            pass

    def toDict(self):
        return self.__dict__

    def __repr__(self):
        return '{%s}' % str(', '.join('%s : %s' % (k, repr(v)) for (k, v) in self.__dict__.iteritems()))
