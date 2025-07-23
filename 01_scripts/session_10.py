from typing import List
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.engine.create import create_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.orm.session import sessionmaker


class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "user_account"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    fullname: Mapped[Optional[str]]
    addresses: Mapped[List["EmailAddress"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r}, fullname={self.fullname!r})"

class EmailAddress(Base):
    __tablename__ = "email_address"
    id: Mapped[int] = mapped_column(primary_key=True)
    email_address: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey("user_account.id"))
    user: Mapped["User"] = relationship(back_populates="addresses")
    def __repr__(self) -> str:
        return f"Address(id={self.id!r}, email_address={self.email_address!r})"

# Setup of database engine. Sie macht Netzwerk connection von Py script zu datenbank, using SQLalechamy
db_engine = create_engine("postgresql://test:test@localhost:5432/test")
# Auf der Netzwerk connection brauchen wir sessions. eine session kann von einem prozess benutzt werden. eine connection kann mehrer sessions haben
Session = sessionmaker(bind=db_engine)
session = Session()

# Base.metadata.create_all(bind=db_engine)

# wir füllen die tabelle mit dummy data
# for i in range(20):
#    user = User(name=f"user {i}", fullname=f"full user {i}")
#    session.add(user)
# session.commit()
# users = session.query(User).all()
# for user in users:
#    print(user)

found_user = session.query(User).filter(User.name=="user 20").first()
print(found_user)