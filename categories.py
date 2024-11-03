import sqlalchemy as sa
import sqlalchemy.orm as orm
from .db_session import SqlAlchemyBase


# Модель класса Category
class Category(SqlAlchemyBase):
    __tablename__ = "categories"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True, nullable=False)
    name = sa.Column(sa.String)

    #news = orm.relation("Categories", back_populates="user", cascade="all, delete")