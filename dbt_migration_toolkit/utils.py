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

import enum
import glob
from typing import Iterable


class DbtResourceType(str, enum.Enum):
    SEED = "seed"
    SOURCE = "source"
    MODEL = "model"
    SNAPSHOT = "snapshot"

    @classmethod
    def get_resource_type(cls, data) -> "DbtResourceType":
        if "models" in data:
            return DbtResourceType.MODEL
        elif "sources" in data:
            return DbtResourceType.SOURCE
        elif "seeds" in data:
            return DbtResourceType.SEED
        elif "snapshots" in data:
            return DbtResourceType.SNAPSHOT
        else:
            raise ValueError(f"Invalid dbt resource type: {data}")


def find_yaml_files(path: str) -> Iterable[str]:
    """Find all YAML files in a directory."""
    for file in glob.glob(f"{path}/*.yml") + glob.glob(f"{path}/*.yaml"):
        yield file
