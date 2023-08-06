from setuptools import setup
from mccolor import __version__


setup(
    name='mccolor',
    packages=['mccolor'],
    version=__version__,
    description='Simple library to use minecraft color codes in terminal',
    long_description=open('README.rst').read(),
    keywords=['color', 'colour', 'paint', 'ansi', 'terminal', 'linux',
              'python', 'python3', 'minecraft'],
    author='wrrulos',
    author_email='vegapedro2004@gmail.com',
    url='https://github.com/wrrulos/mccolor',
    classifiers=[
        'Environment :: Console',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Operating System :: POSIX :: Linux',
        'Operating System :: POSIX :: Other',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Topic :: Terminals']
)
