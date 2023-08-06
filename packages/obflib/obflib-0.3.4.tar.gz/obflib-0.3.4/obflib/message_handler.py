# SPDX-FileCopyrightText: 2022 Freemelt AB <opensource@freemelt.com>
#
# SPDX-License-Identifier: Apache-2.0
"""Module for handling errors and warnings."""

import json
from typing import Dict, List, Optional, Any

MessageDict = Dict[str, List[str]]


class OBFMessages:
    """Simple class for holding and categorizing errors and warnings."""

    def __init__(
        self,
        errors: Optional[MessageDict] = None,
        warnings: Optional[MessageDict] = None,
    ) -> None:
        """Initialize an OBFMessages, optionally with initial contents."""
        self._errors: MessageDict = errors or {}
        self._warnings: MessageDict = warnings or {}

    @property
    def errors(self) -> MessageDict:
        """Accumulated errors."""
        return self._errors

    @property
    def warnings(self) -> MessageDict:
        """Accumulated warnings."""
        return self._warnings

    def is_valid(self) -> bool:
        """Check if there are any errors."""
        return len(self._errors) == 0

    def insert_error(self, key: str, message: str) -> None:
        """Append a new error message to the specified key."""
        self._insert_message(self._errors, key, message)

    def insert_warning(self, key: str, message: str) -> None:
        """Append a new warning message to the specified key."""
        self._insert_message(self._warnings, key, message)

    def has_error(self, key: str) -> bool:
        """Determine if there are any errors matching the specified key."""
        return self._find_message(self._errors, key)

    def has_warning(self, key: str) -> bool:
        """Determine if there are any warnings matching the specified key."""
        return self._find_message(self._warnings, key)

    @staticmethod
    def _insert_message(target: MessageDict, key: str, message: str) -> None:
        if key not in target:
            target[key] = []

        if message not in target[key]:
            target[key].append(message)

    @staticmethod
    def _find_message(target: MessageDict, key: str) -> bool:
        return key in target

    def to_json(self, **kwargs: Any) -> str:
        """Format errors and warnings as json.

        Forwards any keyword arguments to json.dumps.
        """
        return json.dumps(
            {
                "errors": self._errors,
                "warnings": self._warnings,
                "isValid": self.is_valid(),
            },
            **kwargs
        )
