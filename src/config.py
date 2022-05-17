import logging
import os
from dataclasses import dataclass, field
from flask import Flask
from flask_marshmallow import Schema
from marshmallow import ValidationError

from marshmallow_dataclass import class_schema
from yaml import safe_dump, safe_load

from const import APP_NAME, APP_VERSION, DEFAULT_CONFIG_PATH, DEFAULT_HOST, DEFAULT_LOG_LEVEL, DEFAULT_LOG_PATH, DEFAULT_OPENAPI_JSON_PATH, DEFAULT_PORT, DEFAULT_SECRET_KEY, DEFAULT_SQLITE_PATH, REDOC_URL, SWAGGER_UI_URL


@dataclass
class ConfigModel:

    @dataclass
    class LoggingConfig:
        level: str = field(default=DEFAULT_LOG_LEVEL, metadata=dict(required=False))
        path: str = field(default=DEFAULT_LOG_PATH, metadata=dict(required=False))

    @dataclass
    class NetworkingConfig:
        port: int = field(default=DEFAULT_PORT, metadata=dict(required=False))
        host: str = field(default=DEFAULT_HOST, metadata=dict(required=False))

    @dataclass
    class SqliteConfig:
        path: str = field(default=DEFAULT_SQLITE_PATH, metadata=dict(required=False))
        recreate: bool = field(default=False, metadata=dict(required=False))
        echo: bool = field(default=False, metadata=dict(required=False))

    @dataclass
    class AuthConfig:
        admin_username: str = field(default="admin", metadata=dict(required=False))
        admin_password: str = field(default="admin", metadata=dict(required=False))

    secret_key: str = field(default=DEFAULT_SECRET_KEY, metadata=dict(required=False))
    debug: bool = field(default=False, metadata=dict(required=False))
    networking: NetworkingConfig = field(default=NetworkingConfig(), metadata=dict(required=False))
    sqlite: SqliteConfig = field(default=SqliteConfig(), metadata=dict(required=False))
    logging: LoggingConfig = field(default=LoggingConfig(), metadata=dict(required=False))
    auth: AuthConfig = field(default=AuthConfig(), metadata=dict(required=False))


class Config:

    config_model: ConfigModel
    app: Flask

    def __init__(self) -> None:
        pass

    def load(self, config_path: str) -> None:

        if not os.path.exists(config_path):
            logging.warn(f"Config file does not exist at path {config_path}. Using default config.")
            self.create_default()
        else:
            with open(config_path, "r") as f:
                config_dict: dict = safe_load(f)

            config_schema = class_schema(ConfigModel)()

            try:
                self.config_model = config_schema.load(config_dict)

                logging.basicConfig(
                    level=DEFAULT_LOG_LEVEL,
                    format="%(asctime)s %(levelname)s: %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S",
                    handlers=[
                        logging.FileHandler(self.config_model.logging.path),
                        logging.StreamHandler(),
                    ]
                )
            except ValidationError as e:
                logging.error(f"Config file is invalid.")
                logging.error(e)
                exit(1)
            except Exception as e:
                logging.error(f"Failed to load config.")
                logging.error(e)
                exit(1)

        self.create_folders()

    def init_app(self, app: Flask) -> None:
        logging.info(f"Using logging file at {self.config_model.logging.path}.")
        logging.info(f"Connecting to database file at {self.config_model.sqlite.path}.")

        self.app = app

        app.config["DEBUG"] = self.config_model.debug
        app.config["SECRET_KEY"] = self.config_model.secret_key
        app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{self.config_model.sqlite.path}"
        app.config["SCHEDULER_API_ENABLED"] = True
        app.config["SQLALCHEMY_COMMIT_ON_TEARDOWN"] = True
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        app.config["SQLALCHEMY_ECHO"] = self.config_model.sqlite.echo
        app.config["API_TITLE"] = APP_NAME
        app.config["API_VERSION"] = APP_VERSION
        app.config["OPENAPI_VERSION"] = "3.0.0"
        app.config["OPENAPI_URL_PREFIX"] = "/"
        app.config["OPENAPI_JSON_PATH"] = "openapi.json"
        app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui/"
        app.config["OPENAPI_SWAGGER_UI_URL"] = SWAGGER_UI_URL
        app.config["OPENAPI_REDOC_PATH"] = "/redoc/"
        app.config["OPENAPI_REDOC_URL"] = REDOC_URL
        app.config["API_SPEC_OPTIONS"] = {
            "components": {
                "securitySchemes": {
                    "bearerAuth": {
                        "type": "http",
                        "scheme": "bearer",
                        "bearerFormat": "JWT",
                        "in": "header"
                    }
                }
            },
        }

    def create_folders(self):
        db_folder: str = os.path.dirname(os.path.abspath(self.config_model.sqlite.path))
        log_folder: str = os.path.dirname(os.path.abspath(self.config_model.logging.path))

        try:
            if not os.path.exists(db_folder):
                os.makedirs(db_folder)

            if not os.path.exists(log_folder):
                os.makedirs(log_folder)
        except Exception as e:
            logging.error(f"Failed to create folders.")
            logging.error(e)
            exit(1)

    def create_default(self):
        logging.info(f"Creating default config file at {DEFAULT_CONFIG_PATH}.")

        self.config_model = ConfigModel()

        config_schema: Schema = class_schema(ConfigModel)()

        try:
            config_dict: dict = config_schema.dump(self.config_model)
            with open(DEFAULT_CONFIG_PATH, "w") as f:
                f.write(safe_dump(config_dict))
            logging.info("Default config file created.")
        except Exception as e:
            logging.error(f"Failed to create default config.")
            logging.error(e)
            exit(1)
