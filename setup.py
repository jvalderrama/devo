import sys
from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

if sys.version_info < (2, 7):
    requirements.append('argparse')
elif sys.version_info < (2, 7):
    raise 'Must use python 2.7 or greater'

with open('README.md') as f:
    long_description = f.read()

setup(
    name='Devo Web App',
    version='1.0',
    author='Jorge Valderrama',
    author_email='',
    description='API Check RabbitMQ Status',
    long_description=long_description,
    install_requires=requirements,
    packages=['app'],
    data_files=[('app/rabbitmq.yaml', ['app/rabbitmq.yaml'])],
    license='Apache License 2.0',
    classifiers=[
        "Development Status :: 1 - Planning",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: Apache Software License",
        "Natural Language :: English",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Topic :: System"
        "Framework :: Flask"
    ],
    entry_points={
        'console_scripts': [
            'devo=app.app:app.run',
        ],
    },
)