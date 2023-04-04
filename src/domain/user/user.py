from dataclasses_json import dataclass_json, LetterCase
from pydantic import BaseModel


@dataclass_json(letter_case=LetterCase.SNAKE)
class User(BaseModel):
    username: str
    password: str


@dataclass_json(letter_case=LetterCase.SNAKE)
class Token(BaseModel):
    token: str
