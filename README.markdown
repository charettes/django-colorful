django-colorful
================

**django-colorful** is an extension to the Django web framework that provides
database and form color fields (only RGB atm).

Written by Simon Charette
Inspired by http://djangosnippets.org/snippets/1261/
Built with https://github.com/laktek/really-simple-color-picker

Usage
-------------
In order to use a color field you just have to add it to your model definition:

    from django.db import models
    from colorful.fields import RGBColorField

    class Tag(models.Model)
      color = RGBColorField()

The extension will take care of providing the custom widget, just make sure you
include the static files and jQuery >= 1.2.

In order to use with django.contrib.staticfiles add 'colorful' to
project's INSTALLED_APPS.
