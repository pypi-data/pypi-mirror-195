# SPDX-FileCopyrightText: 2022 Freemelt AB <opensource@freemelt.com>
#
# SPDX-License-Identifier: Apache-2.0
"""Reads properties and files from an OBF."""
import json
import typing
import zipfile
from os import PathLike  # pylint: disable=unused-import
from types import TracebackType
from typing import Dict, Any, Optional, Type, IO, Union


Self = typing.TypeVar("Self", bound="OBF")


class OBF:
    """Reader class for OBFs.

    Example usage:
    ```python
    >>> import obflib
    >>> with obflib.OBF("openbuildfile/examples/standard.obf") as obf:
    ...     manifest = obf.manifest()
    ...     build_info = obf.build_info()
    ...
    >>> manifest['name']
    'Test Rod'
    >>> len(build_info['layers'])
    2
    ```
    """

    def __init__(self, filename: Union[str, "PathLike[str]"]) -> None:
        """Open an OBF designated by the given filename."""
        try:
            self._file = zipfile.ZipFile(filename)
        except zipfile.BadZipFile as err:
            raise ValueError(f"File '{filename}' is not an OBF.") from err

        # If we can't open manifest.json, this will raise a KeyError
        with self.open_file("manifest.json") as manifest_file:
            self._manifest: Dict[str, Any] = json.load(manifest_file)

        self._build_processors: Optional[Dict[str, Any]] = None
        self._build_info: Optional[Dict[str, Any]] = None
        self._machine_capabilities: Optional[Dict[str, Any]] = None
        self._module_configs: Dict[str, Any] = {}

    def __enter__(self: Self) -> Self:
        """Allow using this class in a `with` statement."""
        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        """Cleanup of resources after using this class in a `with` statement."""
        self.close()

    def close(self) -> None:
        """Close the OBF."""
        self._file.close()

    def open_file(self, filename: str) -> IO[bytes]:
        """Return a file handle to a file inside the OBF.

        Recommended use is with a `with` statement. Example:
        ```python
        with OBF("example.obf") as obf:
            with obf.open_file("obp/start_heat.obp") as start_heat:
                # ...
        ```
        """
        return self._file.open(filename)

    def manifest(self) -> Dict[str, str]:
        """Return a dict of basic build metadata from the OBF."""
        return {
            key: self._manifest[key]
            for key in self._manifest
            if isinstance(self._manifest[key], str)
        }

    def nested_manifest(self) -> Dict[str, Any]:
        """Return a dict of all build metadata from the OBF.

        Each json file referenced from `manifest.json` is inlined into the resulting dict.
        """
        return {
            **self.manifest(),
            "buildInfo": self.build_info(),
            "buildProcessors": self.build_processors(),
            "machineCapabilities": self.machine_capabilities(),
            "modules": {
                module_name: self.config_for_module(module_name)
                for module_name in self.modules().keys()
            },
        }

    def build_processors(self) -> Dict[str, Any]:
        """Return a dict of build processors from the OBF."""
        if self._build_processors is not None:
            return self._build_processors

        with self.open_file(self._manifest["buildProcessors"]) as build_processors_file:
            self._build_processors = json.load(build_processors_file)["buildProcessors"]

        return self._build_processors

    def build_info(self) -> Dict[str, Any]:
        """Return build information for the OBF."""
        if self._build_info is not None:
            return self._build_info

        with self.open_file(self._manifest["buildInfo"]) as build_file:
            self._build_info = json.load(build_file)

        return self._build_info

    def machine_capabilities(self) -> Dict[str, Any]:
        """Return a dict of machine capabilities required for building the OBF."""
        if self._machine_capabilities is not None:
            return self._machine_capabilities

        with self.open_file(self._manifest["machineCapabilities"]) as capabilities_file:
            self._machine_capabilities = json.load(capabilities_file)

        return self._machine_capabilities

    def modules(self) -> Dict[str, str]:
        """Return a dict of module configurations."""
        return self._manifest["modules"]  # type: ignore[no-any-return]

    def config_for_module(self, module_name) -> Optional[Dict[str, Any]]:
        """Return configuration for a specific module."""
        modules = self.modules()

        if module_name not in modules:
            return None

        if module_name in self._module_configs:
            return self._module_configs[module_name]

        with self.open_file(modules[module_name]) as module_config_file:
            self._module_configs[module_name] = json.load(module_config_file)

        return self._module_configs[module_name]
