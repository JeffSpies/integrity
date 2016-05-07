class ApplicationDirectoryIsNotADirectory(Exception):
    def __init__(self, path):
        message = 'You already have {}, but it is a file rather than a directory'
        Exception.__init__(message.format(path))


class ApplicationDirectoryDoesNotMatchConfig(Exception):
    def __init__(self):
        message = 'Was the folder moved?'
        Exception.__init__(message)

class ApplicationDirectoryBuiltWithWrongVersion(Exception):
    def __init__(self, path):
        message = 'This directory was built with a previous version'
        Exception.__init__(message.format(path))