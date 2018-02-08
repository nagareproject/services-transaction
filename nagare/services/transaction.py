# Encoding: utf-8

# --
# Copyright (c) 2008-2018 Net-ng.
# All rights reserved.
#
# This software is licensed under the BSD License, as described in
# the file LICENSE.txt, which you should have received as part of
# this distribution.
# --

from __future__ import absolute_import

import transaction
from nagare.services import plugin


class TransactionHandler(plugin.Plugin):
    LOAD_PRIORITY = 20

    @classmethod
    def handle_request(cls, chain, **params):
        with transaction.manager:
            return chain.next(**params)

    @staticmethod
    def handle_interactive():
        return {'transaction': transaction.manager}
