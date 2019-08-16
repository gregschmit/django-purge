Purge
#####

.. inclusion-marker-do-not-remove

.. image:: https://travis-ci.org/gregschmit/django-purge.svg?branch=master
    :alt: Build Status
    :target: https://travis-ci.org/gregschmit/django-purge

.. image:: https://readthedocs.org/projects/django-purge/badge/?version=latest
    :alt: Documentation Status
    :target: https://django-purge.readthedocs.io/en/latest/?badge=latest

.. image:: https://img.shields.io/pypi/v/django-purge
    :alt: PyPI
    :target: https://pypi.org/project/django-purge/

.. image:: https://coveralls.io/repos/github/gregschmit/django-purge/badge.svg?branch=master
    :alt: Coverage Report
    :target: https://coveralls.io/github/gregschmit/django-purge?branch=master

Documentation: https://django-purge.readthedocs.io

Source: https://github.com/gregschmit/django-purge

PyPI: https://pypi.org/project/django-purge/

Purge is a reusable Django app for regularly purging old database entries, like
logs.

**The Problem**: Tables/models like sessions and logs can grow without limit.

**The Solution**: This app allows you to schedule database purging of old
records. You can also make ``FilePurgers`` which can purge old files based on
datestamps in the filename or timestamps in the meta-data (atime/mtime/ctime).

How to Use
##########

.. code-block:: shell

    $ pip install django-purge

Include ``purge`` in your ``INSTALLED_APPS``. Then, create your database
purgers or file purgers in the admin interface.

Then, either periodically call the ``purge`` management command (e.g., via a
system cronjob), or install and configure ``django-cron`` (add ``purge.cron``
to your ``CRON_CLASSES`` in your ``settings.py``). The builtin ``CronJob``
class is set to run every 4 hours. You can change this by altering your
``settings.py`` and adding ``PURGE_CRON_RUN_AT_TIMES`` to an array of times you
want to run the job at (e.g., ``['1:00']`` to run at 1am).

Contributing
############

Create a pull request if you want to contribute. You must only contribute code
that you have authored or otherwise hold the copyright to, and you must
make any contributions to this project available under the MIT license.

To collaborators: don't push using the ``--force`` option.

Dev Quickstart
##############

Purge comes with a ``settings.py`` file, technically making it a Django project
as well as a Django app. First clone, the repository into a location of your
choosing:

.. code-block:: shell

    $ git clone https://github.com/gregschmit/django-purge

Then you can go into the ``django-purge`` directory and do the initial
migrations and run the server (you may need to type ``python3`` rather than
``python``):

.. code-block:: shell

    $ cd django-purge
    $ python manage.py makemigrations
    $ python manage.py migrate
    $ python manage.py createsuperuser
    ...
    $ python manage.py runserver

Then you can see the models at http://127.0.0.1:8000/admin.
