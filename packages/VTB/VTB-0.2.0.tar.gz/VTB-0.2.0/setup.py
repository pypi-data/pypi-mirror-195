import os, re
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

NAME = "VTB"

def read_file(path):
    with open(os.path.join(os.path.dirname(__file__), path)) as fp:
        return fp.read()

def _get_version_match(content):
    # Search for lines of the form: # __version__ = 'ver'
    regex = r"^__version__ = ['\"]([^'\"]*)['\"]"
    version_match = re.search(regex, content, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")

def get_version(path):
    return _get_version_match(read_file(path))

setup(
  name=NAME,
  packages=[NAME],
  version=get_version(os.path.join(NAME, '__init__.py')),
  description='Script made in python to try to have as few detections as possible in Virustotal.',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='https://github.com/CookiesKush',
  author='CookiesKush420',
  author_email='cookiesservices@triots.com',
  license='MIT',
  keywords=['Virus Total', 'Bypass'], 
  install_requires=['requests', 'wmi', 'uuid', 'tmp-folder'], # Add any needed packages here that your package will need to work
  # see classifiers https://pypi.org/pypi?%3Aaction=list_classifiers
  classifiers=[
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3 :: Only'
  ]
)
