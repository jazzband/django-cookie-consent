from distutils.core import setup
from setuptools import find_packages


version = '0.2.1'

CLASSIFIERS = [
    'Framework :: Django',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: BSD License',
    'Operating System :: OS Independent',
    'Topic :: Software Development',
]

install_requires = [
    'Django>=1.9',
    'django-appconf',
]

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
)
