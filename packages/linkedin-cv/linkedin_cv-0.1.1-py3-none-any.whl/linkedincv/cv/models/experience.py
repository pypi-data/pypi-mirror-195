from typing import Literal, Optional

import pydantic

EvidenceType = Literal["project", "secondment"]


class Evidence(pydantic.BaseModel):

    type: EvidenceType
    title: str
    technologies: list[str]
    items: list[str]


class Position(pydantic.BaseModel):

    title: str
    grade: Optional[str]
    department: str
    time: str
    evidence: list[Evidence]


class Experience(pydantic.BaseModel):

    company: str
    image: str
    employment: str
    positions: list[Position]
