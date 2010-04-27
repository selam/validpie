#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This module is part of ValidPie
# Copyright 2009 Sinelist

__author__ = 'Timu Eren<timu@sinelist.com>'

from ValidPieRegex import ValidPieRegex

class ValidPieEmail(ValidPieRegex):
  def configure(self, options = {}, messages = {}):
    options.update({
      'pattern': '^.+\\@(\\[?)[a-zA-Z1-9\\-\\.]+\\.([a-zA-Z]{2,4})(\\]?)$'
    })
    ValidPieRegex.configure(self, options, messages)