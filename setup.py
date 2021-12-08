from distutils.core import setup
from setuptools import find_packages


version = '0.3.0'

CLASSIFIERS = [
    'Framework :: Django',
    'Framework :: Django :: 2.2',
    'Framework :: Django :: 3.0',
    'Framework :: Django :: 3.1',     
    'Framework :: Django :: 3.2',     
    'Framework :: Django :: 4.0',     
    'Intended Audience :: Developers',
    'License :: OSI Approved :: BSD License',
    'Operating System :: OS Independent',
    'Topic :: Software Development',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10',
]

install_requires = [
    'Django>=2.2',
    'django-appconf',
]


def read(f):
    return open(f, 'r').read()


setup(
    name="django-cookie-consent",
    description="Django cookie consent application",
    version=version,
    author="Informatika Mihelac",
    author_email="bmihelac@mihelac.org",
    url="https://github.com/bmihelac/django-cookie-consent",
    packages=find_packages(exclude=["tests"]),
    include_package_data=True,
    install_requires=install_requires,
    classifiers=CLASSIFIERS,
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
)
