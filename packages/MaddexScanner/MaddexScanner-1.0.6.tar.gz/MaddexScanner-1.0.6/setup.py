
import re, codecs, sys, os
from setuptools import setup, find_packages

try:
    with codecs.open( "README.md", 'r', errors='ignore' ) as file:
        readme_contents = file.read()
except Exception as error:
    readme_contents = ""
    sys.stderr.write( "Warning: Could not open README.md due %s\n" % error )
    
requirements = ["sqlalchemy==1.3.20", "psycopg2-binary"]

setup(
    name='MaddexScanner',
    author='ShhWizard',
    author_email='cpjojowat007@gmail.com',
    version='1.0.6',
    description='Maddex Scanner module repo.',
    long_description = readme_contents,
    long_description_content_type='text/markdown',
    url='https://github.com/Wizard',
    packages=find_packages(),
    license='GNU General Public License v3.0',
    classifiers=[
        "Framework :: AsyncIO",
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)',
        "Natural Language :: English",
        "Operating System :: OS Independent",
        'Programming Language :: Python :: 3.7',
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Build Tools",

    ],
    include_package_data=True,
    keywords=['telegram', 'Maddex', 'scanner', 'pyrogram'],
    install_requires=requirements
)
