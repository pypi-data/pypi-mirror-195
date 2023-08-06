""" setup.py """
#
# Martin J Levy / W6LHI (c) 2023
#

import re
from distutils.core import setup

_version_re = re.compile(r"__version__\s=\s'(.*)'")
with open('es100/__init__.py', 'r') as f:
    version = _version_re.search(f.read()).group(1)
with open('README.md') as f:
    long_description = f.read()

setup(
    name = 'es100-wwvb',
    packages = ['es100', 'wwvb'],
    version = version,
    license = 'GNU General Public License v3.0',
    description = 'Time and date decoder for the ES100 WWVB receiver',
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    author = 'Martin J Levy',
    author_email = 'mahtin@mahtin.com',
    url = 'https://github.com/mahtin/es100-wwvb',
    download_url = 'https://github.com/mahtin/es100-wwvb/archive/refs/tags/%s.tar.gz' % version,
    keywords = ['WWVB', 'ES100', 'NIST', 'Time', 'Time Synchronization', 'VLW', 'Very Long Wavelength', 'NTP'],
    install_requires = ['smbus', 'ephem', 'RPi.GPIO'],
    options = {"bdist_wheel": {"universal": True}},
    include_package_data = True,
    entry_points = {'console_scripts': ['wwvb=wwvb.__main__:main']},
    python_requires=">=3.7",

    classifiers = [
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Topic :: Communications :: Ham Radio',
        'Topic :: System :: Networking :: Time Synchronization',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3',
    ],
)
