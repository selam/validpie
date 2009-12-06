#!/usr/bin/env python
# -*- coding: utf-8 -*-

class InvalidArgumentException(Exception):
    def __init__(self, message):
      self.message = message;

    def getMessage(self):
        return self.message;

__all__=[InvalidArgumentException]