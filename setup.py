from distutils.core import setup
from setuptools import find_packages

setup(
    name='geoverlay',
    version='0.1.0',
    packages = find_packages(),
    description='Server that provides tiled maps as google earth kml overlays.',
    author='Gregor Sturm',
    author_email='mail@gregor-sturm.de',
    url='https://github.com/grst/geoverlay',  # use the URL to the github repo
    keywords=['maps', 'google earth', 'overlay'],  # arbitrary keywords
    license='GPLv3',
    install_requires=[
        'flask'
    ],
    classifiers=[],
    entry_points={
        'console_scripts': ['geoverlay=server.server:run_app'],
    },
    include_package_data=True
)
