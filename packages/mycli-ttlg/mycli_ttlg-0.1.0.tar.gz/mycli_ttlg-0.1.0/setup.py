
from setuptools import setup, find_packages

setup(
    name='mycli_ttlg',
    version='0.1.0',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'mycli_ttlg=mycli_ttlg.cli:main',
        ],
    },
)

