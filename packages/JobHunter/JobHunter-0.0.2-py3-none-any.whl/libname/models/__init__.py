from pydantic import BaseModel, AnyHttpUrl, EmailStr, Field
from typing import List

class CandidateData(BaseModel):
    url: AnyHttpUrl = Field(None, alias='JOBS_LINK')
    email: EmailStr = Field(None, alias='EMAIL')
    password: str = Field(None, alias='PASSWORD')
    resume_option_text: str = Field(None, alias='RESUME_OPTION_TEXT')

class QuestionData(BaseModel):
    email: EmailStr = Field(None, alias='EMAIL')
    url: AnyHttpUrl = Field(None, alias='JOBS_LINK')
    question_title: str = Field(None, alias='QUESTION')
    question_id: str = Field(None, alias='ID')
    question_type: str = Field(None, alias='TYPE')
    answer: str = Field(None, alias='ANSWER')