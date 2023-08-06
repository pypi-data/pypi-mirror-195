
from pydantic import (
    BaseModel,
    constr,
    AnyUrl
)

from typing import Optional, Union, Dict, List

class FairscapeBaseModel(BaseModel):
    id: str
    context: Union[str, Dict[str,str]] = {
                "@vocab": "https://schema.org/",
                "evi": "https://w3id.org/EVI#"
            }
    type: str
    name: constr(max_length=64)
    keywords: List[str] = []

    class Config:
        allow_population_by_field_name = True
        validate_assignment = True    
        fields={
            "context": {
                "title": "context",
                "alias": "@context"
            },
            "id": {
                "title": "id",
                "alias": "@id"
            },
            "type": {
                "title": "type",
                "alias": "@type"
            },
            "name": {
                "title": "name"
            }
        }

