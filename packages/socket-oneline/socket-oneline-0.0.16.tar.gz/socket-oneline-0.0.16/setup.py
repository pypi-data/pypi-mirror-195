from setuptools import find_packages
from setuptools import setup

from tools import common

common.init()
print(f'==== {"version": <11}: v{common.cmn_version}')

# @formatter:off
setup(
    description='Client server base class over socket',
    keywords=['socket', 'client server', 'simple'],
    install_requires=[
        'pytest-ver',
        'pytest',
    ],
    classifiers=[
        # Choose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable"
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Topic :: Utilities',
        'Programming Language :: Python :: 3.9',
        common.cmn_classifier_license,
    ],

    # common attributes from here on
    name=common.cmn_mod_name,
    include_package_data=True,
    packages=find_packages(include=f'{common.cmn_mod_dir_name}*', ),
    version=common.cmn_version,
    license=common.cmn_license,
    long_description=common.cmn_long_desc,
    long_description_content_type=common.cmn_long_desc_type,
    author=common.cmn_author,
    author_email=common.cmn_email,
    url=common.cmn_homepage_url,
    download_url=common.cmn_download_url,
)
# @formatter:on

print('OK   GenBuildInfo completed successfully')
