from .exceptions import \
    ApplicationDirectoryIsNotADirectory, \
    ApplicationDirectoryBuiltWithWrongVersion,\
    ApplicationDirectoryDoesNotMatchConfig

from .util import read_yaml, write_yaml, split_label_file, globre
from .check import Check
from .config import Config
from .log import Log
from .checkdiffer import CheckDiffer

import arrow
import os
import shutil

DATA_DIRECTORY_NAME = '.integrity'
DATA_FILENAME = 'check.yml'
CONFIG_FILENAME = 'config.yml'
LOG_FILENAME = 'log.txt'
VERSION = '0.0.1'
CHECK_DATE_FORMAT = 'check.[0-9]+.yml'

IGNORE_GLOBS = [
    os.path.join('*', DATA_DIRECTORY_NAME, '*'),
    os.path.join('*', '.DS_Store')
]

migrations = {
}

class Application:

    def __init__(self, source):
        self.absolute_path = os.path.abspath(source)
        print('Integrity', self.absolute_path)

        self.app_directory = os.path.join(self.absolute_path, DATA_DIRECTORY_NAME)
        self.check_path = os.path.join(self.app_directory, DATA_FILENAME)
        self.config_path = os.path.join(self.app_directory, CONFIG_FILENAME)
        self.log_path = os.path.join(self.app_directory, LOG_FILENAME)

        self.config = self.get_config()
        self.log = self.get_current_log()

        if not os.path.exists(self.app_directory):
            self.create_application_directory()

        self.validate_application_directory()
        self.validate_logs()

    def get_config(self):
        return Config(self.config_path, new={
            'VERSION': VERSION,
            'SOURCE': self.absolute_path,
            'IGNORE_GLOBS': IGNORE_GLOBS
        })

    def get_current_log(self):
        return Log(path=self.log_path, version=VERSION)

    def create_application_directory(self):
        os.mkdir(self.app_directory)
        self.config.save()

    def validate_logs(self):
        pass

    def validate_application_directory(self):
        if not os.path.isdir(self.app_directory):
            raise ApplicationDirectoryIsNotADirectory(DATA_DIRECTORY_NAME)

        if self.config.data.SOURCE != self.absolute_path:
            raise ApplicationDirectoryDoesNotMatchConfig()

        if self.config.data.VERSION != VERSION:
            raise ApplicationDirectoryBuiltWithWrongVersion()

    def rotate_data_file(self):
        if os.path.exists(self.check_path):
            old_data_filename = split_label_file(self.check_path, str(arrow.utcnow().format('YYYYMMDDHHmmss')))
            shutil.move(self.check_path, old_data_filename)
            return old_data_filename
        return None

    def serialize_check(self):
        return {
            'config': self.config.export,
            'checked': self._check.date,
            'data': self._check.data
        }

    def write_data_file(self):
        write_yaml(self.check_path, self.serialize_check())

    @property
    def previous_check_path(self):
        paths = globre(self.app_directory, CHECK_DATE_FORMAT)
        if paths:
            return paths[0]
        return None

    def has_previous_check_file(self):
        if os.path.exists(self.check_path):
            if self.previous_check_path:
                return True
        return False

    def create_check(self, hash=False):

        if self.has_previous_check_file():
            CheckDiffer(self.previous_check_path).create_diff(path=self.check_path)

        self._check = Check(
            self.config.data.SOURCE,
            log=self.log,
            partial_log_location=self.app_directory,
            ignore=self.config.data.IGNORE_GLOBS
        )
        self.log.write(action='STAT', params=self._check.action('begin')) if self.log else ''

        self._check.stat_directory(hash=hash)

        previous_data_filename = self.rotate_data_file()
        self.write_data_file()

        self._check.remove_partial_log()
        self.log.write(action='STAT', params=self._check.action('end')) if self.log else ''

        if self.has_previous_check_file():
            CheckDiffer(self.previous_check_path).create_diff(check=self.serialize_check())
