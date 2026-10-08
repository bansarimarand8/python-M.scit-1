from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship

from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, nullable=False)
    password = Column(String(255), nullable=False)

    tasks = relationship(
        "Task",
        back_populates="user"
    )


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)

    task_name = Column(String(150), nullable=False)

    status = Column(
        String(30),
        default="Pending",
        nullable=False
    )

    due_date = Column(Date, nullable=False)

    # 🔗 Connect Task with User
    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    user = relationship(
        "User",
        back_populates="tasks"
    )