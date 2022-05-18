from flask import jsonify
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy_mixins.activerecord import ModelNotFoundError

from models import BaseModel
from common import api
from auth import auth_required, roles_required


def add_view(**kwargs):
    
    def decorator(cls: BaseModel):

        auth: dict = kwargs.pop("auth", {})
        decorators_dict: dict = kwargs.pop("decorators", {})
        
        blueprint: Blueprint = kwargs.get(
            "blueprint",
            Blueprint(
                cls.lower_plural_name,
                cls.lower_plural_name,
                url_prefix=f"/{cls.lower_plural_name}"
            )
        )

        class SingleView(MethodView):
            
            @blueprint.response(200, cls.Schema())
            def get(self, entity_id: int):
                try:
                    entity: BaseModel = cls.find_or_fail(entity_id)
                    entity_dict: dict = cls.dump(entity)
                    return jsonify(entity_dict)
                except ModelNotFoundError:
                    abort(
                        404,
                        message=f"{cls.single_name} with id {entity_id} does not exist."
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
                except ModelNotFoundError:
                    abort(
                        404,
                        message=f"{cls.single_name} with id {entity_id} does not exist."
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
        
        for operation_type, decorators in decorators_dict.items():
            view = locals()[operation_type.view_name]
            apply_decorators(view, operation_type.method_name, decorators)

        for operation_type, auth_dict in auth.items():
            view = locals()[operation_type.view_name]
            apply_auth_decorators(view, operation_type.method_name, auth_dict)

        blueprint.route("/<int:entity_id>")(SingleView)
        blueprint.route("/")(PluralView)

        api.register_blueprint(blueprint)

        return cls

    return decorator


def apply_decorators(cls, method_name, decorators):
    for decorator in decorators:
        apply_decorator(cls, method_name, decorator)


def apply_auth_decorators(cls, method_name, auth_dict):
    is_auth_required: bool = auth_dict.get("auth_required", False)
    roles: list[str] = auth_dict.get("roles", [])

    if is_auth_required:
        apply_decorator(cls, method_name, auth_required)

    if roles:
        apply_decorator(cls, method_name, roles_required(*roles))


def apply_decorator(cls, method_name, decorator):
    method = getattr(cls, method_name)
    setattr(cls, method_name, decorator(method))
