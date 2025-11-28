# External
import bcrypt
from sqlmodel import Session, select
from configs import settings

# Custom
from models import User


def generate_verify_url(host_prefix: str, token: str) -> str:
    verify_url = f"http://{settings.host}:{settings.port}{host_prefix}/verify-email?token={token}"
    return verify_url


def hash_password(password: str) -> str:
    """Hash a password"""
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password=password.encode(encoding="utf-8"), salt=salt)
    return hashed.decode(encoding="utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against a hashed one"""
    return bcrypt.checkpw(
        password=plain_password.encode(encoding="utf-8"),
        hashed_password=hashed_password.encode(encoding="utf-8"),
    )


def get_user_by_username(session: Session, username: str) -> User | None:
    """get user from the SQL database based on the username"""
    statement = select(User).where(User.username == username)
    return session.exec(statement=statement).first()


def get_user_by_email(session: Session, email: str) -> User | None:
    """get user from the SQL database based on the email"""
    statement = select(User).where(User.email == email)
    return session.exec(statement=statement).first()


def authenticate_user(session: Session, username: str, password: str) -> User | None:
    """logic for login a user"""
    user = get_user_by_email(session=session, email=username)
    if not user or not verify_password(
        plain_password=password, hashed_password=user.hashed_password
    ):
        return None
    return user


def is_existing_user(session: Session, username: str, email: str) -> bool:
    statement = select(User).where((User.username == username) | (User.email == email))
    existing_user = session.exec(statement=statement).first()
    return existing_user is not None
