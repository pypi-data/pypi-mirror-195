import json
from io import StringIO
from typing import Optional
from logging import getLogger

from whylogs.core.constraints.metric_constraints import Constraints

logger = getLogger(__name__)

def serialize(contraints: Constraints) -> str:
    return json.dumps(contraints)

def deserialize(contraints_string: str) -> Optional[Constraints]:
    deserialized_constraints = json.loads(contraints_string)
    if isinstance(deserialized_constraints, Constraints):
        logger.info("Successfully deserialized constraints")
        return deserialized_constraints
    logger.warning("json was not deserialized as instance of Constraints")
    return None