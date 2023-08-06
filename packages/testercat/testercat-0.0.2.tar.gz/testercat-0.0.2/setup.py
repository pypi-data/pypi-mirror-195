from os import path
from setuptools import setup, find_packages


setup(
    name='testercat',
    version='0.0.2',
    description='tester',
    long_description_content_type='text/markdown',
    url='https://catalyst.zoho.com/',
    scripts=[],
    packages=find_packages(exclude=['tests*']),
    install_requires=['requests==2.28.1'],
    license='Apache License 2.0',
    python_requires=">= 3.9",
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers'
    ],
)

