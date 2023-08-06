#! /usr/bin/python3
# This file is licensed under the Elastic License 2.0. Copyright 2021-present, StarRocks Inc.
import os

from setuptools import find_namespace_packages, setup

package_name = "dbt-dataops-starrocks"
# make sure this always matches dbt/adapters/starrocks/__version__.py
package_version = "1.4.3"
description = """The starrocks adapter plugin for dbt"""

this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, "README.md")) as f:
    long_description = f.read()

setup(
    name=package_name,
    version=package_version,
    description=description,
    long_description=long_description,
    long_description_content_type="text/markdown",
    platforms="any",
    license="Apache License 2.0",
    license_files=("LICENSE.txt",),
    author="fujianhj, long2ice",
    author_email="fujianhj@gmail.com, long2ice@gmail.com",
    url="https://github.com/StarRocks/starrocks/tree/main/contrib/dbt-connector",
    packages=find_namespace_packages(include=['dbt', 'dbt.*']),
    package_data={
        "dbt": [
            "include/starrocks/dbt_project.yml",
            "include/starrocks/sample_profiles.yml",
            "include/starrocks/macros/*.sql",
            "include/starrocks/macros/*/*.sql",
            "include/starrocks/macros/*/*/*.sql",
        ]
    },
    include_package_data=True,
    install_requires=[
        "dbt-core==1.4.1",
        "mysql-connector-python==8.0.29",
        "pytz==2022.7.1"
    ],
    zip_safe=False,
    classifiers=[
        'Development Status :: 5 - Production/Stable',

        'License :: OSI Approved :: Apache Software License',

        'Operating System :: Microsoft :: Windows',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX :: Linux',

        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
    python_requires=">=3.7",
)
