#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#
# Copyright 2009 Sinelist

from ValidPieError import ValidPieError
from ValidPieBase import ValidPieBase

class ValidPieErrorSchema(ValidPieError):
    def __init__(self, validator, errors = {}):

          if not isinstance(validator, (ValidPieBase)):
              raise InvalidArgumentException('validator must be instance of ValidPieBase')
          ValidPieError.__init__(self, validator, None, {})

          self.__namedErrors = {}
          self.__globalErrors = []
          self.__errors = []

          self.addErrors(errors)


    def addErrors(self, errors):
        """Adds an dict or ValidPieErrorSchema of errors"""
        if isinstance(errors, (ValidPieErrorSchema)):
            for error in errors.getGlobalErrors():
                self.addError(error)
            for name, error in errors.getNamedErrors().iteritems():
                self.addError(error, name)
        else:
          for name, error in errors.iteritems():
              self.addError(error, name)

    def addError(self, error, name = None):
        """Adds an error."""
        if name is None:
          if isinstance(error, ValidPieErrorSchema):
            self.addErrors(error)
          else:
            self.__globalErrors.append(error)
            self.__errors.append(error)
        else:
          if not self.__namedErrors.has_key(name) and not isinstance(error, ValidPieErrorSchema):
              self.__namedErrors[name] = error
              self.__errors.append(error)
          else:
            if not self.__namedErrors.has_key(name):
                self.__namedErrors[name] = ValidPieErrorSchema(error.getValidPie())
                self.__errors.append(error)
            elif not isinstance(self.__namedErrors[name], (ValidPieErrorSchema)):
                current = self.__namedErrors[name]
                self.__namedErrors[name] = ValidPieErrorSchema(current.getValidPie())
                self.__errors.append(current)
                method = 'addErrors' if isinstance(current, ValidPieErrorSchema) else 'addError'
                getattr(self.__namedErrors[name], method)(current)
            method = 'addErrors' if isinstance(error, ValidPieErrorSchema) else 'addError'
            self.__errors.append(error)
            getattr(self.__namedErrors[name], method)(error)

        self.updateCode()
        self.updateMessage()

    def updateCode(self):
        """Updates the exception error code according to the current errors."""
        _globalErrors = []
        _namedErrors = []

        for error in self.getGlobalErrors():
          _globalErrors.append(error.getCode())

        for name, error in self.getNamedErrors().iteritems():
            _namedErrors.append('%s [%s]' % (name, error.getCode()))
        ValidPieError.setCode(self, '%s %s' % (' '.join(_globalErrors), ' '.join(_namedErrors)))

    def updateMessage(self):
        """Updates the exception error message according to the current errors."""
        _globalErrors = []
        _namedErrors = []
        for error in self.getGlobalErrors():
          _globalErrors.append(error.getMessage())

        for name, error in self.getNamedErrors().iteritems():
            _namedErrors.append('%s [%s]' % (name, error.getMessage()))

        ValidPieError.setMessage(self, '%s %s' % (' '.join(_globalErrors), ' '.join(_namedErrors)))


    def getValue(self):
        """See ValidPieError"""
        return None

    def getArguments(self, raw = True):
        """See ValidPieError"""
        return {}

    def count(self):
        """Returns the number of errors."""
        return len(self.__errors)

    def getMessageFormat(self):
      """See ValidPieError"""
      return ''

    def getErrors(self):
        """Gets an list of all errors"""
        return self.__errors

    def getNamedErrors(self):
        """Gets an dict of all named errors"""
        return self.__namedErrors

    def getNamedError(self, name):
        """return an ValidPieError if has error given name, otherwise None"""
        return self.__namedErrors[name] if self.__namedErrors.has_key(name) else None

    def getGlobalErrors(self):
        """Gets an list of all global errors"""
        return self.__globalErrors

    def valid(self):
        """Returns true if the current error is valid"""
        return True if self.count() < 1 else False