###############
django-colorful
###############

An extension to the Django web framework that provides a database and form
field to accept and store colors in the RGB format.

.. image:: https://travis-ci.org/charettes/django-colorful.svg?branch=master
    :target: https://travis-ci.org/charettes/django-colorful

.. image:: https://coveralls.io/repos/charettes/django-colorful/badge.svg?branch=master&service=github
    :target: https://coveralls.io/github/charettes/django-colorful?branch=master

************
Installation
************

>>> pip install django-colorful

Make sure ``'colorful'`` is in your `INSTALLED_APPS`:

::

    INSTALLED_APPS.append('colorful')

*****
Usage
*****

In order to use a color field you just have to add it to your model definition:

::

    from django.db import models
    from colorful.fields import RGBColorField

    class Tag(models.Model):
        color = RGBColorField()

The ``RGBColorField`` class also accepts a ``color`` keyword argument which can
be set to a list of colors that should be visible as preset color palette:

::

    color = RGBColorField(colors=['#FF0000', '#00FF00', '#0000FF'])

The ``ColorFieldWidget`` should take care of providing a JavaScript based shim
on browsers that don't support the HTML5 color input.

Note: To enable HTML5 color input with `Django Grappelli`_ ensure that ``GRAPPELLI_CLEAN_INPUT_TYPES`` is set to ``False`` in your settings file.

.. _Django Grappelli: https://github.com/sehmaschine/django-grappelli
