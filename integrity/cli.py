from .application import Application

import click


@click.command()
@click.argument('path')
def cli(path):
    app = Application(path)
    app.create_check(hash=True)

# pip install --editable .; integrity ./testdir

# if __name__ == '__main__':
#     try:
#         import shutil
#         shutil.rmtree('./testdir/.integrity')
#     except:
#         pass
#
#     cli('./testdir')
