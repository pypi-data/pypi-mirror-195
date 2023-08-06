from fairscape_models.base import FairscapeBaseModel
from fairscape_models.dataset import Dataset
from fairscape_models.software import Software
from fairscape_models.computation import Computation

from typing import Optional, Union, Dict, List
from pydantic import (
    constr,
    AnyUrl
)
from datetime import datetime

class ROCrate(FairscapeBaseModel):
    type: str = "ROCrate"
    graph: List[Union[Dataset, Software, Computation]]

    class Config: 
        fields={
            "graph": {
                "title": "graph",
                "alias": "@graph"
            }
        }
