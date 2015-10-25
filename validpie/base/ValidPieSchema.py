#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This module is part of ValidPie
# Copyright 2009 Sinelist

__author__ = 'Timu Eren<timu@sinelist.com>'

import copy

from Exceptions import InvalidArgumentException
from ValidPieBase import ValidPieBase
from ValidPieError import ValidPieError
from ValidPieErrorSchema import ValidPieErrorSchema


class ValidPieSchema(ValidPieBase):
    def __init__(self, options={}, messages={}):
        self._fields = {}
        self._preValidPie = None
        self._postValidPie = None
        self._errorSchema = ValidPieErrorSchema(self)
        self._cleanedValues = {}
        ValidPieBase.__init__(self, options, messages)

    def setValidPies(self, validators=None):
        if isinstance(validators, dict):
            for name, validator in validators.iteritems():
                self._fields[name] = validator
        elif validators is not None:
            raise InvalidArgumentException('ValidPieSchema constructor takes an dict of ValidPieBase objects')

    def configure(self, options={}, messages={}):
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

    def setUp(self, options={}, messages={}):
        raise NotImplementedError('setUp must be implemented')

    def clean(self, values=None):
        """@see ValidPieBase"""
        return self.doClean(values)

    def setPreValidPie(self, validator):
        """sets pre validator"""
        if isinstance(validator, (ValidPieBase,)):
            self._preValidPie = validator
        else:
            raise InvalidArgumentException('preValidPie must be an instanceof ValidPieBase')

    def getPreValidPie(self):
        """Returns preValidPie"""
        return self._preValidPie

    def getErrors(self):
        """returns all errors"""
        return self._errorSchema.getErrors()

    def getError(self, fieldName):
        """see ValidPieErrorSchema#getNamedError"""
        return self._errorSchema.getNamedError(fieldName)

    def setPostValidPie(self, validator):
        """Sets post validator"""
        if isinstance(validator, (ValidPieBase,)):
            self._postValidPie = validator
        else:
            raise InvalidArgumentException('postValidPie must be an instanceof ValidPieBase')

    def getPostValidPie(self):
        """Returns postValidPie"""
        return self._postValidPie

    def preClean(self, values):
        """Cleans the input values. This method is the first validator executed by doClean()"""
        validator = self.getPreValidPie()

        if validator is None:
            return values
        return validator.clean(values)

    def getFields(self):
        """Returns an dict of fields."""
        return self._fields

    def postClean(self, values):
        """Cleans the input values. This method is the last validator executed by doClean()"""
        validator = self.getPostValidPie()

        if validator is None:
            return values
        return validator.clean(values)

    def isValid(self):
        return self._errorSchema.count() == 0

    def getErrorMessage(self, field):
        """return error message given name"""
        error = self._errorSchema.getNamedError(field)
        if error:
            return error.getMessage()
        return None

    def getErrorCode(self, field):
        """return error code given name"""
        error = self._errorSchema.getNamedError(field)
        if error:
            return error.getCode()
        return None

    def getValue(self, name):
        """Gets validated value of given name"""
        return self._cleanedValues[name] if name in self._cleanedValues else None

    def getValues(self):
        """returns all validated values"""
        return self._cleanedValues

    def getErrorSchema(self):
        return self._errorSchema

    def doClean(self, values=None):
        """validate given values with mapped validators"""
        if values is None:
            values = {}
        if not isinstance(values, (dict)):
            raise InvalidArgumentException('You must pass an dict parameter to the clean() method')

        unused = copy.copy(self.getFields())

        try:
            self.preClean(values)
        except ValidPieErrorSchema, e:
            self._errorSchema.addErrors(e)
        except ValidPieError, e:
            self._errorSchema.addError(e)

        for name, value in values.iteritems():
            # field exists in our schema?
            if name not in self.getFields():
                if not self.getOption('allow_extra_fields'):
                    self._errorSchema.addError(ValidPieError(self, 'extra_fields', {'field': name}))
                elif not self.getOption('filter_extra_fields'):
                    self._cleanedValues[name] = value
                continue
            else:
                del unused[name]

            # validate value
            try:
                self._cleanedValues[name] = self._fields[name].clean(value)

            except ValidPieError, e:
                self._cleanedValues[name] = None
                self._errorSchema.addError(e, name)

        # are non given values required?
        for name, value in unused.iteritems():
            try:
                self._cleanedValues[name] = self._fields[name].clean(None)
            except ValidPieError, e:
                self._cleanedValues[name] = None
                self._errorSchema.addError(e, name)

        """ post validator"""
        try:
            self._cleanedValues = self.postClean(self._cleanedValues)
        except ValidPieErrorSchema, e:
            self._errorSchema.addErrors(e)
        except ValidPieError, e:
            self._errorSchema.addError(e)
