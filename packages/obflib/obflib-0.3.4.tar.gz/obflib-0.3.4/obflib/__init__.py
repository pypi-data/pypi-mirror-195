# SPDX-FileCopyrightText: 2022 Freemelt AB <opensource@freemelt.com>
#
# SPDX-License-Identifier: Apache-2.0
"""Package for handling OBF files.

Presently consists of two main parts:
* `verify`: a function that verifies the validity of an OBF
* `OBF`: a class for reading the contents of an OBF

See the respective item below for usage examples.
"""

from .message_handler import OBFMessages
from .reader import OBF
from .verifier import verify

__all__ = [
    "verify",
    "OBF",
    "OBFMessages",
]
