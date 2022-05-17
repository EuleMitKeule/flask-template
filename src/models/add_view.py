from flask import jsonify
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy_mixins.activerecord import ModelNotFoundError

from models import BaseModel
from common import api


def add_view(**kwargs):
    
    def decorator(cls):
        single_model_name: str = cls.__name__
        plural_model_name: str = f"{single_model_name}s"
        lower_single_model_name: str = cls.__name__.lower()
        lower_plural_model_name: str = f"{lower_single_model_name}s"
        
        blueprint: Blueprint = kwargs.get(
            "blueprint",
            Blueprint(
                lower_plural_model_name,
                lower_plural_model_name,
                url_prefix=f"/{lower_plural_model_name}"
            )
        )


        @blueprint.route("/<int:entity_id>")
        class SingleView(MethodView):

            @blueprint.response(200, cls.Schema())
            def get(self, entity_id: int):
                try:
                    entity: BaseModel = cls.find_or_fail(entity_id)
                    entity_dict: dict = cls.dump(entity)
                    return jsonify(entity_dict)
                except ModelNotFoundError as e:
                    abort(
                        404,
                        message=f"{single_model_name} with id {entity_id} does not exist."
                    )

            @blueprint.response(200, cls.Schema())
            @blueprint.arguments(cls.Schema(), location="json")
            def put(self, entity: BaseModel):
                entity.save()
                entity_dict: dict = cls.dump(entity)
                return jsonify(entity_dict)

            @blueprint.response(204)
            def delete(self, entity_id: int):
                try:
                    entity: BaseModel = cls.find_or_fail(entity_id)
                    entity.delete()
                    return "", 204
                except ModelNotFoundError as e:
                    abort(
                        404,
                        message=f"{single_model_name} with id {entity_id} does not exist."
                    )

        @blueprint.route("/")
        class PluralView(MethodView):

            @blueprint.response(200, cls.Schema(many=True))
            def get(self):
                entities: list[BaseModel] = cls.all()
                entities_dict: dict = cls.dump(entities, many=True)
                return jsonify(entities_dict)

            @blueprint.response(201, cls.Schema())
            @blueprint.arguments(cls.Schema(), location="json")
            def post(self, entity: BaseModel):
                entity.save()
                todo_dict: dict = cls.dump(entity)
                return jsonify(todo_dict), 201

        single_name = f"{single_model_name}View"
        plural_name = f"{plural_model_name}View"

        setattr(cls, single_name, SingleView)
        setattr(cls, plural_name, PluralView)

        api.register_blueprint(blueprint)

        return cls

    return decorator