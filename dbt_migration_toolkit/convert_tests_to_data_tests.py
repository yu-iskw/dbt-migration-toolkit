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


# The script enables us to replace the `test` meta in dbt resource files with the `data_test` meta.
# SEE https://docs.getdbt.com/docs/build/data-tests#new-data_tests-syntax

import copy

import click
from loguru import logger
from ruamel.yaml import YAML

from dbt_migration_toolkit.config import Config
from dbt_migration_toolkit.utils import DbtResourceType, find_yaml_files


@click.command()
@click.option(
    "--path",
    type=click.Path(exists=True),
    required=True,
    help="The path to the dbt resource files",
)
@click.option(
    "--config",
    type=click.Path(exists=True),
    required=False,
    help="The path to the dbt config file.",
)
def main(path: str, config: str = None):
    """Replace the `test` meta in dbt resource files with the `data_test` meta.

    Data tests were historically called "tests" in dbt as the only form of testing available.
    With the introduction of unit tests in v1.8, it was necessary to update our naming conventions and syntax.
    As of v1.8, tests: is still supported in your YML configuration files as an alias but will be deprecated in the future in favor of tests:.

    As we progress towards this deprecation, we'll update the examples in our docs pages to reflect this new syntax,
    but we highly recommend you begin the migration process as soon as you upgrade to v1.8 to avoid interruptions or issues in the future.

    SEE https://docs.getdbt.com/docs/build/data-tests#new-data_tests-syntax
    """
    # Load the config
    config_obj = Config.load(path=config)
    ruamel_yaml = config_obj.to_ruamel_yaml()
    # Load all yaml files in the models_path
    for yaml_file_path in find_yaml_files(path):
        replaced_yaml_data = None
        with open(yaml_file_path, "r", encoding="utf-8") as f:
            yaml_data = ruamel_yaml.load(f)
            replaced_yaml_data = replace_tests(yaml_data)
        with open(yaml_file_path, "w", encoding="utf-8") as f:
            ruamel_yaml.dump(replaced_yaml_data, f)


def replace_tests(yaml_data):
    resource_type = DbtResourceType.get_resource_type(yaml_data)
    if resource_type == DbtResourceType.MODEL:
        return replace_tests_in_models(yaml_data)
    elif resource_type == DbtResourceType.SOURCE:
        return replace_tests_in_sources(yaml_data)
    elif resource_type == DbtResourceType.SEED:
        return replace_tests_in_seeds(yaml_data)
    else:
        logger.warning(f"Unsupported resource type: {resource_type}")


def replace_tests_in_models(yaml_data):
    # Replace table level test meta with data_test meta
    copied_yaml_data = copy.deepcopy(yaml_data)
    for model in copied_yaml_data.get("models", []):
        if "tests" in model:
            model["data_tests"] = model["tests"]
            del model["tests"]
        if "columns" in model:
            for column in model["columns"]:
                if "tests" in column:
                    column["data_tests"] = column["tests"]
                    del column["tests"]
    return copied_yaml_data


def replace_tests_in_sources(yaml_data):
    copied_yaml_data = copy.deepcopy(yaml_data)
    for source in copied_yaml_data.get("sources", []):
        for table in source.get("tables", []):
            if "tests" in table:
                table["data_tests"] = table["tests"]
                del table["tests"]
            if "columns" in table:
                for column in table["columns"]:
                    if "tests" in column:
                        column["data_tests"] = column["tests"]
                        del column["tests"]
    return copied_yaml_data


def replace_tests_in_seeds(yaml_data):
    copied_yaml_data = copy.deepcopy(yaml_data)
    for seed in copied_yaml_data.get("seeds", []):
        if "tests" in seed:
            seed["data_tests"] = seed["tests"]
            del seed["tests"]
        if "columns" in seed:
            for column in seed["columns"]:
                if "tests" in column:
                    column["data_tests"] = column["tests"]
                    del column["tests"]
    return copied_yaml_data
