#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read().replace('.. :changelog:', '')

requirements = [
    'docopt>=0.6.2',
    'openpyxl>=2.2.3',
    'six>=1.9',
    'polib==1.0.6'
]

test_requirements = [
]

setup(
    name='xlpo',
    version=__import__('xlpo').__version__,
    description="Excel/Gettext conversion utilities.",
    long_description=readme + '\n\n' + history,
    author="Fabio Corneti",
    author_email='info@corneti.com',
    url='https://github.com/fabiocorneti/xlpo',
    packages=[
        'xlpo',
    ],
    package_dir={'xlpo': 'xlpo'},
    include_package_data=True,
    scripts=[
        'xlpo/commands/xls2po.py'
    ],
    entry_points={'console_scripts': [
        'xls2po = xlpo.commands.xls2po:execute'
    ]},
    install_requires=requirements,
    license="BSD",
    zip_safe=False,
    keywords='xlpo',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
