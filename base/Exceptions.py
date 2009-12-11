#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This module is part of ValidPie
# Copyright 2009 Sinelist

__author__ = 'Timu Eren<timu@sinelist.com>'

class InvalidArgumentException(Exception):
    def __init__(self, message):
      self.message = message

    def getMessage(self):
        return self.message

__all__ = [InvalidArgumentException]