# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from django.test import TestCase

from ralph_assets.tests.utils import ClientMixin


class TestAddPartView(ClientMixin, TestCase):

    def setUp(self):
        pass

    def should_add_parts_when_all_is_ok(self):
        pass
