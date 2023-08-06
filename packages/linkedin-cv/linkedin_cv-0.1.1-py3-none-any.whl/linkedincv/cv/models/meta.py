from typing import Optional

import pydantic

SUPPORTED_SOCIAL_PLATFORMS = [
    "github",
    "linkedin",
]


class Social(pydantic.BaseModel):

    platform: str
    handle: str

    @pydantic.validator("platform")
    @classmethod
    def check_platform_support(cls, platform: str) -> str:
        if platform not in SUPPORTED_SOCIAL_PLATFORMS:
            raise ValueError(
                f"The social media platform {platform} is not yet supported."
            )
        return platform


class Meta(pydantic.BaseModel):

    name: str
    email: str
    role: Optional[str]
    company: Optional[str]
    mobile: Optional[str]
    socials: list[Social] = pydantic.Field(default_factory=list)
    summary: Optional[str]
