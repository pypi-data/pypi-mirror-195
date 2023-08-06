# SPDX-FileCopyrightText: 2022 Freemelt AB <opensource@freemelt.com>
#
# SPDX-License-Identifier: Apache-2.0
"""Verifies that a filename points ot a valid OBF file."""

import json
import zipfile
import collections
from json import JSONDecodeError
from os import PathLike  # pylint: disable=unused-import
from typing import List, Callable, Union, Dict, Any, Set, Tuple

import jsonschema
import semantic_version
from jsonschema.exceptions import SchemaError, ValidationError

from openbuildfile.schemas import get_schema
from obflib.message_handler import OBFMessages

JsonDict = Dict[str, Any]


class InvalidSchemaError(ValueError):
    """Error raised when an invalid schema is encountered."""


def _extract_json_data(file_name: str, obf_file: zipfile.ZipFile, messages: OBFMessages) -> Any:
    def check_duplicate_keys(pairs: List[Tuple[str, Any]]) -> JsonDict:
        key_counts = collections.Counter(pair[0] for pair in pairs)
        for key, count in key_counts.items():
            if count > 1:
                messages.insert_warning(
                    file_name,
                    f"An object in this file contains duplicates of the key '{key}'",
                )

        return dict(pairs)

    try:
        with obf_file.open(file_name) as json_file:
            return json.load(json_file, object_pairs_hook=check_duplicate_keys)
    except KeyError as err:
        raise FileNotFoundError from err


def _make_filepath_validator(
    namelist: Set[str],
    referred_files: Set[str],
) -> Callable[[str], bool]:
    def validate_filepath(path: str) -> bool:
        if not isinstance(path, str):
            return True  # We only validate strings
        if path in namelist:
            referred_files.add(path)
            return True
        return False

    return validate_filepath


def _validate_version_range(version_range: str) -> bool:
    if not isinstance(version_range, str):
        return True  # We only validate strings

    try:
        semantic_version.NpmSpec(version_range)
        return True
    except ValueError:
        return False


def _validate_recommended_properties(
    json_data: Any, schema: JsonDict, messages: OBFMessages, breadcrumbs: List[str]
) -> None:
    if not isinstance(json_data, dict):
        # Not a dict, we can't check its properties. Type error will be raised elsewhere.
        return
    for field in schema["properties"]:
        if field in json_data:
            subschema = schema["properties"][field]
            if subschema["type"] == "object" and "properties" in subschema:
                _validate_recommended_properties(
                    json_data[field], subschema, messages, breadcrumbs + [field]
                )
        elif "required" in schema and field not in schema["required"]:
            path = "/".join(breadcrumbs + [field])
            messages.insert_warning(path, "This recommended property is missing")


def _validate_format_specs(schema: JsonDict, checkers: Dict[str, Any]) -> None:
    """Make sure the schema only uses known format specifiers.

    :raises: InvalidSchemaError
    """
    for key, value in schema.items():
        if isinstance(value, dict):
            _validate_format_specs(value, checkers)
        elif key == "format" and value not in checkers:
            raise InvalidSchemaError(f"Encountered invalid format specification: '{value}'")


def _validate_subschema(
    filename: str,
    schema: JsonDict,
    obf_file: zipfile.ZipFile,
    referred_files: Set[str],
    messages: OBFMessages,
) -> None:
    try:
        jsonschema.Draft7Validator.check_schema(schema)
    except SchemaError as err:
        raise InvalidSchemaError(err) from err

    try:
        file_data = _extract_json_data(filename, obf_file, messages)
    except JSONDecodeError:
        messages.insert_error(filename, f"{filename} is not a valid JSON file")
        return

    checker = jsonschema.FormatChecker()
    names_in_obf = set(obf_file.namelist())
    checker.checks("filepath")(_make_filepath_validator(names_in_obf, referred_files))
    checker.checks("npm-semver-range")(_validate_version_range)

    _validate_format_specs(schema, checker.checkers)

    validator = jsonschema.Draft7Validator(
        schema=schema,
        format_checker=checker,
    )

    _validate_recommended_properties(
        json_data=file_data, schema=schema, messages=messages, breadcrumbs=[filename]
    )

    for error in validator.iter_errors(file_data):
        path = _build_json_path(filename, error)
        message = error.message
        if error.validator == "format":
            if error.validator_value == "filepath":
                message = f"'{error.instance}' does not exist in the OBF"
            elif error.validator_value == "npm-semver-range":
                message = (
                    f"'{error.instance}' is not a valid npm semver range."
                    " See https://github.com/npm/node-semver#ranges."
                )
        messages.insert_error(path, message)


def _build_json_path(filename: str, error: ValidationError) -> str:
    path = filename
    for elem in error.path:
        if isinstance(elem, int):
            path += f"[{elem}]"
        else:
            path += f"/{elem}"
    return path


def verify(filename: Union[str, "PathLike[str]"]) -> OBFMessages:
    """Verify that given filename is a valid OBF.

    :param filename: path to file to be verified
    :return: A collection of errors and warnings, and whether the verification succeeded.
      See `OBFMessages` for details.

    Example usage:
    ```python
    >>> import obflib
    >>> messages = obflib.verify("openbuildfile/examples/standard.obf")
    >>> messages.to_json()
    '{"errors": {}, "warnings": {}, "isValid": true}'
    >>> messages.is_valid()
    True
    ```
    """
    messages = OBFMessages()

    if not str(filename).lower().endswith(".obf"):
        messages.insert_error("", "Filename must end with '.obf'")

    try:
        with zipfile.ZipFile(filename) as obf_file:
            try:
                manifest_data = _extract_json_data("manifest.json", obf_file, messages)
            except JSONDecodeError:
                messages.insert_error(str(filename), "manifest.json is not a valid JSON file")
                return messages
            except FileNotFoundError:
                messages.insert_error(str(filename), "manifest.json not found in the OBF")
                return messages

            files_in_zip = set(path for path in obf_file.namelist() if not path.endswith("/"))
            referred_files = {"manifest.json"}

            obf_format_version = manifest_data.get("obfFormatVersion", None)
            if not obf_format_version:
                messages.insert_error("manifest.json", "Missing field: obfFormatVersion")
                return messages

            _validate_schemas(manifest_data, messages, obf_file, obf_format_version, referred_files)

        unreferred_files = sorted(list(files_in_zip - referred_files))
        if unreferred_files:
            for unreferred_file in unreferred_files:
                messages.insert_warning(unreferred_file, "This file appears to be unused")

    except zipfile.BadZipFile:
        messages.insert_error("", "File could not be opened as a zip file")

    return messages


def _validate_schemas(
    build_file_data: JsonDict,
    messages: OBFMessages,
    obf_file: zipfile.ZipFile,
    obf_format_version: str,
    referred_files: Set[str],
) -> None:
    _validate_subschema(
        "manifest.json",
        get_schema("manifest", obf_format_version),
        obf_file,
        referred_files,
        messages,
    )
    for subschema in ["buildInfo", "buildProcessors", "machineCapabilities"]:
        filename = build_file_data.get(subschema, None)
        if filename is not None:
            _validate_subschema(
                filename,
                get_schema(subschema, obf_format_version),
                obf_file,
                referred_files,
                messages,
            )
    if not messages.has_error("manifest.json/modules"):
        modules = build_file_data.get("modules", {})
        for name, filepath in modules.items():
            if not messages.has_error(f"manifest.json/modules/{name}"):
                _validate_subschema(
                    filepath,
                    get_schema("module", obf_format_version),
                    obf_file,
                    referred_files,
                    messages,
                )
