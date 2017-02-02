import os
from distutils.core import setup


def read_file_into_string(filename):
    path = os.path.abspath(os.path.dirname(__file__))
    filepath = os.path.join(path, filename)
    try:
        return open(filepath).read()
    except IOError:
        return ''


def get_readme():
    for name in ('README', 'README.rst', 'README.md'):
        if os.path.exists(name):
            return read_file_into_string(name)
    return ''


setup(
    name='kb-invoice',
    packages=['invoice', 'invoice.management', 'invoice.management.commands', 'invoice.tests', 'invoice.migrations'],
    package_data={
        'invoice': [
            'templates/*.*',
            'templates/invoice/*.*',
            'templates/search/*.*',
            'templates/search/indexes/*.*',
            'templates/search/indexes/invoice/*.*',
        ],
    },
    version='0.1.40',
    description='invoice',
    author='Malcolm Dinsmore',
    author_email='code-md@kbsoftware.co.uk',
    url='git@github.com:pkimber/invoice.git',
    classifiers=[
        'Development Status :: 1 - Planning',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Framework :: Django :: 1.8',
        'Topic :: Office/Business :: Scheduling',
    ],
    long_description=get_readme(),
)