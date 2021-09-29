#!/bin/env python3

# CORTX Python common library.
# Copyright (c) 2020 Seagate Technology LLC and/or its Affiliates
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.
# For any questions about this software or licensing,
# please email opensource@seagate.com or cortx-questions@seagate.com.

import sys
import traceback
import errno
import os

from cortx.provisioner.log import Log
from cortx.provisioner.provisioner import CortxProvisioner
from cortx.provisioner.error import CortxProvisionerError
from cortx.utils.cmd_framework import Cmd


class ConfigCmd(Cmd):
    """ Config Setup Cmd """

    name = 'config'

    def __init__(self, args: dict):
        """ Initialize Command line parameters """
        super().__init__(args)

    @staticmethod
    def add_args(parser: str):
        """ Add Command args for parsing """

        parser.add_argument('action', help='apply')
        parser.add_argument('-f', dest='solution_conf', \
            help='Solution Config URL')
        parser.add_argument('-o', dest='cortx_conf', nargs='?', \
            help='CORTX Config URL')
        parser.add_argument('-l', dest='log_level', help='Log level')

    def _validate(self):
        """ Validate config command args """

        if self._args.action not in ['apply']:
            raise CortxProvisionerError(errno.EINVAL, 'Invalid action type')

        if self._args.log_level:
            if self._args.log_level not in \
                ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']:
                    raise CortxProvisionerError(errno.EINVAL, 'Invalid log level')
            else:
                Log.logger.setLevel(self._args.log_level)

    def process(self):
        """ Apply Config """
        self._validate()
        if self._args.action == 'apply':
            CortxProvisioner.config_apply(self._args.solution_conf, self._args.cortx_conf)
        return 0


class ClusterCmd(Cmd):
    """ Cluster Setup Cmd """

    name = 'cluster'

    def __init__(self, args: dict):
        super().__init__(args)

    @staticmethod
    def add_args(parser: str):
        """ Add Command args for parsing """

        parser.add_argument('action', help='bootstrap')
        parser.add_argument('-f', dest='cortx_conf', help='Cortx Config URL')
        parser.add_argument('-l', dest='log_level', help='Log level')
        parser.add_argument('-m', dest='mock', action="store_true",
            help='Boolean - Enable Mocking.')


    def _validate(self):
        """ Validate cluster command args """

        if self._args.action not in ['bootstrap']:
            raise CortxProvisionerError(errno.EINVAL, 'Invalid action type')

        if self._args.log_level:
            if self._args.log_level not in \
                ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']:
                    raise CortxProvisionerError(errno.EINVAL, 'Invalid log level')
            else:
                Log.logger.setLevel(self._args.log_level)

    def process(self, *args, **kwargs):
        """ Bootsrap Cluster """
        self._validate()
        if self._args.action == 'bootstrap':
            mock = True if self._args.mock else False
            CortxProvisioner.cluster_bootstrap(self._args.cortx_conf, mock)
        return 0


def main():
    try:
        # Parse and Process Arguments
        command = Cmd.get_command(sys.modules[__name__], 'cortx_setup', \
            sys.argv[1:])
        rc = command.process()

    except CortxProvisionerError as e:
        Log.error('%s' % str(e))
        Log.error('%s' % traceback.format_exc())
        rc = e.rc

    except Exception as e:
        Log.error('%s' % str(e))
        Log.error('%s' % traceback.format_exc())
        rc = errno.EINVAL

    return rc


if __name__ == "__main__":
    sys.exit(main())