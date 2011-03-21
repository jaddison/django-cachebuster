import os
from distutils.core import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = 'django-cachebuster',
    description = 'Django 1.3 ready cache busting app',
    long_description=read('README.rst'),
    author='James Addison',
    author_email='code@scottisheyes.com',
    packages = ['cachebuster','cachebuster.templatetags','cachebuster.detectors'],
    version = '0.1.2',
    url='http://github.com/jaddison/django-cachebuster',
    keywords=[],
    license='BSD',
    classifiers=[
      'Development Status :: 3 - Alpha',
      'Intended Audience :: Developers',
      'License :: OSI Approved :: BSD License',
      'Topic :: Internet :: WWW/HTTP :: WSGI',
      'Framework :: Django',
    ],
)