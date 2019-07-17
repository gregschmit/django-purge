import os
from setuptools import find_packages, setup
from purge import version


# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

# stamp the package prior to installation
version.stamp_directory('./purge')

setup(
    name='django-purge',
    version=version.get_version(),
    packages=find_packages(),
    include_package_data=True,
    package_data={'purge': ['VERSION_STAMP']},
    description='A reusable Django app for purging database records (e.g., logs).',
    long_description="A reusable Django app for purging old database records and files. Automatic scheduling is supported with `django-cron`, or you can periodically run the management command `purge`.",
    install_requires=['Django>=2', 'python-dateutil'],
    url='https://github.com/gregschmit/django-purge',
    author='Gregory N. Schmit',
    author_email='gschmi4@uic.edu',
    license='MIT',
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

# un-stamp the package after installation
version.unstamp_directory('./purge')
