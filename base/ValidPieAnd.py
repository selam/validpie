#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This module is part of ValidPie
# Copyright 2009 Sinelist

__author__ = 'Timu Eren<timu@sinelist.com>'

from Exceptions import InvalidArgumentException
from ValidPieBase import ValidPieBase
from ValidPieErrorSchema import ValidPieErrorSchema
from ValidPieError import ValidPieError

class ValidPieAnd(ValidPieBase):
    def __init__(self, validators = None, options = {}, messages={}):
        self.__validators = [];

        if isinstance(validators, (ValidPieBase)):
          self.addValidator(validators)
        elif isinstance(validators, (list, dict)):
          for validator in validators:
            self.addValidator(validator);
        elif validators is None:
          raise InvalidArgumentException('ValidPieAnd constructor takes a ValidPieBase object, or a ValidPieBase list/dict')

        ValidPieBase.__init__(self, options, messages);


    def configure(self, options = {}, messages = {}):
        """Configures the current validator."""
        self.addOption('halt_on_error', False);
        self.setMessage('invalid', None);

    def addValidator(self, validator):
        """Adds a validator"""
        if not isinstance(validator, (ValidPieBase)):
          raise InvalidArgumentException('ValidPieAnd addValidator takes a ValidPieBase object')
        self.__validators.append(validator);

    def getValidators(self):
        """Gets all validators"""
        self.__validators;

    def doClean(self, value):
        clean = value
        errors = [];

        for validator in self.getValidators():
          try:
            clean = validator.clean(clean);
          except ValidPieError, e:
            errors.append(e)
            if self.getOption('halt_on_error'):
              break;
        if len(errors) > 0:
          if self.getMessage('invalid'):
            raise ValidPieError(self, 'invalid', {'value': value})
          raise ValidPieErrorSchema(self, errors)

        return clean;

