#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup
from pkgver import package_version
with open('README.rst') as readme_file:
    readme = readme_file.read()

requirements = [
    'slack-sdk>=3.19.1',
    'mixpanel>=4.10.0'
]

setup(
    name='scora-notify',
    version=package_version,
    description="Scora Slack notification lib",
    long_description=readme,
    author="Oncase",
    author_email='contato@oncase.com.br',
    package_dir = {"scora_notify": "src"},
    packages=['scora_notify','pkgver'],
    zip_safe=True,
    install_requires=requirements,
    extras_require={
        'dev': [
            'twine>=3.1.1',
            'Sphinx==3.1.1',
            'sphinxcontrib-napoleon==0.7',
            'sphinx-rtd-theme==0.5.0',
            'sphinx-click==2.3.2',
            'flake8==3.8.3'
        ]
    },
    keywords='scora',
    classifiers=[
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6',
    ]
)
