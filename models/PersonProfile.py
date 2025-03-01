from pydantic import BaseModel, Field
from typing import List, Optional


class PersonProfile(BaseModel):
    id: Optional[int] = None
    name: str = Field(description="Full name of the person")
    phone: str = Field(description="Phone number")
    email: str = Field(description="Email address")
    summary: str = Field(description="Summary of the candidate")
    skills: List[str] = Field(description="List of technical skills")
    experience: List[str] = Field(description="Job titles and companies")
    education: List[str] = Field(description="Degrees and institutions")
    another_info: str = Field(description="Another info about the candidate")
