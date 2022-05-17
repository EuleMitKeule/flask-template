from models import BaseModel, add_schema, add_view
from common import db


@add_view()
@add_schema()
class User(BaseModel):
    __tablename__ = "user"

    name: str = db.Column(db.String(255), nullable=False, default="")
    password: str = db.Column(db.String(255), nullable=False, default="")
    email: str = db.Column(db.String(255), nullable=False, default="")
