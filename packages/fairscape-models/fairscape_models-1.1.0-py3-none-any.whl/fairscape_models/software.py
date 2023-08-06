from fairscape_models.base import FairscapeBaseModel
from typing import Optional, Union, Dict, List
from pydantic import (
    constr,
    AnyUrl
)
from datetime import datetime

class Software(FairscapeBaseModel): 
    type: Optional[str] = "https://w3id.org/EVI#Software"
    author: constr(max_length=64)
    dateModified: str
    version: str
    description: constr(min_length=10)
    associatedPublication: str
    additionalDocumentation: List[str]
    format: str
    usedByComputation: List[str]
    contentUrl: str
    
