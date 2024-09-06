from typing import Annotated

from pydantic import StringConstraints

DomainStr = Annotated[
    str,
    StringConstraints(
        strip_whitespace=True, to_lower=True, min_length=1, max_length=253, pattern=r'^([a-z0-9-]+(\.[a-z0-9-]+)+)$'
    ),
]
