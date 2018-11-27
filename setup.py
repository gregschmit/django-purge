import os
from setuptools import find_packages, setup
from purge import version


# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

# stamp the package prior to installation
version.stamp_directory(os.path.join(os.getcwd(), 'purge'))

setup(
    name='django-purge',
    version=version.get_version(),
    packages=['purge'],
    include_package_data=True,
    package_data={'purge': ['VERSION_STAMP']},
    description='An app for purging database records (e.g., logs).',
    url='https://github.com/gregschmit/django-purge',
    author='Gregory N. Schmit',
    author_email='gschmi4@uic.edu',
    license
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 2.0',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP',
    ],
)
