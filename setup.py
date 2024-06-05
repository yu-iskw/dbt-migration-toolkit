# Copyright 2024 yu-iskw
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from setuptools import find_packages, setup

setup(
    name="dbt-migration-toolkit",
    version="0.0.1",
    description="A toolkit for migrating dbt projects",
    author="yu-iskw",
    author_email="yu.iskw@gmail.com",
    packages=find_packages(),
    install_requires=[
        "pydantic>=2.5.0,<3.0.0",
        "ruamel.yaml>=0.18.0,<0.19.0",
        "click>=8.0.0,<9.0.0",
        "loguru>=0.7,<0.8",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0,<8.0.0",
            "pre-commit>=3.7,<4.0",
        ]
    },
    entry_points={
        "console_scripts": [
            "convert-tests-to-data-tests = dbt_migration_toolkit.convert_tests_to_tests:main",
        ],
    },
)
