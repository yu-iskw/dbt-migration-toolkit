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

from pydantic import BaseModel, Field
from ruamel.yaml import YAML, safe_load


class IndentConfig(BaseModel):
    offset: int = Field(default=2, description="Offset for sequence indentation")
    sequence: int = Field(
        default=4, description="Number of spaces for sequence indentation"
    )
    mapping: int = Field(
        default=2, description="Number of spaces for mapping indentation"
    )

    model_config = {"frozen": True}


class Config(BaseModel):
    explicit_start: bool = Field(
        default=False,
        description="Whether to start the document with an explicit '---'",
    )
    explicit_end: bool = Field(
        default=False, description="Whether to end the document with an explicit '...'"
    )
    preserve_quotes: bool = Field(
        default=False, description="Whether to preserve quotes in the output"
    )
    width: int = 4096
    indent: IndentConfig = Field(default=IndentConfig())

    @classmethod
    def load(cls, path: str) -> "Config":
        if not path:
            return cls()
        yaml = YAML(typ="safe", pure=True)
        with open(path, "r") as f:
            data = yaml.load(f)
            return cls(**data)

    def to_ruamel_yaml(self) -> YAML:
        yaml = YAML()
        yaml.width = self.width
        yaml.explicit_start = self.explicit_start
        yaml.explicit_end = self.explicit_end
        yaml.preserve_quotes = self.preserve_quotes
        yaml.indent(
            mapping=self.indent.mapping,
            sequence=self.indent.sequence,
            offset=self.indent.offset,
        )
        return yaml
