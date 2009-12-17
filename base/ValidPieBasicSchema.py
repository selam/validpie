#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This module is part of ValidPie
# Copyright 2009 Sinelist

__author__ = 'Timu Eren<timu@sinelist.com>'

from ValidPieSchema import ValidPieSchema
"""
# in validators module

from validators.base import ValidPieBasicSchema

class FooValidatorSchema(ValidPieBasicSchema):
      def setUp(self, options, messages):
          self.setValidPies({
              'foo': ValidPieString({'required': True}, {'required': 'required field'})
          })

# in actions

def get(self):
    validatorSchema = FooValidatorSchema({
                        'foo': self.get_argument('foo')
                      });
    if validatorSchema.isValid():
       self.write({'status': 'ok', 'contents': {'foo': validatorSchema.getValue('foo')}})
    else
      self.write({'status': 'error', 'code': validatorSchema.getErrorCode('foo'), 'message': validatorSchema.getErrorMessage('foo')})

"""
class ValidPieBasicSchema(ValidPieSchema):
      def __init__(self, values = {}, options = {}, messages = {}):
          ValidPieSchema.__init__(self, options, messages)
          self.clean(values)


