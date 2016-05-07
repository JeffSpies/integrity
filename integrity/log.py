import datetime
import json
import os
import shutil
import pathlib


class Log():
    def __init__(self, *args, **kwargs):
        self._path = kwargs.get('path', None)
        self._version = kwargs.get('version')
        self._fp = None

    @property
    def path(self):
        return self._path

    def exists(self):
        return os.path.exists(self._path)

    def read(self):
        data = {}
        with open(self._path, 'r') as f:
            for line in f:
                tmp = json.loads(line)
                key = os.path.join(tmp['dir'], tmp['file'])
                data[key] = tmp
        return data

    def write(self, action, params=None, defaults=True):
        log = {}

        if not self._fp:
            self._fp = open(os.path.join(self._path), 'a')

        if defaults:
            log.update({
                '_version': self._version,
                '_action': action,
                '_datetime': str(datetime.datetime.utcnow()),
            })

        log.update(params)

        self._fp.write(json.dumps(log) + os.linesep)

    def close(self):
        self._fp.close()
