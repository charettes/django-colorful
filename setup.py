#!/usr/bin/env python
from setuptools import setup, find_packages

from colorful import VERSION

setup(
    name='django-colorful',
    version='.'.join(str(v) for v in VERSION),
    description='An extension to the Django web framework that provides database and form color fields',
    long_description=open('README.rst').read(),
    url='https://github.com/charettes/django-colorful',
    author='Simon Charette',
    author_email='charette.s@gmail.com',
    install_requires=[
        'Django>=1.8',
    ],
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    license='MIT License',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.8',
        'Framework :: Django :: 1.9',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Internet :: WWW/HTTP :: WSGI',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
