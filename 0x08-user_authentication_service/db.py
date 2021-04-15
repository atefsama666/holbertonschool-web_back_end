#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError

from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Save the user to the database
        """
        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()
        return user

    def find_user_by(self, **kwargs) -> User:
        """
        Returns the first row found in the users
        table as filtered by the method’s input arguments
        """
        valid_args = ['id', 'email', 'hashed_password',
                      'session_id', 'reset_token']
        for k in kwargs.keys():
            if k not in valid_args:
                raise InvalidRequestError
        user = self._session.query(User).filter_by(**kwargs).first()
        if user is None:
            raise NoResultFound
        return user

    def update_user(self, user_id: int, **kwargs) -> None:
        """
        Find user by user_id and updates its data.
        Returns None
        """
        valid_args = [
            'id', 'email', 'hashed_password', 'session_id', 'reset_token'
        ]
        try:
            user = self.find_user_by(id=user_id)
            if user:
                for k, v in kwargs.items():
                    if k not in valid_args:
                        raise ValueError
                    else:
                        setattr(user, k, v)
                self._session.commit()
        except Exception as e:
            raise e
