from pydantic import BaseModel
from datetime import date


class UserBase(BaseModel):
    id: int
    login: str
    email: str
    password: str
    first_name: str
    last_name: str
    birth_date: date
    sex: str

class CompetitionBase(BaseModel):
    title: str
    password: str
    video_instruction: str

class ResultsBase(BaseModel):
    competition_id: int
    user_id: int
    video: str
    count: int
    status: str
