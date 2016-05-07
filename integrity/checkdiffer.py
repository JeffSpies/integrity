from .util import read_yaml, split_label_file, write_yaml

import dictdiffer
import os


class CheckDiffer:
    def __init__(self, previous_check_path):
        self.previous_check_path = previous_check_path
        self.previous_check = read_yaml(previous_check_path)

        self.check = None
        self.diff_list = None

    def create_diff(self, path=None, check=None):
        if not path and not check:
            raise Exception("Needs path or check")

        self.check = check if check else read_yaml(path)

        self.diff_run()
        self.write_diff()
        self.cleanup_old()

    def diff_run(self):
        self.diff_list = list(dictdiffer.diff(self.previous_check, self.check))

    def write_diff(self):
        write_yaml(split_label_file(self.previous_check_path, 'diff'), self.diff_list)

    def cleanup_old(self):
        os.remove(self.previous_check_path)
