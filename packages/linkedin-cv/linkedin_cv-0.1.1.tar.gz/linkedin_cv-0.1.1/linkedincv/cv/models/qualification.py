import pydantic


class Qualification(pydantic.BaseModel):

    title: str
    result: str
    date: str
    accreditor: str
