from models import BaseModel, add_schema, add_view
from common import db


@add_view()
@add_schema()
class Todo(BaseModel):
    __tablename__ = "todo"

    text: str = db.Column(db.String(255), nullable=False, default="")

