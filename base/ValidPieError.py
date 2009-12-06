#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#
# Copyright 2009 Sinelist

class ValidPieError(Exception):
    def __init__(self, validator, errorCode, arguments = {}):
        self.__validator = validator
        self.__arguments = arguments
        self.__code = errorCode
        self.__message = None;

        messageFormat = self.getMessageFormat()
        if messageFormat is None:
          messageFormat = errorCode;

        self.__message = messageFormat % arguments

    def getValue(self):
        """Returns the input value that triggered this error."""
        return self.__arguments['value'] if self.__arguments.has_key('value') else None

    def getValidPie(self):
        """Returns the validator that triggered this error."""
        return self.__validator;

    def getCode(self):
        return self.__code;

    def getMessage(self):
        """returns the error message"""
        return self.__message;

    def getMessageFormat(self):
        """Returns the message format for this error."""
        messageFormat = self.getValidPie().getMessage(self.getCode());

        if messageFormat is None:
           messageFormat = self.getMessage();
        return messageFormat;

    def getArguments(self, raw = False):
        """Returns the arguments needed to format the message."""
        if raw:
          return self.__arguments;

        arguments = {};
        for name, value in self.__arguments.iteritems():
          if isinstance(value, (list, dict)):
            continue;
          arguments[name] = value;

        return arguments;

    def setCode(self, code):
        """set code"""
        self.__code = code;
    def setMessage(self, message):
        """" set message"""
        self.__message = message;