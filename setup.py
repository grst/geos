from distutils.core import setup
from setuptools import find_packages

setup(
    name='geos',
    version='0.2.2',
    packages=find_packages(),
    description='Map server to view, measure and print maps in a web browser'
                'and to display maps as an overlay in google earth.',
    author='Gregor Sturm',
    author_email='mail@gregor-sturm.de',
    url='https://github.com/grst/geos',  # use the URL to the github repo
    keywords=['maps', 'google earth', 'overlay', 'map printing'],  # arbitrary keywords
    license='GPLv3',
    install_requires=[
        'flask', 'lxml', 'pillow'
    ],
    classifiers=[],
    entry_points={
        'console_scripts': ['geos=geos.scripts.runserver:run_app'],
    },
    include_package_data=True
)
