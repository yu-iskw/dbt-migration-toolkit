# dbt-migration-toolkit

This is a toolkit for migrating dbt projects to newer versions.

## Install

```shell
git clone https://github.com/yu-iskw/dbt-migration-toolkit.git
cd dbt-migration-toolkit
pip install -e .
```

## Configuration

The commands take advantage of [ruamel.yaml](https://pypi.org/project/ruamel.yaml/) to parse and write YAML files so that we can keep comments in the YAML files.
A config YAML file enables us to configure output formats of YAML files.
The config parser is implemented in [config.py](./dbt_migration_toolkit/config.py).
[config.yml.example](./config.yml.example) is an example of a config YAML file.

```yaml
explicit_start: false
explicit_end: false
preserve_quotes: true
width: 4096
indent:
  offset: 2
  sequence: 4
  mapping: 2
```

## Commands

### `convert-tests-to-data-tests`

#### Background

This command converts tests to data_tests.

Data tests were historically called "tests" in dbt as the only form of testing available. With the introduction of unit tests in v1.8, it was necessary to update our naming conventions and syntax.
As of v1.8, tests: is still supported in your YML configuration files as an alias but will be deprecated in the future in favor of data_tests:.

As we progress towards this deprecation, we'll update the examples in our docs pages to reflect this new syntax, but we highly recommend you begin the migration process as soon as you upgrade to v1.8 to avoid interruptions or issues in the future.

<https://docs.getdbt.com/docs/build/data-tests#new-data_tests-syntax>

#### How to use it

The `convert-tests-to-data-tests` command has the following options:

- `--path`: This option is required and specifies the path to the dbt resource files that need to be processed. The path should point to the directory containing your dbt models, sources, or seeds.

- `--config`: This option is optional and specifies the path to the dbt config file. The config file should be a YAML file that contains settings for how the YAML files should be processed and formatted. If not provided, default settings will be used.

Example usage:

```shell
convert-tests-to-data-tests --path path/to/your/models
```

## Limitations

If a YAML file starts with `---`, the commands may encounter issues parsing the YAML file.
They are designed to handle only a single block of YAML in a file.

```yaml
---
models:
  - name: ....
```
