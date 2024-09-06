import sys

if sys.version_info < (3, 9):  # pragma: no cover
    from typing_extensions import Annotated  # pragma: no cover
else:
    from typing import Annotated  # pragma: no cover

from pydantic import StringConstraints

DomainStr = Annotated[
    str,
    StringConstraints(
        strip_whitespace=True, to_lower=True, min_length=1, max_length=253, pattern=r'^([a-z0-9-]+(\.[a-z0-9-]+)+)$'
    ),
]
