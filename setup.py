#!/usr/bin/python

from setuptools import setup, find_packages

from colorful import VERSION

github_url = 'https://github.com/charettes/django-colorful'

setup(
    name='django-colorful',
    version='.'.join(str(v) for v in VERSION),
    description='An extension to the Django web framework that provides database and form color fields',
    long_description=open('README.markdown').read(),
    url=github_url,
    author='Simon Charette',
    author_email='charette.s@gmail.com',
    install_requires=[
        'Django>=1.2',
    ],
    packages=find_packages(),
    include_package_data=True,
    license='MIT License',
    classifiers=[
        'Development Status :: 1 - Planning',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
)
