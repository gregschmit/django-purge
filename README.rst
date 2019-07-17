Purge
#####

.. inclusion-marker-do-not-remove

.. image:: https://readthedocs.org/projects/django-purge/badge/?version=latest
    :target: https://django-purge.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

Documentation: https://django-purge.readthedocs.io

Source: https://github.com/gregschmit/django-purge

PyPI: https://pypi.org/project/django-purge/

Purge is a reusable Django app for regularly purging old database entries, like
logs.

**The Problem**: Tables/models like sessions and logs can grow without limit.

**The Solution**: This app allows you to schedule database purging of old
records. You can also make FilePurgers which can purge old files based on
datestamps in the filename or timestamps in the meta-data (atime/mtime/ctime).

How to Use
##########

.. code-block:: shell

    $ pip install django-purge

Include :code:`purge` in your :code:`INSTALLED_APPS`. Then, create your
database purgers or file purgers in the admin interface.

Then, either periodically call the :code:`purge` management command (e.g., via a
system cronjob), or install and configure :code:`django-cron` (add
:code:`purge.cron` to your :code:`CRON_CLASSES` in your
:code:`settings.py`). The builtin :code:`CronJob` class is set to run every 4
hours. You can change this by altering your :code:`settings.py` and adding
:code:`PURGE_CRON_RUN_AT_TIMES` to an array of times you want to run the job at
(e.g., :code:`['1:00']` to run at 1am).

Contributing
############

Email gschmi4@uic.edu if you want to contribute. You must only contribute code
that you have authored or otherwise hold the copyright to, and you must
make any contributions to this project available under the MIT license.

To collaborators: don't push using the :code:`--force` option.

Dev Quickstart
##############

Purge comes with a `settings.py` file, technically making it a Django project as
well as a Django app. First clone, the repository into a location of your
choosing:

.. code-block:: shell

    $ git clone https://github.com/gregschmit/django-purge

Then you can go into the :code:`django-purge` directory and do the initial
migrations and run the server (you may need to type :code:`python3` rather than
:code:`python`):

.. code-block:: shell

    $ cd django-purge
    $ python manage.py makemigrations
    $ python manage.py migrate
    $ python manage.py createsuperuser
    ...
    $ python manage.py runserver

Then you can see the models at http://127.0.0.1:8000/admin.
