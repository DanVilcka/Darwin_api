from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import relationship

from .database import Base


class Privelige(Base):
    __tablename__ = "priveliges"

    id = Column(Integer, primary_key=True)
    read = Column(Boolean, default=True)
    update = Column(Boolean, default=True)
    item_id = Column(Integer, ForeignKey("items.id"))
    user_id = Column(Integer, ForeignKey("users.id"))

    __table_args__ = (
        UniqueConstraint('user_id', 'item_id', name='uq_privileges_user_id_item_id'),
    )

    items_con = relationship("Item", back_populates="item_id")
    users_con = relationship("User", back_populates="priveliges")


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="items")
    item_id = relationship("Privelige", back_populates="items_con")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    items = relationship("Item", back_populates="owner")
    priveliges = relationship("Privelige", back_populates="users_con")

