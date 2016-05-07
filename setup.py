from setuptools import setup

setup(
    name='integrity',
    version='0.0.1',
    py_modules=['integrity'],
    include_package_data=True,
    install_requires=[
    ],
    entry_points='''
        [console_scripts]
        integrity=integrity.cli:cli
    ''',
)