import pydantic

from linkedincv.cv.models.experience import Experience
from linkedincv.cv.models.meta import Meta
from linkedincv.cv.models.qualification import Qualification


class CV(pydantic.BaseModel):

    meta: Meta
    experience: list[Experience]
    skillset: dict[str, list[str]]
    qualifications: dict[str, list[Qualification]]
