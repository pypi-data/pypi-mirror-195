import re
import os
import subprocess

from setuptools import setup, find_packages

##########################################################
AUTHOR = 'ChihYing_Lin'
EMAIL = ''
PACKAGE_NAME = 'cylibs'
URL = 'https://gitlab.com/chihyinglin/cylibs'
LICENSE='MIT'
DESCRIPTION = 'Python libraries by ChihYing'
LONG_DESCRIPTION_FILE = 'README.md'
LONG_DESCRIPTION_TYPE = 'text/markdown'
KEYWORDS = 'cylibs'
INSTALL_REQUIRES = ['requests', 'requests_ntlm']
CLASSIFIERS = [
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Topic :: Software Development :: Libraries'
]
##########################################################


# convert version from git tag to pypi style
# V0.1-3-g908f162 -> V0.1.post3
def convert_version(git_version):
    print("Convert version:")
    print("\tgit version: {}".format(git_version))

    pattern = re.compile(
        r"^[vV]*(?P<main>[0-9.]+)(-(?P<post>[0-9]+))?(-.+)?$")
    ver = pattern.search(git_version)

    if not ver:
        return None

    new_ver = ver.group('main')

    if ver.group('post'):
        new_ver += ".{}".format(ver.group('post'))
    else:
        new_ver += ".0"

    print("\tpypi version: {}".format(new_ver))
    return new_ver


def get_pypi_version():
    init_file_path = f'{PACKAGE_NAME}/ver.py'
    ver_pattern = r'version\s*=\s*[\'"](\d+\.\d+\.\d+)[\'"]'
    version = None
    git_version = None

    with open(init_file_path, "r") as f:
        file_contents = f.read()
        match = re.search(ver_pattern, file_contents)
        if match:
            version = match.group(1)

    print(f"version from ver.py: {version}")
    try:
        ver = subprocess.check_output(
            'git describe --tags', shell=True).rstrip().decode('utf-8')
        git_version = convert_version(ver)
    except subprocess.CalledProcessError:
        pass
    print(f"\tversion from git: {git_version}")

    if git_version and git_version != version:
        new_file_contents = None
        with open(init_file_path, 'r') as f:
            file_contents = f.read()
            new_file_contents = re.sub(ver_pattern, f"version = \"{git_version}\"", file_contents)
        if new_file_contents:
            with open(init_file_path, 'w') as f:
                f.write(new_file_contents)
        version = git_version


    return version


def read_file(file_name):
    # noinspection PyBroadException
    try:
        cur_path = os.path.abspath(os.path.dirname(__file__))
        with open(os.path.join(cur_path, file_name)) as f:
            long_description = f.read()
    except Exception:
        long_description = ""
    return long_description


setup(name=PACKAGE_NAME,
      version=get_pypi_version(),
      description=DESCRIPTION,
      url=URL,
      author=AUTHOR,
      author_email=EMAIL,
      license=LICENSE,
      packages=find_packages(exclude=['tests', 'test_*']),
      long_description=read_file(LONG_DESCRIPTION_FILE),
      long_description_content_type=LONG_DESCRIPTION_TYPE,
      install_requires=INSTALL_REQUIRES,
      classifiers=CLASSIFIERS,
      keywords=KEYWORDS,
      zip_safe=False)
