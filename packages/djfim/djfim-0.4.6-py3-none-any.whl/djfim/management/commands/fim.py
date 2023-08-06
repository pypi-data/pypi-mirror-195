# -*- python -*-
#
# Copyright 2021, 2022, 2023 Cecelia Chen
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# djfim.management.commands.fim

from django.core.management.base import BaseCommand, CommandError
try:
    from django.core.management.base import no_translations
except ImportError:
    from djfim.function import no_translations
    pass


class Command(BaseCommand):

    MODE_BLANK  = 0
    MODE_EXPORT = 1
    MODE_LOAD   = 2
    MODE_FREEZE = 4
    MODE_RESUME = 8

    ACTION_HUB = {
        MODE_LOAD  : 'LOAD',
        MODE_EXPORT: 'EXPORT',
        MODE_FREEZE: 'SAVE',
        MODE_RESUME: 'MERGE',
    }

    MSG_INVALID_MODE = 'invalid operation mode'

    help = ''

    def add_arguments(self, parser):
        parser.add_argument(
            '--data-path',
            dest='datafile',
            metavar='/path/to/update.dat',
            help='file path',
            action='store',
            type=str,
        )

        mode_group = parser.add_mutually_exclusive_group(
            required=True
        )
        mode_group.add_argument(
            '--dump',
            help='export pool data',
            action='store_const',
            const=self.MODE_EXPORT,
            dest='mode',
        )
        mode_group.add_argument(
            '--foreign',
            help='load foreign data',
            action='store_const',
            const=self.MODE_LOAD,
            dest='mode',
        )
        mode_group.add_argument(
            '--preview',
            help='perform initial conflict check',
            action='store_const',
            const=self.MODE_FREEZE,
            dest='mode',
        )
        mode_group.add_argument(
            '--resolve',
            help='resolve data conflict',
            action='store_const',
            const=self.MODE_RESUME,
            dest='mode',
        )
        mode_group.add_argument(
            '--secondary',
            help='one-step shortcut',
            action='store_const',
            const=self.MODE_BLANK,
        )

        parser.add_argument(
            '--head',
            dest='head',
            metavar='HEAD',
            help='alternative tracking head name',
            default=None,
            action='store',
            type=str,
        )
        return

    def handle(self, *args, **opts):
        #raise CommandError(self.MSG_INVALID_MODE)
        return None
