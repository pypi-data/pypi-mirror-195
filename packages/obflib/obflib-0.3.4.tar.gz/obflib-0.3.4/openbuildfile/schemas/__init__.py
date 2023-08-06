# SPDX-FileCopyrightText: 2022 Freemelt AB <opensource@freemelt.com>
#
# SPDX-License-Identifier: Apache-2.0
import glob
import json
import os
import pathlib
from typing import Dict, Any, List


class SchemaNotFoundError(RuntimeError):
    ...


def get_schema_path(schema_name: str, version: str) -> pathlib.Path:
    version_segments = version.split(".")
    if len(version_segments) != 2:
        raise ValueError(f"Invalid version string: '{version}'")
    major_version, minor_version = version_segments
    if not major_version.isnumeric() or not minor_version.isnumeric():
        raise ValueError(f"Invalid version string: '{version}'")

    return pathlib.Path(__file__).parent / f"v{major_version}" / f"{schema_name}.json"


def get_schema(schema_name: str, version: str) -> Dict[str, Any]:
    path = get_schema_path(schema_name, version)
    try:
        with open(path.resolve()) as schema_file:
            schema: Dict[str, Any] = json.load(schema_file)
            return schema
    except FileNotFoundError:
        raise SchemaNotFoundError(f"Could not find schema v{version}/{schema_name}")


def list_schemas() -> Dict[str, List[str]]:
    def split_filepath(path):
        dirname, filename = os.path.split(path)
        return (os.path.basename(dirname), filename)

    file_paths = glob.glob(str(pathlib.Path(__file__).parent / "v*" / "*.json"))

    schemas: Dict[str, List[str]] = {}
    for version, filename in map(split_filepath, file_paths):
        schema_name = os.path.splitext(filename)[0]
        if version in schemas:
            schemas[version].append(schema_name)
        else:
            schemas[version] = [schema_name]

    return schemas
