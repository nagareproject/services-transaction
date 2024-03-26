# Encoding: utf-8

# --
# Copyright (c) 2008-2024 Net-ng.
# All rights reserved.
#
# This software is licensed under the BSD License, as described in
# the file LICENSE.txt, which you should have received as part of
# this distribution.
# --

from __future__ import absolute_import

from transaction import doom, abort, begin, commit, manager, isDoomed, interfaces, _transaction  # noqa: F401

from nagare.services import plugin


class Transaction(plugin.Plugin):
    LOAD_PRIORITY = 103  # After state service
    CONFIG_SPEC = dict(plugin.Plugin.CONFIG_SPEC, retries='integer(default=3)')

    def __init__(self, name, dist, retries, services_service, **config):
        services_service(super(Transaction, self).__init__, name, dist, retries=retries, **config)
        self.retries = retries
        _transaction._LOGGER = self.logger

    def handle_request(self, chain, **params):
        r = None

        try:
            for attempt in manager.attempts(self.retries):
                with attempt:
                    r = chain.next(**params)
        except interfaces.DoomedTransaction:
            abort()

        return r

    @staticmethod
    def handle_interaction():
        return {'transaction': manager}
