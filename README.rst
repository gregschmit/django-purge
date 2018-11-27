Purge
#####

Purge is a Django app for regularly purging old database entries. You can run the jobs using the app `django-dcron` or you can periodically call the management command `purge`.

How to Use
##########

Include :code:`purge` in your :code:`INSTALLED_APPS`. Then configure the settings (some defaults are provided) and create your database purgers.

Contributing
############

Email gschmi4@uic.edu if you want to contribute. You must only contribute code
that you have authored or otherwise hold the copyright to, and you must
make any contributions to this project available under the MIT license.

To collaborators: don't push using the :code:`--force` option.

Dev Quickstart
##############

First clone, the repository into a location of your choosing:

.. code-block:: shell

    $ git clone https://github.com/gregschmit/django-purge

Then you can go into the :code:`django-purge` directory and do the initial migrations and run the server (you may need to type :code:`python3` rather than :code:`python`):

.. code-block:: shell

    $ cd django-purge
    $ python manage.py makemigrations purge
    $ python manage.py migrate
    $ python manage.py runserver

Then you can see the models at 127.0.0.1:8000/admin.
