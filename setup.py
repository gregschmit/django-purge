import os
from setuptools import find_packages, setup
import purge


# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

# get README
with open('README.rst') as f:
    long_description = f.read()

setup(
    name='django-purge',
    version=purge.__version__,
    packages=find_packages(),
    description='A reusable Django app for purging database records (e.g., logs).',
    long_description=long_description,
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
