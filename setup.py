from distutils.core import setup
from setuptools import find_packages

setup(
    name='geos',
    version='0.1.0',
    packages=find_packages(),
    description='Server for displaying tiled maps in Google Earth',
    author='Gregor Sturm',
    author_email='mail@gregor-sturm.de',
    url='https://github.com/grst/geos',  # use the URL to the github repo
    keywords=['maps', 'google earth', 'overlay'],  # arbitrary keywords
    license='GPLv3',
    install_requires=[
        'flask', 'pykml', 'lxml'
    ],
    classifiers=[],
    entry_points={
        'console_scripts': ['geos=geos.scripts.runserver:run_app'],
    },
    include_package_data=True
)
