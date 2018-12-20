Purge
#####

.. inclusion-marker-do-not-remove

.. image:: https://readthedocs.org/projects/django-purge/badge/?version=latest
    :target: https://django-purge.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

Documentation: https://django-purge.readthedocs.io

Source: https://github.com/gregschmit/django-purge

PyPI: https://pypi.org/project/django-purge/

Purge is a reusable Django app for regularly purging old database entries, like logs.

**The Problem**: Tables/models like sessions and logs can grow without limit.

**The Solution**: This app allows you to schedule database purging of old
records.

How to Use
##########

.. code-block:: shell

    $ pip install django-purge

Include :code:`purge` in your :code:`INSTALLED_APPS`. Then, create your database purgers in the admin interface.

Then, either install and configure :code:`django-dcron` or setup a system cronjob to run the management command :code:`purge` periodically.

Contributing
############

Email gschmi4@uic.edu if you want to contribute. You must only contribute code
that you have authored or otherwise hold the copyright to, and you must
make any contributions to this project available under the MIT license.

To collaborators: don't push using the :code:`--force` option.

Dev Quickstart
##############

Purge comes with a `settings.py` file, technically making it a Django project as well as a Django app. First clone, the repository into a location of your choosing:

.. code-block:: shell

    $ git clone https://github.com/gregschmit/django-purge

Then you can go into the :code:`django-purge` directory and do the initial migrations and run the server (you may need to type :code:`python3` rather than :code:`python`):

.. code-block:: shell

    $ cd django-purge
    $ python manage.py makemigrations purge
    $ python manage.py migrate
    $ python manage.py createsuperuser
    ...
    $ python manage.py runserver

Then you can see the models at http://127.0.0.1:8000/admin.
