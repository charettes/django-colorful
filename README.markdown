django-colorful
===============

[![Build Status](https://travis-ci.org/charettes/django-colorful.svg?branch=master)](https://travis-ci.org/charettes/django-colorful)
[![Coverage Status](https://coveralls.io/repos/charettes/django-colorful/badge.png)](https://coveralls.io/r/charettes/django-colorful)

**django-colorful** is an extension to the Django web framework that provides
database and form color fields (only RGB atm).

Written by Simon Charette
Inspired by http://djangosnippets.org/snippets/1261/
Built with https://github.com/laktek/really-simple-color-picker

Installation
------------

From PyPI:

    $ pip install django-colorful

Or by downloading the source and running:

    $ python setup.py install

Latest git version:

    $ pip install -e git+git://github.com/charettes/django-colorful.git#egg=django-colorful

Usage
-------------
In order to use a color field you just have to add it to your model definition:

    from django.db import models
    from colorful.fields import RGBColorField

    class Tag(models.Model)
      color = RGBColorField()

There's the keyword argument `colors` which can set to a list of colors that
should be visible as preset color palette:

    color = RGBColorField(colors=['#FF0000', '#00FF00', '#0000FF'])

The extension will take care of providing the custom widget, just make sure you
include the static files and jQuery >= 1.2.

In order to use with django.contrib.staticfiles add 'colorful' to
project's INSTALLED_APPS.
