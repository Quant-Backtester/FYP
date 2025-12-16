#External
from sqlalchemy.orm import Session
from fastapi import status

#Custom
from database.sql_statement import is_existing_user
from auth_model import UserCreate
from custom.custom_exception import NotFoundException


def register_account(session: Session, user: UserCreate):
  if is_existing_user(session=session, username=user.username, email=user.email):
    raise NotFoundException(message="User does not exist")
    #redis cache (to be implement)