# Encoding: utf-8

# --
# Copyright (c) 2008-2024 Net-ng.
# All rights reserved.
#
# This software is licensed under the BSD License, as described in
# the file LICENSE.txt, which you should have received as part of
# this distribution.
# --

from transaction import doom, abort, begin, commit, manager, isDoomed, interfaces, _transaction  # noqa: F401

from nagare.services import plugin


class Transaction(plugin.Plugin):
    LOAD_PRIORITY = 103  # After state service

    def __init__(self, name, dist, services_service, **config):
        services_service(super(Transaction, self).__init__, name, dist, **config)
        _transaction._LOGGER = self.logger

    def handle_request(self, chain, **params):
        try:
            r = chain.next(**params)
            commit()
            return r
        except Exception as exc:
            if getattr(exc, 'commit_transaction', False):
                commit()
            else:
                abort()

            raise

    @staticmethod
    def handle_interaction():
        return {'transaction': manager}
