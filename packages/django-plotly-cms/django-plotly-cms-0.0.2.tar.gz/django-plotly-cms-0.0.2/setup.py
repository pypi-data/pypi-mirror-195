#!/usr/bin/env python

from setuptools import setup


with open('dpcms/version.py') as f:
    exec(f.read())


with open('README.md') as f:
    long_description = f.read()


setup(
    name="django-plotly-cms",
    version=__version__,
    url="https://gitlab.com/GibbsConsulting/dpcms",
    description="Django-CMS use of django-plotly-dash and plotly dash",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Gibbs Consulting",
    author_email="py.dpcms@gibbsconsulting.ca",
    license='AGPL v3',
    packages=[
        'dpcms',
    ],
    include_package_data=True,
    classifiers = [
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: GNU Affero General Public License v3',
    'Programming Language :: Python :: 3',
    'Framework :: Dash',
    ],
    keywords='django plotly plotly-dash dash dashboard django-cms',
    project_urls = {
    'Source': "https://gitlab.com/GibbsConsulting/djcms",
    'Tracker': "https://gitlab.com/GibbsConsulting/djcms/issues",
    'Documentation': 'http://djcms.readthedocs.io/',
    },
    install_requires = [#'django-plotly-dash',
    ],
    python_requires=">=3.8",
    )
