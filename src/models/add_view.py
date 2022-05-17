from flask import jsonify
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy_mixins.activerecord import ModelNotFoundError

from models import BaseModel
from common import api
from auth import auth_required, roles_required


def add_view(**kwargs):
    
    def decorator(cls):

        auth: dict = kwargs.pop("auth", {})
        decorators: dict = kwargs.pop("decorators", {})
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
        
        for operation_type, decorator_list in decorators.items():
            method = getattr(SingleView if operation_type.value[0] == "SingleView" else PluralView, operation_type.value[1])

            for decorator in decorator_list:
                setattr(SingleView if operation_type.value[0] == "SingleView" else PluralView, operation_type.value[1], decorator(method))

        for operation_type, auth_dict in auth.items():
            view = SingleView if operation_type.value[0] == "SingleView" else PluralView
            method_name = operation_type.value[1]

            method = getattr(view, method_name)

            is_auth_required: bool = auth_dict.get("auth_required", False)
            roles: list[str] = auth_dict.get("roles", [])

            if is_auth_required:
                method = auth_required(method)
                setattr(view, method_name, method)

            if roles:
                method = roles_required(*roles)(method)
                setattr(view, method_name, method)

        SingleView = blueprint.route("/<int:entity_id>")(SingleView)
        PluralView = blueprint.route("/")(PluralView)

        api.register_blueprint(blueprint)

        return cls

    return decorator