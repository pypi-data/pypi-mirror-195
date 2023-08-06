
import io
import os
import sys
import re
from shutil import rmtree

from setuptools import find_packages, setup, Command


with open("arjunarth/__init__.py", encoding="utf-8") as f:
    version = re.findall(r"__version__ = \"(.+)\"", f.read())[0]


with open("README.md", encoding="utf-8") as f:
    readme = f.read()


class UploadCommand(Command):
    """Support setup.py upload."""

    description = 'Build and publish the package.'
    user_options = []

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print('\033[1m{0}\033[0m'.format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

        self.status('Building Source and Wheel (universal) distribution…')
        os.system('{0} setup.py sdist bdist_wheel --universal'.format(sys.executable))

        self.status('Uploading the package to PyPI via Twine…')
        os.system('twine upload dist/*')

        self.status('Pushing git tags…')
        os.system('git tag v{0}'.format(version))
        os.system('git push --tags')

        sys.exit()


# Where the magic happens:
setup(
    name="arjunarth",
    version=version,
    description="BlackWeb Userbot ",
    long_description=readme,
    long_description_content_type='text/markdown',
    author="Ekankth",
    author_email="ekankth@gmail.com",
    python_requires="~=3.8",
    url="https://blackweb.tech",
    packages=find_packages(exclude=["tests", "*.tests", "*.tests.*", "tests.*"]),

    # If your package is a single module, use this instead of 'packages':
    # py_modules=['arjunarth'],

    # entry_points={
    #     'console_scripts': ['mycli=mymodule:cli'],
    # },
    include_package_data=True,
    license='MIT',
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy'
    ],
    # $ setup.py publish support.
    cmdclass={
        'upload': UploadCommand,
    },
)
