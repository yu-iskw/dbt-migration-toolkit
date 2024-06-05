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

import os
import tempfile
import unittest

from ruamel.yaml import YAML

from dbt_migration_toolkit.config import IndentConfig, YamlConfig


class TestConfig(unittest.TestCase):

    def setUp(self):
        self.config_data = {
            "explicit_start": True,
            "explicit_end": True,
            "preserve_quotes": True,
            "width": 80,
            "indent": {
                "offset": 4,
                "sequence": 8,
                "mapping": 4,
            }
        }
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, mode='w')
        yaml = YAML()
        yaml.dump(self.config_data, self.temp_file)
        self.temp_file.close()

    def tearDown(self):
        os.remove(self.temp_file.name)

    def test_load(self):
        config = YamlConfig.load(self.temp_file.name)
        self.assertTrue(config.explicit_start)
        self.assertTrue(config.explicit_end)
        self.assertTrue(config.preserve_quotes)
        self.assertEqual(config.width, 80)
        self.assertEqual(config.indent.offset, 4)
        self.assertEqual(config.indent.sequence, 8)
        self.assertEqual(config.indent.mapping, 4)

    def test_to_ruamel_yaml(self):
        config = YamlConfig.load(self.temp_file.name)
        yaml = config.to_ruamel_yaml()
        self.assertEqual(yaml.explicit_start, config.explicit_start)
        self.assertEqual(yaml.explicit_end, config.explicit_end)
        self.assertEqual(yaml.preserve_quotes, config.preserve_quotes)
        self.assertEqual(yaml.width, config.width)
        self.assertEqual(yaml.map_indent, config.indent.mapping)
        self.assertEqual(yaml.sequence_indent, config.indent.sequence)
        self.assertEqual(yaml.sequence_dash_offset, config.indent.offset)

if __name__ == '__main__':
    unittest.main()
