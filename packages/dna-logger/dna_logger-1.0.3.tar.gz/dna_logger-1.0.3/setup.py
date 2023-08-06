from distutils.command.register import register as register_orig
from distutils.command.upload import upload as upload_orig
from setuptools import find_packages
import setuptools
import os


with open("README.md", "r") as fh:
    long_description = fh.read()

class Register(register_orig):
    def _get_rc_file(self):
        return os.path.join('.', '.pypirc')

class Upload(upload_orig):
    def _get_rc_file(self):
        return os.path.join('.', '.pypirc')

__version__ = '1.0.3'
__author_email = "vishalrv1904@gmail.com"

setuptools.setup(
    name="dna_logger",
    version=__version__,
    author="Vishal Periyasamy Rajendran",
    author_email=__author_email,
    description="Data and Analytics Logging Module",
    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    cmdclass={
        'register': Register,
        'upload': Upload,
    },
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=[],
    dependency_links=[],
    python_requires=">=3.6"
)