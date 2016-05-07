import munch
import os
import yaml


class Config:
    def __init__(self, path, new=None):
        self.path = path
        d = {}
        if os.path.exists(self.path):
            with open(self.path, 'r') as fp:
                d = yaml.load(fp)
                if d is None:
                    d = {}
        else:
            if new:
                d.update(new)
        self._data = munch.munchify(d)

    @property
    def data(self):
        return self._data

    @property
    def export(self):
        return munch.unmunchify(self._data)

    def update(self, **kwargs):
        self._data.update(kwargs)

    def save(self):
        with open(self.path, 'w') as fp:
            fp.write(yaml.dump(self.export, default_flow_style=False))
