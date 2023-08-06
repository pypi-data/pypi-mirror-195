from fairscape_models.base import FairscapeBaseModel
from typing import Optional, Union, Dict, List
from pydantic import (
    constr,
    AnyUrl
)
from datetime import datetime

class Dataset(FairscapeBaseModel):
    type: Optional[str] = "https://w3id.org/EVI#Dataset"
    author: constr(max_length=64)
    datePublished: str
    version: str
    description: constr(min_length=10)
    associatedPublication: str
    additionalDocumentation: List[AnyUrl]
    format: str
    dataSchema: Optional[Union[str, dict]]
    generatedBy: List[str]
    derivedFrom: List[str]
    usedBy: List[str]
    contentUrl: str

    class Config:
        fields={
            "dataSchema": {
                "title": "dataSchema",
                "alias": "schema"
            }
        }
