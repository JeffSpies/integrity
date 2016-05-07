from .util import did_any_pattern_match, make_relative_path, get_id
from .checksum import get_checksums
from .log import Log

import arrow
import copy
import os


class Action:
    def action(self, status=None, **kwargs):
        params = copy.copy(self.params)
        if status:
            params['status'] = status
        params.update(kwargs)
        return params


class Check(Action):
    def __init__(self, path=None, log=None, partial_log_location=None, ignore=None):
        self.source = path
        self.log = log
        self.ignore_list = ignore

        self.name = get_id()

        self.create_partial_log(partial_log_location)

        self._data = {}
        if self.partial_log:
            if self.partial_log.exists():
                self._data = self.partial_log.read()

        self.params = {
            'name': self.name,
            'source': self.source
        }

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, x):
        self._data = x

    def create_partial_log(self, partial_log_location):
        tmp_log_path = os.path.join(partial_log_location, 'partial_check.txt')
        self.partial_log = Log(path=tmp_log_path)

    def remove_partial_log(self):
        os.remove(self.partial_log.path)

    def run_path(self, relative_path, filename, hash):
        data = {
            'file': filename
        }

        error = None

        full_path = os.path.join(self.source, relative_path, filename)

        try:
            stat_info = os.stat(full_path)
            if hash:
                data['hashes'] = get_checksums(full_path)
            data.update({
                'bytes': stat_info.st_size,
                'ctime': stat_info.st_ctime,
                'mtime': stat_info.st_mtime,
            })
        except Exception as e:
            error = e

        return data, error

    def stat_directory(self, hash=False):
        count = 0

        for path, directory_names, file_names in os.walk(self.source):
            print("Stat'ing {} (hash={})".format(path, hash))
            for filename in file_names:
                file_path = os.path.join(path, filename)
                relative_directory = make_relative_path(self.source, path)
                relative_path = os.path.join(relative_directory, filename)
                if not did_any_pattern_match(file_path, self.ignore_list):
                    if relative_path not in self._data:
                        file_data, error = self.run_path(path, filename, hash)
                        file_data['dir'] = relative_directory
                        self._data[relative_path] = file_data
                        self.partial_log.write(
                            action='STAT',
                            params=file_data,
                            defaults=False
                        ) if self.partial_log else ''
                        if error:
                            self.log.write(
                                action='STAT',
                                params=self.action(
                                    'fail', path=relative_path, error=error.__class__.__name__
                                )
                            ) if self.log else ''
                        count += 1
        self.date = str(arrow.now())
