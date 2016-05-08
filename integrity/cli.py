from .application import Application

import click


@click.command()
@click.argument('path', type=click.Path(exists=True))
@click.option('--hash', '-h', multiple=True)
def cli(path, hash):
    hashes = [i for i in hash]
    app = Application(path)
    app.create_check(hashes=hashes)

# pip install --editable .; integrity ./testdir

# if __name__ == '__main__':
#     try:
#         import shutil
#         shutil.rmtree('./testdir/.integrity')
#     except:
#         pass
#
#     cli('./testdir')
