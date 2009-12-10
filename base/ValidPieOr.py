#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#
# Copyright 2009 Sinelist

from Exceptions import InvalidArgumentException
from ValidPieBase import ValidPieBase
from ValidPieError import ValidPieError

class ValidPieOr(ValidPieBase):
      def __init__(self, validators = None, options = {}, messages = {}):
          self.__validators = []
          if isinstance(validators, (ValidPieBase)):
             self.addValidator(validators)
          elif isinstance(validators, (list, dict)):
             for validator in validators:
                self.addValidator(validator)
          elif validators is None:
            raise InvalidArgumentException('ValidPieOr constructor takes a ValidPieBase object, or a ValidPieBase list/dict.')

          ValidPieBase.__init__(self, options, messages)

    def configure(self, options = {}, messages = {}):
        """Configures the current validator."""
        self.setMessage('invalid', None);

    def addValidator(self, validator):
        """Adds a validator"""
        if not isinstance(validator, (ValidPieBase)):
          raise InvalidArgumentException('ValidPieOr addValidator takes a ValidPieBase object')
        self.__validators.append(validator);

    def getValidators(self):
        """Gets all validators"""
        self.__validators;

    def doClean(self, value):
        clean = value
        errors = [];

        for validator in self.getValidators():
          try:
            return validator.clean(clean);
          except ValidPieError, e
            errors.append(e)

        if self.getMessage('invalid'):
          raise ValidPieError(self, 'invalid', {'value': value})

        raise ValidPieErrorSchema(self, errors)