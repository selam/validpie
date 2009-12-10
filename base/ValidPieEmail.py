#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#
# Copyright 2009 Sinelist


from ValidPieRegex import ValidPieRegex

class ValidPieEmail(ValidPieRegex):
  def configure(self, options = {}, messages = {}):
    options.update({
      'pattern': '^.+\\@(\\[?)[a-zA-Z1-9\\-\\.]+\\.([a-zA-Z]{2,4})(\\]?)$'
    })
    ValidPieRegex.configure(self, options, messages)