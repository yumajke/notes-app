import sqlalchemy as sa
import sqlalchemy.orm as orm
from .db_session import SqlAlchemyBase


# Модель класса News
class News(SqlAlchemyBase):
    __tablename__ = "news"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True, nullable=False)
    title = sa.Column(sa.String, nullable=False)
    content = sa.Column(sa.String, nullable=False)
    user_id = sa.Column(sa.Integer, sa.ForeignKey("users.id", ondelete="CASCADE"))
    name_of_category = sa.Column(sa.String, nullable=False)
    data = sa.Column(sa.String, nullable=False)

    #user = orm.relation("News")
