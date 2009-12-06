#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#
# Copyright 2009 Sinelist

import copy

from Exceptions import InvalidArgumentException
from ValidPieBase import ValidPieBase
from ValidPieError import ValidPieError
from ValidPieErrorSchema import ValidPieErrorSchema

class ValidPieSchema(ValidPieBase):
    def __init__(self, options = {}, messages = {}):
        self.__fields = {}
        self.__preValidPie = None
        self.__postValidPie = None
        self.__errorSchema = ValidPieErrorSchema(self)
        self.__cleanedValues = {}
        ValidPieBase.__init__(self, options, messages)


    def setValidPies(self, validators = None):
        if isinstance(validators, dict):
          for name, validator in validators.iteritems():
            self.__fields[name] = validator
        elif validators is not None:
          raise InvalidArgumentException('ValidPieSchema constructor takes an dict of ValidPieBase objects')



    def configure(self, options = {}, messages = {}):
        """Configures the validator.
           Available options:
             allow_extra_fields:  if false, the validator adds an error if extra fields are given in the input array of values (default to false)
             filter_extra_fields: if true, the validator filters extra fields from the returned array of cleaned values (default to true)
           Available error codes:
             extra_fields
        """
        self.addOption('allow_extra_fields', False)
        self.addOption('filter_extra_fields', True)
        self.addMessage('extra_fields', 'Unexpected extra field named "%(field)s".')

        self.setUp(self.getOptions(), self.getMessages())

    def setUp(self, options = {}, messages = {}):
        raise NotImplementedError('setUp must be implemented')


    def clean(self, values):
        """@see ValidPieBase"""
        return self.doClean(values)

    def setPreValidPie(self, validator):
        """sets pre validator"""
        if isinstance(validator, (ValidPieBase)):
          self.__preValidPie = validator
        else:
          raise InvalidArgumentException('preValidPie must be an instanceof ValidPieBase')

    def getPreValidPie(self):
      """Returns preValidPie"""
      return self.__preValidPie

    def getErrors(self):
      """returns all errors"""
      return self.__errorSchema.getErrors()

    def getError(self, fieldName):
      """see ValidPieErrorSchema#getNamedError"""
      return self.__errorSchema.getNamedError(fieldName)

    def setPostValidPie(self, validator):
        """Sets post validator"""
        if isinstance(validator, (ValidPieBase)):
          self.__postValidPie = validator
        else:
          raise InvalidArgumentException('postValidPie must be an instanceof ValidPieBase')

    def getPostValidPie(self):
      """Returns postValidPie"""
      return self.__postValidPie

    def preClean(self, values):
      """Cleans the input values. This method is the first validator executed by doClean()"""
      validator = self.getPreValidPie()

      if validator is None:
        return None
      validator.clean(values)

    def getFields(self):
        """Returns an dict of fields."""
        return self.__fields

    def postClean(self, values):
      """Cleans the input values. This method is the last validator executed by doClean()"""
      validator = self.getPostValidPie()

      if validator is None:
        return None
      validator.clean(values)

    def isValid(self):
      return False if self.__errorSchema.count() > 0 else True

    def getValue(self, name):
      """Gets validated value of given name"""
      return self.__cleanedValues[name] if self.__cleanedValues.has_key(name) else None

    def getValues(self):
      """returns all validated values"""
      return self.__cleanedValues

    def getErrorSchema(self):
      return self.__errorSchema

    def doClean(self, values = None):
      """validate given values with mapped validators"""
      if values is None:
          values = {}
      if not isinstance(values, (dict)):
          raise InvalidArgumentException('You must pass an dict parameter to the clean() method')

      clean  = {}
      unused = copy.copy(self.getFields())

      try:
        self.preClean(values)
      except ValidPieErrorSchema, e:
        self.__errorSchema.addErrors(e)
      except ValidPieError, e:
        self.__errorSchema.addError(e)

      for name, value in values.iteritems():
        # field exists in our schema?
        if name not in self.getFields():
          if not self.getOption('allow_extra_fields'):
            self.__errorSchema.addError(ValidPieError(self, 'extra_fields', {'field': name}))
          elif not self.getOption('filter_extra_fields'):
            self.__cleanedValues[name] = value
          continue
        else:
          del unused[name]

        # validate value
        try:
          self.__cleanedValues[name] = self.__fields[name].clean(value)

        except ValidPieError, e:
          self.__cleanedValues[name] = None
          self.__errorSchema.addError(e, name)

      # are non given values required?
      try:
        for name in unused.iteritems():
          pass
          #self.__cleanedValues[name] = self.__fields[name].clean(None)
      except ValidPieError, e:
          self.__cleanedValues[name] = None
          self.__errorSchema.addError(e, name)

      """ post validator"""
      try:
        self.__cleanedValues = self.postClean(self.__cleanedValues)
      except ValidPieErrorSchema, e:
        self.__errorSchema.addErrors(e)
      except ValidPieError, e:
        self.__errorSchema.addError(e)