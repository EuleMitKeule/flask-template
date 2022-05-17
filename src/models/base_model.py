from __future__ import annotations
from typing import Optional

from common import db
from sqlalchemy_mixins import AllFeaturesMixin


class BaseModel(db.Model, AllFeaturesMixin):
    __abstract__ = True

    id: int = db.Column(db.Integer, primary_key=True)

    @classmethod
    def load(cls, data: dict, **kwargs) -> Optional[BaseModel]:
        if not hasattr(cls, "Schema"):
            return None

        return cls.Schema().load(data, **kwargs)

    @classmethod
    def dump(cls, data: dict, **kwargs) -> dict:
        if not hasattr(cls, "Schema"):
            return None

        return cls.Schema().dump(data, **kwargs)

    def update(self, data: dict = None, **kwargs) -> Optional[BaseModel]:
        if data is not None:
            if "id" not in data:
                data["id"] = self.id
            entity: Optional[BaseModel] = self.load(data)
            db.session.commit()
            return entity

        return super().update(**kwargs)