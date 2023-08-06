# -*- python -*-
#
# Copyright 2021, 2022, 2023 Cecelia Chen
# Copyright 2018, 2019, 2020, 2021 Liang Chen
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
# djfim.management.commands.dupdb

from io import StringIO
import sys

from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError
from django.db import DEFAULT_DB_ALIAS, connections
from django.db.migrations.executor import MigrationExecutor
try:
    from django.core.management.base import no_translations
except ImportError:
    from djfim.function import no_translations
    pass


class Command(BaseCommand):
    help = '''Duplicate database content to a new SQLite database.'''

    DB_NAME = 'duplicate'
    DB_FILENAME = '/tmp/dup.sqlite3'

    MSG_PENDING_MIGRATION = 'pending migrations detected.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--new-db',
            dest='new_db_name',
            metavar='NEW_DATABASE',
            default=self.DB_NAME,
            help='alias name of the new database',
            action='store',
            type=str,
        )
        parser.add_argument(
            '--new-db-file',
            dest='new_db_filename',
            metavar=self.DB_FILENAME,
            default=self.DB_FILENAME,
            help='file path of the new database (sqlite3)',
            action='store',
            type=str,
        )

    def setup_db_connection(self, options):
        self.new_db = options['new_db_name']
        self.new_db_file = options['new_db_filename']
        assert self.new_db != DEFAULT_DB_ALIAS, "invalid db alias"
        return self

    def check_migration_status(self):
        '''
        code adapted from `django.core.management.commands.migrate:handle`
        '''
        conn = connections[DEFAULT_DB_ALIAS]
        conn.prepare_database()
        executor = MigrationExecutor(
            conn,
            self.dummy_migration_callback
        )
        plan = executor.migration_plan(
            executor.loader.graph.leaf_nodes()
        )
        if plan:
            msg = self.style.ERROR(self.MSG_PENDING_MIGRATION)
            raise CommandError(msg)
        return None

    def dummy_migration_callback(self, *args, **kwargs):
        return None

    def create_new_database(self):
        settings.DATABASES[ self.new_db ] = {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': self.new_db_file,
        }

        self.migration_out = StringIO()
        self.migration_err = StringIO()
        new_db_migration_args = {
            'database': self.new_db,
            'interactive': False,
            'verbosity': 0,
            'stdout': self.migration_out,
            'stderr': self.migration_err,
        }
        self.stdout.write('start creating new database')
        try:
            call_command(
                'migrate',
                **new_db_migration_args
            )
        except Exception as e:
            self.stderr.write('datebase creation failed.')
            if self.verbosity >= 1:
                self.stderr.write(sys.exc_info()[-1])
        return None

    def duplicate_data(self, *args, **options):
        '''
        this template method will invoke `self.doCopy` method if available.
        '''
        if hasattr(self, 'doCopy'):
            self.doCopy(*args, **options)
        return None

    @no_translations
    def handle(self, *args, **options):
        self.verbosity = options.get('verbosity')

        # set the new db connection
        self.setup_db_connection(options)

        # precondition check: up-to-date migration
        self.check_migration_status()

        # initiate the new db
        self.create_new_database()

        # copy data
        self.duplicate_data(*args, **options)
        return None
