from common import db, ma


def add_schema(**kwargs):
    
    def decorator(cls):
        single_model_name: str = cls.__name__
        plural_model_name: str = f"{single_model_name}s"
        lower_single_model_name: str = cls.__name__.lower()
        lower_plural_model_name: str = f"{lower_single_model_name}s"
        schema_name: str = f"{single_model_name}Schema"

        class Meta:
            model = cls
            load_instance = True
            sqla_session = db.session

        if "meta" in kwargs:
            for key, value in kwargs.get("meta").items():
                setattr(Meta, key, value)

            kwargs.pop("meta")

        name: str = kwargs.pop("name", "Schema")

        schema = type(schema_name, (ma.SQLAlchemyAutoSchema,), {
            "Meta": Meta,
            "id": ma.Integer(dump_only=True),
            **kwargs
        })

        setattr(cls, name, schema)
        return cls

    return decorator