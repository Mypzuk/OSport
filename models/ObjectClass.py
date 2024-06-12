from pydantic import BaseModel
from datetime import date


class UserBase(BaseModel):
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
    end_date: date

class ResultsBase(BaseModel):
    competition_id: str
    user_id: str
    video: str
    count: str
    status: str
