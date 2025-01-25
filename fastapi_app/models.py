from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Text


# Define the base class for your models
class Base(DeclarativeBase):
    pass


# Define the Recipe model
class Recipe(Base):
    __tablename__ = "recipes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String, index=True)
    views: Mapped[int] = mapped_column(Integer, default=0)
    cook_time: Mapped[int] = mapped_column(Integer)
    ingredients: Mapped[str] = mapped_column(Text)
    description: Mapped[str] = mapped_column(Text)
