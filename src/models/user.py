from sqlalchemy.ext.hybrid import hybrid_property

from models import BaseModel, add_schema, add_view, OperationType
from common import db, guard, ma


@add_view(
    auth={
        OperationType.READ: {
            "auth_required": True,
            "roles": ["admin"]
        }
    },
)
@add_schema(
    meta={
        "dump_only": ["roles"],
        "exclude": ["password_hash"]
    },
    password=ma.String(load_only=True)
)
class User(BaseModel):
    __tablename__ = "user"

    name: str = db.Column(db.String(255), nullable=False, default="", unique=True)
    password_hash: str = db.Column(db.Text)
    email: str = db.Column(db.String(255), nullable=False, default="")
    roles = db.Column(db.Text, default="user")
    is_active = db.Column(db.Boolean, default=True)
    access_token: str = db.Column(db.String)

    @property
    def identity(self):
        return self.id

    @property
    def rolenames(self):
        try:
            return self.roles.split(",")
        except Exception:
            return []
    
    @hybrid_property
    def password(self):
        return self.password_hash

    @password.setter
    def password(self, password):
        self.password_hash = guard.hash_password(password)

    @classmethod
    def lookup(cls, name):
        return cls.where(name=name).first()

    @classmethod
    def identify(cls, id):
        return cls.find(id)

    def is_valid(self):
        return self.is_active